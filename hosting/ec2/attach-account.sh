ID=$1
#10015
NAME=$2
#"Town of Comox"
ACCOUNT=$3
#comox
DRIVE=sd$4
#c


die() {
    echo $1 > /dev/stderr
    exit 1
}


mkdir -p /home/${ACCOUNT}
mount -t reiserfs -o user_xattr,noatime,nodiratime,notail -L ${ACCOUNT} /home/${ACCOUNT}

if [ $? -ne 0 ] ; then
    echo "0," | sfdisk /dev/${DRIVE} -L || die "Unable to partition account block volume."
    mkfs.reiserfs -q -l ${ACCOUNT} /dev/${DRIVE}1 || die "Unable to format account partition."
    mount -t reiserfs -o user_xattr,noatime,nodiratime,notail -L ${ACCOUNT} /home/${ACCOUNT} || die "Unable to mount account home folder after partitioning and formatting."
fi

id ${ACCOUNT} &> /dev/null || useradd -c "${NAME}" -d /home/${ACCOUNT} -G users -s /bin/bash -u ${ID} -U ${ACCOUNT} || die "Unable to add account."

if [ ! -e /home/${ACCOUNT}/app ] ; then
    cp -ar /etc/skel/* /etc/skel/.[a-z]* /home/${ACCOUNT}
    chown -R ${ACCOUNT}:${ACCOUNT} /home/${ACCOUNT}
    chown nginx:wheel -R /home/${ACCOUNT}/etc/nginx
fi

if [ ! -e /home/${ACCOUNT}/var/mysql/${ACCOUNT} ] ; then
    mkdir -p /home/${ACCOUNT}/var/mysql/${ACCOUNT}
    echo -e "default-character-set=utf8\ndefault-collation=utf8_general_ci" > /home/${ACCOUNT}/var/mysql/${ACCOUNT}/db.opt
    PASS=`pwgen -B -c -N 1 -n -v 15 | tr -d '\n'`
    echo -n "${PASS}" > /home/${ACCOUNT}/var/mysql/${ACCOUNT}/db.pw
    chown mysql:wheel -R /home/${ACCOUNT}/var/mysql
fi

find /home/${ACCOUNT}/{etc/nginx,var/mysql} -type d -exec chmod 2770 {} \;
find /home/${ACCOUNT}/{etc/nginx,var/mysql} -type f -exec chmod 660 {} \;

rm -f /tmp/.query.sql
touch /tmp/.query.sql

for db in `ls /home/${ACCOUNT}/var/mysql` ; do
    PASS=`cat /home/${ACCOUNT}/var/mysql/${db}/db.pw | tr -d '\n'`
    
    if [ "$db" == "$ACCOUNT" ] ; then
        ln -sf /home/${ACCOUNT}/var/mysql/${db} /var/lib/mysql/${db}
        echo "GRANT ALL ON TABLE \`${db}\`.* TO '${db}'@'localhost' IDENTIFIED BY '${PASS}';" >> /tmp/.query.sql
        echo "GRANT ALL ON TABLE \`${db}\_%\`.* TO '${db}'@'localhost' IDENTIFIED BY '${PASS}';" >> /tmp/.query.sql
    else
        ln -sf /home/${ACCOUNT}/var/mysql/${db} /var/lib/mysql/${ACCOUNT}_${db}
        echo "GRANT ALL ON TABLE \`${ACCOUNT}\_${db}\`.* TO '${ACCOUNT}_${db}'@'localhost' IDENTIFIED BY '${PASS}';" >> /tmp/.query.sql
    fi
done

echo "FLUSH PRIVILEGES;" >> /tmp/.query.sql

mysql < /tmp/.query.sql

rm /tmp/.query.sql
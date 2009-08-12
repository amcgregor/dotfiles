rm -f /tmp/.query.sql
touch /tmp/.query.sql

ACCOUNT=$1
shift

for DB in $@ ; do
    if [ -e /home${ACCOUNT}/var/mysql/${ACCOUNT}_${DB} ]; then
        echo -en "Attaching existing database: ${ACCOUNT}_${DB} ... "
        
        PASS=`cat /home/${ACCOUNT}/var/mysql/${DB}/db.pw | tr -d '\n'`
        
        echo -en "Password: ${PASS} ... "
        
        ln -sf /home/${ACCOUNT}/var/mysql/${DB} /var/lib/mysql/${ACCOUNT}_${DB}
        echo "GRANT ALL ON TABLE \`${ACCOUNT}\_${DB}\`.* TO '${ACCOUNT}_${DB}'@'localhost' IDENTIFIED BY '${PASS}';" >> /tmp/.query.sql
        
        echo -en "done.\n"
    else
        echo -en "Creating new database: ${ACCOUNT}_${DB} ... "
        
        mkdir -p /home/${ACCOUNT}/var/mysql/${ACCOUNT}_${DB}
        echo -e "default-character-set=utf8\ndefault-collation=utf8_general_ci" > /home/${ACCOUNT}/var/mysql/${ACCOUNT}_${DB}/db.opt
        PASS=`pwgen -B -c -N 1 -n -v 15 | tr -d '\n'`
        echo -n "${PASS}" > /home/${ACCOUNT}/var/mysql/${ACCOUNT}_${DB}/db.pw
        chown mysql:wheel -R /home/${ACCOUNT}/var/mysql
        
        echo -en "Password: ${PASS} ... "
        
        if [ -e /var/lib/mysql/${ACOUNT}_${DB} ]; then
            echo -en "warning!\nSymlink already exists.\n"
            ls -ahl /var/lib/mysql/${ACOUNT}_${DB} | tail -n 1
            echo -en "Replacing... "
        fi
        
        ln -sf /home/${ACCOUNT}/var/mysql/${ACCOUNT}_${DB} /var/lib/mysql/${ACCOUNT}_${DB}
        echo "GRANT ALL ON TABLE \`${ACCOUNT}\_${DB}\`.* TO '${ACCOUNT}_${DB}'@'localhost' IDENTIFIED BY '${PASS}';" >> /tmp/.query.sql
        
        echo -en "done.\n"
    fi
done

echo "FLUSH PRIVILEGES;" >> /tmp/.query.sql

mysql < /tmp/.query.sql

rm /tmp/.query.sql
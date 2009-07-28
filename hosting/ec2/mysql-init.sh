#!/sbin/runscript
# Copyright 2009 Alice Bevan-McGregor  
# Distributed under the terms of the GNU General Public License v2

depend() {
	before mysql
}

checkconfig() {
	if [[ -e "/var/lib/mysql/mysql" ]] ; then
		ewarn "MySQL database already found."
		return 1
	fi
	
	return 0
}

start() {
	ebegin "Initializing MySQL database"
	/usr/bin/mysql_install_db &> /dev/null
	eend $? "Failed to initialize MySQL database."
	
	ebegin "Securing MySQL"
	
	PASS=`pwgen -B -c -N 1 -n -v 15 | tr -d '\n'`
	echo "UPDATE mysql.user SET Password=PASSWORD('$PASS') WHERE User='root';" > /usr/share/mysql/init.sql
	echo "FLUSH PRIVILEGES;" >> /usr/share/mysql/init.sql
	echo "DELETE FROM mysql.user WHERE User = '' OR Host = '%' OR ( User = 'root' AND Host != 'localhost' );" >> /usr/share/mysql/init.sql
	echo "DROP DATABASE test;" >> /usr/share/mysql/init.sql
	echo "DELETE FROM mysql.db WHERE Db = 'test' OR Db = 'test_%'" >> /usr/share/mysql/init.sql
	
	echo -e "[mysql]\nuser=root\npassword=$PASS\n\n[mysqladmin]\nuser=root\npassword=$PASS\n\n" > /root/.my.cnf
	
	chown mysql:wheel /usr/share/mysql/init.sql
	chmod 660 /usr/share/mysql/init.sql /root/.my.cnf
	
	eend $? "Failed to secure MySQL database."
}

# vim:ts=4
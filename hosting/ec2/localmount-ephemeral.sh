#!/sbin/runscript
# Copyright 2009 Alice Bevan-McGregor  
# Distributed under the terms of the GNU General Public License v2

# By default Amazon EC2 uses ext3.  I hate ext3 with a passion.	 Let's fix this.
# Note: This will only work if your /etc/fstab references /dev/sda2 as /ephemeral.
# This script will not overwrite an existing valid reiserfs partition, e.g. after a soft instance reboot.

# I'm using the following in my /etc/fstab:
# /dev/sda2		/ephemeral	reiserfs	user_xattr,noatime,nodiratime,notail,data=writeback,noauto	0 0

depend() {
	after localmount
}

start() {
	ebegin "Mounting ephemeral storage"
	mount /ephemeral 2> /dev/null || mkfs.reiserfs -l ephemeral -q /dev/sda2 &> /dev/null && mount /ephemeral
	eend $? "Unable to create and/or mount ephemeral storage"

	if [[ ! -f /ephemeral/.keep ]] ; then
		mkdir -p /ephemeral/{usr,var}

		for i in "/tmp" "/var/tmp" "/var/spool" "/var/cache" "/var/db" "/usr/portage"
		do
			ebegin "Migrating $i to ephemeral storage"
			mv $i /ephemeral$i && ln -sf /ephemeral$i $i
			eend $? "Unable to migrate $i to ephemeral storage"
		done
	fi
}

# vim:ts=4

#!/bin/bash

osVersion=`sw_vers -productVersion`

case $osVersion in
    10.4*)
	    catalogURLValue="http://Server.local:8088/index.sucatalog"
	    ;;
    10.5*)
    	catalogURLValue="http://Server.local:8088/index-leopard.merged-1.sucatalog"
    	;;
    10.6*)
    	catalogURLValue="http://Server.local:8088/index-leopard-snowleopard.merged-1.sucatalog"
    	;;
    10.[1-3]*)
        echo "Versions of Mac OS X earlier than 10.4 are not supported."
	    exit 1
	    ;;
esac

defaults write /Library/Preferences/com.apple.SoftwareUpdate CatalogURL $catalogURLValue

if [ -e /Users/Shared/.initswupd_inprog ]
then
    # If the 'updates in progress' marker is there, run the updates.
    # Temporarily prevent machine from sleeping.
    pmset -a sleep 0 force
    
    # Install all available software updates.
    softwareupdate -ai
    
    # Run softwareupdate again to see if there's anything left.
    # Softwareupdate returns 3 lines if there are no updates.
    
    if [ `softwareupdate -l | wc -l` -le 3 ]
    then
        # If there are no more updates available, clean up the marker, launchdaemon and login window text.
        rm /Users/Shared/.initswupd_inprog
        rm /Library/LaunchDaemons/com.management.initswupdater.plist
        defaults delete /Library/Preferences/com.apple.loginwindow LoginwindowText
    fi
else
    # If the 'updates in progress' marker is not there, prep the machine.
    # Create the marker file so the script knows to keep going.
    touch /Users/Shared/.initswupd_inprog
    
    #Set the loginwindow banner to warn people not to use the machine.
    defaults write /Library/Preferences/com.apple.loginwindow LoginwindowText "Software updates are currently being installed on this computer. Please do not attempt to log in until this message is gone."
    
    #Put the daemon in the LaunchDaemons folder, so the script runs again after reboot.
    plistfile='<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n<plist version="1.0">\n<dict>\n<key>Label</key>\n<string>com.management.initswupdater</string>\n<key>ProgramArguments</key>\n<array>\n<string>/bin/sh</string><string>/Library/Management/initswupdater.sh</string>\n</array>\n<key>RunAtLoad</key>\n<true/>\n</dict>\n</plist>'
    
    # Writing the LaunchDaemon plist file must be done differently in Tiger than Leopard
    osversionlong=`sw_vers -productVersion`
    osvers=${osversionlong:3:1}
    
    case $osVersion in
        10.4*)
            echo -e $plistfile > "/Library/LaunchDaemons/com.management.initswupdater.plist"
    	    ;;
        10.5*)
        10.6*)
            echo $plistfile > "/Library/LaunchDaemons/com.management.initswupdater.plist"
        	;;
    esac
fi

# Reboot
shutdown -r now

exit 0

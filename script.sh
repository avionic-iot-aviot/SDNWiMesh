# edit your /etc/opkg/distfeeds.conf, uncomment lines 2 and 5. Run opkg update, then run opkg install nano
 
opkg update
opkg install nano
opkg install git git-http ca-bundle
opkg install python3
opkg install python-urllib3
opkg install python3-pip
# edit your /etc/opkg/distfeeds.conf, uncomment lines 2 and 5. Run opkg update, then run opkg install nano
opkg install nano


opkg update
opkg install git git-http ca-bundle
opkg install python3
opkg install python-urllib3
opkg install python3-pip

python3 -m pip install --upgrade pip



cd /tmp
rm -rf SDNPy
git clone https://github.com/CarmeloRicci/SDNPy.git
cd SDNPy 
python3 main.py
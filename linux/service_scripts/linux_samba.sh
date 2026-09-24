ufw allow netbios-ns
ufw allow netbios-dgm
ufw allow netbios-ssn
ufw allow microsoft-ds

apt-get install samba -y -qq
apt-get install system-config-samba -y -qq

cp /etc/samba/smb.conf ~/Desktop/backups/
if [ "$(grep '####### Authentication #######' /etc/samba/smb.conf)"==0 ]
then
    sed -i 's/####### Authentication #######/####### Authentication #######\nsecurity = user/g' /etc/samba/smb.conf
fi

sed -i 's/usershare allow guests = no/usershare allow guests = yes/g' /etc/samba/smb.conf

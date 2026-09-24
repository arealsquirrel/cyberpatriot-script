#/bin/bash

apt install vsftpd

ufw allow ftp 
ufw allow sftp 
ufw allow saft 
ufw allow ftps-data 
ufw allow ftps

systemctl enable --now vsftpd

#/bin/bash

apt-get update
apt-get upgrade -y
apt-get fill-upgrade -y
apt-get dist-upgrade -y

apt install -y unattended-upgrades
dpkg-reconfigure --priority=low unattended-upgrades

passwd -l root
chown 640:640 /etc/passwd
chown 640:640 /etc/shadow
chown 640:640 /etc/security/opasswd

#/bin/bash

echo "------------ UNALIASING ALL ------------"
unalias -a

echo "------------ DISABELING ROOT ACCOUNT LOGIN ------------"
usermod -L root

echo "------------ DOING SYSTEM UPDATE ------------"
apt-get update
apt-get upgrade -y
apt-get full-upgrade -y
apt-get dist-upgrade -y

echo "------------ LOCKING SENSITIVE FILES ------------"
passwd -l root
chown 640:640 /etc/passwd
chown 644:644 /etc/shadow
chown 644:644 /etc/security/opasswd
chmod 640 .bash_history

# remove all scrips in bin
echo "------------ REMOVING ALL SCRIPTS IN /BIN ------------"
find /bin/ -name "*.sh" -type f -delete

# disable IRQ balance

echo "------------ DOING IRQ BALANCE ------------"
cp /etc/default/irqbalance ~/Desktop/backups/
echo > /etc/default/irqbalance
echo -e "#Configuration for the irqbalance daemon\n\n#Should irqbalance be enabled?\nENABLED=\"0\"\n#Balance the IRQs only once?\nONESHOT=\"0\"" >> /etc/default/irqbalance

echo "------------ DISABELING STARTUP SCRIPTS ------------"
echo > /etc/rc.local
echo 'exit 0' >> /etc/rc.local

echo "------------ SECURING LIGHT DM ------------"
chmod 644 /etc/lightdm/lightdm.conf
sed -i 's/greeter-hide-users.*/greeter-hide-users=true/' /etc/lightdm/lightdm.conf
sed -i 's/greeter-allow-guest.*/greeter-allow-guest=false/' /etc/lightdm/lightdm.conf
sed -i 's/greeter-show-manual-login.*/greeter-show-manual-login=true/' /etc/lightdm/lightdm.conf
sed -i 's/allow-guest.*/allow-guest=false/' /etc/lightdm/lightdm.conf
sed -i 's/autologin-guest.*/autologin-guest=false/' /etc/lightdm/lightdm.conf
sed -i 's/autologin-user.*/autologin-user=NONE/' /etc/lightdm/lightdm.conf

chmod +x linux/linux_pam.sh
chmod +x linux/linux_sysctl.sh
chmod +x linux/linux_ufw_default.sh

./linux/linux_sysctl.sh
./linux/linux_ufw_default.sh
./linux/linux_pam.sh

python3 linux/linux_apt_purge.py
python3 linux/linux_critical_services.py

apt-get autoremove -y -qq
apt-get autoclean -y -qq
apt-get clean -y -qq

echo "scripts are done"

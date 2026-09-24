#/bin/bash

unalias -a
usermod -L root

apt-get update
apt-get upgrade -y
apt-get full-upgrade -y
apt-get dist-upgrade -y

apt install -y unattended-upgrades
dpkg-reconfigure --priority=low unattended-upgrades

passwd -l root
chown 640:640 /etc/passwd
chown 644:644 /etc/shadow
chown 644:644 /etc/security/opasswd
chmod 640 .bash_history
cp /etc/rc.local ~/Desktop/backups/

# remove all scrips in bin
find /bin/ -name "*.sh" -type f -delete

# disable IRQ balance
cp /etc/default/irqbalance ~/Desktop/backups/
echo > /etc/default/irqbalance
echo -e "#Configuration for the irqbalance daemon\n\n#Should irqbalance be enabled?\nENABLED=\"0\"\n#Balance the IRQs only once?\nONESHOT=\"0\"" >> /etc/default/irqbalance

# startup scripts
echo > /etc/rc.local
echo 'exit 0' >> /etc/rc.local

# light dm
chmod 644 /etc/lightdm/lightdm.conf
sed -i 's/greeter-hide-users=.*/greeter-hide-users=true/' /etc/lightdm/lightdm.conf
sed -i 's/greeter-allow-guest=.*/greeter-allow-guest=false/' /etc/lightdm/lightdm.conf
sed -i 's/greeter-show-manual-login=.*/greeter-show-manual-login=true/' /etc/lightdm/lightdm.conf
sed -i 's/allow-guest=.*/allow-guest=false/' /etc/lightdm/lightdm.conf
sed -i 's/autologin-guest=.*/autologin-guest=false/' /etc/lightdm/lightdm.conf
sed -i 's/autologin-user=.*/autologin-user=NONE/' /etc/lightdm/lightdm.conf

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


clear
if [[ $(grep root /etc/passwd | wc -l) -gt 1 ]]
then
	grep root /etc/passwd | wc -l
	echo -e "UID 0 is not correctly set to root. Please fix.\nPress enter to continue..."
	read waiting
else
	printTime "UID 0 is correctly set to root."
fi



echo "scripts are done"

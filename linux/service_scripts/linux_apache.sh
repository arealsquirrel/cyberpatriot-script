#/bin/bash

apt-get install apache2 -y
chown -R root:root /etc/apache2
chown -R root:root /etc/apache
echo \<Directory \> >> /etc/apache2/apache2.conf
echo -e ' \t AllowOverride None' >> /etc/apache2/apache2.conf
echo -e ' \t Order Deny,Allow' >> /etc/apache2/apache2.conf
echo -e ' \t Deny from all' >> /etc/apache2/apache2.conf
echo UserDir disabled root >> /etc/apache2/apache2.conf

systemctl start apache2


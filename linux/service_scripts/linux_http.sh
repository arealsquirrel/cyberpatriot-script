apt-get install apache2 -y -qq
ufw allow http 
ufw allow https

if [ -e /etc/apache2/apache2.conf ]
then
    echo -e '\<Directory \>\n\t AllowOverride None\n\t Order Deny,Allow\n\t Deny from all\n\<Directory \/\>\nUserDir disabled root' >> /etc/apache2/apache2.conf
fi

chown -R root:root /etc/apache2

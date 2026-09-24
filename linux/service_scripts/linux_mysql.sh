
ufw allow ms-sql-s 
ufw allow ms-sql-m 
ufw allow mysql 
ufw allow mysql-proxy
apt-get install mysql-server-5.6 -y -qq

if grep -q "bind-address" "/etc/mysql/my.cnf"
then
    sed -i "s/bind-address\t\t=.*/bind-address\t\t= 127.0.0.1/g" /etc/mysql/my.cnf
fi

service mysql restart

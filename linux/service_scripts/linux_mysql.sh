
replace_command() {
    local PATTERN="$1"
    local NEW_LINE="$2"
    local filename="$3"
  grep -q "$PATTERN" "$filename" && \
    sed -i "/$PATTERN/s/.*/$NEW_LINE/" "$filename" || \
    printf "\n$NEW_LINE" >> "$filename"
}

ufw allow ms-sql-s 
ufw allow ms-sql-m 
ufw allow mysql 
ufw allow mysql-proxy
apt-get install mysql-server-5.6 -y -qq

mysql_secure_installation

replace_command "bind-address" "bind-address 127.0.0.1" /etc/mysql/mysql.conf.d/mysqld.cnf
replace_command "local-infile" "local-infile = 0" /etc/mysql/mysql.conf.d/mysqld.cnf
replace_command "skip-symbolic-links" "skip-symbolic-links" /etc/mysql/mysql.conf.d/mysqld.cnf

echo "------------ LOOK FOR WEIRD USERS IN DATABASE ------------"
mysql -e "SELECT user,host FROM mysql.user"

service restart mysql

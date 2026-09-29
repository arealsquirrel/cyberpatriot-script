#/bin/bash

replace_command() {
    local PATTERN="$1"
    local NEW_LINE="$2"
    local filename="$3"
  grep -q "$PATTERN" "$filename" && \
    sed -i "/$PATTERN/s/.*/$NEW_LINE/" "$filename" || \
    printf "\n$NEW_LINE" >> "$filename"
}

apt-get install apache2 -y
chown -R root:root /etc/apache2
chown -R root:root /etc/apache

replace_command "ServerTokens" "ServerTokens Prod" /etc/apache2/conf-available/security.conf
replace_command "ServerSignature" "ServerSignature Off" /etc/apache2/conf-available/security.conf
replace_command "TraceEnable" "TraceEnable Off" /etc/apache2/conf-available/security.conf
replace_command "Header always set X-Content-Type-Options" "Header always set X-Content-Type-Options \"nosniff\"" /etc/apache2/conf-available/security.conf
replace_command "Header always set X-FrameOptions" "Header always set X-Content-Type-Options \"SAMEORIGIN\"" /etc/apache2/conf-available/security.conf

a2enmod headers
a2enconf security
apache2ctl configtest 

systemctl restart apache2

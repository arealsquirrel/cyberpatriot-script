#/bin/bash

replace_command() {
    local PATTERN="$1"
    local NEW_LINE="$2"
    local filename="$3"
  grep -q "$PATTERN" "$filename" && \
    sed -i "/$PATTERN/s/.*/$NEW_LINE/" "$filename" || \
    printf "\n$NEW_LINE" >> "$filename"
}

apt install vsftpd

ufw allow ftp
ufw allow sftp
ufw allow saft
ufw allow ftps-data
ufw allow ftps

replace_command "anonymous_enable" "anonymous_enable=NO" vsftpd.conf
replace_command "chroot_local_user" "chroot_local_user=YES" vsftpd.conf
replace_command "chroot_local_user" "chroot_local_user=YES" vsftpd.conf

replace_command "ssl_enable" "ssl_enable=YES" vsftpd.conf
replace_command "force_local_logins_ssl" "force_local_logins_ssl=YES" vsftpd.conf
replace_command "force_local_data_ssl" "force_local_data_ssl=YES" vsftpd.conf

replace_command "ssl_sslv2" "ssl_sslv2=NO" vsftpd.conf
replace_command "ssl_sslv3" "ssl_sslv3=NO" vsftpd.conf

replace_command "anon_upload_enable" "anon_upload_enable=NO" vsftpd.conf
replace_command "anon_mkdir_write_enable" "anon_mkdir_write_enable=NO" vsftpd.conf
replace_command "anon_other_write_enable" "anon_other_write_enable=NO" vsftpd.conf

replace_command "max_clients" "max_clients=20" vsftpd.conf
replace_command "max_per_ip" "max_per_ip=3" vsftpd.conf
replace_command "idle_session_timeout" "idle_session_timeout=300" vsftpd.conf
replace_command "data_connection_timeout" "data_connection_timeout=60" vsftpd.conf

# sudo vsftpd -olisten=NO /etc/vsftpd.conf
# systemctl enable --now vsftpd
# sudo systemctl restart vsftpd

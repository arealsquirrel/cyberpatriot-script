
replace_command() {
    local PATTERN="$1"
    local NEW_LINE="$2"
    local filename="$3"
  grep -q "$PATTERN" "$filename" && \
    sed -i "/$PATTERN/s/.*/$NEW_LINE/" "$filename" || \
    printf "\n$NEW_LINE" >> "$filename"
}

ufw allow netbios-ns
ufw allow netbios-dgm
ufw allow netbios-ssn
ufw allow microsoft-ds

apt-get install samba -y -qq
apt-get install system-config-samba -y -qq

replace_command "server min protocol" "server min protocol = SMB2" /etc/samba/smb.conf
replace_command "restrict anonymous" "restrict anonymous = 2" /etc/samba/smb.conf
replace_command "map to guest" "map to guest = never" /etc/samba/smb.conf
replace_command "server signing" "server signing = mandatory" /etc/samba/smb.conf
replace_command "smb encrypt" "smb encrypt = desired" /etc/samba/smb.conf
replace_command "guest ok" "guest ok = no" /etc/samba/smb.conf
replace_command "browsable" "browsable = no" /etc/samba/smb.conf

testparam
pdbedit -L
systemctl restart smbd

#/bin/bash

replace_command() {
    local PATTERN="$1"
    local NEW_LINE="$2"
    local filename="$3"
  grep -q "$PATTERN" "$filename" && \
    sed -i "/$PATTERN/s/.*/$NEW_LINE/" "$filename" || \
    printf "\n$NEW_LINE" >> "$filename"
}

# apt-get install openssh-server -y -qq

echo "----------------- SECURING SSH -----------------"
cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak

replace_command "Port" "Port 22" /etc/ssh/sshd_config
replace_command "PermitRootLogin" "PermitRootLogin no" /etc/ssh/sshd_config
replace_command "MaxAuthTries" "MaxAuthTries 2" /etc/ssh/sshd_config

# no password based logins
replace_command "PasswordAuthentication" "PasswordAuthentication yes" /etc/ssh/sshd_config
replace_command "UsePAM" "UsePAM yes" /etc/ssh/sshd_config
replace_command "ChallengeResponseAuthentication" "ChallengeResponseAuthentication no" /etc/ssh/sshd_config
replace_command "KbdInteractiveAuthentication" "KbdInteractiveAuthentication no" /etc/ssh/sshd_config
replace_command "PermitEmptyPasswords" "PermitEmptyPasswords no" /etc/ssh/sshd_config

# terminate idle sessions
replace_command "ClientAliveInterval" "ClientAliveInterval 300" /etc/ssh/sshd_config
replace_command "ClientAliveCountMax" "ClientAliveCountMax 0" /etc/ssh/sshd_config

# weak and insecure features
replace_command "X11Forwarding" "X11Forwarding no" /etc/ssh/sshd_config
replace_command "HostbasedAuthentication" "HostbasedAuthentication no" /etc/ssh/sshd_config
replace_command "AllowAgentForwarding" "AllowAgentForwarding no" /etc/ssh/sshd_config
replace_command "AllowTcpForwarding" "AllowTcpForwarding no" /etc/ssh/sshd_config
replace_command "PermitTunnel" "PermitTunnel no" /etc/ssh/sshd_config
replace_command "PermitUserEnvironment" "PermitUserEnvironment no" /etc/ssh/sshd_config

# bullshit
replace_command "LoginGraceTime" "LoginGraceTime 30" /etc/ssh/sshd_config
replace_command "MaxSessions" "MaxSessions 2" /etc/ssh/sshd_config
replace_command "MaxStartups" "MaxStartups 10:30:60" /etc/ssh/sshd_config

# replace_command "AllowUsers" "AllowUsers sshusers" sshd_config

ssh-keygen -t rsa

ufw allow 22/tcp

systemctl restart sshd



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

replace_command "Port" "Port 22" sshd_config
replace_command "PermitRootLogin" "PermitRootLogin no" sshd_config
replace_command "MaxAuthTries" "MaxAuthTries 2" sshd_config

# no password based logins
replace_command "PasswordAuthentication" "PasswordAuthentication yes" sshd_config
replace_command "UsePAM" "UsePAM yes" sshd_config
replace_command "ChallengeResponseAuthentication" "ChallengeResponseAuthentication no" sshd_config
replace_command "KbdInteractiveAuthentication" "KbdInteractiveAuthentication no" sshd_config
replace_command "PermitEmptyPasswords" "PermitEmptyPasswords no" sshd_config

# terminate idle sessions
replace_command "ClientAliveInterval" "ClientAliveInterval 300" sshd_config
replace_command "ClientAliveCountMax" "ClientAliveCountMax 0" sshd_config

# weak and insecure features
replace_command "X11Forwarding" "X11Forwarding no" sshd_config
replace_command "HostbasedAuthentication" "HostbasedAuthentication no" sshd_config
replace_command "AllowAgentForwarding" "AllowAgentForwarding no" sshd_config
replace_command "AllowTcpForwarding" "AllowTcpForwarding no" sshd_config
replace_command "PermitTunnel" "PermitTunnel no" sshd_config
replace_command "PermitUserEnvironment" "PermitUserEnvironment no" sshd_config

# bullshit
replace_command "LoginGraceTime" "LoginGraceTime 30" sshd_config
replace_command "MaxSessions" "MaxSessions 2" sshd_config
replace_command "MaxStartups" "MaxStartups 10:30:60" sshd_config

# replace_command "AllowUsers" "AllowUsers sshusers" sshd_config

ssh-keygen -t rsa

ufw allow 22/tcp

systemctl restart sshd



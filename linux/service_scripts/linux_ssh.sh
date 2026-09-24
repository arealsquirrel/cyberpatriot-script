
apt-get install openssh-server -y -qq
ufw allow ssh

if [[ -f /etc/ssh/sshd_config ]]; then
    echo "Hardening SSH..."
    sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config
    sed -i 's/^#\?PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config
    sed -i 's/^#\?X11Forwarding.*/X11Forwarding no/' /etc/ssh/sshd_config
    systemctl restart sshd
fi

# do all the ssh configs

service ssh restart
mkdir ~/.ssh
chmod 700 ~/.ssh
ssh-keygen -t rsa

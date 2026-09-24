
apt install ufw
ufw enable
ufw logging on
ufw status verbose
ufw default deny incoming
ufw default allow outgoing

ufw allow ssh
ufw allow http
ufw allow https

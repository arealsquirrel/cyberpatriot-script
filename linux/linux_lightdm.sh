#/bin/bash

replace_command() {
    local PATTERN="$1"
    local NEW_LINE="$2"
    local filename="$3"
  grep -q "$PATTERN" "$filename" && \
    sed -i "/$PATTERN/s/.*/$NEW_LINE/" "$filename" || \
    printf "\n$NEW_LINE" >> "$filename"
}

echo "------------ SECURING LIGHT DM ------------"
read -p "Type in the root user: " username

replace_command "allow-guest" "allow-guest=false" /etc/lightdm/lightdm.conf
replace_command "greeter-hide-users" "greeter-hide-users=true" /etc/lightdm/lightdm.conf
replace_command "greeter-show-manual-login" "greeter-show-manual-login=true" /etc/lightdm/lightdm.conf
replace_command "autologin-user" "autologin-user=$username" /etc/lightdm/lightdm.conf
replace_command "autologin-guest" "autologin-guest=false" /etc/lightdm/lightdm.conf

chmod 644 /etc/lightdm/lightdm.conf
sed -i 's/greeter-hide-users.*/greeter-hide-users=true/' /etc/lightdm/lightdm.conf
sed -i 's/greeter-allow-guest.*/greeter-allow-guest=false/' /etc/lightdm/lightdm.conf
sed -i 's/greeter-show-manual-login.*/greeter-show-manual-login=true/' /etc/lightdm/lightdm.conf
sed -i 's/allow-guest.*/allow-guest=false/' /etc/lightdm/lightdm.conf
sed -i 's/autologin-guest.*/autologin-guest=false/' /etc/lightdm/lightdm.conf
sed -i 's/autologin-user.*/autologin-user=NONE/' /etc/lightdm/lightdm.conf

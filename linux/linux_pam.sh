#/bin/bash

replace_command() {
    local PATTERN="$1"
    local NEW_LINE="$2"
    local filename="$3"
  grep -q "$PATTERN" "$filename" && \
    sed -i "/$PATTERN/s/.*/$NEW_LINE/" "$filename" || \
    printf "\n$NEW_LINE" >> "$filename"
}

apt-get install libpam-cracklib

# make backups of files we are going to edit
cp backups/common-password /etc/pam.d/common-password
cp backups/common-auth /etc/pam.d/common-auth
cp backups/login.defs /etc/login.defs
cp backups/pwquality.conf /etc/security/pwquality.conf

sed -i 's/nullok//g' /etc/pam.d/common-auth
sed -i 's/\(pam_unix\.so.*\)$/\1 remember=5 minlen=12/' /etc/pam.d/common-password
sed -i 's/\(pam_cracklib\.so.*\)$/\1 ucredit=-1 lcredit=-1 dcredit=-1 ocredit=-1/' /etc/pam.d/common-password
# sed -i 's/# minlen = 8/minlen = 12/' /etc/security/pwquality.conf
# sed -i 's/# maxrepeat = 3/maxrepeat = 3/' /etc/security/pwquality.conf

# set good login diffs
replace_command "PASS_MIN_DAYS" "PASS_MIN_DAYS 7" /etc/login.defs
replace_command "PASS_MAX_DAYS" "PASS_MAX_DAYS 90" /etc/login.defs
replace_command "PASS_WARN_AGE" "PASS_WARN_AGE 14" /etc/login.defs
replace_command "FAILLOG_ENAB" "FAILLOG_ENAB YES" /etc/login.defs
replace_command "SYSLOG_SU_ENAB" "SYSLOG_SU_ENAB YES" /etc/login.defs
replace_command "SYSLOG_SG_ENAB" "SYSLOG_SG_ENAB YES" /etc/login.defs

# make the pam faillock
cp linux/templates/faillock /usr/share/pam-configs/faillock
cp linux/templates/faillock_reset /usr/share/pam-configs/faillock_reset
cp linux/templates/faillock_notify /usr/share/pam-configs/faillock_notify
pam-auth-update

#/bin/bash

apt-get install libpam-cracklib

# make backups of files we are going to edit
cp linux/templates/common-password /etc/pam.d/common-password
cp linux/templates/common-auth /etc/pam.d/common-auth
cp linux/templates/login.defs /etc/login.defs
cp linux/templates/pwquality.conf /etc/security/pwquality.conf

echo 'auth required pam_tally2.so deny=5 onerr=fail unlock_time=1800' >> /etc/pam.d/common-auth
sed -i 's/nullok//g' /etc/pam.d/common-auth
sed -i 's/\(pam_unix\.so.*\)$/\1 remember=5 minlen=8/' /etc/pam.d/common-password
sed -i 's/\(pam_cracklib\.so.*\)$/\1 ucredit=-1 lcredit=-1 dcredit=-1 ocredit=-1/' /etc/pam.d/common-password
sed -i 's/# minlen = 8/minlen = 12/' /etc/security/pwquality.conf
sed -i 's/# maxrepeat = 3/maxrepeat = 3/' /etc/security/pwquality.conf

# set good login diffs
sed -i '/PASS_MIN_DAYS/c\PASS_MIN_DAYS 7' /etc/login.defs
sed -i '/PASS_MAX_DAYS/c\PASS_MAX_DAYS 90' /etc/login.defs
sed -i '/PASS_WARN_AGE/c\PASS_WARN_AGE 14' /etc/login.defs
sed -i '/FAILLOG_ENAB/c\FAILLOG_ENAB YES' /etc/login.defs
sed -i '/SYSLOG_SU_ENAB/c\SYSLOG_SU_ENAB YES' /etc/login.defs
sed -i '/SYSLOG_SG_ENAB/c\SYSLOG_SG_ENAB YES' /etc/login.defs

# make the pam faillock
cp linux/templates/faillock /usr/share/pam-configs/faillock
cp linux/templates/faillock_reset /usr/share/pam-configs/faillock_reset
cp linux/templates/faillock_notify /usr/share/pam-configs/faillock_notify

pam-auth-update

#!/bin/bash

crontab -l > crontab-old
crontab -r
printTime "Crontab has been backed up. All startup tasks have been removed from crontab."

cd /etc/
/bin/rm -f cron.deny at.deny
echo root >cron.allow
echo root >at.allow
/bin/chown root:root cron.allow at.allow
/bin/chmod 400 cron.allow at.allow

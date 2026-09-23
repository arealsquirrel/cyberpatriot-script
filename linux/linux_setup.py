
from run_command import run_command

def setup_linux():
    with open("log.txt", "a") as file:
        input("IF ITS SLOW PRESS ENTER (try it out)")
        if "n" not in input("system upgrade [y/n]"):
            run_command(["sudo", "apt-get", "update"])
            run_command(["sudo", "apt-get", "full-upgrade", "-y"])
            run_command(["sudo", "apt-get", "dist-upgrade"])

        if "n" not in input("install and run antivirus scan [y/n]"):
            run_command(["sudo", "apt-get", "install", "clamtk"])
            run_command(["sudo", "freshclam"])

        if "n" not in input("enable firewall [y/n]"):
            run_command(["sudo", "apt", "install", "ufw"])
            run_command(["sudo", "ufw", "enable"])
            run_command(["sudo", "ufw", "logging", "on"])
            run_command(["sudo", "ufw", "status", "verbose"])
            run_command(["sudo", "ufw", "default", "deny", "incoming"])
            run_command(["sudo", "ufw", "default", "allow", "outgoing"])

            run_command(["sudo", "ufw", "allow", "ssh"])
            run_command(["sudo", "ufw", "allow", "http"])
            run_command(["sudo", "ufw", "allow", "https"])

        if "n" not in input("configure pam"):
            run_command(["sudo", "apt-get", "install", "libpam-cracklib"])
            run_command(["sudo", "sed", "-i", 's/pam_unix.so/pam_unix.so md5 remember=5 use_authtok minlen=12/', "/etc/pam.d/common-password"])
            run_command(["sudo", "sed", "-i", 's/nullok//g', "/etc/pam.d/common-auth"])

            run_command(["sudo", "sed", "-i", '/PASS_MIN_DAYS/c\PASS_MIN_DAYS 7', "/etc/login.defs"])
            run_command(["sudo", "sed", "-i", '/PASS_MAX_DAYS/c\PASS_MAX_DAYS 90', "/etc/login.defs"])
            run_command(["sudo", "sed", "-i", '/PASS_WARN_AGE/c\PASS_WARN_AGE 14', "/etc/login.defs"])
            run_command(["sudo", "sed", "-i", '/FAILLOG_ENAB/c\FAILLOG_ENAB YES', "/etc/login.defs"])
            run_command(["sudo", "sed", "-i", '/SYSLOG_SU_ENAB/c\SYSLOG_SU_ENAB YES', "/etc/login.defs"])
            run_command(["sudo", "sed", "-i", '/SYSLOG_SG_ENAB/c\SYSLOG_SG_ENAB YES', "/etc/login.defs"])

            run_command(["sudo", "passwd", "-l", "root"])
            run_command(["sudo", "chown", "root:root", "/etc/passwd"])
            run_command(["sudo", "chmod", "root:root", "/etc/shadow"])
            run_command(["sudo", "touch", "/etc/security/opasswd"])
            run_command(["sudo", "chmod", "root:root", "/etc/security/opasswd"])
            
        
        if "n" not in input("adding lockout policy"):
            run_command(["sudo", "cp", "good_files/linux/faillock", "/usr/share/pam-configs/faillock"])
            run_command(["sudo", "cp", "good_files/linux/faillock_reset", "/usr/share/pam-configs/faillock_reset"])
            run_command(["sudo", "cp", "good_files/linux/faillock_notify", "/usr/share/pam-configs/faillock_notify"])
            # run_command(["sudo", "pam-auth-update"])

setup_linux()


from run_command import run_command

def setup_linux():
    with open("log.txt", "a") as file:
        #run_command(["sudo", "passwd", "-l", "root"])
        #run_command(["sudo", "chmod", "640", "/etc/shadow"])
        #run_command(["sudo", "chmod", "640", "/etc/gshadow"])

        if "y" in input("system upgrade [y/n]"):
            run_command(["sudo", "apt-get", "update"])
            run_command(["sudo", "apt-get", "upgrade"])
            run_command(["sudo", "apt-get", "dist-upgrade"])

        if "y" in input("install and run antivirus scan [y/n]"):
            run_command(["sudo", "apt-get", "install", "clamtk"])
            run_command(["sudo", "freshclam"])

        if "y" in input("enable firewall [y/n]"):
            run_command(["sudo", "apt", "install", "ufw"])
            run_command(["sudo", "ufw", "enable"])


        



setup_linux()

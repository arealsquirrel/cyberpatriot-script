#!/usr/bin/env python3
"""
cp_user_sync.py — CyberPatriot README user reconciliation tool.

Reads the "Authorized Administrators and Users" section out of a CyberPatriot
README page (the WordPress <pre class="wp-block-preformatted"> block) and
reconciles the real Linux user accounts on this machine against it:

    * Deletes any local account that is NOT listed as an authorized
      administrator or authorized user.
    * Sets every remaining authorized account's password to the password
      belonging to the account marked "(you)".
    * Makes sure the "(you)" account is in the sudo/admin group, so that
      "sudo password" is effectively the you-account's password (sudo
      authenticates with the invoking user's own password by default).

Works on any README that follows the same layout, e.g.:

    Authorized Administrators:
    chowe (you)
        password: Cyb3rCont3st
    ezekiel
        password: Sup3rHum4n16

    Authorized Users:
    rowan
    kaia
    ...

USAGE
-----
    # Dry run against a live URL (default — nothing is changed)
    sudo python3 cp_user_sync.py --url https://.../README/

    # Dry run against a saved HTML file
    sudo python3 cp_user_sync.py --file readme.html

    # Actually apply the changes
    sudo python3 cp_user_sync.py --file readme.html --apply

    # Apply, but keep home directories of deleted users instead of wiping them
    sudo python3 cp_user_sync.py --file readme.html --apply --keep-home

Requires: beautifulsoup4, requests (only if using --url), and must be run
as root (or via sudo) to actually apply changes.
"""

import argparse
import getpass
import pwd
import re
import subprocess
import requests
from bs4 import BeautifulSoup
import sys
from dataclasses import dataclass, field
import pwd


try:
    from bs4 import BeautifulSoup
except ImportError:
    sys.exit("Missing dependency: pip install beautifulsoup4")


# --------------------------------------------------------------------------
# Parsing
# --------------------------------------------------------------------------

@dataclass
class AuthorizedAccounts:
    admins: dict = field(default_factory=dict)   # username -> password (or None)
    users: list = field(default_factory=list)    # usernames, no passwords listed
    you_user: str = None
    you_password: str = None

    @property
    def all_authorized(self):
        return set(self.admins) | set(self.users)

    def get_password(self):
        return you_password


def fetch_html(url: str) -> str:
    import requests
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    return resp.text


def find_readme_pre_block(soup: BeautifulSoup) -> str:
    """
    Locate the <pre> block that actually contains the authorized
    admins/users list. We don't hardcode a class name match beyond
    'pre' + the keyword, so this survives theme/markup changes.
    """
    for pre in soup.find_all("pre"):
        text = pre.get_text("\n")
        if re.search(r"Authorized\s+Administrators", text, re.IGNORECASE):
            return text
    raise ValueError(
        "Could not find an 'Authorized Administrators' <pre> block in this page. "
        "The README format may differ from what this script expects."
    )


def parse_readme(soup) -> AuthorizedAccounts:
    # soup = BeautifulSoup(html, "html.parser")
    block = find_readme_pre_block(soup)

    result = AuthorizedAccounts()

    # Split the block into the "Administrators" section and the "Users" section.
    split_re = re.compile(
        r"Authorized\s+Administrators\s*:?\s*(.*?)\s*Authorized\s+Users\s*:?\s*(.*)",
        re.IGNORECASE | re.DOTALL,
    )
    m = split_re.search(block)
    if not m:
        raise ValueError("Found the README block but couldn't split it into "
                          "Administrators / Users sections.")
    admins_text, users_text = m.group(1), m.group(2)

    # --- Administrators: "username [(you)]" then a "password: xxxx" line ---
    admin_entry_re = re.compile(
        r"^[ \t]*(?P<user>\S+)(?P<you>\s*\(\s*you\s*\))?[ \t]*\r?\n"
        r"[ \t]*password:\s*(?P<pass>\S+)",
        re.IGNORECASE | re.MULTILINE,
    )
    for entry in admin_entry_re.finditer(admins_text):
        username = entry.group("user")
        password = entry.group("pass")
        result.admins[username] = password
        if entry.group("you"):
            result.you_user = username
            result.you_password = password

    # --- Users: bare usernames, one per line, no passwords ---
    for line in users_text.splitlines():
        line = line.strip()
        if not line:
            continue
        # Stop if we've wandered past the <pre> content into something else
        if re.match(r"^[A-Za-z0-9._-]+$", line):
            you_match = re.match(r"^(\S+)\s*\(\s*you\s*\)$", line, re.IGNORECASE)
            if you_match:
                username = you_match.group(1)
                result.users.append(username)
                result.you_user = username
            else:
                result.users.append(line)

    if not result.admins and not result.users:
        raise ValueError("Parsed the README block but found zero accounts. "
                          "Check the page format.")
    if not result.you_user:
        print("WARNING: no account marked '(you)' was found. "
              "Password-sync and sudo steps will be skipped.", file=sys.stderr)

    return result


# --------------------------------------------------------------------------
# System inspection
# --------------------------------------------------------------------------

def get_human_system_users(min_uid: int = 1000, max_uid: int = 60000) -> list:
    """
    Return usernames of real human accounts on this machine: normal UID
    range, excluding 'nobody' and other placeholder accounts.
    """
    users = []
    for entry in pwd.getpwall():
        if min_uid <= entry.pw_uid <= max_uid and entry.pw_name != "nobody":
            users.append(entry.pw_name)
    return users


# --------------------------------------------------------------------------
# Actions
# --------------------------------------------------------------------------

def authorized_admins_users(context):
    accounts = parse_readme(context[0])
    system_users = get_human_system_users()
    authorized = accounts.all_authorized

    print(accounts)
    print(system_users)
    print(authorized)

    # find all the hidden users and remove em
    for sys_user in system_users:
        if sys_user not in authorized:
            print(f"random person - im going to delete it, {sys_user}")
            subprocess.run(["userdel", "--remove-home", username])

    # revoke sudo from users
    print("revoking sudo")
    for user in accounts.users:
        if user not in authorized:
            print(f"{user} does not exist, adding this user")
            subprocess.run(["useradd", "-m", user], input=inputpchange.encode())

        inputpchange = f"{user}:{accounts.you_password}"
        print(inputpchange)
        subprocess.run(["chpasswd"], input=inputpchange.encode())
        subprocess.run(["gpasswd", "-d", user, "sudo"])
        subprocess.run(["gpasswd", "-d", user, "adm"])
        subprocess.run(["gpasswd", "-d", user, "lpadmin"])
        subprocess.run(["gpasswd", "-d", user, "sambashare"])
        subprocess.run(["chage", "-M", "90", user])

    for user in accounts.admins:
        print(f"giving admin to {user}")
        subprocess.run(["gpasswd", "-a", user, "sudo"])
        subprocess.run(["gpasswd", "-a", user, "adm"])
        subprocess.run(["gpasswd", "-a", user, "lpadmin"])
        subprocess.run(["gpasswd", "-a", user, "sambashare"])

    # typical_groups = ["root", "daemon", "bin", "sys", "adm", "tty", "disk", "lp", "mail", "news", "uucp", "man", "proxy", "kmem", "dialout", "fax", "voice", "cdrom", "floppy", "tape", "sudo", "audio", "dip", "www-data", "backup", "operator", "list", "irc", "src", "gnats", "shadow", "utmp", "video", "sasl", "plugdev", "staff", "games", "users"]
    typical_users = ["root", "daemon", "bin", "sys", "sync", "games", "man", "lp", "mail", "news", "uucp", "proxy", "www-data", "backup", "list", "irc", "systemd-network", "systemd-resolve", "messagebus", "syslog", "uuidd", "lightdm", "avahi", "colord", "cups", "dnsmasq", "geoclue", "ntp", "polkitd", "saned", "speech-dispatcher", "statd", "systemd-coredump", "systemd-timesync", "tcpdump", "usbmux"]

    with open('/etc/passwd', 'r') as f:
        for line in f:
            parts = line.strip().split(':')
            username = parts[0]
            uid = int(parts[2])
            if uid < 1000 and username not in typical_users:
                if "y" in input(f"do ya wanna delete {username} (y/n): "):
                    print(f"{username} (UID: {uid})")
                    subprocess.run(["userdel", "--remove-home", username])


if __name__ == '__main__':
    url = input("gimme the read me url: ") #https://www.uscyberpatriot.org/competition/scenario/390849r4g8oab/"
    response = requests.get(url)
    if response.status_code != 200:
        print("[x] invalid url!")
        exit(1)
    print("[!] url returned 200 (very good)")
    soup = BeautifulSoup(response.text, "html.parser")
    response = requests.get(url)
    log_file = open("log.txt", "w")
    context = [soup, log_file]
    authorized_admins_users(context)
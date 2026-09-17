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
import sys
from dataclasses import dataclass, field

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

def run(cmd, apply_changes: bool):
    printable = " ".join(cmd)
    if apply_changes:
        print(f"  $ {printable}")
        subprocess.run(cmd, check=True)
    else:
        print(f"  [dry-run] would run: {printable}")


def delete_unauthorized_users(system_users, authorized, apply_changes, keep_home, protect):
    to_delete = [u for u in system_users if u not in authorized and u not in protect]
    if not to_delete:
        print("No unauthorized accounts found.")
        return
    print(f"Unauthorized accounts to delete: {', '.join(to_delete)}")
    for user in to_delete:
        cmd = ["userdel"]
        if not keep_home:
            cmd.append("-r")
        cmd.append(user)
        run(cmd, apply_changes)


def set_passwords(authorized_present, password, apply_changes):
    if not password:
        print("Skipping password sync — no '(you)' password was found.")
        return
    print(f"Setting password for: {', '.join(sorted(authorized_present))}")
    if apply_changes:
        payload = "\n".join(f"{u}:{password}" for u in authorized_present) + "\n"
        subprocess.run(["chpasswd"], input=payload, text=True, check=True)
    else:
        for u in sorted(authorized_present):
            print(f"  [dry-run] would run: echo '{u}:********' | chpasswd")


def ensure_sudo_access(you_user, apply_changes):
    if not you_user:
        return
    # 'sudo' is the standard admin group on Debian/Ubuntu/Mint.
    print(f"Ensuring '{you_user}' has sudo rights (sudo auth uses their own password).")
    run(["usermod", "-aG", "sudo", you_user], apply_changes)

SUDO_GROUP_CANDIDATES = ("sudo", "admin", "wheel")
 
 
def get_sudo_group_name() -> str:
    """Return whichever admin group actually exists on this system."""
    for name in SUDO_GROUP_CANDIDATES:
        try:
            grp.getgrnam(name)
            return name
        except KeyError:
            continue
    # Default assumption for Debian/Ubuntu/Mint if none exist yet.
    return "sudo"
 
def get_group_members(group_name: str) -> set:
    try:
        return set(grp.getgrnam(group_name).gr_mem)
    except KeyError:
        return set()
 
def reconcile_sudo_access(admin_users, non_admin_users, apply_changes):
    """
    Make sudo-group membership match the authorized administrators list
    exactly: every authorized admin who still exists on the system gets
    added, and anyone else currently in the group — including authorized
    *users* who aren't admins — gets removed.
    """
    group_name = get_sudo_group_name()
    current_members = get_group_members(group_name)
 
    target_admins = set(admin_users)
    to_add = sorted(target_admins - current_members)
    to_remove = sorted(current_members - target_admins)
 
    if to_add:
        print(f"Granting '{group_name}' group membership to: {', '.join(to_add)}")
        for user in to_add:
            run(["usermod", "-aG", group_name, user], apply_changes)
    else:
        print(f"All authorized administrators already have '{group_name}' access.")
 
    if to_remove:
        print(f"Revoking '{group_name}' group membership from: {', '.join(to_remove)}")
        for user in to_remove:
            run(["gpasswd", "-d", user, group_name], apply_changes)
    else:
        print(f"No non-administrator accounts currently hold '{group_name}' access.")


def authorized_admins_users(context):
    accounts = parse_readme(context[0])
    system_users = get_human_system_users()
    authorized = accounts.all_authorized

    # context.you_user = accounts.you_user
    # context.you_password = accounts.you_password

    print(accounts)
    print(system_users)
    print(authorized)

    # delete_unauthorized_users(system_users, authorized, args.apply, args.keep_home, protect)
    #remaining = [u for u in system_users if u in authorized]
    #set_passwords(remaining, accounts.you_password, args.apply)
    #ensure_sudo_access(accounts.you_user, args.apply)
    #admin_present = [u for u in system_users if u in accounts.admins]
    #non_admin_present = [u for u in system_users if u in accounts.users]
    #reconcile_sudo_access(admin_present, non_admin_present, args.apply)



if __name__ == "__main__":
    main()

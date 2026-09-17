
import requests
from bs4 import BeautifulSoup
from linux.authroized_admins_users import authorized_admins_users

class Context:
    def __init__(self, soup, log_file, you_user, you_password):
        self.soup = soup
        self.log_file = log_file
        self.you_user = you_user
        self.you_password = you_password

if __name__ == '__main__':
    url = "https://www.uscyberpatriot.org/competition/scenario/390849r4g8oab/"
    response = requests.get(url)
    os = ""

    if response.status_code != 200:
        print("[x] invalid url!")
        exit(1)

    print("[!] url returned 200 (very good)")
    soup = BeautifulSoup(response.text, "html.parser")

    # ----------- OS DETECTION -----------
    print("[*] trying OS detection")
    quotes = soup.find_all("h1", class_="entry-title")
    if "Linux" in str(quotes[0]):
        os = "Linux"
    else:
        os = input("[x] os detection failed, please enter os CASE SENSITIVE (Linux, Windows): ")
    print("[!] found OS " + os)

    log_file = open("log.txt", "w")
    context = [soup, log_file]

    if os == "Linux":
        authorized_admins_users(context)
    
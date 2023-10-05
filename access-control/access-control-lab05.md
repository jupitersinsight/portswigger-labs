_Testing for Bypassing Authorization Schema (OWASP)_: https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/05-Authorization_Testing/02-Testing_for_Bypassing_Authorization_Schema

### Lab: URL-based access control can be circumvented

This website has an unauthenticated admin panel at /admin, but a front-end system has been configured to block external access to that path. However, the back-end application is built on a framework that supports the X-Original-URL header.

To solve the lab, access the admin panel and delete the user carlos.


_____

Exploit&Test:

1. Trying to access the Admin panel at /admin returns the error message: "Access denied"
2. **[BURP REPEATER]** Testing HTTP Header "X-Original-URL"
    1. As stated in the OWASP link, sent GET / with "X-Original-URL /donotexist1" and the server returned the error message "Not Found", meaning the Web Framework **does** support the HTTP header
3. **[BURP REPEATER]** Sent GET / with X-Original-Url: /admin, the web server returned the admin panel webpage (status code 200)
4. **[BURP REPEATER]** Sent GET / with X-Original-Url: /admin and params "username=carlos" ==> User carlos deleted successfully
    1. Response = status code 302 Found

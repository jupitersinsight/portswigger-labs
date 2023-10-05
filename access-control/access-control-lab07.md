### Lab: User ID controlled by request parameter

This lab has a horizontal privilege escalation vulnerability on the user account page.

To solve the lab, obtain the API key for the user carlos and submit it as the solution.

You can log in to your own account using the following credentials: wiener:peter


_____

Exploit:

1. Access as user _wiener_
    1. Send GET request for the _/my-account?id=wiener_ resource to Burp Repeater
2. **[BURP-REPEATER]** Change username in request from _wiener_ to _carlos_:  _/my-account?id=carlos_
    1. Extract carlos API key from the response
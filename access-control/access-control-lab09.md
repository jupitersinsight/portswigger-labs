### Lab: User ID controlled by request parameter with data leakage in redirect


This lab contains an access control vulnerability where sensitive information is leaked in the body of a redirect response.

To solve the lab, obtain the API key for the user carlos and submit it as the solution.

You can log in to your own account using the following credentials: wiener:peter

_____

Analysis and Exploit:

1. Login as user _wiener_, redirect to **/my-account**
    1. Click on _My Account_ reveals in the URL syntax of the query and the user id: **/my-account?id=wiener**
2. Changing the user id from _wiener_ to _carlos_ results in a redirect to **/login**
    1. The redirect 302 contains the information requests even if not rendered in the browser
    2. **[BURP-PROXY]** Intercept the redirect which contains the API KEY of carlos
        1. Be sure to check that it's carlos' (look for strings in the body of the response)
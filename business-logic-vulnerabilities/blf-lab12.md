#### Lab: Authentication bypass via encryption oracle  

This lab contains a logic flaw that exposes an encryption oracle to users.  
To solve the lab, exploit this flaw to gain access to the admin panel and delete Carlos.

You can log in to your own account using the following credentials: wiener:peter

_____

Analysis and Exploit:

1. Login form is composed by 3 input field: username, password, checkbox to "stay loggedin"
    - Log-in w/o checkbox: _session cookie_
    - Log-in w/ checkbox: _session cookie_ + _stay-logged-in cookie_
2. My-Account page has an input field that can be used to change the currente-mail ('wiener@normal-user.net') to a new one
    - Email changed (all ok)
3. Can leave comment under blog posts
    - Using an invalid email address results in an error message displayed in the page ("Invalid email address: [EMAIL]") and a new cookie _notification_ to be set for **/post**
4. That cookie is a ciphertext
    - The error message "Invalid email address: [EMAIL]" is set as cookie via Set-Cookie on POST
    - Likewise, the content of the cookie is decrypted on GET requests (to **/post** as set in the cookie validity domain)
5. Pasting the _stay-logged-in_ cookie in the _notification_ one and sending a GET request, results in the decrypt of the former one: [USERNAME]:[TIMESTAMP]
    - POST with email value='administrator:[TIMESTAMP FROM 5]
    - Paste the new notification cookie in the GET request and take note of the prefix pattern (Invalid email address: )
6. Send the encoded notification cookie to **[BURP-DECODER]**
    - Decode as URL, then as Base64
    - In the hex editor delete the first 23 bytes (Invalid email address: )
    - Re-encode the data as Base64, then URL (use external URL encoder)
    - Paste the modified cookie in the _notification_ cookie of the GET request and send
7. Upon receiving the cookie, the web server returns an error: "Input length must be multiple of 16 when decrypting with padded cipher"
    - Add 9 bytes (9 times 'x') adding this way 32 bytes before the useful data
        - Bytes that will be removed are:"Invalid email address: xxxxxxxxx"
    - Add 9 times x before the string 'administrator:[TIMESTAMP]' as the email value and send the POST request, check the decryption using the GET request
8. If the new value is descrypted, send the new _notification_ cookie to **[BURP-DECODER]**
    - Repeat steps of point 6 but this time delete 32 bytes
    - Check then if the new cookie sent via GET is decrypted in "administrator:[TIMESTAMP]"
9. Replace the _stay-logged-in_ cookie in a new request GET **/** in **[BURP-REPEATER]**
    - Delete the session cookie and send the request
    - If everything went correctly the _Admin panel_ should the there
10. GET **/admin**
    - To delete the user _carlos_: GET **/admin/delete?username=carlos**


_____

Script:

1. Log-in as user _wiener_ (psw: peter) | POST **/login** | params: csrf, username, password, stay-logged-in (**on** | or missing if not needed)
2. Decrypt the cookie _stay-logged-in_ | GET **/post?postId=[ID]** | params: cookies
    - notification: stay-logged-in (content)
3. Retrieve the content in the response from point 2
    - BeautifulSoup : \<header class="notification-header">.content
    - Split the value at ':' and store the timestamp
4. Try to forge a new cookie _stay-logged-in_ | POST **/post/comment** | params: csrf, postId, comment, name, email, website
    - csrf from GET **/post?postId=[ID]**
    - postId: [ID]
    - comment: 'test'
    - name: 'test'
    - email: 'xxxxxxxxxadministrator:[timestamp]'
    - website: 'http://www.test.test'
5. Retrieve the content repeating point 3
6. Decode and delete the first 32-bytes of the new _notification_ cookie
    - URL-decode it
    - Base64-decode it
    - Delete the first 32-bytes
7. Re-encode the modified cookie
    - Base64-encode it
    - URL-encode it
8. Repeat point 4 and 3 to verify the integrity of the new cookie
9. Log-in using the new cookie | GET **/login** | params: cookies
    - stay-logged-in: new stay-logged-in
    - if "Log out" and "Admin panel" not in response, stops
10. Delete user _carlos_ | GET **/admin/delete?username=carlos** | params: cookies
    - stay-logged-in: new stay-logged-in
    - if the status code is not 200, stops

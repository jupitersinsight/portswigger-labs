### Lab: Exploiting XSS to perform CSRF

This lab contains a stored XSS vulnerability in the blog comments function. To solve the lab, exploit the vulnerability to perform a CSRF attack and change the email address of someone who views the blog post comments.

You can log in to your own account using the following credentials: wiener:peter

_____

Analysis and Exploit:

1. Log-in as user wiener (password: peter)
2. Test 'change-email' functionality
3. Use XSS vulnerable comment section to store an XSS that trigger the 'chane-email' function for logged-in users visiting the 'infected' blog post


_____

Script notes:

1. POST **/login**
    - csrf
    - username
    - password

2. POST **/my-account/change-email**
    - email
    - csrf

3. POST **/post/comment**
    - csrf
    - postId
    - comment
    - name
    - email
    - website


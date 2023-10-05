### Lab: Inconsistent security controls

This lab's flawed logic allows arbitrary users to access administrative functionality that should only be available to company employees.  
To solve the lab, access the admin panel and delete Carlos.


_____

Analysis and Exploit:

1. Browsing the page /admin returns the message "Admin interface only available if logged in as a DontWannaCry user"
2. Create new user and confirm activation from email client
3. Once logged-in there is a form where one can input a new email address and change it
    - Change the email to something@dontwannacry.com
4. As soon as the email changes the _Admin panel_ button appears
    - From there one can delete the registered users


_____

Script:

1. Store the main url and the exploit-server url
    - If the number of arguments is less than 2 thows an error
2. Register a new user | POST **/register** | params: csrf, username, email, password
    - csrf token from GET **/register**
    - email client must be [SOMETHING]@[EXPLOIT-URL]
3. Confirm the registration from email
    - To view raw email content GET **/email?raw=[INT]** where INT=0 is the first email received
    - Extract the activation URL and send GET request
4. Log-in as the newly created user | POST **/login** | params: csrf, username, password
    - csrf token from GET **/login**
5. Once logged in change the email | POST **/my-account/change-email** | params: csrf, email
    - csrf token from GET **/my-account**
    - email must be [SOMETHING]@[dontwannacry.com]
6. Delete user carlos | GET **/admin/delete?username=carlos**
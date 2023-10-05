### Lab: Inconsistent handling of exceptional input

This lab doesn't adequately validate user input.  
You can exploit a logic flaw in its account registration process to gain access to administrative functionality.  
To solve the lab, access the admin panel and delete Carlos.


_____

Analysis and Exploit: (Used PortSwigger solution)

1. Open the registration page | GET **/register**
    - Trying to register as _administrator_ : "An account already exists with that username"
2. There is and admin page /admin, message: "Admin interface only available if logged in as a DontWannaCry user"
3. Registering an account using a very long email address like a(x200)@[DOMAIN]
    - in the Email client (which allows to read emails for all addresses in the @[DOMAIN]) click the activation link
    - Logging-in as the newly created user displays the registration email but it is truncated at 255 chars
4. Register another user but using an email like this: (index0) [RANDOM-NAME]@[dontwannacry.com] (index255).[DOMAIN]
    - Logging-in as the newly created user, the webapp displays the registration email being cropped at exactly donwannacry.com, meaning the user is considered to be an admin
    - Access the now available admin panel and delete the user _carlos_


_____

Script:

1. Store the main url and the exploit-server url
    - If the number of arguments is less than 2 then throws an error
2. Register a new user | POST **/register** | params: csrf, username, email, password
    - csrf token | GET **/register**
    - the email address must be [RANDOM CHARSx242]@[dontwannacry.com].[exploit-server domain]
3. Retrieve the confirmation url from the confirmation email and confirm
    - GET **/email?raw=[ID]**
    - GET request to the confirmation url
4. Log-in as the newly created user | POST **/login** | params: csrf, username, password
    - check if the _Admin panel_ is there
5. Delete the user _carlos_
    - GET **/admin/delete?username=carlos**
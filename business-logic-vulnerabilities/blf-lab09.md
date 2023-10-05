### Lab: Authentication bypass via flawed state machine


This lab makes flawed assumptions about the sequence of events in the login process.  
To solve the lab, exploit this flaw to bypass the lab's authentication, access the admin interface, and delete Carlos.

You can log in to your own account using the following credentials: wiener:peter

_____

Analysis and Exploit:

1. Log-in as _wiener_ (**/login**)
    1. Redirect to **/role-selector**
        - Two options available: _User_ and _Content author_
    2. If the role _User_ is selected, redirect to **/** but stays logged-in
    3. If the role _Content author_ is selected, same as 2
    4. **[BURP-REPEATER]** Sending the POST request to change the user role results in message: "No login credentials provided"
2. Intercepting traffic and trying to modify the role into _admin_ or _administrator_ did not work
3. Intercepting traffic, droppgin redirect to **/role-selector** after login, shows how the webapp defaults to _administrator_ (**/my-account**) hence granting access to **/admin**
    - **[BRUP-PROXY]** Log-in
    - **[BRUP-PROXY]** Drop redirect to **/role-selector**
    - **[BRUP-PROXY]** Browse to **/** and see that _Admin panel_ button is there
    - **[BRUP-PROXY]** Open the _Admin panel_ and delete the user _carlos_
4. Delete the user _carlos_ **/admin/delete?username=carlos**
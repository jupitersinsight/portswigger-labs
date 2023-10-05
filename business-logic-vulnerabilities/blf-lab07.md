### Lab: Weak isolation on dual-use endpoint

This lab makes a flawed assumption about the user's privilege level based on their input.  
As a result, you can exploit the logic of its account management features to gain access to arbitrary users' accounts.  
To solve the lab, access the administrator account and delete Carlos.

You can log in to your own account using the following credentials: wiener:peter

_____

Analysis and Exploit:


1. Comment form in blog posts which accepts a _comment_, a _name_, an _email_, and a _website_
2. Login requires a _username_ and a _password_
    1. Update email only checks if the input contains the char @
3. At /my-account (after successful login) there is a field to update the email and a 4 input field form to change the password (_username_, _current password_, _new password_, _confirma new password_)
    1. Different new passwords: "New passwords do not match"
    2. Wrong current password: "Current password is incorrect"
    3. Deleting the param _current-password_: "Password changed successfully!"
        1. Send request **[BURP-REPEATER]** without current password and change username to administrator: "Password changed successfully!"
4. The admin page is reachable only for admin users: "Admin interface only available if logged in as an administrator"
5. Log-in as _administrator_ using the new password
6. Reach the admin panel and delete the user carlos

_____

Script:

1. Log-in as user _wiener_ (psw: _peter_) | POST **/login** | params: csrf, username, password
    - csrf token from GET **/login**
    - check if string "Log out" and "wiener" are in the reponse
2. Change the password for the user _administrator_ | POST **/my-account/change-password** | params: csrf, username, new-password-1, new-password-2
    - csrf token from GET **/my-account**
    - check if "Password changed successfully" is in the response
3. Log-in as the user _administrator_ | POST **/login** | params: csrf, username, password
    - csrf token from GET **/login**
    - check if "Admin panel" is in the response
4. Delete user _carlos_ | GET **/admin/delete?username=carlos"**
    - check if "Deleted successfully" is in the response


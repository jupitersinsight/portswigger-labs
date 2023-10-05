### Lab: Multi-step process with no access control on one step

This lab has an admin panel with a flawed multi-step process for changing a user's role.
You can familiarize yourself with the admin panel by logging in using the credentials administrator:admin.

To solve the lab, log in using the credentials wiener:peter and exploit the flawed access controls to promote yourself to become an administrator.


_____

Analysis and Exploit:

1. Login as _administrator_
    1. POST **/login**; params required are username and password
    2. Redirect 302 to **/my-account**
2. Access _Admin panel_
    1. List of users and properties (NORMAL or ADMIN)
3. Change level from NORMAL to ADMIN for user _carlos_
    1. POST **/admin-roles**; params required are username and action (upgrade | downgrade)
    2. Returns a page to confirm action
    3. To confirm action, POST **/admin-roles**; params required action (upgrade|downgrade), confirmed (true|false) and username
    4. Redirect to **/admin**
4. **[BURP-REPEATER]** Send request at 3.3 using cookies from authenticated session of user _wiener_
5. Login as _wiener_ and check if the _Admin Panel_ is visible

### Lab: Method-based access control can be circumvented

This lab implements access controls based partly on the HTTP method of requests.
You can familiarize yourself with the admin panel by logging in using the credentials administrator:admin.

To solve the lab, log in using the credentials wiener:peter and exploit the flawed access controls to promote yourself to become an administrator.


_____

Exploit:

1.  Accessing as user 'administrator'. Taking note of the post request used to promote users to the administrator role.

    **URL**: POST /admin-roles  
    **PARAMS**: username=[USER]]&action=upgrade

2. Accessing as the regular user 'wiener'.
    1. **[BURP-REPEATER]** Trying to send a post request to /admin-roles to self promote (changing the value of the username param), results in error "Unauthorized"
3. **[BURP-REPEATER]** Changing the session cookie of the POST request caught at point 1, with the session cookie from point 2.  
Changing then the request method from POST to GET (right click -> change request method), resuslts in: **GET /admin-roles?username=wiener&action=upgrade**

IMPORTANT... ACCESS CONTROLS BASED ON HTTP METHOD CAN BE BYPASSED... REMEMBER TO CHANGE THE REQUESTED PAGE ACCONRDINGLY TO THE WEB APP FUNCTION (AS JUST SEEN)
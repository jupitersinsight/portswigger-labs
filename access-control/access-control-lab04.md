### Lab: User role can be modified in user profile

This lab has an admin panel at /admin.  It's only accessible to logged-in users with a roleid of 2.

Solve the lab by accessing the admin panel and using it to delete the user carlos.

You can log in to your own account using the following credentials: wiener:peter


_____

Expoit:  
1. Log as user wiener, use the provided button/function to change email to something else  
    1. [BURP-REPEATER] Notice that the response to the request made at point 1 contains a "roleid" parameter (with value 1)  
    2. [BURP-REPEATER] Send a new request to change the email, this adding a string to the JSON-like set of data: "roleid": 2  (/my-account/change-email)  
2. Access /admin (keep using the authorized session cookie from previous login as user wiener): if "Admin panel" is there, the exploit worked  
    1. Access to /admin with wrong roleid: "Admin interface only available if logged in as an administrator".  
3. Delete user carlos (/admin/delete?username=carlos), if deleted successfully: "User deleted successfully!"  
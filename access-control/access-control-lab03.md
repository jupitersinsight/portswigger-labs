### Lab: User role controlled by request parameter

This lab has an admin panel at /admin, which identifies administrators using a forgeable cookie.

Solve the lab by accessing the admin panel and using it to delete the user carlos.

You can log in to your own account using the following credentials: wiener:peter


_____

Exploit:  

1. [BURP] The cookie got from the server (just by visiting a random page) contains an explicit value to help the webapp to indentify admin users: Cookie: Admin=false; session=euv2qQJf6peigg1Ou0xhqumKf9OxdkTK  
    1. [BURP-REPEATER] Trying to access /admin with the cookie value "Admin" set to False, results in the following error message: "Admin interface only available if logged in as an administrator"  
    2. [BURP-REPEATER] Trying to access /admin with the cookie value "Admin" set to True, results in the admin-panel being loaded (String "Admin panel" present)  
2. [WEBBROSER] Manually changing the cookie value to True and accessing /admin  
    1. Delete user "carlos" (/admin/delete?username=carlos), message returned: "User deleted successfully!"  

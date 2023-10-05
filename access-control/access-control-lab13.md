### Lab: Referer-based access control

This lab controls access to certain admin functionality based on the Referer header.
You can familiarize yourself with the admin panel by logging in using the credentials administrator:admin.

To solve the lab, log in using the credentials wiener:peter and exploit the flawed access controls to promote yourself to become an administrator.

_____

Analysis and Exploit:

1. Log-in as _administrator_, params required are username and password, redirect to **/my-account**
    1. Access the _Admin panel_ at **/admin**
2. Upgrade user _carlos_ to admin role, GET request for **/admin-roles?username=carlos&action=upgrade**
    1. Send the same GET Request (be sure to keep the **referer** as *.web-security-academy.net/admin) and set cookie to an authorized session cookie of a regular user like _wiener_
    2. Redirect 302 to **/admin**, check if the _Admin panel_ is there
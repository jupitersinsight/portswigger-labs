### Lab: User ID controlled by request parameter with password disclosure

This lab has user account page that contains the current user's existing password, prefilled in a masked input.

To solve the lab, retrieve the administrator's password, then use it to delete carlos.

You can log in to your own account using the following credentials: wiener:peter


_____

Analysis and Exploit:

1. Login as user _wiener_, redirect to **/my-account** 
    1. Click on _My Account_ button reveals syntax and user id: **/my-account?id=wiener**
2. As stated in the lab instructions, there is a prefilled password field
    1. **[BURP-PROXY]** The prefilled password is the current password of the user
3. **[BURP-REPEATER]** Send a GET request **/my-account?id=administrator**
    1. Since the current password is there, in the prefilled password field, it can be extracted
    ```<input required type=password name=password value='qhbdqfl9rr1lf7i2pl1e'/>```
4. Login as user _administrator_, redirect to ***/my-account**
    1. Access the _Admin Panel_ (**/admin**)
    2. Delete user _carlos_ (**/admin/delete?username=carlos**)

### Lab: User ID controlled by request parameter, with unpredictable user IDs


This lab has a horizontal privilege escalation vulnerability on the user account page, but identifies users with GUIDs.

To solve the lab, find the GUID for carlos, then submit his API key as the solution.

You can log in to your own account using the following credentials: wiener:peter

_____

Analysis and Exploit:
1. Access as user _wiener_ generated a random id: (click the _My Account_ button to reveal id in the URL) **/my-account?id=ef0febe7-ee02-4c02-928d-d42a3451b698**
    1. Params needed to login: csrf token, username, password
    2. After login, 302 status code received and redirected to _/my-account_ (need to check if the login was successful)
2. Browsing the app, the user _carlos_ appears to be the author of some posts (as other users are)
    1. The script should then iterate though posts (**/post?postId=4**) looking for specific entries like
    ```<span id=blog-author><a href='/blogs?userId=b7fc4672-cb6b-41d0-9126-6709a686e95a'>carlos</a></span>```
    2. Extract _carlos_' user id
3. **[BURP-REPEATER]** send a GET request in the form: **/my-account?id=b7fc4672-cb6b-41d0-9126-6709a686e95a**
    1. Check if the login was successful
    2. Extract the API Key
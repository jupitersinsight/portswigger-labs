### Lab: Unprotected admin functionality with unpredictable URL

This lab has an unprotected admin panel.
It's located at an unpredictable location, but the location is disclosed somewhere in the application.

Solve the lab by accessing the admin panel, and using it to delete the user carlos.


_____

Exploit:
1. [BURP] Request /login  
    1. Script found:  
        ```javascript
        var isAdmin = false;  
        if (isAdmin) {  
        var topLinksTag = document.getElementsByClassName("top-links")[0];  
        var adminPanelTag = document.createElement('a');  
        adminPanelTag.setAttribute('href', '/admin-eqdbsm');  ===> random name changes as the session cookie sent along with the GET /login request changes  
        adminPanelTag.innerText = 'Admin panel';  
        topLinksTag.append(adminPanelTag);  
        var pTag = document.createElement('p');  
        pTag.innerText = '|';  
        topLinksTag.appendChild(pTag);}
        ``` 
2. Visit /admin-eqdbsm  
3. Delete user 'carlos'  
    1. Upon successful deletion: User deleted successfully!  
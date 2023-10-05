## Lab: Modifying serialized objects

This lab uses a serialization-based session mechanism and is vulnerable to privilege escalation as a result. To solve the lab, edit the serialized object in the session cookie to exploit this vulnerability and gain administrative privileges. Then, delete the user **carlos**.

You can log in to your own account using the following credentials: **wiener:peter**

### Exploit and analysis

1. Login as user _wiener_
    1. Intercept proxy and capture cookie session
2. Decode the cookie (base64 encoding)
    1. `Tzo0OiJVc2VyIjoyOntzOjg6InVzZXJuYW1lIjtzOjY6IndpZW5lciI7czo1OiJhZG1pbiI7YjowO30%3d;` = `O:4:"User":2:{s:8:"username";s:6:"wiener";s:5:"admin";b:0;};`  

PHP serialization syntax:

- `O:4`: Object made by 4-character => User
- `2`: Made by two arguments
- `s:8:"username"`: First key of the first argument
- `s:6:"wiener"`: First value of the first argument
- `s:5:"admin"`: First key of the second argument
- `b:0`: First value of the second argument

3. Change boolean value of **b** from 0 to 1
    1. Base64 encode the cookie
    2. Repeat request for **/my-account?id=wiener**
    3. Note that a link for **Admin panel** is not available

```html
 <div>
    <span>carlos - </span>
    <a href="/admin/delete?username=carlos">Delete</a>
</div>
```

4. Perform a GET request for the URL above and delete the user carlos
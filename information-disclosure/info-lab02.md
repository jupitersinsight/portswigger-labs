### Lab: Information disclosure on debug page

This lab contains a debug page that discloses sensitive information about the application.
To solve the lab, obtain and submit the SECRET_KEY environment variable.

_____

Exploit:
1) At the bottom of every page (even /) there is this comment: "<!-- <a href=/cgi-bin/phpinfo.php>Debug</a> -->"
2) Sending a GET request via Repeater for the php file from the comment, return a reponse in which there is a lot of debug information (the SECRET_KEY value included)
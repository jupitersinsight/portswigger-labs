### Lab: Authentication bypass via information disclosure

This lab's administration interface has an authentication bypass vulnerability, but it is impractical to exploit without knowledge of a custom HTTP header used by the front-end.

To solve the lab, obtain the header name then use it to bypass the lab's authentication.
Access the admin interface and delete Carlos's account.

You can log in to your own account using the following credentials: wiener:peter


_____

Exploit:
1) In Burp Repeater - TRACE / ==> Take notice of the additional parameter in the response: X-Custom-Ip-Authorization: [IP]
2) In Burp Repeater - GET /admin ==> Add string "X-Custom-Ip-Authorization: 127.0.0.1" (127.0.0.1 because only authorized IPs are allowed)
3) Delete user carlos


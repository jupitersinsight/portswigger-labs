### Lab: Information disclosure in error messages

his lab's verbose error messages reveal that it is using a vulnerable version of a third-party framework.  
To solve the lab, obtain and submit the version number of this framework.


____

Exploit:
1) In BurpSuite capture GET request for a product (random pick) and sent it to the Repeater module
2) Modify the query from "GET /product?productId=[NUMBER]" to "GET /product?productId=[LETTER]"
3) Since the remote server expects to receive a number (an integer) but receives a letter instead, throws an error in which the version number of the framework can be found



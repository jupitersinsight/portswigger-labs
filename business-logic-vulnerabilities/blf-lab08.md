### Lab: Insufficient workflow validation

This lab makes flawed assumptions about the sequence of events in the purchasing workflow.  
To solve the lab, exploit this flaw to buy a "Lightweight l33t leather jacket".

You can log in to your own account using the following credentials: wiener:peter


_____

Analysis and Exploit:

1. Log-in as the user wiener
    - requires _username_ and _password_
    - wallet: $ 100.00
2. Add the "Jacket" to cart
    - price: $ 1337.00
3. Place order with insufficient credits: "Not enough store credit for this purchase"
4. Attempts at altering the workflow:
    1. After a successful checkout the application redirects to the page **/cart/order-confirmation?order-confirmed=true**
    2. If trying to request the page from **[BURP-REPEATER]** without completing a purchase, an error message is returned
    3. If repeating the task above after having purchased something affordable and having then added the jacket to cart, the order completes successfully


_____

Script:

1. Log-in as user _wiener_ (psw: _peter_) | POST **/login** | params: csrf, username, password
    - csrf token from GET **/login**
    - if "Log out" and "wiener" not in response, stops
2. Add to cart something affordable | POST **/cart** | params: productId, redir, quantity
    - productId must be greater than 1 (since 1 is the jacket)
3. Place the order | POST **/cart/checkout** | params: csrf
    - csrf token from GET **/cart**
    - if "Your order is on its way!" not in response, stops
4. Add the jacket to cart | POST **/cart** | params: productId, redir, quantity
    - productId must be 1
5. Skip the checkout and asks for the order confirmation page | GET **/cart/order-confirmation?order-confirmed=true**
    - if "Your order is on its way!" not in response, stops
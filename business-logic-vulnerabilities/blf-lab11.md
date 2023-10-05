### Lab: Infinite money logic flaw

This lab has a logic flaw in its purchasing workflow.  
To solve the lab, exploit this flaw to buy a "Lightweight l33t leather jacket".

You can log in to your own account using the following credentials: wiener:peter


_____

Analysis and Exploit:

1. Bottom page, newsletter signup, insert fake email: "Use coupon SIGNUP30 at checkout"
2. Log-in as user _wiener_
    - Wallet is $100.00
    - Can change email
    - Can Redeem code for Gift Cards
3. Bought Gift Card x1 for $10.00
    - Received code (like soWwI7Q4zq)
    - Same code received via email to registered email in the account profile
4. Reedem code gives back $10.00
    - **[BURP-REPEATER]** Trying repeating/reusing the same gift code results in error message: "Invalid gift card"
5. Bought Gift Cards x10 for $100.00
    - Received 10 codes in 10 emails (1 code per single email)
6. Discount coupon SIGNUP30 can be applied to the cart even with gift cards in the shopping cart
7. Price of the jacket is $1337.00 - $401.10 (SIGNUP30) = $935.90
    - Price of gift cards is $10.00 - $3.00 (SIGNUP30) = $7.00
    - 935.90/7 = 133.7 (134)


_____

Script:

1. Log-in as user _wiener_ | POST **/login** | params: csrf, username, password
    - csrf from GET **/login**
    - username _wiener_
    - password _peter_
    - if "Log out" and "wiener" not in response exit the script
2. Add gift card to cart | POST **/cart** | params: productId, redir, quantity
    - productId = 2
    - redir : PRODUCT or CART
    - quantitiy = 1
    - if the response status is not 200 exit the script
3. Apply coupon to the shopping cart | POST **/cart/coupon** | params: csrf, coupon
    - csrf from GET **/cart**
    - coupon = SIGNUP30
    - if the response status is not 200 exit the script
4. Place order | POST **/cart/checkout** | params: csrf
    - csrf from GET **/cart**
    - if "Your order is on its way" not in response exit the script
    - follow redirect **/cart/order-confirmation?order-confirmed=true**
        - retrieve code from within the body of the response
5. Reedem code | POST **/gift-card** | params: csrf, gift-card
    - csrf from GET **/my-account?id=wiener**
6. Check wallet
    - retrieve balance from "Store credt:"
    - keep repeating points 5 and 6 until wallet is > $935.00
7. Add jacket to cart | POST **/cart** | params: productId, redir, quantity
    - productId = 1
    - redir : CART or PRODUCTION
    - quantity = 1
    - if the response status is not 200 exit the script
8. Apply coupon, see point 3
9. Place order, see point 4

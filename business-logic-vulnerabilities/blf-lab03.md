### Lab: Low-level logic flaw

This lab doesn't adequately validate user input.
You can exploit a logic flaw in its purchasing workflow to buy items for an unintended price.
To solve the lab, buy a "Lightweight l33t leather jacket".

You can log in to your own account using the following credentials: wiener:peter

_____

Analysis and Exploit:

1. Log-in as user _wiener_ | POST **/login** | params : csrf, username, password
    - script: check if login is correct
2. Choose product Jacket from home page | GET **/**
    - Script: Find the Jacket product ID in **/**
        - look through posts using BSoup | params: img, src=/image/productcatalog/specialproducts/LeetLeatherJacket.jpg
3. Adding products with negative quantity does not impact the web application, they are simply ignored if quantity in the cart is already 0
    - Max quantity per single request capped at 99
4. Cart total value becomes negative between $21'442'806.00 and $21'242'140.96
    - Adding more products reduces the negative value towards 0
    - Removing products increases the negative value towards -infinite
5. Keep adding 'jackets' until the total value of the cart is near the 0 then other products to the shopping basket so that the overall total is between 0 and 100 dollars
    - Script: Find the product id of the jacket and use the next product id
    - Script: Find the price of products in their pages | GET **/product?productId=[ID]**
    - Add 99 jackets per request | POST **productId=[ID]&quantity=[QUANTITY]&redir=CART**
        - Keep tracking the total value | GET **/cart**
    - Add other products to reach a value between 1 and 100 dollars
6. Proceed to checkout | POST **/cart/checkout** | params : csrf


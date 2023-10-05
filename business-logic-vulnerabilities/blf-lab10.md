### Lab: Flawed enforcement of business rules

This lab has a logic flaw in its purchasing workflow.  
To solve the lab, exploit this flaw to buy a "Lightweight l33t leather jacket".

You can log in to your own account using the following credentials: wiener:peter


_____

Analysis and Exploit:

1. Banner at the home page: "New customers use code at checkout: NEWCUST5"
2. Log-in as user _wiener_ (psw:peter)
    - Wallet: $100.00
    - Coupon: - $5.00
3. If item with price lower than $5.00 the total goes to 0
4. Cannot apply the coupon more than once
5. Attempt1:
    - add product with price lower than $5.00
    - Total value is $0.00
    - Place order
    - **[BURP-PROXY/REPEATER]** Intercept request, send POST to add jacket to cart
    - confirm purchase, error because of insufficient funds
6. Attempt2:
    - add product with price lower than $5.00
    - Total value is $0.00
    - Place order
    - **[BURP-PROXY/REPEATER]** Intercept request and forward, try to add jacket
    - error, purchase completes, jacket added to cart when empty
7. At the bottom of the homepage there is a "Sign-up to newsletter" field
    - Doing that and receive a new coupon SIGNUP30 (30% discount)
8. Add jacket to cart and insert both coupon
    - Bug: one can use coupons more than once but need to alternate between them
    - Continue until the total value of the basket is affordable
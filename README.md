
# paymob integration using python
this a simple paymob integration using python this covers 2 ways to pay 

  1- Card Payments 

  2- Wallets Payments


# Requirements
 and you nedd to pass in your 
 
 ``api_key``  : your paymob api_key
 
 and  
 
 ``integration_id``  your paymob Payment Integration Id  



 
 # 1- Card Payments

For card payments you need to have the iframe key or u can get the  url so u can start the payment 

and after this you need to pass in this url you payment key that u have generated to ``payment_token`` and also pass in your ``your_iframe_id`` in the url 

Example : ``https://accept.paymobsolutions.com/api/acceptance/iframes/{{your_iframe_id}}?payment_token={payment_key}``

 # 2- Wallets Payments












# you can visit  [paymob docs](https://docs.paymob.com/) for more info. 


  

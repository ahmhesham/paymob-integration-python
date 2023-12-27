import requests





apiKey = ''





class PaymobManager:
    def getPaymentKey(self, amount, currency, integration_id):
        try:
            authanticationToken = self._getAuthanticationToken(api_key=apiKey)

            orderId = self._getOrderId(
                authanticationToken=authanticationToken,
                amount=str(100 * amount),
                currency=currency,
            )

            paymentKey = self._getPaymentKey(
                authanticationToken=authanticationToken,
                amount=str(100 * amount),
                currency=currency,
                orderId=str(orderId),
                integration_id = integration_id
            )
            return paymentKey
        except Exception as e:
            print("Exc==========================================")
            print(str(e))
            raise Exception()

    def _getAuthanticationToken(self, api_key):
        response = requests.post(
            "https://accept.paymob.com/api/auth/tokens",
            json={
                "api_key": api_key,
            }
        )
        print("auth token")
        print("---------------------------")
        print(response.json()["token"])
        print("-----------------------------")
        return response.json()["token"]

    def _getOrderId(self, authanticationToken, amount, currency):
        response = requests.post(
            "https://accept.paymob.com/api/ecommerce/orders",
            json={
                "auth_token": authanticationToken,
                "amount_cents": amount,
                "currency": currency,
                "delivery_needed": False,
                "items": [],
            }
        )
        print("orderid")
        print("---------------------------")
        print(response.json()["id"])
        print("--------------------------")
        return response.json()["id"]

    def _getPaymentKey(self, authanticationToken, orderId, amount, currency, integration_id):
        response = requests.post(
            "https://accept.paymob.com/api/acceptance/payment_keys",
            json={
                "expiration": 3600,
                "auth_token": authanticationToken,
                "order_id": orderId,
                "amount_cents": amount,
                "currency": currency,
                "integration_id": integration_id,
                "billing_data": {
                    "first_name": "Clifford", 
                    "last_name": "Nicolas", 
                    "email": "claudette09@exa.com",
                    "phone_number": "+86(8)9135210487",
                    "apartment": "NA",  
                    "floor": "NA", 
                    "street": "NA", 
                    "building": "NA", 
                    "shipping_method": "NA", 
                    "postal_code": "NA", 
                    "city": "NA", 
                    "country": "NA", 
                    "state": "NA"
                    }
                    }
        )
        print("paymentkey")
        print("---------------------------")
        print(response.json()["token"])
        print("---------------------------")
        return response.json()["token"]








# Create an instance of the PaymobManager class
paymob_manager = PaymobManager()

print()

# Call the getPaymentKey method with the required arguments , amount, currency

integration_id = 00 #Your Payment Integration id to spicify what payment is it like (cards, or mobile wallet, etc..)
amount = 100 # amount that you want the user to pay 
currency = "EGP" #currency USD or EGP , etc..
payment_key = paymob_manager.getPaymentKey(amount=amount, currency=currency, integration_id=integration_id)


# for cards payments you can use your payment iframes and pass the payment key you have created.

# https://accept.paymobsolutions.com/api/acceptance/iframes/{{your_iframe_id}}?payment_token={{payment_key}}


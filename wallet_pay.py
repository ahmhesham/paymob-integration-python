import requests

class PaymobManager:
    def getPaymentKey(self, amount, currency):
        try:
            authanticationToken = self._getAuthanticationToken()

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
            )
            return paymentKey
        except Exception as e:
            print("Exc==========================================")
            print(str(e))
            raise Exception()

    def _getAuthanticationToken(self):
        response = requests.post(
            "https://accept.paymob.com/api/auth/tokens",
            json={
                "api_key": "ZXlKaGJHY2lPaUpJVXpVeE1pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SmpiR0Z6Y3lJNklrMWxjbU5vWVc1MElpd2ljSEp2Wm1sc1pWOXdheUk2T1RRMU5USTFMQ0p1WVcxbElqb2lhVzVwZEdsaGJDSjkubWVXdEFaWjhLQ09GTVUtTlhfS0VOMldHZkRzT3RlM2dCcGdRaEd4T1hJMFRMVVh1YUt4Z0RBOVNpaXVPbXlSN0RVR3A3TXc4cWUtaWIzUzlCS2phNkE=",
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

    def _getPaymentKey(self, authanticationToken, orderId, amount, currency):
        response = requests.post(
            "https://accept.paymob.com/api/acceptance/payment_keys",
            json={
                "expiration": 3600,
                "auth_token": authanticationToken,
                "order_id": orderId,
                "amount_cents": amount,
                "currency": currency,
                "integration_id": 4410201,
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

# Call the getPaymentKey method with the required arguments
amount = 100
currency = "EGP"
payment_key = paymob_manager.getPaymentKey(amount, currency)

# Print the payment key
print(payment_key)



def getredirect_url(payment_key,wallet_num):
    response = requests.post(
        "https://accept.paymob.com/api/acceptance/payments/pay",
        json={
            "source": {
                "identifier": f"{wallet_num}", 
                "subtype": "WALLET"
            },
            "payment_token": payment_key  
        }
        )
    print("redirect_url")
    print(response.json()['iframe_redirection_url'])

    print("---------------------------")
    return response.json()['iframe_redirection_url']

getredirect_url(payment_key=payment_key, wallet_num="01010101010")




def get_callback(request):
    if request.method == 'POST':
        data = request.json()
        data = request.Post.get('obj')



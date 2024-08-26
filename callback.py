import hmac
import hashlib
import json
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

def extract_value(data, keys):
    """Extract a nested value from a dictionary using a list of keys."""
    for key in keys:
        if isinstance(data, dict):
            data = data.get(key, '')
        else:
            return ''
    return data

def calc_hmac(request_data, hmac_secret):
    # Define the field paths
    fields = [
        ('obj', 'amount_cents'),
        ('obj', 'created_at'),
        ('obj', 'currency'),
        ('obj', 'error_occured'),
        ('obj', 'has_parent_transaction'),
        ('obj', 'id'),
        ('obj', 'integration_id'),
        ('obj', 'is_3d_secure'),
        ('obj', 'is_auth'),
        ('obj', 'is_capture'),
        ('obj', 'is_refunded'),
        ('obj', 'is_standalone_payment'),
        ('obj', 'is_voided'),
        ('obj', 'order', 'id'),
        ('obj', 'owner'),
        ('obj', 'pending'),
        ('obj', 'source_data', 'pan'),
        ('obj', 'source_data', 'sub_type'),
        ('obj', 'source_data', 'type'),
        ('obj', 'success'),
    ]

    # Extract values
    values = {}
    for path in fields:
        value = extract_value(request_data, path)
        if isinstance(value, bool):
            value = "true" if value else "false"
        values[':'.join(path)] = str(value)

    # Concatenate the values
    concatenated_string = ''.join(values.values())
    print(f"Concatenated string for HMAC: {concatenated_string}")  # Debugging output

    # Generate the HMAC
    hmac_generated = hmac.new(hmac_secret.encode(), concatenated_string.encode(), hashlib.sha512).hexdigest()
    return hmac_generated



@csrf_exempt
def processed_callback(request):
    if request.method == 'POST':
        request_data = json.loads(request.body)
        
    
        hmac_secret = ''  # Replace with your actual HMAC secret key
        
        # Calculate the HMAC using the provided data
        generated_hmac = calc_hmac(request_data, hmac_secret)

        # Get the received HMAC from query parameters
        hmac_received = request.GET.get('hmac')
        print(f"Received HMAC: {hmac_received}")
        print(f"Generated HMAC: {generated_hmac}")

        if generated_hmac == hmac_received:
            # Process the transaction as needed
            success_status = extract_value(request_data, ['obj', 'success'])
            order_id = extract_value(request_data, ('obj', 'order', 'id'))
            print(f"Payment Success Status: {success_status}, order_id: {order_id}")
            if success_status == True:
                # Handle successful payment
               


            
                return redirect('course_list')

            else:
                # Handle failed payment
                messages.error(request, 'Something went wrong. Please try again.')
                return redirect('cart_detail')

        else:
            print("HMAC validation failed")
            messages.error(request, 'Invalid HMAC validation.')
            return redirect('cart_detail')



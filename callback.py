#handle callback using django
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
    

    # Generate the HMAC
    hmac_generated = hmac.new(hmac_secret.encode(), concatenated_string.encode(), hashlib.sha512).hexdigest()
    return hmac_generated







@csrf_exempt
def processed_callback(request):
    if request.method == 'POST':
        # Parse the JSON body of the request
        request_data = json.loads(request.body)
        
        # Your HMAC secret
        hmac_secret = settings.PAYMOB_HMAC 
        
        # Calculate the HMAC using the provided data
        generated_hmac = calc_hmac(request_data, hmac_secret)

        # Get the received HMAC from query parameters
        hmac_received = request.GET.get('hmac')
       

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








def response_extract_value(data, path):
    """
    Extracts a value from a dictionary using a path.
    For the updated structure, paths are flat and directly match keys in the dictionary.
    """
    # Directly get the value for the path
    value = data.get(path, "")
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)

def response_calc_hmac(request_data, hmac_secret):
    """
    Calculate the HMAC for the given request data.
    """
    # Define the field paths
    fields = [
        'amount_cents',
        'created_at',
        'currency',
        'error_occured',
        'has_parent_transaction',
        'id',
        'integration_id',
        'is_3d_secure',
        'is_auth',
        'is_capture',
        'is_refunded',
        'is_standalone_payment',
        'is_voided',
        'order',
        'owner',
        'pending',
        'source_data.pan',
        'source_data.sub_type',
        'source_data.type',
        'success',
    ]

    # Extract values
    values = []
    for field in fields:
        value = response_extract_value(request_data, field)
        values.append(value)
        # Print for debugging
        #print(f"Field: {field}, Value: {value}")

    # Concatenate the values
    concatenated_string = ''.join(values)
    

    # Generate the HMAC
    hmac_generated = hmac.new(hmac_secret.encode(), concatenated_string.encode(), hashlib.sha512).hexdigest()
    return hmac_generated

@csrf_exempt
def order_success(request):
    if request.method == 'GET':  # Assuming the data is being sent via a GET request
        # Parse the query parameters
        query_params = request.GET.dict()

        # Your HMAC secret
        hmac_secret = settings.PAYMOB_HMAC 
        
        generated_hmac = response_calc_hmac(query_params, hmac_secret)

        # Get the received HMAC from query parameters
        hmac_received = query_params.get('hmac')
        if generated_hmac == hmac_received:
            # Process the transaction as needed
            success_status = query_params.get('success')
            order_id = query_params.get('order')
            print(f"Payment Success Status: {success_status}, order_id: {order_id}")
            
            if success_status == 'true':
               
                return redirect('home')

            else:
                # Handle failed payment
                messages.error(request, 'Something went wrong. Please try again.')
                return render(request, 'order_success.html')

        else:
            print("HMAC validation failed")
            messages.error(request, 'Invalid HMAC validation.')
            return render(request, 'order_success.html')

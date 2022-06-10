import re
import json
from urllib.parse import quote
from hashlib import sha1
from base64 import b64encode, b64decode

email_regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'


def generate_signature(transaction_reference, app_key, secret_key):
    signature = f"{transaction_reference}|{app_key}|{secret_key}"
    encoded_url = sha1(signature.encode()).digest()
    signature = b64encode(encoded_url)
    return signature.decode()


def get_decoded_transaction_details(encoded_details):
    try:
        decoded_details_str = b64decode(encoded_details).decode('utf-8')
        decoded_details_json = json.loads(decoded_details_str)
    except:
        raise Exception("Transaction details decoding failed")

    user_email = decoded_details_json.get('email', '')
    requested_credits = decoded_details_json.get('credits', '')
    is_transaction_detail_valid = is_email(user_email) and requested_credits.isdigit()

    if not is_transaction_detail_valid:
        raise Exception("Invalid transaction details")

    return user_email, float(requested_credits)


def is_email(email):
    return re.search(email_regex, email)

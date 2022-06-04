import string
import secrets

def generate_verification_code():
    return ''.join(secrets.choice(string.digits) for i in range(6))

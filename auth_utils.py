import jwt
from datetime import datetime, timedelta

def generate_token(user_id, role_id, user_name, secret_key, expiration_minutes=30):
    payload = {
        'user_id': user_id,
        'role_id': role_id,
        'user_name': user_name,
        'exp': datetime.utcnow() + timedelta(minutes=expiration_minutes)
    }
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token

def decode_token(token, secret_key):
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token expired
    except jwt.InvalidTokenError:
        return None  # Invalid token

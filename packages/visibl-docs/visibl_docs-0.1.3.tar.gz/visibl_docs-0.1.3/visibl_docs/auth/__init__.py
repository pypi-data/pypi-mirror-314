import jwt
import os

def validate_token(token):
    """Validate the provided token"""
    try:
        # Check if it's a test token
        is_test = token.startswith("dev_")
        if is_test:
            # Only allow test tokens in test mode
            if not os.getenv("VISIBL_TEST_MODE", "false").lower() == "true":
                return False
            token = token[len("dev_"):]  # Remove prefix for validation
            
        # Regular token validation
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return True
    except jwt.InvalidTokenError:
        return False 
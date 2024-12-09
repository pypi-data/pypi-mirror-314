import keyring
import sys
from auth0.authentication import GetToken
from auth0.management import Auth0

# Your Auth0 configuration
AUTH0_DOMAIN = 'your-tenant.auth0.com'
AUTH0_CLIENT_ID = 'your-client-id'
AUTH0_CLIENT_SECRET = 'your-client-secret'

SERVICE_NAME = "visibl-docs"
TOKEN_KEY = "api_token"

def validate_token(token):
    """Validate token with Auth0"""
    try:
        # Initialize Auth0 management API client
        auth0_mgmt = Auth0(AUTH0_DOMAIN, token)
        
        # Try to get user info - this will fail if token is invalid
        userinfo = auth0_mgmt.users.get_user_info()
        return True
    except Exception:
        return False

def get_stored_token():
    """Get stored token from system keyring"""
    return keyring.get_password(SERVICE_NAME, TOKEN_KEY)

def store_token(token):
    """Store token in system keyring"""
    keyring.set_password(SERVICE_NAME, TOKEN_KEY, token)

def ensure_authenticated():
    """Ensure user has valid token"""
    token = get_stored_token()
    
    if not token:
        print("\nNo access token found. Please enter your Auth0 access token.")
        print("You can get this from your Auth0 dashboard or administrator.")
        token = input("Token: ").strip()
        if not validate_token(token):
            print("Invalid token. Please obtain a valid token from Auth0.")
            sys.exit(1)
        store_token(token)
    elif not validate_token(token):
        print("\nToken expired. Please enter a new Auth0 access token:")
        token = input("Token: ").strip()
        if not validate_token(token):
            print("Invalid token. Please obtain a valid token from Auth0.")
            sys.exit(1)
        store_token(token) 
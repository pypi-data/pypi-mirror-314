import os
import json
import requests
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlencode
import secrets
import click

# Load from environment variables
AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
CLIENT_SECRET = os.getenv('AUTH0_CLIENT_SECRET')
CALLBACK_PORT = 3000
CALLBACK_URL = f"http://localhost:{CALLBACK_PORT}/callback"

TOKEN_PATH = os.path.expanduser("~/.visibl_token.json")

class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if '/callback' in self.path:
            # Extract the authorization code from URL parameters
            from urllib.parse import urlparse, parse_qs
            query_components = parse_qs(urlparse(self.path).query)
            
            if 'code' in query_components:
                code = query_components['code'][0]
                
                # Exchange code for token
                token_payload = {
                    'grant_type': 'authorization_code',
                    'client_id': CLIENT_ID,
                    'client_secret': CLIENT_SECRET,
                    'code': code,
                    'redirect_uri': CALLBACK_URL
                }
                
                token_url = f"https://{AUTH0_DOMAIN}/oauth/token"
                token_response = requests.post(token_url, json=token_payload)
                
                if token_response.status_code == 200:
                    access_token = token_response.json().get('access_token')
                    save_auth_token(access_token)
                    self.server.auth_success = True
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(b"Authentication successful! You can close this window.")
                else:
                    self.send_response(400)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(b"Failed to exchange code for token")
            else:
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"No authorization code received")

def get_auth_token():
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'r') as f:
            data = json.load(f)
            return data.get('access_token')
    return None

def save_auth_token(token):
    os.makedirs(os.path.dirname(TOKEN_PATH), exist_ok=True)
    with open(TOKEN_PATH, 'w') as f:
        json.dump({'access_token': token}, f)

def authenticate_user():
    """Start browser-based authentication flow"""
    # Open browser directly to Visibl login page
    login_url = "https://docs.visiblsemi.com/login"
    
    # Start local server to receive callback
    server = HTTPServer(('localhost', CALLBACK_PORT), CallbackHandler)
    server.auth_success = False
    
    # Open browser for authentication
    webbrowser.open(login_url)
    
    print("Waiting for authentication in your browser...")
    server.handle_request()
    
    return server.auth_success

def ensure_authenticated():
    """Ensure user is authenticated, handle login if needed"""
    token = get_auth_token()
    if not token:
        if not authenticate_user():
            raise click.ClickException("Authentication failed")
    return True
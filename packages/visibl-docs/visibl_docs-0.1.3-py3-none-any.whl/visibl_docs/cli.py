import os
from dotenv import load_dotenv
import click
import webbrowser
import http.server
import socketserver
import threading
import json
import requests
from urllib.parse import parse_qs, urlparse
from .commands.view import view_docs
from .commands.gen import run_gen_docs
from .commands.autogen import autogen_docs
from .auth import ensure_authenticated

# Load environment variables
load_dotenv()

AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
AUTH0_CLIENT_SECRET = os.getenv('AUTH0_CLIENT_SECRET')
AUTH0_CALLBACK_PORT = 3000

class TokenHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        query_components = parse_qs(urlparse(self.path).query)
        
        if 'code' in query_components:
            # Exchange the code for a token
            token_url = f"https://{AUTH0_DOMAIN}/oauth/token"
            token_payload = {
                'grant_type': 'authorization_code',
                'client_id': AUTH0_CLIENT_ID,
                'client_secret': AUTH0_CLIENT_SECRET,
                'code': query_components['code'][0],
                'redirect_uri': f'http://localhost:{AUTH0_CALLBACK_PORT}/callback'
            }
            
            token_response = requests.post(token_url, json=token_payload)
            if token_response.status_code == 200:
                self.server.access_token = token_response.json().get('access_token')
                self.wfile.write(b"Authentication successful! You can close this window and return to the terminal.")
            else:
                self.wfile.write(b"Authentication failed during token exchange!")
            
            # Stop the server
            threading.Thread(target=self.server.shutdown).start()
        else:
            self.wfile.write(b"Authentication failed!")

def authenticate_user():
    """Start browser-based Auth0 authentication flow"""
    # Construct Auth0 authorization URL
    auth_url = f"https://{AUTH0_DOMAIN}/authorize?"
    auth_url += f"client_id={AUTH0_CLIENT_ID}&"
    auth_url += f"redirect_uri=http://localhost:{AUTH0_CALLBACK_PORT}/callback&"
    auth_url += "response_type=code&"
    auth_url += "scope=openid profile email"

    # Start local server to receive callback
    handler = TokenHandler
    with socketserver.TCPServer(("", AUTH0_CALLBACK_PORT), handler) as httpd:
        # Open browser for authentication
        webbrowser.open(auth_url)
        
        print(f"Waiting for authentication in your browser...")
        httpd.serve_forever()
        
        if hasattr(httpd, 'access_token'):
            # Store token securely
            return True
    return False

def ensure_authenticated():
    """Ensure user is authenticated, redirect to login if not"""
    # Check for existing valid token
    if not is_authenticated():
        if not authenticate_user():
            raise click.ClickException("Authentication failed")

@click.group()
def main():
    """Documentation generation tool"""
    pass

@main.command()
def view():
    """View documentation status"""
    ensure_authenticated()
    view_docs()

@main.command()
def gen():
    """Generate documentation"""
    ensure_authenticated()
    run_gen_docs()

@main.command()
def autogen():
    """Auto-generate documentation"""
    ensure_authenticated()
    autogen_docs()

if __name__ == '__main__':
    main()

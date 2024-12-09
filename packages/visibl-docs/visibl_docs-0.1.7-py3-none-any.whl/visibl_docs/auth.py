import os
import json
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests
from pathlib import Path

# Auth0 configuration
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "your-domain.auth0.com")
CLIENT_ID = os.getenv("AUTH0_CLIENT_ID", "your-client-id")
CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET", "your-client-secret")
REDIRECT_URI = "http://localhost:8000/callback"

# File to store auth token
TOKEN_FILE = Path.home() / ".visibl" / "auth_token.json"

class AuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if "/callback" in self.path:
            try:
                code = self.path.split("code=")[1].split("&")[0]
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                success_html = """
                <html>
                    <head><title>Authentication Successful</title></head>
                    <body>
                        <h1>Authentication Successful!</h1>
                        <p>You can close this window and return to the command line.</p>
                        <script>setTimeout(function(){ window.close(); }, 3000);</script>
                    </body>
                </html>
                """
                self.wfile.write(success_html.encode('utf-8'))
                self.server.auth_code = code
            except Exception as e:
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                error_html = f"""
                <html>
                    <head><title>Authentication Failed</title></head>
                    <body>
                        <h1>Authentication Failed</h1>
                        <p>Error: {str(e)}</p>
                    </body>
                </html>
                """
                self.wfile.write(error_html.encode('utf-8'))

def ensure_auth():
    """Ensure user is authenticated, if not initiate auth flow"""
    if is_authenticated():
        return True
        
    print("Authentication required. Opening browser for login...")
    auth_url = (
        f"https://{AUTH0_DOMAIN}/authorize"
        f"?response_type=code"
        f"&client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope=openid%20profile%20email"
    )
    
    webbrowser.open(auth_url)
    
    # Start local server to receive callback
    server = HTTPServer(('localhost', 8000), AuthHandler)
    server.auth_code = None
    server.handle_request()
    
    if server.auth_code:
        exchange_code_for_token(server.auth_code)
        return True
    return False

def exchange_code_for_token(auth_code):
    """Exchange authorization code for access token"""
    response = requests.post(
        f"https://{AUTH0_DOMAIN}/oauth/token",
        json={
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": REDIRECT_URI,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        },
    )
    
    if response.status_code == 200:
        token_data = response.json()
        save_token(token_data)
        return True
    return False

def save_token(token_data):
    """Save token to file"""
    TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(TOKEN_FILE, "w") as f:
        json.dump(token_data, f)

def is_authenticated():
    """Check if user is authenticated"""
    return TOKEN_FILE.exists()
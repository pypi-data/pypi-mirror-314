import os
import json
import requests
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer

AUTH0_DOMAIN = "YOUR_AUTH0_DOMAIN"
CLIENT_ID = "YOUR_CLIENT_ID"
ORGANIZATION_ID = "YOUR_ORGANIZATION_ID"
REDIRECT_URI = "http://localhost:5000/callback"

TOKEN_PATH = os.path.expanduser("~/.myapp_token.json")


def get_auth_token():
    """
    Retrieve stored token from the local file system.
    """
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, "r") as file:
            return json.load(file).get("access_token")
    return None


def save_auth_token(token):
    """
    Save the token to the local file system.
    """
    with open(TOKEN_PATH, "w") as file:
        json.dump({"access_token": token}, file)


def login_with_oauth():
    """
    Perform OAuth login using Auth0.
    """
    # Step 1: Open the login page in the browser
    auth_url = (
        f"https://{AUTH0_DOMAIN}/authorize?"
        f"audience=https://{AUTH0_DOMAIN}/api/v2/&"
        f"client_id={CLIENT_ID}&"
        f"redirect_uri={REDIRECT_URI}&"
        f"scope=openid profile email&"
        f"response_type=code&"
        f"organization={ORGANIZATION_ID}"
    )
    webbrowser.open(auth_url)

    # Step 2: Start a local server to handle the callback
    class OAuthCallbackHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            # Parse the authorization code from the URL
            query = self.path.split("?")[-1]
            params = dict(p.split("=") for p in query.split("&"))
            if "code" in params:
                code = params["code"]
                token = exchange_code_for_token(code)
                save_auth_token(token)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Login successful! You can close this tab.")
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Login failed!")

    server = HTTPServer(("localhost", 5000), OAuthCallbackHandler)
    server.handle_request()


def exchange_code_for_token(code):
    """
    Exchange the authorization code for an access token.
    """
    token_url = f"https://{AUTH0_DOMAIN}/oauth/token"
    payload = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(token_url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        raise Exception(f"Failed to exchange code for token: {response.text}")


def ensure_authenticated():
    """
    Ensure the user is authenticated before using the CLI.
    """
    token = get_auth_token()
    if not token:
        print("You are not authenticated. Redirecting to login...")
        login_with_oauth()
    else:
        print("You are already authenticated.")
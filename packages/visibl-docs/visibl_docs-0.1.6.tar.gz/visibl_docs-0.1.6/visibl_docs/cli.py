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
from .auth import ensure_authenticated, authenticate_user

# Load environment variables
load_dotenv()

AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
AUTH0_CLIENT_SECRET = os.getenv('AUTH0_CLIENT_SECRET')
AUTH0_CALLBACK_PORT = 3000

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

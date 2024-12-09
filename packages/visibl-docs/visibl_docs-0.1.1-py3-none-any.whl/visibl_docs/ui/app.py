from flask import Flask, render_template, send_from_directory
import os
import threading
import webbrowser

app = Flask(__name__)

@app.route('/')
def index():
    """Render the main documentation page."""
    docs_path = os.path.join(os.getcwd(), 'docs')
    if not os.path.exists(docs_path):
        return "No documentation found. Please run 'docs gen' or 'docs autogen' first."

    # Get list of markdown files in the docs directory
    markdown_files = []
    for file in os.listdir(docs_path):
        if file.endswith('.md'):
            markdown_files.append(file)

    return f"""
    <html>
        <head>
            <title>Visibl Docs</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; }}
                h1 {{ color: #333; }}
                ul {{ list-style-type: none; padding: 0; }}
                li {{ margin: 10px 0; }}
                a {{ color: #0066cc; text-decoration: none; }}
                a:hover {{ text-decoration: underline; }}
            </style>
        </head>
        <body>
            <h1>Visibl Docs</h1>
            <h2>Documentation Files:</h2>
            <ul>
                {''.join(f'<li><a href="/docs/{file}">{file}</a></li>' for file in markdown_files)}
            </ul>
        </body>
    </html>
    """

@app.route('/docs/<path:filename>')
def serve_docs(filename):
    """Serve documentation files."""
    return send_from_directory('docs', filename)

def open_browser():
    """Open the browser after a short delay."""
    webbrowser.open('http://localhost:5000')

def run_ui():
    """Run the UI server."""
    threading.Timer(1.5, open_browser).start()
    app.run(port=5000, debug=False)

if __name__ == '__main__':
    run_ui()

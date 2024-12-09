import sys

def display_message(message):
    """Display a success or information message to the user."""
    print(f"\033[92m{message}\033[0m")  # Green text

def display_error(error_message):
    """Display an error message to the user."""
    print(f"\033[91mError: {error_message}\033[0m", file=sys.stderr)  # Red text

def display_progress(message):
    """Display a progress message to the user."""
    print(f"\033[94m{message}\033[0m")  # Blue text

def display_warning(message):
    """Display a warning message to the user."""
    print(f"\033[93mWarning: {message}\033[0m")  # Yellow text

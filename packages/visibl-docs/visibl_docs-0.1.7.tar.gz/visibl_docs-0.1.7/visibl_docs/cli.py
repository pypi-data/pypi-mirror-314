import click
from .commands.init import init_docs
from .commands.gen import gen_docs
from .commands.autogen import autogen_docs
from .auth import ensure_auth

@click.group()
def cli():
    """Visibl documentation generation and viewing tool."""
    pass

@cli.command()
def init():
    """Initialize docs in your project."""
    if ensure_auth():
        init_docs()
    else:
        click.echo("Authentication failed. Please try again.")

@cli.command()
def gen():
    """Generate documentation for your project."""
    if ensure_auth():
        gen_docs()
    else:
        click.echo("Authentication failed. Please try again.")

@cli.command()
def autogen():
    """Auto-generate enhanced documentation using AI."""
    if ensure_auth():
        autogen_docs()
    else:
        click.echo("Authentication failed. Please try again.")

def main():
    cli(prog_name="visibl_docs")

if __name__ == '__main__':
    main() 
import click
from .commands.view import view_docs
from .commands.gen import run_gen_docs
from .commands.autogen import autogen_docs
from .auth import ensure_authenticated

@click.group()
def main():
    """Documentation generation tool"""
    ensure_authenticated()  # Check token before running any command
    pass

@main.command()
def view():
    """View documentation status"""
    view_docs()

@main.command()
def gen():
    """Generate documentation"""
    run_gen_docs()

@main.command()
def autogen():
    """Auto-generate documentation"""
    autogen_docs()

if __name__ == '__main__':
    main()

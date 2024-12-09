from models.repository_processor import RepositoryProcessor
from models.markdown_generator import MarkdownGenerator
from models.ollama_processor import OllamaProcessor
from views.terminal_view import display_message, display_error

def handle_command(args):
    if not args:
        display_error("No command provided.")
        return

    command = args[0]

    if command == 'init':
        initialize_repository()
    elif command == 'gen':
        generate_docs()
    elif command == 'autogen':
        auto_generate_docs()
    elif command == 'view':
        launch_ui()
    else:
        display_error(f"Unknown command: {command}")

def initialize_repository():
    try:
        processor = RepositoryProcessor()
        processor.initialize_docs_folder()
        display_message("Visibl Docs initialized successfully.")
    except Exception as e:
        display_error(str(e))

def generate_docs():
    try:
        processor = RepositoryProcessor()
        source_files = processor.scan_source_files()
        generator = MarkdownGenerator()
        for file in source_files:
            generator.generate_markdown(file)
        display_message("Documentation generated successfully.")
    except Exception as e:
        display_error(str(e))

def auto_generate_docs():
    try:
        processor = RepositoryProcessor()
        source_files = processor.scan_source_files()
        generator = MarkdownGenerator()
        ollama = OllamaProcessor()
        for file in source_files:
            generator.generate_markdown(file)
            ollama.enhance_documentation(file)
        display_message("Automatic documentation generated successfully.")
    except Exception as e:
        display_error(str(e))

def launch_ui():
    try:
        from ui.app import run_ui
        run_ui()
        display_message("UI launched successfully. Access it at http://localhost:5000")
    except Exception as e:
        display_error(str(e))

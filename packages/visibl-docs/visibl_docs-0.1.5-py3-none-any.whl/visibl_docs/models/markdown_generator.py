import os

class MarkdownGenerator:
    def generate_markdown(self, source_file):
        # Read source file content
        with open(source_file, 'r') as f:
            content = f.read()

        # Generate basic markdown content
        markdown_content = self._generate_basic_markdown(source_file, content)

        # Save markdown file in docs folder
        docs_path = os.path.join(os.getcwd(), 'docs')
        markdown_file = os.path.join(docs_path, os.path.basename(source_file) + '.md')
        
        with open(markdown_file, 'w') as f:
            f.write(markdown_content)

    def _generate_basic_markdown(self, source_file, content):
        filename = os.path.basename(source_file)
        markdown_content = [
            f"# Documentation for {filename}",
            "",
            "## Overview",
            "This file contains Verilog/SystemVerilog code.",
            "",
            "## File Contents",
            "```verilog",
            content,
            "```",
            "",
            "## Module Description",
            "This section will be enhanced by the LLM processor.",
            "",
            "## Dependencies",
            "- List of dependencies will be added here",
            "",
            "## Usage Examples",
            "Usage examples will be added here.",
        ]
        return '\n'.join(markdown_content)

import os

class RepositoryProcessor:
    def initialize_docs_folder(self):
        current_dir = os.getcwd()
        docs_path = os.path.join(current_dir, 'docs')
        marker_file = os.path.join(current_dir, '.visibldocs')

        if os.path.exists(docs_path):
            raise Exception("Docs folder already exists.")

        os.makedirs(docs_path)
        with open(marker_file, 'w') as f:
            f.write("This is a Visibl Docs repository.")

        # Create initial metadata file
        metadata_path = os.path.join(docs_path, 'metadata.json')
        with open(metadata_path, 'w') as f:
            f.write('{}')  # Empty JSON object

    def scan_source_files(self):
        source_files = []
        for root, dirs, files in os.walk(os.getcwd()):
            # Skip the docs directory and hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'docs']
            
            for file in files:
                if file.endswith(('.sv', '.v')):
                    source_files.append(os.path.join(root, file))
        return source_files

import os
import shutil
from pathlib import Path

def create_docs_directory(workspace_dir: Path) -> Path:
    """Create the docs directory if it doesn't exist."""
    docs_dir = workspace_dir / 'docs'
    if not docs_dir.exists():
        docs_dir.mkdir()
        print("✓ Created docs directory")
    return docs_dir

def get_template_directory() -> Path:
    """Get the path to the template directory."""
    current_file = Path(__file__)
    template_dir = current_file.parent.parent / 'data' / 'init_docs'
    
    if not template_dir.exists():
        raise Exception(f"Template directory not found at {template_dir}")
    
    print(f"Found template directory at {template_dir}")
    return template_dir

def should_skip_file(item: Path) -> bool:
    """Check if the file should be skipped during copying."""
    return '__pycache__' in str(item) or item.name.startswith('.')

def copy_template_item(item: Path, template_dir: Path, docs_dir: Path):
    """Copy a single template item (file or directory) to the docs directory."""
    rel_path = item.relative_to(template_dir)
    target_path = docs_dir / rel_path
    
    # print(f"Processing: {rel_path}")
    
    # Create parent directories if they don't exist
    target_path.parent.mkdir(parents=True, exist_ok=True)
    
    if item.is_file():
        # print(f"Copying file: {rel_path}")
        shutil.copy2(item, target_path)
    elif item.is_dir():
        # print(f"Creating directory: {rel_path}")
        target_path.mkdir(exist_ok=True)

def init_docs():
    """Initialize the docs folder structure in the current directory."""
    try:
        # In Docker, files are mounted to /workspace
        workspace_dir = Path('/workspace')
        docs_dir = create_docs_directory(workspace_dir)
        
        template_dir = get_template_directory()
        print(f"Copying templates to {docs_dir}")
        
        # First, list all files to be copied
        template_files = list(template_dir.rglob('*'))
        print(f"Found {len(template_files)} files to copy")
        
        # Copy all contents from init_docs to the new docs directory
        for item in template_files:
            if should_skip_file(item):
                continue
            
            copy_template_item(item, template_dir, docs_dir)
        
        print("\n✓ Initialized documentation structure")
        print("\nYou can now start adding your documentation in the docs folder!")
        print("Run 'docs serve' to preview your documentation.")

    except Exception as e:
        print(f"Error initializing docs: {str(e)}")
        raise
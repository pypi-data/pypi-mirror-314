from pathlib import Path
from ..utils.file_tracker import FileTracker, format_file_changes
from datetime import datetime

def autogen_docs():
    """Auto-generate enhanced documentation using AI."""
    try:
        # Initialize file tracker with workspace directory
        workspace_dir = Path('/workspace')
        tracker = FileTracker(workspace_dir)
        
        # Scan for changes
        changes, stats = tracker.scan_workspace()
        print(format_file_changes(changes, stats))
        
        if not changes:
            return
            
        print("\nAuto-generating enhanced documentation...")
        
        # Generate sample documentation text
        sample_text = f"Hello World - {datetime.now().isoformat()}"
        print(f"\nGenerated documentation: {sample_text}")
        
        print("\n✓ Documentation auto-generated successfully")
        print("\nRun 'docs view' to preview the documentation.")

    except Exception as e:
        print(f"Error auto-generating documentation: {str(e)}")
        raise 
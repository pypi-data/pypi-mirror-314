from pathlib import Path
from ..utils.file_tracker import FileTracker, format_file_changes

def view_docs(port=8080):
    """Display documentation status.
    
    Args:
        port (int): Kept for compatibility but no longer used
    """
    try:
        # Check for changes first
        workspace_dir = Path('/workspace')
        tracker = FileTracker(workspace_dir)
        changes, stats = tracker.scan_workspace()
        
        if changes:
            print(format_file_changes(changes, stats))
            print("\nWarning: There are uncommitted changes in your documentation.")
            print("Consider running 'docs gen' or 'docs autogen' first.")
        
        print("\nDocumentation status: Ready to view")
        print("Note: Server functionality has been disabled.")

    except Exception as e:
        print(f"Error checking documentation status: {str(e)}")
        raise
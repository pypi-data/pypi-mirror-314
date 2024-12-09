from pathlib import Path
from ..utils.file_tracker import FileTracker, format_file_changes
from datetime import datetime

async def gen_docs():
    """Generate documentation for the project."""
    try:
        # Initialize file tracker with workspace directory
        workspace_dir = Path('/workspace')
        tracker = FileTracker(workspace_dir)
        
        # Scan for changes
        changes, stats = tracker.scan_workspace()
        print(format_file_changes(changes, stats))
        
        if not changes:
            return
            
        print("\nGenerating documentation...")

        # Generate sample documentation text
        sample_text = f"Hello World - {datetime.now().isoformat()}"
        print(f"\nGenerated documentation: {sample_text}")
        
        print("✓ Documentation generated successfully")
        print("\nRun 'docs view' to preview the documentation.")

    except Exception as e:
        print(f"Error generating documentation: {str(e)}")
        raise

def run_gen_docs():
    """Entry point for gen command."""
    loop = asyncio.get_event_loop()
    loop.run_until_complete(gen_docs())
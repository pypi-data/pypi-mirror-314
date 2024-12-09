import os
import json
import hashlib
from pathlib import Path
from typing import Dict, Set, Tuple, List
from dataclasses import dataclass
from datetime import datetime

# Define valid file extensions
VALID_EXTENSIONS = {'.v', '.sv'}

@dataclass
class FileChange:
    path: str
    status: str  # 'new', 'modified', 'deleted'
    last_modified: str
    size: int = 0

class FileTracker:
    def __init__(self, workspace_dir: Path):
        self.workspace_dir = workspace_dir
        self.state_file = workspace_dir / 'docs' / '.file_state.json'
        self.previous_state: Dict[str, dict] = {}
        self.current_state: Dict[str, dict] = {}
        self._load_previous_state()

    def _load_previous_state(self):
        """Load the previous file state from the state file."""
        if self.state_file.exists():
            with open(self.state_file) as f:
                self.previous_state = json.load(f)

    def _save_current_state(self):
        """Save the current file state to the state file."""
        self.state_file.parent.mkdir(exist_ok=True)
        with open(self.state_file, 'w') as f:
            json.dump(self.current_state, f, indent=2)

    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calculate SHA-256 hash of a file."""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def _get_file_info(self, file_path: Path) -> dict:
        """Get file information including hash, size, and modification time."""
        stat = file_path.stat()
        return {
            'hash': self._calculate_file_hash(file_path),
            'size': stat.st_size,
            'modified': datetime.fromtimestamp(stat.st_mtime).isoformat()
        }

    def _is_valid_file(self, file_path: Path) -> bool:
        """Check if the file is a valid Verilog or SystemVerilog file."""
        return file_path.suffix.lower() in VALID_EXTENSIONS

    def _process_file(self, file_path: Path, stats: Dict[str, int], current_files: Set[str]) -> FileChange:
        """Process a single file and update statistics."""
        rel_path = str(file_path.relative_to(self.workspace_dir))
        current_files.add(rel_path)
        stats['total_files'] += 1
        
        # Track file type statistics
        if file_path.suffix.lower() == '.v':
            stats['verilog_files'] += 1
        else:  # Must be .sv
            stats['systemverilog_files'] += 1
        
        file_info = self._get_file_info(file_path)
        stats['total_size'] += file_info['size']
        
        self.current_state[rel_path] = file_info
        
        # Determine file status and create FileChange object
        if rel_path not in self.previous_state:
            stats['new'] += 1
            return FileChange(rel_path, 'new', file_info['modified'], file_info['size'])
        elif self.previous_state[rel_path]['hash'] != file_info['hash']:
            stats['modified'] += 1
            return FileChange(rel_path, 'modified', file_info['modified'], file_info['size'])
        return None

    def _find_deleted_files(self, current_files: Set[str], stats: Dict[str, int]) -> List[FileChange]:
        """Find files that have been deleted since the last scan."""
        deleted_changes = []
        for old_file in self.previous_state:
            if old_file not in current_files and Path(old_file).suffix.lower() in VALID_EXTENSIONS:
                deleted_changes.append(FileChange(
                    old_file, 
                    'deleted', 
                    self.previous_state[old_file]['modified'],
                    self.previous_state[old_file]['size']
                ))
                stats['deleted'] += 1
        return deleted_changes

    def _should_process_file(self, file_path: Path, file_name: str, ignore_patterns: Set[str]) -> bool:
        """Determine if a file should be processed based on various criteria."""
        return (self._is_valid_file(file_path) and 
                not file_name.startswith('.') and 
                file_name not in ignore_patterns)

    def scan_workspace(self, ignore_patterns: Set[str] = None) -> Tuple[List[FileChange], Dict[str, int]]:
        """
        Scan the workspace for Verilog/SystemVerilog file changes.
        Returns a tuple of (changes, stats).
        """
        if ignore_patterns is None:
            ignore_patterns = {'.git', '__pycache__', '.file_state.json', 'node_modules'}

        changes: List[FileChange] = []
        stats = {
            'total_files': 0, 
            'total_size': 0, 
            'new': 0, 
            'modified': 0, 
            'deleted': 0,
            'verilog_files': 0,
            'systemverilog_files': 0
        }

        print("\nScanning workspace for Verilog/SystemVerilog files...")
        
        # Track current files
        current_files = set()
        
        for root, dirs, files in os.walk(self.workspace_dir):
            # Skip ignored directories
            dirs[:] = [d for d in dirs if d not in ignore_patterns]
            
            for file in files:
                file_path = Path(root) / file
                
                if not self._should_process_file(file_path, file, ignore_patterns):
                    continue
                
                print(f"\rProcessing: {file_path.relative_to(self.workspace_dir)}", end='', flush=True)
                
                try:
                    file_change = self._process_file(file_path, stats, current_files)
                    if file_change:
                        changes.append(file_change)
                except Exception as e:
                    print(f"\nError processing {file_path.relative_to(self.workspace_dir)}: {str(e)}")

        # Find deleted files
        deleted_changes = self._find_deleted_files(current_files, stats)
        changes.extend(deleted_changes)

        print("\rCompleted workspace scan." + " " * 50)  # Clear the processing line
        
        # Save the current state
        self._save_current_state()
        
        return changes, stats

def format_file_changes(changes: List[FileChange], stats: Dict[str, int]) -> str:
    """Format the file changes and stats into a human-readable string."""
    if not changes:
        return "No changes detected in Verilog/SystemVerilog files since last documentation generation."

    output = []
    output.append("\nChanges detected in HDL files:")
    output.append("=" * 50)

    # Group changes by type
    new_files = [c for c in changes if c.status == 'new']
    modified_files = [c for c in changes if c.status == 'modified']
    deleted_files = [c for c in changes if c.status == 'deleted']

    if new_files:
        output.append("\n📄 New Files:")
        for change in new_files:
            output.append(f"  + {change.path} ({_format_size(change.size)})")

    if modified_files:
        output.append("\n📝 Modified Files:")
        for change in modified_files:
            output.append(f"  * {change.path} ({_format_size(change.size)})")

    if deleted_files:
        output.append("\n🗑️  Deleted Files:")
        for change in deleted_files:
            output.append(f"  - {change.path}")

    output.append("\n" + "=" * 50)
    output.append("Summary:")
    output.append(f"Total HDL files scanned: {stats['total_files']}")
    output.append(f"  - Verilog (.v) files: {stats['verilog_files']}")
    output.append(f"  - SystemVerilog (.sv) files: {stats['systemverilog_files']}")
    output.append(f"Total size: {_format_size(stats['total_size'])}")
    output.append(f"New files: {stats['new']}")
    output.append(f"Modified files: {stats['modified']}")
    output.append(f"Deleted files: {stats['deleted']}")

    return "\n".join(output)

def _format_size(size: int) -> str:
    """Format file size in human readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.1f}{unit}"
        size /= 1024
    return f"{size:.1f}TB" 
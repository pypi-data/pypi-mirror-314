from pathlib import Path
from typing import Union

from .parser import FileChange


class ChangeApplicationError(Exception):
    """Custom exception for change application errors"""
    pass


def apply_file_changes(change: FileChange, project_directory: Union[str, Path]) -> None:
    """Apply a single file change to the project directory"""
    project_path = Path(project_directory).resolve()
    full_path = (project_path / change.file_path).resolve()
    
    # Security check: ensure the target path is within project directory
    try:
        full_path.relative_to(project_path)
    except ValueError:
        raise ChangeApplicationError(
            f"Security Error: Path '{change.file_path}' attempts to write outside project directory"
        )
    
    # Ensure parent directories exist for create/update operations
    if change.file_operation.upper() in ('CREATE', 'UPDATE'):
        full_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        match change.file_operation.upper():
            case 'CREATE':
                full_path.write_text(change.file_code or '')
                
            case 'UPDATE':
                full_path.write_text(change.file_code or '')
                
            case 'DELETE':
                if full_path.exists():
                    full_path.unlink()
                    
            case _:
                print(f"Warning: Unknown file operation '{change.file_operation}' "
                      f"for file: {change.file_path}")
                
    except Exception as e:
        raise ChangeApplicationError(
            f"Failed to {change.file_operation.lower()} {change.file_path}: {str(e)}"
        )

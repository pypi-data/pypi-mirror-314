from pathlib import Path
from typing import Optional

class WorkflowConfig:
    _root_path: Optional[Path] = None
    
    @classmethod
    def set_root_path(cls, path: str | Path) -> None:
        """Set the root path for module imports."""
        cls._root_path = Path(path).resolve()
    
    @classmethod
    def get_root_path(cls) -> Optional[Path]:
        """Get the current root path."""
        return cls._root_path
    
    @classmethod
    def get_module_path(cls, file_path: str | Path) -> str:
        """Convert a file path to a module path relative to root."""
        if cls._root_path is None:
            raise ValueError("Root path not set. Call set_root_path first.")
            
        file_path = Path(file_path).resolve()
        try:
            rel_path = file_path.relative_to(cls._root_path)
            return str(rel_path.with_suffix('')).replace('/', '.')
        except ValueError:
            raise ValueError(f"File path {file_path} is not under root path {cls._root_path}") 
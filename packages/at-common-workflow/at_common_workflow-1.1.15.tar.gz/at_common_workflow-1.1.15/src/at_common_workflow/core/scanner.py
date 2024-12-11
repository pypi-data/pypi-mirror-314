from typing import List
import os
import inspect
from pathlib import Path
from ..utils.logging import setup_logger
import importlib.util
from .task import Task
from .config import WorkflowConfig

logger = setup_logger(__name__)

class TaskScanner:
    """Scanner for tasks decorated with @task in a directory."""
    
    @staticmethod
    def scan(directory: str = None, module_prefix: str = "", package_name: str = None) -> List[Task]:
        """
        Scan a directory or package for all functions decorated with @task and create Task objects.
        
        Args:
            directory: The directory path to scan (optional if package_name is provided)
            module_prefix: Optional prefix to prepend to module paths
            package_name: Name of the installed package to scan (optional)
            
        Returns:
            List of Task objects
        
        Raises:
            FileNotFoundError: If the directory or package does not exist
        """
        if package_name:
            # Find the package location
            spec = importlib.util.find_spec(package_name)
            if spec is None:
                raise FileNotFoundError(f"Package not found: {package_name}")
            directory = os.path.dirname(spec.origin)
        elif directory:
            directory_path = Path(directory)
            if not directory_path.exists():
                raise FileNotFoundError(f"Directory does not exist: {directory}")
        else:
            raise ValueError("Either directory or package_name must be provided")
        
        # Set root path if not already set
        if WorkflowConfig.get_root_path() is None:
            WorkflowConfig.set_root_path(directory)
        
        tasks = []
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.py'):
                    file_path = Path(root) / file
                    try:
                        module_path = WorkflowConfig.get_module_path(file_path)
                        if module_prefix:
                            module_path = f"{module_prefix}.{module_path}"
                            
                        spec = importlib.util.spec_from_file_location(module_path, str(file_path))
                        if spec is None or spec.loader is None:
                            continue
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        
                        for name, obj in inspect.getmembers(module):
                            if inspect.isfunction(obj) and hasattr(obj, '_is_workflow_task'):
                                task = Task(
                                    name=obj._name,
                                    func=obj,
                                    description=obj._description,
                                    requires=obj._requires,
                                    provides=obj._provides
                                )
                                tasks.append(task)
                                logger.debug(f"Found task: {name} in {file_path}")
                                
                    except Exception as e:
                        logger.error(f"Error processing {file_path}: {str(e)}")
                        
        return tasks
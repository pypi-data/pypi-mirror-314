from typing import List, Dict, Any, TypeVar, Callable, ParamSpec, get_type_hints
import asyncio
from ..utils.logging import setup_logger
from .context import Context
import inspect
from functools import wraps
from .schema import InputSchema, OutputSchema
from enum import Enum
from dataclasses import dataclass
from typing import Optional
from at_common_workflow.exceptions.workflow_exceptions import TaskExecutionError

logger = setup_logger(__name__)

P = ParamSpec('P')
T = TypeVar('T')

class TaskStatus(Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

@dataclass
class TaskProgress:
    """Represents the progress status of a task in the workflow."""
    name: str
    status: TaskStatus

TaskFunction = Callable[['Context'], Any]

def normalize_task_function(func: Callable[P, T]) -> Callable[P, T]:
    """Normalize and validate a task function."""
    
    @wraps(func)
    async def wrapper(context: Context, **kwargs):
        if not asyncio.iscoroutinefunction(func):
            raise ValueError(f"Task function '{func.__name__}' must be async")
            
        # Validate type hints
        hints = get_type_hints(func)
        if 'context' not in hints or not issubclass(hints['context'], Context):
            raise ValueError(f"Task function '{func.__name__}' must have 'context: Context' as first parameter")
            
        # Validate return type is None (tasks shouldn't return values, they should modify context)
        if hints.get('return') is not None:
            raise ValueError(f"Task function '{func.__name__}' should not return any value")
            
        return await func(context, **kwargs)
        
    return wrapper

class Task:
    """Represents a single task in the workflow."""
    def __init__(
        self,
        name: str,
        func: TaskFunction,
        description: str,
        requires: InputSchema,
        provides: OutputSchema
    ):
        self.name: str = name
        self.description: str = description
        self.func: TaskFunction = normalize_task_function(func)
        self.requires: InputSchema = requires
        self.provides: OutputSchema = provides
        self.status: TaskStatus = TaskStatus.PENDING
    
    async def execute(self, context: Context) -> None:
        """Execute the task function."""
        try:
            self.status = TaskStatus.RUNNING
            logger.info(f"Starting task: {self.name}")
            
            if not asyncio.iscoroutinefunction(self.func):
                raise ValueError(f"Task {self.name} must be an async function")
            
            # Validate input schema
            for key, expected_type in self.requires.items():
                if key not in context:
                    raise ValueError(f"Required input '{key}' not found in context")
                value = context[key]
                if not isinstance(value, expected_type):
                    raise TypeError(
                        f"Input '{key}' has wrong type. Expected {expected_type.__name__}, "
                        f"got {type(value).__name__}"
                    )
            
            # Execute function
            await self.func(context)
            
            # Validate output schema
            for key, expected_type in self.provides.items():
                if key not in context:
                    raise ValueError(f"Task did not provide required output '{key}'")
                value = context[key]
                if not isinstance(value, expected_type):
                    raise TypeError(
                        f"Output '{key}' has wrong type. Expected {expected_type.__name__}, "
                        f"got {type(value).__name__}"
                    )
            
            self.status = TaskStatus.COMPLETED
            logger.info(f"Completed task: {self.name}")
            
        except Exception as e:
            self.status = TaskStatus.FAILED
            logger.error(f"Task {self.name} failed: {str(e)}")
            raise TaskExecutionError(self.name, e) from e

def task(
    *,
    name: Optional[str] = None,
    description: Optional[str] = None,
    requires: Optional[Dict[str, type]] = None,
    provides: Optional[Dict[str, type]] = None
) -> callable:
    """Decorator to define a task."""
    def decorator(func: TaskFunction) -> callable:
        # Validate that the function is async immediately
        if not asyncio.iscoroutinefunction(func):
            raise ValueError(f"Task function '{func.__name__}' must be async")

        # Validate context parameter
        sig = inspect.signature(func)
        params = list(sig.parameters.keys())
        if len(params) != 1 or params[0] != 'context':
            raise ValueError(f"Task function '{func.__name__}' must have exactly one parameter named 'context'")

        # Validate return type annotation
        hints = get_type_hints(func)
        if hints.get('return') is not None:
            raise ValueError(f"Task function '{func.__name__}' should not return any value")

        
        func._is_workflow_task = True
        func._name = name or func.__name__
        func._description = description or func.__doc__ or ""
        func._requires = InputSchema(requires or {})
        func._provides = OutputSchema(provides or {})
        
        return normalize_task_function(func)
    
    return decorator
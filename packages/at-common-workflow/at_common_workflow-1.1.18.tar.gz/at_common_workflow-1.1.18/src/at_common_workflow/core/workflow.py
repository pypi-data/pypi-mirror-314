from typing import Dict, List, Set, Callable
import asyncio
from .schema import InputSchema, OutputSchema, Input, Output
from .task import Task, TaskStatus, TaskProgress, TaskFunction
from .context import Context
from ..utils.validation import validate_dag, validate_schema
from ..exceptions.workflow_exceptions import DependencyNotFoundError
from ..utils.logging import setup_logger

logger = setup_logger(__name__)

class Workflow:
    """Manages the execution of tasks in a directed acyclic graph (DAG).
    
    Attributes:
        name: str = Unique identifier for the workflow
        description: str = Description of the workflow
        tasks: Dict[str, Task] = Dictionary of tasks keyed by task name
        input_schema: InputSchema = Schema defining required workflow inputs
        output_schema: OutputSchema = Schema defining expected workflow outputs
    """
    def __init__(self, name: str, description: str, input_schema: InputSchema, output_schema: OutputSchema):
        self.name = name
        self.description = description
        self.tasks: Dict[str, Task] = {}
        self.input_schema = input_schema
        self.output_schema = output_schema
        logger.info(f"Created workflow: {name}")
    
    

    def add_task(self, task_or_func: Task | TaskFunction) -> None:
        """Add a task to the workflow.
        
        Args:
            task_or_func: Either a Task instance or a decorated task function
        """
        if isinstance(task_or_func, Task):
            task = task_or_func
            task_name = task.name
        else:
            # Original function-based logic
            if not hasattr(task_or_func, '_is_workflow_task'):
                raise ValueError("Function must be decorated with @task")
            
            task_name = task_or_func._name
            
            task = Task(
                name=task_or_func._name,
                func=task_or_func,
                description=task_or_func._description,
                requires=task_or_func._requires,
                provides=task_or_func._provides,
            )
        
        if task_name in self.tasks:
            raise ValueError(f"Task '{task_name}' already exists")
        
        # Check for duplicate outputs
        for existing_task in self.tasks.values():
            duplicate_outputs = set(task.provides) & set(existing_task.provides)
            if duplicate_outputs:
                raise ValueError(
                    f"Tasks '{task.name}' and '{existing_task.name}' "
                    f"provide the same outputs: {duplicate_outputs}"
                )
        
        self.tasks[task_name] = task
        logger.debug(f"Added task: {task_name}")
    
    def _get_ready_tasks(self, context: Context, completed: Set[str]) -> List[Task]:
        """Get tasks whose dependencies are satisfied."""
        ready = []
        for task in self.tasks.values():
            # Check if task is pending
            if task.status != TaskStatus.PENDING:
                continue
                
            # Get all provided data keys from completed tasks AND existing context data
            available_data = set(context.keys())
            for completed_task in self.tasks.values():
                if completed_task.name in completed:
                    available_data.update(completed_task.provides.keys())
                    
            # Check if all required data is available
            if set(task.requires.keys()).issubset(available_data):
                ready.append(task)
                
        return ready
    
    async def execute(self, input: Input, callback: Callable[[TaskProgress], None] | None = None) -> Output:
        """Execute the workflow and report progress through callback if provided."""
        logger.info(f"Starting workflow execution: {self.name}")

        validate_schema(input, self.input_schema, "input")
        context = Context()
        context.update(input)

        validate_dag(self.tasks, context)
        completed_tasks: Set[str] = set()
        
        while len(completed_tasks) < len(self.tasks):
            ready_tasks = self._get_ready_tasks(context, completed_tasks)
            if not ready_tasks:
                # Find missing dependencies
                for task_name, task in self.tasks.items():
                    if task_name not in completed_tasks:
                        required_keys = set(task.requires.keys())
                        available_keys = set(context.keys()).union(
                            *[t.provides.keys() for t in self.tasks.values() if t.name in completed_tasks]
                        )
                        missing_keys = required_keys - available_keys
                        if missing_keys:
                            raise DependencyNotFoundError(task_name, missing_keys)
                
                raise RuntimeError("No tasks ready to execute but no missing dependencies found")
            
            # Report starting tasks
            for task in ready_tasks:
                if callback:
                    callback(TaskProgress(task.name, TaskStatus.RUNNING))
            
            try:
                tasks = [task.execute(context) for task in ready_tasks]
                await asyncio.gather(*tasks)
                
                # Report completed tasks
                for task in ready_tasks:
                    task.status = TaskStatus.COMPLETED
                    completed_tasks.add(task.name)
                    if callback:
                        callback(TaskProgress(task.name, TaskStatus.COMPLETED))
                
            except Exception as e:
                # Report failed tasks
                for task in ready_tasks:
                    if task.status != TaskStatus.COMPLETED:
                        task.status = TaskStatus.FAILED
                        if callback:
                            callback(TaskProgress(task.name, TaskStatus.FAILED))
                raise
        
        output = Output()
        for key, value in context.items():
            if key in self.output_schema:
                output[key] = value

        validate_schema(output, self.output_schema, "output")
        logger.info(f"Completed workflow execution: {self.name}")
        return output
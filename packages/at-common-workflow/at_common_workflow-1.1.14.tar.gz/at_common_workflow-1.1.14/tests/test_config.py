import pytest
from pathlib import Path
import tempfile
import os
from at_common_workflow import WorkflowConfig, TaskScanner

def test_config_root_path():
    test_path = "/test/path"
    WorkflowConfig.set_root_path(test_path)
    assert WorkflowConfig.get_root_path() == Path(test_path).resolve()

def test_config_module_path():
    with tempfile.TemporaryDirectory() as temp_dir:
        WorkflowConfig.set_root_path(temp_dir)
        
        # Create a nested file structure
        nested_dir = Path(temp_dir) / "nested" / "deeper"
        nested_dir.mkdir(parents=True)
        test_file = nested_dir / "test_file.py"
        
        # Test module path generation
        module_path = WorkflowConfig.get_module_path(test_file)
        assert module_path == "nested.deeper.test_file"

def test_config_invalid_path():
    with pytest.raises(ValueError, match="Root path not set"):
        WorkflowConfig._root_path = None
        WorkflowConfig.get_module_path("some/path")

def test_config_path_outside_root():
    with tempfile.TemporaryDirectory() as temp_dir:
        WorkflowConfig.set_root_path(temp_dir)
        
        # Try to get module path for file outside root
        with pytest.raises(ValueError, match="is not under root path"):
            WorkflowConfig.get_module_path("/some/other/path/file.py")

@pytest.mark.asyncio
async def test_scanner_with_config():
    with tempfile.TemporaryDirectory() as temp_dir:
        # Set up test directory structure
        temp_path = Path(temp_dir)
        WorkflowConfig.set_root_path(temp_path)
        
        # Create a test task file
        task_content = '''
from at_common_workflow import task
from at_common_workflow.core.context import Context

@task(name="config_test_task")
async def test_task(context: Context):
    pass
'''
        task_file = temp_path / "tasks.py"
        task_file.write_text(task_content)
        
        # Scan for tasks
        tasks = TaskScanner.scan(str(temp_path))
        assert len(tasks) == 1
        assert tasks[0].name == "config_test_task"

def test_multiple_root_paths():
    # Test changing root paths
    path1 = "/path/one"
    path2 = "/path/two"
    
    WorkflowConfig.set_root_path(path1)
    assert WorkflowConfig.get_root_path() == Path(path1).resolve()
    
    WorkflowConfig.set_root_path(path2)
    assert WorkflowConfig.get_root_path() == Path(path2).resolve()

def test_relative_root_path():
    with tempfile.TemporaryDirectory() as temp_dir:
        os.chdir(temp_dir)
        
        # Use relative path
        WorkflowConfig.set_root_path("./relative/path")
        expected_path = Path(temp_dir) / "relative" / "path"
        assert WorkflowConfig.get_root_path() == expected_path.resolve() 
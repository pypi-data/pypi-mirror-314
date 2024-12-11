def clean_module_path(module_path: str) -> str:
    """Clean up module path by removing 'site-packages.' prefix if present.
    
    Args:
        module_path: The module path to clean
        
    Returns:
        Cleaned module path
    """
    if 'site-packages.' in module_path:
        return module_path.split('site-packages.')[-1]
    return module_path 
# roksana/search_methods/registry.py

from typing import Type, Dict, Any
from .base_search import SearchMethod

# Registry dictionary to hold search method classes
SEARCH_METHODS: Dict[str, Type[SearchMethod]] = {}

def register_search_method(name: str):
    """
    Decorator to register a search method class with a given name.

    Args:
        name (str): The name to register the search method under.

    Returns:
        Callable: The decorator function.
    """
    def decorator(cls: Type[SearchMethod]):
        if not issubclass(cls, SearchMethod):
            raise ValueError("Can only register subclasses of SearchMethod")
        SEARCH_METHODS[name.lower()] = cls
        return cls
    return decorator

def get_search_method(name: str, data: Any, device: str = None, **kwargs) -> SearchMethod:
    """
    Retrieve an instance of the specified search method.

    Args:
        name (str): Name of the search method (e.g., 'gcn', 'gat', 'sage').
        data (Any): The graph dataset.
        device (str, optional): Device to run the computations on ('cpu' or 'cuda').
        **kwargs: Additional keyword arguments for the search method.

    Returns:
        SearchMethod: An instance of the requested search method.

    Raises:
        ValueError: If the specified search method is not registered.
    """
    name = name.lower()
    if name not in SEARCH_METHODS:
        raise ValueError(f"Search method '{name}' not found. Available methods: {list(SEARCH_METHODS.keys())}")
    search_method_class = SEARCH_METHODS[name]
    return search_method_class(data, device=device, **kwargs)
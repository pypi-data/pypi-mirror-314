# roksana/attack_methods/registry.py

from typing import Type, Dict, Any
from .base_attack import AttackMethod
from .degree import degree
from .pagerank import pagerank
from .random import random
from .viking import viking

# Registry dictionary to hold attack method classes
ATTACK_METHODS: Dict[str, Type[AttackMethod]] = {
    'degree': degree,
    'pagerank': pagerank,
    'random': random,
    'viking': viking,
    # Add more predefined attacks here
}

def register_attack_method(name: str):
    """
    Decorator to register an attack method class with a given name.

    Args:
        name (str): The name to register the attack method under.

    Returns:
        Callable: The decorator function.
    """
    def decorator(cls: Type[AttackMethod]):
        if not issubclass(cls, AttackMethod):
            raise ValueError("Can only register subclasses of AttackMethod")
        ATTACK_METHODS[name.lower()] = cls
        return cls
    return decorator

def get_attack_method(name: str, data: Any, **kwargs) -> AttackMethod:
    """
    Retrieve an instance of the specified attack method.

    Args:
        name (str): Name of the attack method (e.g., 'predefined_attack1', 'predefined_attack2').
        data (Any): The graph dataset.
        **kwargs: Additional keyword arguments for the attack method.

    Returns:
        AttackMethod: An instance of the requested attack method.

    Raises:
        ValueError: If the specified attack method is not registered.
    """
    name = name.lower()
    if name not in ATTACK_METHODS:
        raise ValueError(f"Attack method '{name}' not found. Available methods: {list(ATTACK_METHODS.keys())}")
    attack_method_class = ATTACK_METHODS[name]
    return attack_method_class(data, **kwargs)
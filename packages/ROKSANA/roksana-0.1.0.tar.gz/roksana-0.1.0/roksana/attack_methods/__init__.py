# roksana/attack_methods/__init__.py

from .base_attack import AttackMethod
from .registry import get_attack_method, ATTACK_METHODS
from .degree import degree
from .pagerank import pagerank
from .random import random
from .viking import viking


__all__ = [
    'AttackMethod',
    'get_attack_method',
    'ATTACK_METHODS',
    'degree',
    'pagerank',
    'random',
    'viking',
]
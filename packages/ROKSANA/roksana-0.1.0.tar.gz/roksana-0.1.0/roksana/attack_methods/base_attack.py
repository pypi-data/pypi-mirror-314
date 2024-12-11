# roksana/attack_methods/base_attack.py

from abc import ABC, abstractmethod
from typing import Any, Dict

class AttackMethod(ABC):
    """
    Abstract base class for attack methods.
    """

    @abstractmethod
    def __init__(self, data: Any, **kwargs):
        """
        Initialize the attack method with the given dataset.

        Args:
            data (Any): The graph dataset.
            **kwargs: Additional keyword arguments specific to the attack method.
        """
        pass

    @abstractmethod
    def attack(self, query_node: int, perturbations: int = 1) -> Dict[str, Any]:
        """
        Perform an attack on the specified query node.

        Args:
            query_node (int): Index of the node to attack.
            perturbations (int, optional): Number of perturbations to apply. Defaults to 1.

        Returns:
            Dict[str, Any]: Details of the attack performed.
        """
        pass
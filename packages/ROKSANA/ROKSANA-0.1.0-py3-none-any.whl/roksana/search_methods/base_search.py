# roksana/search_methods/base_search.py

from abc import ABC, abstractmethod
from typing import Any, List

class SearchMethod(ABC):
    """
    Abstract base class for search methods.
    """

    @abstractmethod
    def __init__(self, data: Any, device: str = None, **kwargs):
        """
        Initialize the search method with the given dataset.

        Args:
            data (Any): The graph dataset.
            device (str, optional): Device to run the computations on ('cpu' or 'cuda').
        """
        pass

    @abstractmethod
    def search(self, query_features: Any, top_k: int = 10) -> List[int]:
        """
        Perform a search with the given query features.

        Args:
            query_features (Any): Feature vector of the query node.
            top_k (int, optional): Number of top similar nodes to retrieve.

        Returns:
            List[int]: List of node indices sorted by similarity to the query.
        """
        pass
# roksana/datasets.py

from torch_geometric.data import InMemoryDataset, Data
from torch_geometric.datasets import Planetoid
import os
import os.path as osp
import torch
from typing import List, Optional, Callable, Union, Any, Tuple, Dict
import json
import csv
import pickle
import random
import hashlib

class UserDataset(InMemoryDataset):
    """
    A dataset class for user-provided datasets adhering to PyG's InMemoryDataset structure.

    Users should provide their data in a specific format, typically as a list of `torch_geometric.data.Data` objects.
    """
    def __init__(
        self,
        root: str,
        transform: Optional[Callable] = None,
        pre_transform: Optional[Callable] = None,
        pre_filter: Optional[Callable] = None,
        data_list: Optional[List[Data]] = None
    ):
        """
        Initialize the UserDataset.

        Args:
            root (str): Root directory where the dataset should be saved.
            transform (Callable, optional): A function/transform that takes in an
                `torch_geometric.data.Data` object and returns a transformed version.
                The data object will be transformed before every access.
            pre_transform (Callable, optional): A function/transform that takes in
                an `torch_geometric.data.Data` object and returns a transformed version.
                The data object will be transformed before being saved to disk.
            pre_filter (Callable, optional): A function that takes in a `torch_geometric.data.Data`
                object and returns a boolean value, indicating whether the data object
                should be included in the final dataset.
            data_list (List[Data], optional): A list of `torch_geometric.data.Data` objects.
                If provided, it will be used to initialize the dataset.
        """
        self.custom_data = data_list
        super(UserDataset, self).__init__(root, transform, pre_transform, pre_filter)
        self.data, self.slices = torch.load(self.processed_paths[0])

    @property
    def raw_file_names(self) -> List[str]:
        """
        Since users provide their own data, this can be left empty or used to list expected raw files.
        """
        return []

    @property
    def processed_file_names(self) -> List[str]:
        """
        The name of the processed file.
        """
        return ['data.pt']

    def download(self):
        """
        Users are expected to provide their own data, so no download is necessary.
        """
        pass

    def process(self):
        """
        Process the user-provided data and save it in the processed file.

        Users can modify this method if they have specific processing requirements.
        """
        if self.custom_data is None:
            raise ValueError("No data provided for UserDataset. Please provide `data_list`.")

        data_list = self.custom_data

        if self.pre_filter is not None:
            data_list = [data for data in data_list if self.pre_filter(data)]

        if self.pre_transform is not None:
            data_list = [self.pre_transform(data) for data in data_list]

        data, slices = self.collate(data_list)
        torch.save((data, slices), self.processed_paths[0])

def load_standard_dataset(name: str, root: str = 'data') -> Planetoid:
    """
    Load a standard dataset from PyG's built-in datasets.

    Supported datasets: 'cora', 'citeseer', 'pubmed', etc. Refer to PyG's Planetoid datasets for more.

    Args:
        name (str): Name of the dataset to load (e.g., 'Cora', 'Citeseer').
        root (str, optional): Root directory where the dataset should be saved. Defaults to 'data'.

    Returns:
        Planetoid: An instance of the Planetoid dataset.
    """
    name = name.lower()
    supported_datasets = ['cora', 'citeseer', 'pubmed']
    if name not in supported_datasets:
        raise ValueError(f"Dataset '{name}' is not supported. Supported datasets are: {supported_datasets}")

    return Planetoid(root=root, name=name.capitalize())

def load_dataset(
    dataset_name: Optional[str] = None,
    root: str = 'data',
    transform: Optional[Callable] = None,
    pre_transform: Optional[Callable] = None,
    pre_filter: Optional[Callable] = None,
    data_list: Optional[List[Data]] = None
) -> InMemoryDataset:
    """
    Load a dataset, either a standard dataset or a user-provided dataset.

    Args:
        dataset_name (str, optional): Name of the standard dataset to load (e.g., 'cora', 'citeseer').
            If None, a UserDataset should be provided via `data_list`.
        root (str, optional): Root directory where the dataset should be saved or loaded from.
            Defaults to 'data'.
        transform (Callable, optional): A function/transform that takes in an
            `torch_geometric.data.Data` object and returns a transformed version.
            The data object will be transformed before every access.
        pre_transform (Callable, optional): A function/transform that takes in
            an `torch_geometric.data.Data` object and returns a transformed version.
            The data object will be transformed before being saved to disk.
        pre_filter (Callable, optional): A function that takes in a `torch_geometric.data.Data`
            object and returns a boolean value, indicating whether the data object
            should be included in the final dataset.
        data_list (List[Data], optional): A list of `torch_geometric.data.Data` objects.
            Required if `dataset_name` is None.

    Returns:
        InMemoryDataset: An instance of the loaded dataset.
    """
    if dataset_name is not None:
        return load_standard_dataset(name=dataset_name, root=root)
    else:
        if data_list is None:
            raise ValueError("`data_list` must be provided if `dataset_name` is None.")
        return UserDataset(
            root=root,
            transform=transform,
            pre_transform=pre_transform,
            pre_filter=pre_filter,
            data_list=data_list
        )

def load_user_dataset_from_files(
    data_dir: str,
    file_format: str = 'json',
    transform: Optional[Callable] = None,
    pre_transform: Optional[Callable] = None,
    pre_filter: Optional[Callable] = None
) -> UserDataset:
    """
    Load a user dataset from files in a specified directory.

    Supported file formats: 'json', 'csv', 'pickle'.

    Args:
        data_dir (str): Directory containing the dataset files.
        file_format (str, optional): Format of the dataset files. Defaults to 'json'.
        transform (Callable, optional): A function/transform that takes in an
            `torch_geometric.data.Data` object and returns a transformed version.
            The data object will be transformed before every access.
        pre_transform (Callable, optional): A function/transform that takes in
            an `torch_geometric.data.Data` object and returns a transformed version.
            The data object will be transformed before being saved to disk.
        pre_filter (Callable, optional): A function that takes in a `torch_geometric.data.Data`
            object and returns a boolean value, indicating whether the data object
            should be included in the final dataset.

    Returns:
        UserDataset: An instance of the UserDataset loaded from the files.
    """
    data_list = []

    if file_format == 'json':
        for filename in os.listdir(data_dir):
            if filename.endswith('.json'):
                filepath = osp.join(data_dir, filename)
                with open(filepath, 'r') as f:
                    data_dict = json.load(f)
                data = Data(**data_dict)
                data_list.append(data)

    elif file_format == 'csv':
        # Assuming each CSV file represents edge lists with source and target nodes
        edge_index = []
        for filename in os.listdir(data_dir):
            if filename.endswith('.csv'):
                filepath = osp.join(data_dir, filename)
                with open(filepath, 'r') as f:
                    reader = csv.reader(f)
                    next(reader)  # Skip header if present
                    for row in reader:
                        src, dst = map(int, row)
                        edge_index.append([src, dst])
        if edge_index:
            edge_index = torch.tensor(edge_index, dtype=torch.long).t().contiguous()
            data = Data(edge_index=edge_index)
            data_list.append(data)

    elif file_format == 'pickle':
        for filename in os.listdir(data_dir):
            if filename.endswith('.pkl'):
                filepath = osp.join(data_dir, filename)
                with open(filepath, 'rb') as f:
                    data = pickle.load(f)
                data_list.append(data)

    else:
        raise ValueError(f"Unsupported file format '{file_format}'. Supported formats are 'json', 'csv', 'pickle'.")

    return UserDataset(
        root=data_dir,
        transform=transform,
        pre_transform=pre_transform,
        pre_filter=pre_filter,
        data_list=data_list
    )

def list_available_standard_datasets() -> List[str]:
    """
    List all available standard datasets supported by ROKSANA.

    Returns:
        List[str]: A list of supported dataset names.
    """
    return ['cora', 'citeseer', 'pubmed']

def get_dataset_info(dataset: InMemoryDataset) -> Dict[str, Any]:
    """
    Retrieve basic information about a dataset.

    Args:
        dataset (InMemoryDataset): The dataset instance.

    Returns:
        Dict[str, Any]: A dictionary containing dataset information.
    """
    info = {
        'num_graphs': len(dataset),
        'num_features': dataset.num_features if hasattr(dataset, 'num_features') else 'N/A',
        'num_classes': dataset.num_classes if hasattr(dataset, 'num_classes') else 'N/A',
    }
    return info

def prepare_search_set(
    data: Data,
    percentage: float = 0.1,
    seed: int = 42
) -> Tuple[List[int], List[List[int]]]:
    """
    Prepare a search set for search evaluation by selecting a percentage of nodes as queries
    and creating corresponding gold sets based on feature similarity.

    Args:
        data (Data): The graph dataset.
        percentage (float, optional): Percentage of nodes to select as queries. Must be between 0 and 1.
                                     Defaults to 0.1 (10%).
        seed (int, optional): Seed for random number generator to ensure reproducibility.
                              Defaults to 42.

    Returns:
        Tuple[List[int], List[List[int]]]: A tuple containing:
            - queries (List[int]): List of node indices selected as queries.
            - gold_sets (List[List[int]]): List of gold sets, where each gold set is a list of node indices
                                           with the same features as the corresponding query.
    
    Raises:
        ValueError: If percentage is not between 0 and 1.
        AttributeError: If dataset does not contain node features (`data.x`).
    """
    if not (0 < percentage < 1):
        raise ValueError("`percentage` must be between 0 and 1.")

    if not hasattr(data, 'x') or data.x is None:
        raise AttributeError("The dataset must have node features (`data.x`) to create gold sets.")

    num_nodes = data.num_nodes
    num_queries = max(1, int(num_nodes * percentage))

    # Set random seed for reproducibility
    random.seed(seed)
    torch.manual_seed(seed)

    # Randomly select query node indices
    all_node_indices = list(range(num_nodes))
    query_ids = random.sample(all_node_indices, num_queries)
    
    query_features = torch.stack([data.x[i] for i in query_ids])

    # Create a mapping from feature hash to node indices
    feature_map: Dict[str, List[int]] = {}
    for idx in range(num_nodes):
        # Convert feature tensor to bytes for hashing
        feature_bytes = data.x[idx].cpu().numpy().tobytes()
        feature_hash = hashlib.sha256(feature_bytes).hexdigest()
        if feature_hash in feature_map:
            feature_map[feature_hash].append(idx)
        else:
            feature_map[feature_hash] = [idx]

    gold_sets = []
    for query in query_ids:
        # Get the feature hash of the query node
        query_feature_bytes = data.x[query].cpu().numpy().tobytes()
        query_feature_hash = hashlib.sha256(query_feature_bytes).hexdigest()
        # Retrieve all nodes with the same feature hash
        similar_nodes = feature_map.get(query_feature_hash, [])
        # Exclude the query node itself
        similar_nodes = [node for node in similar_nodes]
        gold_sets.append(similar_nodes)

    return query_ids, query_features, gold_sets

def load_user_dataset_from_files(
    data_dir: str,
    file_format: str = 'json',
    transform: Optional[Callable] = None,
    pre_transform: Optional[Callable] = None,
    pre_filter: Optional[Callable] = None
) -> UserDataset:
    """
    Load a user dataset from files in a specified directory.

    Supported file formats: 'json', 'csv', 'pickle'.

    Args:
        data_dir (str): Directory containing the dataset files.
        file_format (str, optional): Format of the dataset files. Defaults to 'json'.
        transform (Callable, optional): A function/transform that takes in an
            `torch_geometric.data.Data` object and returns a transformed version.
            The data object will be transformed before every access.
        pre_transform (Callable, optional): A function/transform that takes in
            an `torch_geometric.data.Data` object and returns a transformed version.
            The data object will be transformed before being saved to disk.
        pre_filter (Callable, optional): A function that takes in a `torch_geometric.data.Data`
            object and returns a boolean value, indicating whether the data object
            should be included in the final dataset.

    Returns:
        UserDataset: An instance of the UserDataset loaded from the files.
    """
    data_list = []

    if file_format == 'json':
        for filename in os.listdir(data_dir):
            if filename.endswith('.json'):
                filepath = osp.join(data_dir, filename)
                with open(filepath, 'r') as f:
                    data_dict = json.load(f)
                data = Data(**data_dict)
                data_list.append(data)

    elif file_format == 'csv':
        # Assuming each CSV file represents edge lists with source and target nodes
        edge_index = []
        for filename in os.listdir(data_dir):
            if filename.endswith('.csv'):
                filepath = osp.join(data_dir, filename)
                with open(filepath, 'r') as f:
                    reader = csv.reader(f)
                    header = next(reader, None)  # Skip header if present
                    for row in reader:
                        src, dst = map(int, row)
                        edge_index.append([src, dst])
        if edge_index:
            edge_index = torch.tensor(edge_index, dtype=torch.long).t().contiguous()
            data = Data(edge_index=edge_index)
            data_list.append(data)

    elif file_format == 'pickle':
        for filename in os.listdir(data_dir):
            if filename.endswith('.pkl'):
                filepath = osp.join(data_dir, filename)
                with open(filepath, 'rb') as f:
                    data = pickle.load(f)
                data_list.append(data)

    else:
        raise ValueError(f"Unsupported file format '{file_format}'. Supported formats are 'json', 'csv', 'pickle'.")

    return UserDataset(
        root=data_dir,
        transform=transform,
        pre_transform=pre_transform,
        pre_filter=pre_filter,
        data_list=data_list
    )

# Example utility functions to inspect datasets
def list_available_standard_datasets() -> List[str]:
    """
    List all available standard datasets supported by ROKSANA.

    Returns:
        List[str]: A list of supported dataset names.
    """
    return ['cora', 'citeseer', 'pubmed']

def get_dataset_info(dataset: InMemoryDataset) -> Dict[str, Any]:
    """
    Retrieve basic information about a dataset.

    Args:
        dataset (InMemoryDataset): The dataset instance.

    Returns:
        Dict[str, Any]: A dictionary containing dataset information.
    """
    info = {
        'num_graphs': len(dataset),
        'num_features': dataset.num_features if hasattr(dataset, 'num_features') else 'N/A',
        'num_classes': dataset.num_classes if hasattr(dataset, 'num_classes') else 'N/A',
    }
    return info

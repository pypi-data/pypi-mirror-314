# ROKSANA

ROKSANA is a Python toolkit for performing keyword search and attack methods on user-provided datasets.

## Features

- **Custom Datasets:** Bring your own dataset using PyG Geometric's dataset structure.
- **Search Methods:** Choose from pre-defined keyword search methods.
- **Attack Methods:** Utilize pre-defined attack methods or implement your own.
- **Result Handling:** Save results to files in various formats.
- **Leaderboard Integration:** Submit your results to the leaderboard.

## Installation

```bash
pip install roksana
```

## Preparing the Test Set

To evaluate the effectiveness of the search methods, you can prepare a search set consisting of query nodes and their corresponding gold sets. The gold set for each query consists of all nodes in the dataset that share the exact same feature vector as the query node.

### Function: `prepare_search_set`

```python
from roksana.datasets import prepare_search_set

# Assume 'data' is a torch_geometric.data.Data object
queries, gold_sets = prepare_search_set(data, percentage=0.1, seed=42)
```

## Attack Methods

ROKSANA provides a suite of attack methods to evaluate the robustness of your search algorithms. Currently, the package includes predefined attack methods that you can leverage out-of-the-box or extend with your custom implementations.

### Available Attack Methods

- `random`: Randomly adds or removes edges connected to the query node.
- `viking`: Perturbs the feature vectors of the query node.

### Using Attack Methods

```python
from roksana.datasets import load_dataset, prepare_test_set
from roksana.attack_methods import get_attack_method
```

# Load the Cora dataset
```python
dataset = load_dataset(dataset_name='cora', root='data/')
data = dataset[0]
```

# Prepare the test set
```python
queries, gold_sets = prepare_test_set(data, percentage=0.1, seed=123)
```

# Initialize an attack method
```python
attack_method = get_attack_method('predefined_attack1', data=data, perturbations=2)
```

# Perform attacks on queries
```
for query_node in queries:
    attack_details = attack_method.attack(query_node=query_node, perturbations=2)
    print(f"Attack on Node {query_node}: {attack_details}")
```

## Evaluation

The **Evaluation** module in ROKSANA provides tools to assess the effectiveness of attack strategies on your search methods. By computing key metrics—**Hit@k**, **Recall@k**, and **Demotion Value**—you can quantify how attacks influence the performance and reliability of your search algorithms.

### **Key Metrics**

1. **Hit@k**
   - **Definition:** Measures whether at least one relevant node (from the gold set) appears in the top-k retrieved nodes.
   - **Interpretation:** Higher values indicate better performance in retrieving relevant nodes within the top-k results.

2. **Recall@k**
   - **Definition:** Quantifies the proportion of relevant nodes that are retrieved in the top-k results.
   - **Interpretation:** Higher values signify that a larger fraction of relevant nodes are captured within the top-k retrieved nodes.

3. **Demotion Value**
   - **Definition:** Measures the change in the rank of a target node (typically the query node itself) before and after an attack.
   - **Interpretation:** Positive values indicate that the target node has been ranked lower post-attack, reflecting the attack's effectiveness in degrading its visibility.

### **Using the Evaluation Module**

Here's a step-by-step guide to evaluating the impact of an attack on a search method.

#### **1. Load Dataset and Prepare Test Set**

```python
from roksana.datasets import load_dataset, prepare_test_set
```

# Load the Cora dataset
```python
dataset = load_dataset(dataset_name='cora', root='data/')
data = dataset[0]
```

# Prepare the test set with 10% of nodes as queries
```python
queries, gold_sets = prepare_test_set(data, percentage=0.1, seed=123)
```

## Saving Evaluation Results

ROKSANA provides utility functions to save evaluation results in various formats, including JSON, CSV, and Pickle. These functions are located within the `evaluation.utils` module.

### **Available Functions**

- `save_results_to_json(results: List[Dict[str, Any]], filepath: str) -> None`
- `save_results_to_csv(results: List[Dict[str, Any]], filepath: str) -> None`
- `save_results_to_pickle(results: List[Dict[str, Any]], filepath: str) -> None`

### **Usage Example**

```python
from roksana.evaluation import save_results_to_csv, save_results_to_json, save_results_to_pickle

# Assuming 'results' is a list of dictionaries containing evaluation metrics
results = [
    {
        'query_node': 0,
        'k': 5,
        'Hit@k_before_attack': 1.0,
        'Hit@k_after_attack': 0.0,
        'Recall@k_before_attack': 0.5,
        'Recall@k_after_attack': 0.3,
        'Demotion_value': 2
    },
    # Add more results as needed
]

# Save results in different formats
save_results_to_csv(results, 'evaluation_results/results.csv')
save_results_to_json(results, 'evaluation_results/results.json')
save_results_to_pickle(results, 'evaluation_results/results.pkl')
```
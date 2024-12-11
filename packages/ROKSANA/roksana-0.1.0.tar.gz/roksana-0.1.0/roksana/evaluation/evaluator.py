# roksana/evaluation/evaluator.py

from typing import List, Tuple, Dict, Any
import csv
import json
import os
from .metrics import hit_at_k, recall_at_k, demotion_value

class Evaluator:
    """
    Evaluator class to assess the impact of attack methods on search strategies.
    """

    def __init__(self, search_method_before, search_method_after, k_values: List[int] = [5, 10, 20]):
        """
        Initialize the Evaluator.

        Args:
            search_method_before: Instance of SearchMethod before attack.
            search_method_after: Instance of SearchMethod after attack.
            k_values (List[int], optional): List of k values for Hit@k and Recall@k. Defaults to [5, 10, 20].
        """
        self.search_before = search_method_before
        self.search_after = search_method_after
        self.k_values = k_values
        self.results = []  # Store results internally

    def evaluate(
        self,
        queries: List[int],
        gold_sets: List[List[int]],
        results_dir: str = 'results',
        filename: str = 'evaluation_results.csv'
    ) -> None:
        """
        Perform evaluation on the given queries and save the results.

        Args:
            queries (List[int]): List of query node indices.
            gold_sets (List[List[int]]): List of gold sets corresponding to each query.
            results_dir (str, optional): Directory to save the results file. Defaults to 'results'.
            filename (str, optional): Name of the results file. Defaults to 'evaluation_results.csv'.
        """
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)

        filepath = os.path.join(results_dir, filename)

        # Prepare header
        header = [
            'query_node',
            'k',
            'Hit@k_before_attack',
            'Hit@k_after_attack',
            'Recall@k_before_attack',
            'Recall@k_after_attack',
            'Demotion_value'
        ]

        with open(filepath, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)

            for query, gold_set in zip(queries, gold_sets):
                # Search before attack
                retrieved_before = self.search_before.search(
                    query_features=self.search_before.data.x[query],
                    top_k=max(self.k_values)
                )

                # Search after attack
                retrieved_after = self.search_after.search(
                    query_features=self.search_after.data.x[query],
                    top_k=max(self.k_values)
                )

                # Calculate Demotion Value
                # Find the rank of the query node in retrieved_before and retrieved_after
                try:
                    rank_before = retrieved_before.index(query) + 1
                except ValueError:
                    rank_before = len(retrieved_before) + 1  # Not found

                try:
                    rank_after = retrieved_after.index(query) + 1
                except ValueError:
                    rank_after = len(retrieved_after) + 1  # Not found

                demotion = demotion_value(rank_before, rank_after)

                for k in self.k_values:
                    hit_before = hit_at_k(retrieved_before, gold_set, k)
                    hit_after = hit_at_k(retrieved_after, gold_set, k)
                    recall_before = recall_at_k(retrieved_before, gold_set, k)
                    recall_after = recall_at_k(retrieved_after, gold_set, k)

                    result = {
                        'query_node': query,
                        'k': k,
                        'Hit@k_before_attack': hit_before,
                        'Hit@k_after_attack': hit_after,
                        'Recall@k_before_attack': recall_before,
                        'Recall@k_after_attack': recall_after,
                        'Demotion_value': demotion
                    }
                    self.results.append(result)
                    writer.writerow([
                        query,
                        k,
                        hit_before,
                        hit_after,
                        recall_before,
                        recall_after,
                        demotion
                    ])

        print(f"Evaluation results saved to {filepath}")

    def get_all_results(self) -> List[Dict[str, Any]]:
        """
        Retrieve all evaluation results.

        Returns:
            List[Dict[str, Any]]: List of evaluation result dictionaries.
        """
        return self.results
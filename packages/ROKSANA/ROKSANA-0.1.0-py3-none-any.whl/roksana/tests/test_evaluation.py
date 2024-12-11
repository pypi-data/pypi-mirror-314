# tests/test_evaluation.py

import unittest
import torch
from torch_geometric.data import Data
from roksana.search_methods import GCNSearch
from roksana.attack_methods import PredefinedAttack1
from roksana.evaluation import Evaluator, save_results_to_json, save_results_to_csv, save_results_to_pickle

class TestEvaluation(unittest.TestCase):
    def setUp(self):
        # Create a simple graph
        self.x = torch.tensor([
            [1.0, 2.0],
            [3.0, 4.0],
            [1.0, 2.0],
            [5.0, 6.0]
        ], dtype=torch.float)
        self.edge_index = torch.tensor([
            [0, 1, 2],
            [1, 2, 3]
        ], dtype=torch.long)
        self.y = torch.tensor([0, 1, 0, 1], dtype=torch.long)
        self.train_mask = torch.tensor([True, True, True, True], dtype=torch.bool)
        self.data = Data(x=self.x, edge_index=self.edge_index, y=self.y, train_mask=self.train_mask)

        # Initialize search methods
        self.search_before = GCNSearch(data=self.data, epochs=10, lr=0.01)
        self.attack_method = PredefinedAttack1(data=self.data, perturbations=1)
        self.attack_method.attack(query_node=0, perturbations=1)  # Perform attack on node 0
        self.search_after = GCNSearch(data=self.data, epochs=10, lr=0.01)

        # Prepare queries and gold sets
        self.queries = [0]
        self.gold_sets = [[2]]  # Node 0 and 2 share the same features

    def test_evaluator(self):
        evaluator = Evaluator(
            search_method_before=self.search_before,
            search_method_after=self.search_after,
            k_values=[1, 2]
        )
        evaluator.evaluate(
            queries=self.queries,
            gold_sets=self.gold_sets,
            results_dir='test_results',
            filename='test_evaluation.csv'
        )
        # Check if the file exists
        import os
        self.assertTrue(os.path.exists('test_results/test_evaluation.csv'))

        # Clean up
        os.remove('test_results/test_evaluation.csv')
        os.rmdir('test_results')

    def test_save_results_to_csv(self):
        results = [
            {'query_node': 0, 'k': 5, 'Hit@k_before_attack': 1.0, 'Hit@k_after_attack': 0.0,
             'Recall@k_before_attack': 0.5, 'Recall@k_after_attack': 0.3, 'Demotion_value': 2},
        ]
        save_results_to_csv(results, 'test_results/save_test.csv')
        import os
        self.assertTrue(os.path.exists('test_results/save_test.csv'))
        # Clean up
        os.remove('test_results/save_test.csv')
        os.rmdir('test_results')

    def test_save_results_to_json(self):
        results = [
            {'query_node': 0, 'k': 5, 'Hit@k_before_attack': 1.0, 'Hit@k_after_attack': 0.0,
             'Recall@k_before_attack': 0.5, 'Recall@k_after_attack': 0.3, 'Demotion_value': 2},
        ]
        save_results_to_json(results, 'test_results/save_test.json')
        import os, json
        self.assertTrue(os.path.exists('test_results/save_test.json'))
        with open('test_results/save_test.json', 'r') as f:
            loaded = json.load(f)
        self.assertEqual(loaded, results)
        # Clean up
        os.remove('test_results/save_test.json')
        os.rmdir('test_results')

    def test_save_results_to_pickle(self):
        results = [
            {'query_node': 0, 'k': 5, 'Hit@k_before_attack': 1.0, 'Hit@k_after_attack': 0.0,
             'Recall@k_before_attack': 0.5, 'Recall@k_after_attack': 0.3, 'Demotion_value': 2},
        ]
        save_results_to_pickle(results, 'test_results/save_test.pkl')
        import os, pickle
        self.assertTrue(os.path.exists('test_results/save_test.pkl'))
        with open('test_results/save_test.pkl', 'rb') as f:
            loaded = pickle.load(f)
        self.assertEqual(loaded, results)
        # Clean up
        os.remove('test_results/save_test.pkl')
        os.rmdir('test_results')

    def test_metrics(self):
        from roksana.evaluation.metrics import hit_at_k, recall_at_k, demotion_value

        retrieved = [2, 1, 3]
        gold_set = [2]
        self.assertEqual(hit_at_k(retrieved, gold_set, 1), 0.0)
        self.assertEqual(hit_at_k(retrieved, gold_set, 2), 1.0)

        gold_set_multiple = [2, 3]
        self.assertEqual(recall_at_k(retrieved, gold_set_multiple, 1), 0.5)
        self.assertEqual(recall_at_k(retrieved, gold_set_multiple, 3), 1.0)

        self.assertEqual(demotion_value(2, 4), 2)
        self.assertEqual(demotion_value(3, 1), -2)
        self.assertEqual(demotion_value(1, 1), 0)

if __name__ == '__main__':
    unittest.main()
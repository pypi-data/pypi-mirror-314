import unittest
import torch
from torch_geometric.data import Data
from roksana.datasets import prepare_search_set

class TestPrepareTestSet(unittest.TestCase):
    def setUp(self):
        # Create a simple graph with features
        self.x = torch.tensor([[1.0, 2.0], [3.0, 4.0], [1.0, 2.0], [5.0, 6.0]], dtype=torch.float)
        self.edge_index = torch.tensor([[0, 1, 2, 3],
                                       [1, 0, 3, 2]], dtype=torch.long)
        self.y = torch.tensor([0, 1, 0, 1], dtype=torch.long)
        self.train_mask = torch.tensor([True, True, True, True], dtype=torch.bool)
        self.data = Data(x=self.x, edge_index=self.edge_index, y=self.y, train_mask=self.train_mask)

    def test_prepare_search_set_percentage(self):
        # Test with 50% queries
        queries, gold_sets = prepare_search_set(self.data, percentage=0.5, seed=123)
        self.assertEqual(len(queries), 2)
        self.assertEqual(len(gold_sets), 2)
        for gold in gold_sets:
            # Verify that all nodes in gold have the same features as the query
            for node_idx in gold:
                self.assertTrue(torch.equal(self.data.x[node_idx], self.data.x[queries[gold_sets.index(gold)]]))

    def test_prepare_search_set_invalid_percentage(self):
        with self.assertRaises(ValueError):
            prepare_search_set(self.data, percentage=1.5)

    def test_prepare_search_set_no_features(self):
        data_no_features = Data(edge_index=self.edge_index, y=self.y, train_mask=self.train_mask)
        with self.assertRaises(AttributeError):
            prepare_search_set(data_no_features, percentage=0.5)

    def test_prepare_search_set_seed_reproducibility(self):
        queries1, gold_sets1 = prepare_search_set(self.data, percentage=0.5, seed=42)
        queries2, gold_sets2 = prepare_search_set(self.data, percentage=0.5, seed=42)
        self.assertEqual(queries1, queries2)
        self.assertEqual(gold_sets1, gold_sets2)

    def test_prepare_search_set_unique_features(self):
        # All nodes have unique features
        unique_x = torch.tensor([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0], [7.0, 8.0]], dtype=torch.float)
        data_unique = Data(x=unique_x, edge_index=self.edge_index, y=self.y, train_mask=self.train_mask)
        queries, gold_sets = prepare_search_set(data_unique, percentage=0.5, seed=42)
        for gold in gold_sets:
            self.assertEqual(len(gold), 0)  # No other nodes share the same features

    def test_prepare_search_set_multiple_matches(self):
        # Multiple nodes share the same features
        multiple_x = torch.tensor([[1.0, 2.0], [1.0, 2.0], [1.0, 2.0], [5.0, 6.0]], dtype=torch.float)
        data_multiple = Data(x=multiple_x, edge_index=self.edge_index, y=self.y, train_mask=self.train_mask)
        queries, gold_sets = prepare_search_set(data_multiple, percentage=0.5, seed=42)
        self.assertEqual(len(queries), 2)
        # Each query should have 2 gold nodes (excluding itself)
        for gold in gold_sets:
            self.assertEqual(len(gold), 2)

if __name__ == '__main__':
    unittest.main()

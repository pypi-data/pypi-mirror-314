# tests/test_search_methods.py

import unittest
import torch
from torch_geometric.data import Data
from roksana.search_methods import GCNSearch, GATSearch, SAGESearch, get_search_method

class TestSearchMethods(unittest.TestCase):
    def setUp(self):
        # Create a simple graph for testing
        # 4 nodes with 2 features each
        x = torch.tensor([[1.0, 2.0], [3.0, 4.0], [1.0, 2.0], [5.0, 6.0]], dtype=torch.float)
        edge_index = torch.tensor([[0, 1, 2, 3],
                                   [1, 0, 3, 2]], dtype=torch.long)
        y = torch.tensor([0, 1, 0, 1], dtype=torch.long)
        train_mask = torch.tensor([True, True, True, True], dtype=torch.bool)
        self.data = Data(x=x, edge_index=edge_index, y=y, train_mask=train_mask)

    def test_gcn_search(self):
        search_method = GCNSearch(data=self.data, epochs=10, lr=0.01)
        query_features = torch.tensor([1.0, 2.0], dtype=torch.float)
        results = search_method.search(query_features, top_k=2)
        self.assertEqual(len(results), 2)
        self.assertTrue(all(isinstance(idx, int) for idx in results))

    def test_gat_search(self):
        search_method = GATSearch(data=self.data, epochs=10, lr=0.005)
        query_features = torch.tensor([3.0, 4.0], dtype=torch.float)
        results = search_method.search(query_features, top_k=2)
        self.assertEqual(len(results), 2)
        self.assertTrue(all(isinstance(idx, int) for idx in results))

    def test_sage_search(self):
        search_method = SAGESearch(data=self.data, epochs=10, lr=0.01)
        query_features = torch.tensor([5.0, 6.0], dtype=torch.float)
        results = search_method.search(query_features, top_k=2)
        self.assertEqual(len(results), 2)
        self.assertTrue(all(isinstance(idx, int) for idx in results))

    def test_get_search_method_factory(self):
        gcn = get_search_method('gcn', data=self.data, epochs=10, lr=0.01)
        gat = get_search_method('gat', data=self.data, epochs=10, lr=0.005)
        sage = get_search_method('sage', data=self.data, epochs=10, lr=0.01)

        self.assertIsInstance(gcn, GCNSearch)
        self.assertIsInstance(gat, GATSearch)
        self.assertIsInstance(sage, SAGESearch)

    def test_invalid_search_method(self):
        with self.assertRaises(ValueError):
            get_search_method('invalid_method', data=self.data)

if __name__ == '__main__':
    unittest.main()
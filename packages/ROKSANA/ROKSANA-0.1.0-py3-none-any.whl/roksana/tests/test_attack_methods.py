# tests/test_attack_methods.py

import unittest
import torch
from torch_geometric.data import Data
from roksana.attack_methods import (
    PredefinedAttack1,
    PredefinedAttack2,
    get_attack_method
)

class TestAttackMethods(unittest.TestCase):
    def setUp(self):
        # Create a simple graph for testing
        # 3 nodes with 2 features each
        x = torch.tensor([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]], dtype=torch.float)
        edge_index = torch.tensor([[0, 1, 2],
                                   [1, 2, 0]], dtype=torch.long)
        y = torch.tensor([0, 1, 0], dtype=torch.long)
        train_mask = torch.tensor([True, True, True], dtype=torch.bool)
        self.data = Data(x=x, edge_index=edge_index, y=y, train_mask=train_mask)

    def test_predefined_attack1(self):
        attack_method = PredefinedAttack1(data=self.data, perturbations=2)
        attack_details = attack_method.attack(query_node=1, perturbations=2)
        self.assertIn('added_edges', attack_details)
        self.assertIn('removed_edges', attack_details)
        self.assertIsInstance(attack_details['added_edges'], list)
        self.assertIsInstance(attack_details['removed_edges'], list)

    def test_predefined_attack2(self):
        attack_method = PredefinedAttack2(data=self.data, perturbations=1)
        attack_details = attack_method.attack(query_node=0, perturbations=1)
        self.assertIn('original_features', attack_details)
        self.assertIn('perturbed_features', attack_details)
        self.assertIsInstance(attack_details['perturbed_features'], list)
        self.assertEqual(len(attack_details['perturbed_features']), 1)

    def test_get_attack_method_factory(self):
        attack1 = get_attack_method('predefined_attack1', data=self.data, perturbations=2)
        attack2 = get_attack_method('predefined_attack2', data=self.data, perturbations=1)

        self.assertIsInstance(attack1, PredefinedAttack1)
        self.assertIsInstance(attack2, PredefinedAttack2)

    def test_invalid_attack_method(self):
        with self.assertRaises(ValueError):
            get_attack_method('invalid_attack', data=self.data)

    def test_attack_effect_on_edge_index(self):
        attack_method = PredefinedAttack1(data=self.data, perturbations=1)
        original_edge_index = self.data.edge_index.clone()
        attack_details = attack_method.attack(query_node=1, perturbations=1)
        # Check if edges are added or removed correctly
        self.assertTrue(len(self.data.edge_index) <= len(original_edge_index) + 1)
        # Further checks can be implemented based on attack_details

    def test_attack_effect_on_features(self):
        attack_method = PredefinedAttack2(data=self.data, perturbations=1)
        original_features = self.data.x.clone()
        attack_details = attack_method.attack(query_node=0, perturbations=1)
        # Check if the specified feature has been perturbed
        feature_idx, noise = attack_details['perturbed_features'][0]
        self.assertNotEqual(self.data.x[0, feature_idx].item(), original_features[0, feature_idx].item())
        self.assertAlmostEqual(
            self.data.x[0, feature_idx].item(),
            original_features[0, feature_idx].item() + noise,
            places=4
        )

if __name__ == '__main__':
    unittest.main()
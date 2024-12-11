import unittest
from roksana.datasets import UserDataset

class TestUserDataset(unittest.TestCase):
    def test_dataset_loading(self):
        dataset = UserDataset(root='tests/data/sample_dataset')
        self.assertIsNotNone(dataset)
        self.assertGreater(len(dataset), 0)

if __name__ == '__main__':
    unittest.main()
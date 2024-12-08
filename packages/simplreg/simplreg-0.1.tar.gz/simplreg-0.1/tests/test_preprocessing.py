import unittest
import pandas as pd
from simplreg.preprocessing import preprocess_data

class TestPreprocessing(unittest.TestCase):
    def setUp(self):
        # Sample data
        self.df = pd.DataFrame({
            'feature1': [1, 2, None],
            'feature2': [4, None, 6],
            'target': [0, 1, 0]
        })

    def test_preprocess_data(self):
        X_train, X_test, y_train, y_test = preprocess_data(self.df, 'target')
        self.assertEqual(X_train.shape[1], 2)  # Check number of features
        self.assertEqual(len(y_train), 2)      # Check train-test split

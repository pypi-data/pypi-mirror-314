import unittest
from sklearn.ensemble import RandomForestClassifier
from simplreg.model_training import train_model

class TestModelTraining(unittest.TestCase):
    def test_train_model_classification(self):
        X_train = [[1, 2], [3, 4], [5, 6]]
        y_train = [0, 1, 0]
        model = train_model(X_train, y_train, 'classification')
        self.assertIsInstance(model, RandomForestClassifier)

    def test_invalid_task_type(self):
        with self.assertRaises(ValueError):
            train_model([[1]], [1], 'invalid')

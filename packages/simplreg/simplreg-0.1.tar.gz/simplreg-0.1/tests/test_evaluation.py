import unittest
from sklearn.ensemble import RandomForestClassifier
from simplreg.evaluation import evaluate_model

class TestEvaluation(unittest.TestCase):
    def test_evaluate_model_classification(self):
        model = RandomForestClassifier()
        model.fit([[1, 2], [3, 4]], [0, 1])
        self.assertIsNone(evaluate_model(model, [[5, 6]], [0], 'classification'))

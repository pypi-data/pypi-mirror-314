import unittest
import numpy as np
import pandas as pd
from marketing_analytics.core.base import BaseModel
from marketing_analytics.core.exceptions import ModelNotFittedError, ValidationError

class DummyModel(BaseModel):
    def fit(self, X, y=None):
        self.is_fitted = True
        return self
        
    def predict(self, X):
        if not self.is_fitted:
            raise ModelNotFittedError()
        return np.ones(len(X))

class TestBaseModel(unittest.TestCase):
    def setUp(self):
        self.model = DummyModel()
        self.X = pd.DataFrame({'feature1': [1, 2, 3]})
        
    def test_not_fitted_error(self):
        """Test if model raises error when not fitted"""
        with self.assertRaises(ModelNotFittedError):
            self.model.predict(self.X)
            
    def test_fit_predict(self):
        """Test basic fit and predict functionality"""
        self.model.fit(self.X)
        predictions = self.model.predict(self.X)
        self.assertEqual(len(predictions), len(self.X))
        
    def test_validation_input_type(self):
        """Test input validation for correct types"""
        # DataFrame should work
        self.model.validate_input(self.X)
        
        # List should raise error
        with self.assertRaises(ValidationError):
            self.model.validate_input([1, 2, 3])
            
    def test_model_metadata(self):
        """Test model metadata handling"""
        self.assertIn('created_at', self.model.model_metadata)
        self.assertIn('version', self.model.model_metadata)
        
        # Test metadata update
        self.model.update_metadata('test_key', 'test_value')
        self.assertEqual(self.model.model_metadata['test_key'], 'test_value')
import unittest
import pandas as pd
import numpy as np
from marketing_analytics.utils import AdvancedPreprocessor

class TestPreprocessor(unittest.TestCase):
    def setUp(self):
        self.preprocessor = AdvancedPreprocessor()
        self.data = pd.DataFrame({
            'numeric': [1, 2, np.nan, 4],
            'categorical': ['A', 'B', None, 'A']
        })
        
    def test_init(self):
        """Test initialization"""
        self.assertEqual(self.preprocessor.scaling_method, 'robust')
        self.assertEqual(self.preprocessor.encoding_method, 'target')
        self.assertEqual(self.preprocessor.imputation_method, 'knn')
        
    def test_handle_missing_values_basic(self):
        """Test basic missing value handling"""
        result = self.preprocessor.handle_missing_values(
            self.data,
            categorical_features=['categorical']
        )
        # Eksik değer kalmamalı
        self.assertFalse(result.isnull().any().any())
        
    def test_handle_missing_values_numeric_only(self):
        """Test missing value handling for numeric data only"""
        numeric_data = pd.DataFrame({
            'A': [1, 2, np.nan],
            'B': [4, np.nan, 6]
        })
        result = self.preprocessor.handle_missing_values(numeric_data)
        self.assertFalse(result.isnull().any().any())
        
    def test_initialize_components(self):
        """Test component initialization"""
        self.preprocessor._initialize_components()
        self.assertIsNotNone(self.preprocessor.scaler)
        self.assertIsNotNone(self.preprocessor.encoder)
        self.assertIsNotNone(self.preprocessor.imputer) 
import unittest
import numpy as np
import pandas as pd
from marketing_analytics.models import AdvancedSegmentationModel

class TestSegmentation(unittest.TestCase):
    def setUp(self):
        """Test setup"""
        self.model = AdvancedSegmentationModel(
            method='kmeans',
            n_segments=3,
            random_state=42
        )
        # Test verisi oluştur
        np.random.seed(42)
        self.X = pd.DataFrame({
            'feature1': np.concatenate([
                np.random.normal(0, 1, 50),
                np.random.normal(5, 1, 50),
                np.random.normal(-5, 1, 50)
            ]),
            'feature2': np.concatenate([
                np.random.normal(0, 1, 50),
                np.random.normal(5, 1, 50),
                np.random.normal(-5, 1, 50)
            ])
        })
        
    def test_initialization(self):
        """Test model initialization"""
        self.assertEqual(self.model.n_segments, 3)
        self.assertEqual(self.model.method, 'kmeans')
        self.assertIsNotNone(self.model.scaler)
        self.assertIsNotNone(self.model.dim_reducer)
        
    def test_fit_predict(self):
        """Test fitting and prediction"""
        # Model eğitimi
        self.model.fit(self.X)
        self.assertTrue(self.model.is_fitted)
        
        # Tahmin
        segments = self.model.predict(self.X)
        self.assertEqual(len(segments), len(self.X))
        self.assertEqual(len(np.unique(segments)), 3)
        
    def test_analyze_segments(self):
        """Test segment analysis"""
        self.model.fit(self.X)
        segments = self.model.predict(self.X)
        analysis = self.model.analyze_segments(self.X, segments)
        
        # Analiz sonuçlarını kontrol et
        self.assertIn('segment_metrics', analysis)
        self.assertIn('segment_distribution', analysis)
        self.assertIn('feature_importance', analysis)
        
    def test_get_segment_recommendations(self):
        """Test segment recommendations"""
        self.model.fit(self.X)
        recommendations = self.model.get_segment_recommendations(0, self.X)
        
        # Önerileri kontrol et
        self.assertIn('targeting', recommendations)
        self.assertIn('marketing_mix', recommendations)
        self.assertIn('growth_potential', recommendations)

if __name__ == '__main__':
    unittest.main() 
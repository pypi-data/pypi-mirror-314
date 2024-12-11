from abc import ABC, abstractmethod
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, Union, List
import joblib
import json
from datetime import datetime
import logging
from ..core.exceptions import ModelNotFittedError, ValidationError
import warnings
import hashlib

class BaseModel(ABC):
    """
    Gelişmiş Temel Model Sınıfı
    
    Özellikler:
    - Model yaşam döngüsü yönetimi
    - Otomatik doğrulama
    - Model versiyonlama
    - Performans izleme
    - Hata yönetimi
    """
    
    def __init__(self):
        self.is_fitted = False
        self.model_params = {}
        self.model_metadata = {
            'created_at': datetime.now().isoformat(),
            'version': '1.0.0',
            'last_trained': None,
            'performance_metrics': {},
            'data_checksums': {}
        }
        self._setup_logging()
        
    def _setup_logging(self):
        """Loglama yapılandırması"""
        self.logger = logging.getLogger(self.__class__.__name__)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
        
    @abstractmethod
    def fit(self, X, y=None):
        """Model eğitimi için temel metod"""
        pass
    
    @abstractmethod
    def predict(self, X):
        """Tahmin için temel metod"""
        pass
    
    def validate_input(self, X: Union[pd.DataFrame, np.ndarray],
                      expected_columns: Optional[List[str]] = None,
                      strict: bool = True) -> None:
        """Gelişmiş girdi doğrulama"""
        try:
            # Veri tipi kontrolü
            if not isinstance(X, (pd.DataFrame, np.ndarray)):
                raise ValidationError("Input must be pandas DataFrame or numpy array")
            
            # DataFrame kontrolü
            if isinstance(X, pd.DataFrame):
                # Kolon kontrolü
                if expected_columns:
                    missing_cols = set(expected_columns) - set(X.columns)
                    if missing_cols:
                        raise ValidationError(f"Missing columns: {missing_cols}")
                
                # Veri kalitesi kontrolü
                null_cols = X.columns[X.isnull().any()].tolist()
                if null_cols and strict:
                    raise ValidationError(f"Null values found in columns: {null_cols}")
                elif null_cols:
                    warnings.warn(f"Null values found in columns: {null_cols}")
                    
                # Veri tipi kontrolü
                numeric_cols = X.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) == 0 and strict:
                    raise ValidationError("No numeric columns found")
                    
            # Numpy array kontrolü
            elif isinstance(X, np.ndarray):
                if X.size == 0:
                    raise ValidationError("Empty numpy array")
                if not np.isfinite(X).all():
                    raise ValidationError("Array contains infinite or NaN values")
                    
            # Veri bütünlüğü kontrolü
            self._update_data_checksum(X)
            
        except Exception as e:
            self.logger.error(f"Validation error: {str(e)}")
            raise
            
    def _update_data_checksum(self, X: Union[pd.DataFrame, np.ndarray]) -> None:
        """Veri bütünlüğü için checksum hesapla"""
        if isinstance(X, pd.DataFrame):
            data_str = X.to_json()
        else:
            data_str = X.tobytes()
            
        checksum = hashlib.md5(str(data_str).encode()).hexdigest()
        self.model_metadata['data_checksums'][datetime.now().isoformat()] = checksum
        
    def save_model(self, path: str, include_metadata: bool = True) -> None:
        """Model kaydetme"""
        if not self.is_fitted:
            raise ModelNotFittedError("Cannot save unfitted model")
            
        model_data = {
            'model': self,
            'params': self.model_params,
            'metadata': self.model_metadata if include_metadata else None
        }
        
        try:
            joblib.dump(model_data, path)
            self.logger.info(f"Model saved successfully to {path}")
        except Exception as e:
            self.logger.error(f"Error saving model: {str(e)}")
            raise
            
    @classmethod
    def load_model(cls, path: str) -> 'BaseModel':
        """Model yükleme"""
        try:
            model_data = joblib.load(path)
            model = model_data['model']
            model.model_params = model_data['params']
            if model_data['metadata']:
                model.model_metadata = model_data['metadata']
            return model
        except Exception as e:
            logging.error(f"Error loading model: {str(e)}")
            raise
            
    def update_metadata(self, key: str, value: Any) -> None:
        """Metadata güncelleme"""
        self.model_metadata[key] = value
        self.logger.debug(f"Updated metadata: {key}={value}")
        
    def get_model_info(self) -> Dict[str, Any]:
        """Model bilgilerini getir"""
        return {
            'model_type': self.__class__.__name__,
            'is_fitted': self.is_fitted,
            'parameters': self.model_params,
            'metadata': self.model_metadata
        }
        
    def validate_performance(self, y_true: np.ndarray,
                           y_pred: np.ndarray,
                           threshold: float = 0.7) -> bool:
        """Model performans doğrulama"""
        from sklearn.metrics import r2_score, accuracy_score
        
        try:
            if y_true.dtype == y_pred.dtype == np.bool:
                score = accuracy_score(y_true, y_pred)
            else:
                score = r2_score(y_true, y_pred)
                
            self.model_metadata['performance_metrics']['latest_score'] = score
            return score >= threshold
            
        except Exception as e:
            self.logger.error(f"Performance validation error: {str(e)}")
            return False
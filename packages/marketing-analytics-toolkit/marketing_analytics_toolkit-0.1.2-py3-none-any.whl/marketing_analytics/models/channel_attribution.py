from ..core.base import BaseModel
import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Union, Tuple
from sklearn.ensemble import RandomForestClassifier
import networkx as nx
from scipy.optimize import minimize
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
import shap

class AdvancedAttributionModel(BaseModel):
    """
    Gelişmiş Kanal Atribüsyon Modeli
    
    Özellikler:
    - Markov Chain Attribution
    - Shapley Value Attribution
    - Data-driven Attribution (ML based)
    - Time-decay Attribution
    - Position-based Attribution
    """
    
    def __init__(self, 
                 method: str = 'markov',
                 decay_factor: float = 0.7,
                 n_simulations: int = 10000,
                 random_state: int = 42):
        super().__init__()
        self.method = method
        self.decay_factor = decay_factor
        self.n_simulations = n_simulations
        self.random_state = random_state
        self.channel_encoder = LabelEncoder()
        self.transition_matrix = None
        self.removal_effects = None
        self.channel_importance = None
        self._initialize_model()
        
    def _initialize_model(self):
        """Model bileşenlerini başlat"""
        if self.method == 'ml':
            self.ml_model = RandomForestClassifier(
                n_estimators=100,
                random_state=self.random_state
            )
            
        elif self.method == 'deep':
            self.deep_model = self._build_deep_model()
            
    def _build_deep_model(self) -> tf.keras.Model:
        """Deep learning modeli oluştur"""
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.Dense(1, activation='sigmoid')
        ])
        
        model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy', tf.keras.metrics.AUC()]
        )
        
        return model
        
    def _create_transition_matrix(self, 
                                paths: List[List[str]]) -> np.ndarray:
        """Markov geçiş matrisi oluştur"""
        unique_channels = np.unique([channel for path in paths for channel in path])
        n_channels = len(unique_channels)
        
        # Geçiş matrisi başlat
        transitions = np.zeros((n_channels + 2, n_channels + 2))  # +2 for start/end states
        
        for path in paths:
            # Start state transitions
            start_idx = np.where(unique_channels == path[0])[0][0]
            transitions[0, start_idx + 1] += 1
            
            # Channel transitions
            for i in range(len(path)-1):
                current_idx = np.where(unique_channels == path[i])[0][0]
                next_idx = np.where(unique_channels == path[i+1])[0][0]
                transitions[current_idx + 1, next_idx + 1] += 1
            
            # End state transitions
            last_idx = np.where(unique_channels == path[-1])[0][0]
            transitions[last_idx + 1, -1] += 1
            
        # Normalize
        row_sums = transitions.sum(axis=1)
        row_sums[row_sums == 0] = 1  # Avoid division by zero
        transitions = transitions / row_sums[:, np.newaxis]
        
        return transitions
        
    def _calculate_removal_effect(self,
                                base_conversion_rate: float,
                                channel: str,
                                paths: List[List[str]]) -> float:
        """Kanal kaldırma etkisini hesapla"""
        # Kanalı kaldırılmış yollar oluştur
        removed_paths = [
            [c for c in path if c != channel]
            for path in paths
        ]
        
        # Yeni geçiş matrisi
        new_transitions = self._create_transition_matrix(removed_paths)
        
        # Yeni dönüşüm oranı
        new_conversion_rate = self._simulate_conversions(new_transitions)
        
        return (base_conversion_rate - new_conversion_rate) / base_conversion_rate
        
    def _simulate_conversions(self, 
                            transition_matrix: np.ndarray,
                            n_simulations: int = None) -> float:
        """Monte Carlo simülasyonu ile dönüşüm oranı hesapla"""
        if n_simulations is None:
            n_simulations = self.n_simulations
            
        conversions = 0
        
        for _ in range(n_simulations):
            current_state = 0  # Start state
            while current_state != transition_matrix.shape[0] - 1:  # Until end state
                current_state = np.random.choice(
                    len(transition_matrix),
                    p=transition_matrix[current_state]
                )
                if current_state == transition_matrix.shape[0] - 1:
                    conversions += 1
                    
        return conversions / n_simulations
        
    def _calculate_shapley_values(self,
                                paths: List[List[str]],
                                conversions: List[int]) -> Dict[str, float]:
        """Shapley değerlerini hesapla"""
        unique_channels = np.unique([channel for path in paths for channel in path])
        n_channels = len(unique_channels)
        
        shapley_values = {}
        
        for channel in unique_channels:
            value = 0
            for path, conv in zip(paths, conversions):
                if channel in path:
                    # Kanalın pozisyon etkisi
                    position = path.index(channel)
                    
                    # Önceki ve sonraki kanalların etkisi
                    prev_channels = path[:position]
                    next_channels = path[position+1:]
                    
                    # Shapley değeri hesapla
                    marginal_contribution = conv / (len(path) * (1 + np.exp(-position)))
                    value += marginal_contribution
                    
            shapley_values[channel] = value
            
        # Normalize
        total = sum(shapley_values.values())
        return {k: v/total for k, v in shapley_values.items()}
        
    def fit(self,
           paths: List[List[str]],
           conversions: List[int],
           features: Optional[pd.DataFrame] = None) -> 'AdvancedAttributionModel':
        """
        Atribüsyon modelini eğit
        
        Parameters:
        -----------
        paths: Müşteri yolculukları
        conversions: Dönüşüm değerleri
        features: Ek özellikler (ML/Deep modeller için)
        
        Returns:
        --------
        self
        """
        if self.method == 'markov':
            # Markov Chain attribution
            self.transition_matrix = self._create_transition_matrix(paths)
            base_conversion_rate = self._simulate_conversions(self.transition_matrix)
            
            # Removal effects
            unique_channels = np.unique([channel for path in paths for channel in path])
            self.removal_effects = {
                channel: self._calculate_removal_effect(base_conversion_rate, channel, paths)
                for channel in unique_channels
            }
            
            # Normalize removal effects
            total_effect = sum(self.removal_effects.values())
            self.channel_importance = {
                k: v/total_effect for k, v in self.removal_effects.items()
            }
            
        elif self.method == 'shapley':
            # Shapley value attribution
            self.channel_importance = self._calculate_shapley_values(paths, conversions)
            
        elif self.method in ['ml', 'deep']:
            if features is None:
                raise ValueError("Features required for ML/Deep attribution methods")
                
            # Prepare features
            X = features.copy()
            y = np.array(conversions)
            
            if self.method == 'ml':
                self.ml_model.fit(X, y)
                # SHAP değerleri ile kanal önem skorları
                explainer = shap.TreeExplainer(self.ml_model)
                shap_values = explainer.shap_values(X)
                
                self.channel_importance = {
                    col: np.abs(shap_values[:, i]).mean()
                    for i, col in enumerate(X.columns)
                }
                
            else:  # deep
                self.deep_model.fit(
                    X, y,
                    epochs=50,
                    batch_size=32,
                    validation_split=0.2,
                    verbose=0
                )
                
                # Integrated Gradients ile kanal önem skorları
                ig = tf.keras.metrics.IntegratedGradients(self.deep_model)
                attributions = ig(X, y)
                
                self.channel_importance = {
                    col: np.abs(attributions[:, i]).mean()
                    for i, col in enumerate(X.columns)
                }
                
        self.is_fitted = True
        return self
        
    def predict_channel_importance(self,
                                 path: List[str],
                                 features: Optional[pd.DataFrame] = None) -> Dict[str, float]:
        """
        Belirli bir yolculuk için kanal önem skorlarını tahmin et
        
        Parameters:
        -----------
        path: Müşteri yolculuğu
        features: Ek özellikler (ML/Deep modeller için)
        
        Returns:
        --------
        Dict[str, float]: Kanal önem skorları
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted first")
            
        if self.method == 'markov':
            # Time-decay faktörünü uygula
            importance = {}
            path_length = len(path)
            
            for i, channel in enumerate(path):
                position_weight = self.decay_factor ** (path_length - i - 1)
                channel_weight = self.channel_importance.get(channel, 0)
                importance[channel] = channel_weight * position_weight
                
        elif self.method == 'shapley':
            importance = {
                channel: self.channel_importance.get(channel, 0)
                for channel in path
            }
            
        else:  # ml/deep
            if features is None:
                raise ValueError("Features required for ML/Deep attribution methods")
                
            if self.method == 'ml':
                importance = {
                    col: np.abs(self.ml_model.feature_importances_[i])
                    for i, col in enumerate(features.columns)
                }
            else:
                # Deep model için gradient-based attribution
                with tf.GradientTape() as tape:
                    predictions = self.deep_model(features)
                gradients = tape.gradient(predictions, features)
                importance = {
                    col: np.abs(gradients[:, i].numpy()).mean()
                    for i, col in enumerate(features.columns)
                }
                
        # Normalize
        total = sum(importance.values())
        return {k: v/total for k, v in importance.items()}
        
    def get_conversion_probability(self,
                                 path: List[str],
                                 features: Optional[pd.DataFrame] = None) -> float:
        """
        Belirli bir yolculuk için dönüşüm olasılığını tahmin et
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted first")
            
        if self.method == 'markov':
            current_state = 0
            prob = 1.0
            
            for channel in path:
                channel_idx = np.where(self.channel_encoder.classes_ == channel)[0][0] + 1
                prob *= self.transition_matrix[current_state, channel_idx]
                current_state = channel_idx
                
            prob *= self.transition_matrix[current_state, -1]
            return prob
            
        elif self.method in ['ml', 'deep']:
            if features is None:
                raise ValueError("Features required for ML/Deep methods")
                
            if self.method == 'ml':
                return self.ml_model.predict_proba(features)[:, 1]
            else:
                return self.deep_model.predict(features).flatten()
                
        else:
            raise ValueError(f"Conversion probability not supported for {self.method}")
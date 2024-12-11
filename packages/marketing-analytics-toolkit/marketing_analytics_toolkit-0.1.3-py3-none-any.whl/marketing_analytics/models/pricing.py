from ..core.base import BaseModel
import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Union, Tuple
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
import optuna
from scipy.optimize import minimize, differential_evolution
from scipy.stats import norm
import statsmodels.api as sm
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel
import shap

class AdvancedPricingModel(BaseModel):
    """
    Gelişmiş Dinamik Fiyatlandırma Modeli
    
    Özellikler:
    - Dinamik fiyatlandırma
    - Elastisite analizi
    - Rekabet bazlı fiyatlandırma
    - Optimal fiyat noktası tahmini
    - Fiyat segmentasyonu
    """
    
    def __init__(self,
                 method: str = 'ml',
                 price_bounds: Optional[Tuple[float, float]] = None,
                 elasticity_window: int = 30,
                 random_state: int = 42):
        super().__init__()
        self.method = method
        self.price_bounds = price_bounds
        self.elasticity_window = elasticity_window
        self.random_state = random_state
        
        # Model bileşenleri
        self.demand_model = None
        self.elasticity_model = None
        self.competition_model = None
        self.deep_model = None
        self.gp_model = None
        self.scaler = StandardScaler()
        
        self._initialize_models()
        
    def _initialize_models(self):
        """Model bileşenlerini başlat"""
        if self.method == 'ml':
            self.demand_model = GradientBoostingRegressor(
                n_estimators=100,
                random_state=self.random_state
            )
            self.elasticity_model = RandomForestRegressor(
                n_estimators=100,
                random_state=self.random_state
            )
            
        elif self.method == 'deep':
            self.deep_model = self._build_deep_model()
            
        elif self.method == 'bayesian':
            kernel = ConstantKernel(1.0) * RBF([1.0])
            self.gp_model = GaussianProcessRegressor(
                kernel=kernel,
                random_state=self.random_state
            )
            
    def _build_deep_model(self) -> tf.keras.Model:
        """Deep learning modeli oluştur"""
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.Dense(16, activation='relu'),
            tf.keras.layers.Dense(1)
        ])
        
        model.compile(
            optimizer='adam',
            loss='mse',
            metrics=['mae']
        )
        
        return model
        
    def _calculate_price_elasticity(self,
                                  prices: np.ndarray,
                                  demand: np.ndarray,
                                  window: Optional[int] = None) -> np.ndarray:
        """Fiyat esnekliği hesapla"""
        if window is None:
            window = self.elasticity_window
            
        elasticities = []
        for i in range(len(prices) - window):
            price_change = (prices[i + window] - prices[i]) / prices[i]
            demand_change = (demand[i + window] - demand[i]) / demand[i]
            
            if price_change != 0:
                elasticity = demand_change / price_change
            else:
                elasticity = 0
                
            elasticities.append(elasticity)
            
        return np.array(elasticities)
        
    def _optimize_price_point(self,
                            features: np.ndarray,
                            constraints: Optional[Dict] = None) -> Dict:
        """Optimal fiyat noktası bul"""
        def objective(price):
            features_with_price = np.append(features, price)
            demand = self.predict_demand(features_with_price.reshape(1, -1))[0]
            revenue = price * demand
            return -revenue  # Minimize negative revenue
            
        if self.price_bounds is None:
            raise ValueError("Price bounds must be set")
            
        if constraints is None:
            constraints = []
            
        result = minimize(
            objective,
            x0=np.mean(self.price_bounds),
            bounds=[self.price_bounds],
            constraints=constraints,
            method='SLSQP'
        )
        
        return {
            'optimal_price': result.x[0],
            'expected_revenue': -result.fun,
            'success': result.success
        }
        
    def _segment_prices(self,
                       features: pd.DataFrame,
                       n_segments: int = 3) -> Dict[str, List[float]]:
        """Fiyat segmentasyonu"""
        if not self.is_fitted:
            raise ValueError("Model must be fitted first")
            
        # Fiyat tahminleri
        predictions = self.predict_optimal_price(features)
        
        # Segmentlere ayır
        segments = pd.qcut(predictions, q=n_segments, labels=['Low', 'Medium', 'High'])
        
        return {
            segment: predictions[segments == segment].tolist()
            for segment in segments.unique()
        }
        
    def fit(self,
            X: pd.DataFrame,
            y: pd.Series,
            competition_data: Optional[pd.DataFrame] = None) -> 'AdvancedPricingModel':
        """
        Model eğitimi
        
        Parameters:
        -----------
        X: Özellik matrisi
        y: Hedef değişken (fiyat/talep)
        competition_data: Rekabet verileri
        """
        X_scaled = self.scaler.fit_transform(X)
        
        if self.method == 'ml':
            # Talep modeli eğitimi
            self.demand_model.fit(X_scaled, y)
            
            # Elastisite modeli eğitimi
            elasticities = self._calculate_price_elasticity(
                X['price'].values,
                y.values
            )
            self.elasticity_model.fit(
                X_scaled[:-self.elasticity_window],
                elasticities
            )
            
        elif self.method == 'deep':
            self.deep_model.fit(
                X_scaled, y,
                epochs=50,
                batch_size=32,
                validation_split=0.2,
                verbose=0
            )
            
        elif self.method == 'bayesian':
            self.gp_model.fit(X_scaled, y)
            
        # Rekabet modeli eğitimi
        if competition_data is not None:
            self.competition_model = GradientBoostingRegressor(
                n_estimators=100,
                random_state=self.random_state
            )
            self.competition_model.fit(
                competition_data.drop('price', axis=1),
                competition_data['price']
            )
            
        self.is_fitted = True
        return self
        
    def predict_demand(self,
                      features: np.ndarray,
                      return_std: bool = False) -> Union[np.ndarray, Tuple[np.ndarray, np.ndarray]]:
        """Talep tahmini"""
        if not self.is_fitted:
            raise ValueError("Model must be fitted first")
            
        features_scaled = self.scaler.transform(features)
        
        if self.method == 'ml':
            predictions = self.demand_model.predict(features_scaled)
            if return_std:
                # Bootstrap ile standart sapma hesapla
                preds = []
                for _ in range(100):
                    idx = np.random.choice(len(features), len(features))
                    preds.append(self.demand_model.predict(features_scaled[idx]))
                return predictions, np.std(preds, axis=0)
            return predictions
            
        elif self.method == 'deep':
            return self.deep_model.predict(features_scaled)
            
        else:  # bayesian
            return self.gp_model.predict(features_scaled, return_std=return_std)
            
    def predict_optimal_price(self,
                            features: pd.DataFrame,
                            competition_features: Optional[pd.DataFrame] = None) -> np.ndarray:
        """Optimal fiyat tahmini"""
        if not self.is_fitted:
            raise ValueError("Model must be fitted first")
            
        optimal_prices = []
        
        for i in range(len(features)):
            constraints = []
            
            # Rekabet bazlı kısıtlar
            if competition_features is not None and self.competition_model is not None:
                comp_price = self.competition_model.predict(
                    competition_features.iloc[i].values.reshape(1, -1)
                )[0]
                constraints.append({
                    'type': 'ineq',
                    'fun': lambda x: x - comp_price * 0.8  # Min %20 düşük
                })
                constraints.append({
                    'type': 'ineq',
                    'fun': lambda x: comp_price * 1.2 - x  # Max %20 yüksek
                })
                
            result = self._optimize_price_point(
                features.iloc[i].values,
                constraints
            )
            optimal_prices.append(result['optimal_price'])
            
        return np.array(optimal_prices)
        
    def get_price_insights(self,
                          features: pd.DataFrame,
                          actual_prices: Optional[np.ndarray] = None) -> Dict:
        """Fiyatlandırma içgörüleri"""
        insights = {}
        
        # Optimal fiyat tahminleri
        optimal_prices = self.predict_optimal_price(features)
        insights['optimal_prices'] = optimal_prices
        
        # Fiyat segmentasyonu
        insights['price_segments'] = self._segment_prices(features)
        
        # Elastisite analizi
        if self.method == 'ml':
            elasticities = self.elasticity_model.predict(
                self.scaler.transform(features[:-self.elasticity_window])
            )
            insights['elasticities'] = {
                'mean': np.mean(elasticities),
                'std': np.std(elasticities),
                'percentiles': np.percentile(elasticities, [25, 50, 75])
            }
            
        # SHAP değerleri
        if self.method == 'ml':
            explainer = shap.TreeExplainer(self.demand_model)
            shap_values = explainer.shap_values(self.scaler.transform(features))
            
            insights['feature_importance'] = {
                'shap_values': shap_values,
                'mean_importance': np.abs(shap_values).mean(0)
            }
            
        # Fiyat optimizasyon potansiyeli
        if actual_prices is not None:
            potential_revenue = optimal_prices * self.predict_demand(features)
            actual_revenue = actual_prices * self.predict_demand(features)
            
            insights['optimization_potential'] = {
                'revenue_increase': (potential_revenue.sum() - actual_revenue.sum()) / actual_revenue.sum() * 100,
                'price_differences': optimal_prices - actual_prices
            }
            
        return insights
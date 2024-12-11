from ..core.base import BaseModel
import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Union, Tuple
from sklearn.preprocessing import StandardScaler, LabelEncoder
import tensorflow as tf
from lifelines import CoxPHFitter, KaplanMeierFitter, WeibullAFTFitter
from sklearn.ensemble import GradientBoostingRegressor, RandomForestClassifier
import shap
from scipy.stats import gamma, weibull_min
import optuna
from sklearn.metrics import roc_auc_score, precision_recall_curve

class AdvancedCustomerLifecycleModel(BaseModel):
    """
    Gelişmiş Müşteri Yaşam Döngüsü Modeli
    
    Özellikler:
    - RNN tabanlı davranış modellemesi
    - Survival analizi
    - CLV tahmini
    - Churn tahmini
    - Müşteri segmentasyonu
    """
    
    def __init__(self,
                 method: str = 'deep',
                 sequence_length: int = 10,
                 n_states: int = 5,
                 random_state: int = 42):
        super().__init__()
        self.method = method
        self.sequence_length = sequence_length
        self.n_states = n_states
        self.random_state = random_state
        
        # Model bileşenleri
        self.rnn_model = None
        self.survival_model = None
        self.clv_model = None
        self.churn_model = None
        self.encoder = LabelEncoder()
        self.scaler = StandardScaler()
        
        self._initialize_models()
        
    def _initialize_models(self):
        """Model bileşenlerini başlat"""
        if self.method == 'deep':
            self.rnn_model = self._build_rnn_model()
            
        # Survival modelleri
        self.survival_model = CoxPHFitter()
        self.parametric_survival = WeibullAFTFitter()
        
        # CLV modeli
        self.clv_model = GradientBoostingRegressor(
            n_estimators=100,
            random_state=self.random_state
        )
        
        # Churn modeli
        self.churn_model = RandomForestClassifier(
            n_estimators=100,
            random_state=self.random_state
        )
        
    def _build_rnn_model(self) -> tf.keras.Model:
        """RNN modeli oluştur"""
        model = tf.keras.Sequential([
            tf.keras.layers.LSTM(128, return_sequences=True,
                               input_shape=(self.sequence_length, self.n_states)),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.LSTM(64),
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.Dense(self.n_states, activation='softmax')
        ])
        
        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model
        
    def _prepare_sequence_data(self,
                             data: pd.DataFrame,
                             time_col: str,
                             event_col: str) -> Tuple[np.ndarray, np.ndarray]:
        """Sekans verisi hazırla"""
        # Olayları sırala ve kodla
        events = data.sort_values(time_col).groupby('customer_id')[event_col].apply(list)
        
        # Sekansları oluştur
        X = np.zeros((len(events), self.sequence_length, self.n_states))
        y = np.zeros((len(events), self.n_states))
        
        for i, sequence in enumerate(events):
            for t, event in enumerate(sequence[-self.sequence_length:]):
                X[i, t, self.encoder.transform([event])[0]] = 1
            if len(sequence) > self.sequence_length:
                y[i, self.encoder.transform([sequence[-1]])[0]] = 1
                
        return X, y
        
    def _calculate_survival_curves(self,
                                 data: pd.DataFrame,
                                 duration_col: str,
                                 event_col: str) -> Dict[str, np.ndarray]:
        """Survival eğrilerini hesapla"""
        kmf = KaplanMeierFitter()
        kmf.fit(data[duration_col], data[event_col])
        
        # Parametrik survival fit
        self.parametric_survival.fit(data, duration_col=duration_col, event_col=event_col)
        
        return {
            'survival_curve': kmf.survival_function_,
            'hazard_curve': kmf.hazard_,
            'cumulative_hazard': kmf.cumulative_hazard_
        }
        
    def _optimize_hyperparameters(self,
                                X: pd.DataFrame,
                                y: pd.Series,
                                model_type: str) -> Dict:
        """Hyperparameter optimizasyonu"""
        def objective(trial):
            if model_type == 'clv':
                params = {
                    'n_estimators': trial.suggest_int('n_estimators', 50, 300),
                    'max_depth': trial.suggest_int('max_depth', 3, 10),
                    'learning_rate': trial.suggest_loguniform('learning_rate', 1e-3, 1e-1)
                }
                model = GradientBoostingRegressor(**params)
            else:  # churn
                params = {
                    'n_estimators': trial.suggest_int('n_estimators', 50, 300),
                    'max_depth': trial.suggest_int('max_depth', 3, 10),
                    'min_samples_split': trial.suggest_int('min_samples_split', 2, 10)
                }
                model = RandomForestClassifier(**params)
                
            model.fit(X, y)
            return -model.score(X, y)  # Minimize negative score
            
        study = optuna.create_study()
        study.optimize(objective, n_trials=50)
        
        return study.best_params
        
    def fit(self,
            data: pd.DataFrame,
            sequence_data: Optional[pd.DataFrame] = None,
            survival_data: Optional[pd.DataFrame] = None,
            clv_features: Optional[pd.DataFrame] = None,
            churn_features: Optional[pd.DataFrame] = None) -> 'AdvancedCustomerLifecycleModel':
        """
        Model eğitimi
        
        Parameters:
        -----------
        data: Ana veri seti
        sequence_data: Sekans verileri (event data)
        survival_data: Survival analizi verileri
        clv_features: CLV tahmini için özellikler
        churn_features: Churn tahmini için özellikler
        """
        if self.method == 'deep' and sequence_data is not None:
            # RNN modeli eğitimi
            X_seq, y_seq = self._prepare_sequence_data(
                sequence_data,
                time_col='timestamp',
                event_col='event_type'
            )
            
            self.rnn_model.fit(
                X_seq, y_seq,
                epochs=50,
                batch_size=32,
                validation_split=0.2
            )
            
        if survival_data is not None:
            # Survival modeli eğitimi
            self.survival_curves = self._calculate_survival_curves(
                survival_data,
                duration_col='tenure',
                event_col='churn'
            )
            
            self.survival_model.fit(
                survival_data,
                duration_col='tenure',
                event_col='churn'
            )
            
        if clv_features is not None:
            # CLV modeli eğitimi
            best_params = self._optimize_hyperparameters(
                clv_features,
                data['customer_value'],
                model_type='clv'
            )
            self.clv_model.set_params(**best_params)
            self.clv_model.fit(clv_features, data['customer_value'])
            
        if churn_features is not None:
            # Churn modeli eğitimi
            best_params = self._optimize_hyperparameters(
                churn_features,
                data['churn'],
                model_type='churn'
            )
            self.churn_model.set_params(**best_params)
            self.churn_model.fit(churn_features, data['churn'])
            
        self.is_fitted = True
        return self
        
    def predict_next_events(self,
                          sequence: List[str],
                          n_steps: int = 1) -> List[str]:
        """Sonraki olayları tahmin et"""
        if not self.is_fitted or self.method != 'deep':
            raise ValueError("RNN model must be fitted first")
            
        # Sekansı hazırla
        X = np.zeros((1, self.sequence_length, self.n_states))
        for t, event in enumerate(sequence[-self.sequence_length:]):
            X[0, t, self.encoder.transform([event])[0]] = 1
            
        # Tahminler
        predictions = []
        for _ in range(n_steps):
            pred = self.rnn_model.predict(X)
            next_event = self.encoder.inverse_transform([pred.argmax()])[0]
            predictions.append(next_event)
            
            # Sekansı güncelle
            X = np.roll(X, -1, axis=1)
            X[0, -1] = 0
            X[0, -1, pred.argmax()] = 1
            
        return predictions
        
    def predict_survival_probability(self,
                                   features: pd.DataFrame,
                                   time_horizons: List[int]) -> pd.DataFrame:
        """Survival olasılıklarını tahmin et"""
        if not self.is_fitted:
            raise ValueError("Survival model must be fitted first")
            
        survival_curves = self.survival_model.predict_survival_function(features)
        
        return pd.DataFrame(
            {f't_{t}': survival_curves.loc[t] for t in time_horizons},
            index=features.index
        )
        
    def predict_clv(self,
                   features: pd.DataFrame,
                   return_confidence: bool = False) -> Union[np.ndarray, Tuple[np.ndarray, np.ndarray]]:
        """CLV tahmini"""
        if not self.is_fitted:
            raise ValueError("CLV model must be fitted first")
            
        predictions = self.clv_model.predict(features)
        
        if return_confidence:
            # SHAP değerleri ile güven aralığı
            explainer = shap.TreeExplainer(self.clv_model)
            shap_values = explainer.shap_values(features)
            confidence = np.std(shap_values, axis=0)
            return predictions, confidence
            
        return predictions
        
    def predict_churn_probability(self,
                                features: pd.DataFrame,
                                threshold: float = 0.5) -> Tuple[np.ndarray, np.ndarray]:
        """Churn olasılığı tahmini"""
        if not self.is_fitted:
            raise ValueError("Churn model must be fitted first")
            
        probabilities = self.churn_model.predict_proba(features)[:, 1]
        predictions = (probabilities >= threshold).astype(int)
        
        return predictions, probabilities
        
    def get_customer_insights(self,
                            customer_data: pd.DataFrame) -> Dict[str, Dict]:
        """Müşteri içgörüleri"""
        insights = {}
        
        # Survival analizi
        if self.survival_model is not None:
            survival_prob = self.predict_survival_probability(
                customer_data,
                time_horizons=[30, 60, 90, 180, 360]
            )
            insights['survival'] = {
                'survival_probabilities': survival_prob,
                'median_lifetime': self.survival_model.predict_median(customer_data)
            }
            
        # CLV tahmini
        if self.clv_model is not None:
            clv_pred, clv_conf = self.predict_clv(customer_data, return_confidence=True)
            insights['clv'] = {
                'predicted_value': clv_pred,
                'confidence_interval': clv_conf
            }
            
        # Churn riski
        if self.churn_model is not None:
            _, churn_prob = self.predict_churn_probability(customer_data)
            insights['churn'] = {
                'churn_probability': churn_prob,
                'risk_level': pd.qcut(churn_prob, q=3, labels=['Low', 'Medium', 'High'])
            }
            
        # Davranış analizi
        if self.method == 'deep' and self.rnn_model is not None:
            next_events = self.predict_next_events(
                customer_data['event_sequence'].iloc[0],
                n_steps=3
            )
            insights['behavior'] = {
                'predicted_next_events': next_events,
                'event_probabilities': self.rnn_model.predict(
                    self._prepare_sequence_data(
                        customer_data,
                        'timestamp',
                        'event_type'
                    )[0]
                )
            }
            
        return insights
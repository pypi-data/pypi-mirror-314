import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.impute import KNNImputer
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from category_encoders import TargetEncoder, WOEEncoder
from feature_engine.outliers import OutlierTrimmer
from feature_engine.selection import SmartCorrelatedSelection
from imblearn.over_sampling import SMOTENC
from typing import Union, List, Optional, Dict
import shap
import optuna

class AdvancedPreprocessor:
    """Gelişmiş veri ön işleme sınıfı"""
    
    def __init__(self, scaling_method: str = 'robust',
                 encoding_method: str = 'target',
                 imputation_method: str = 'knn'):
        self.scaling_method = scaling_method
        self.encoding_method = encoding_method
        self.imputation_method = imputation_method
        self._initialize_components()
        
    def _initialize_components(self):
        """Bileşenleri başlat"""
        # Scaler seçimi
        scalers = {
            'standard': StandardScaler(),
            'minmax': MinMaxScaler(),
            'robust': RobustScaler()
        }
        self.scaler = scalers.get(self.scaling_method, RobustScaler())
        
        # Encoder seçimi
        encoders = {
            'target': TargetEncoder(),
            'woe': WOEEncoder()
        }
        self.encoder = encoders.get(self.encoding_method, TargetEncoder())
        
        # Imputer seçimi
        imputers = {
            'knn': KNNImputer(),
            'iterative': IterativeImputer()
        }
        self.imputer = imputers.get(self.imputation_method, KNNImputer())
        
        # Diğer bileşenler
        self.outlier_detector = OutlierTrimmer(capping_method='iqr')
        self.correlation_selector = SmartCorrelatedSelection()
        self.feature_selector = None  # SHAP bazlı seçici
        
    def handle_missing_values(self, data: pd.DataFrame,
                            categorical_features: List[str] = None) -> pd.DataFrame:
        """Gelişmiş eksik değer doldurma"""
        df = data.copy()
        
        # Kategorik değişkenler için mod ile doldurma
        if categorical_features is None:
            categorical_features = []  # Boş liste olarak başlat
        
        for col in categorical_features:
            df[col] = df[col].fillna(df[col].mode()[0])
        
        # Sayısal değişkenler için gelişmiş imputation
        numeric_features = df.select_dtypes(include=[np.number]).columns
        numeric_features = [col for col in numeric_features if col not in categorical_features]
        
        if len(numeric_features) > 0:
            df[numeric_features] = self.imputer.fit_transform(df[numeric_features])
            
        return df
    
    def handle_outliers(self, data: pd.DataFrame,
                       columns: List[str] = None) -> pd.DataFrame:
        """Aykırı değer işleme"""
        if columns is None:
            columns = data.select_dtypes(include=[np.number]).columns
            
        self.outlier_detector.fit(data[columns])
        return self.outlier_detector.transform(data)
    
    def encode_categories(self, data: pd.DataFrame,
                         categorical_features: List[str],
                         target: pd.Series = None) -> pd.DataFrame:
        """Gelişmiş kategorik değişken kodlama"""
        df = data.copy()
        
        if self.encoding_method == 'target' and target is None:
            raise ValueError("Target encoding requires target variable")
            
        if target is not None:
            self.encoder.fit(df[categorical_features], target)
        else:
            self.encoder.fit(df[categorical_features])
            
        encoded_features = self.encoder.transform(df[categorical_features])
        df[categorical_features] = encoded_features
        
        return df
    
    def select_features(self, data: pd.DataFrame,
                       target: pd.Series,
                       n_features: int = None,
                       method: str = 'shap') -> pd.DataFrame:
        """Özellik seçimi"""
        if method == 'shap':
            # SHAP değerleri ile özellik seçimi
            model = xgboost.XGBRegressor()
            model.fit(data, target)
            
            explainer = shap.TreeExplainer(model)
            shap_values = explainer.shap_values(data)
            
            feature_importance = np.abs(shap_values).mean(0)
            important_features = pd.DataFrame(
                feature_importance,
                index=data.columns,
                columns=['importance']
            ).sort_values('importance', ascending=False)
            
            if n_features:
                selected_features = important_features.head(n_features).index
                return data[selected_features]
            
            return data[important_features.index]
        
        elif method == 'correlation':
            # Korelasyon bazlı seçim
            self.correlation_selector.fit(data)
            return self.correlation_selector.transform(data)
    
    def balance_dataset(self, X: pd.DataFrame,
                       y: pd.Series,
                       categorical_features: List[str]) -> tuple:
        """Veri seti dengeleme"""
        smote = SMOTENC(categorical_features=categorical_features)
        X_resampled, y_resampled = smote.fit_resample(X, y)
        return X_resampled, y_resampled
    
    def optimize_preprocessing(self, X: pd.DataFrame,
                             y: pd.Series,
                             model,
                             n_trials: int = 100) -> Dict:
        """Hyperparameter optimizasyonu"""
        def objective(trial):
            # Preprocessing parametreleri
            scaling_method = trial.suggest_categorical('scaling_method',
                                                     ['standard', 'minmax', 'robust'])
            encoding_method = trial.suggest_categorical('encoding_method',
                                                      ['target', 'woe'])
            imputation_method = trial.suggest_categorical('imputation_method',
                                                        ['knn', 'iterative'])
            
            # Preprocessor'ı yapılandır
            self.scaling_method = scaling_method
            self.encoding_method = encoding_method
            self.imputation_method = imputation_method
            self._initialize_components()
            
            # Veriyi işle
            X_processed = self.transform(X)
            
            # Model performansını değerlendir
            scores = cross_val_score(model, X_processed, y, cv=5)
            return scores.mean()
        
        study = optuna.create_study(direction='maximize')
        study.optimize(objective, n_trials=n_trials)
        
        return study.best_params
    
    def get_feature_importance_plot(self, data: pd.DataFrame,
                                  target: pd.Series) -> None:
        """SHAP değerleri ile özellik önem grafiği"""
        model = xgboost.XGBRegressor()
        model.fit(data, target)
        
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(data)
        
        shap.summary_plot(shap_values, data)
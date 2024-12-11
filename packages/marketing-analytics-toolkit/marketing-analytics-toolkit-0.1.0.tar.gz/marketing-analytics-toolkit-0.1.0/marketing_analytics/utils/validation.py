import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional, Union, Callable
from ..core.exceptions import ValidationError
from scipy import stats
import re
from datetime import datetime, timedelta
import networkx as nx
from sklearn.ensemble import IsolationForest
from sklearn.covariance import EllipticEnvelope

class AdvancedDataValidator:
    """
    Gelişmiş Veri Doğrulama Sınıfı
    
    Özellikler:
    - Kapsamlı veri doğrulama
    - İş kuralları kontrolü
    - Anomali tespiti
    - Veri tutarlılık kontrolü
    - Özel kısıt doğrulama
    """
    
    def __init__(self,
                 schema: Optional[Dict] = None,
                 business_rules: Optional[Dict] = None,
                 anomaly_detection: bool = False,
                 consistency_check: bool = True):
        self.schema = schema or {}
        self.business_rules = business_rules or {}
        self.anomaly_detection = anomaly_detection
        self.consistency_check = consistency_check
        
        # Anomali detektörleri
        self.anomaly_detectors = {}
        
    def validate_dataframe(self,
                          df: pd.DataFrame,
                          required_columns: List[str] = None,
                          dtypes: Dict[str, Any] = None,
                          custom_validators: Dict[str, Callable] = None) -> Dict[str, Any]:
        """
        DataFrame doğrulama
        
        Parameters:
        -----------
        df: Doğrulanacak DataFrame
        required_columns: Gerekli kolonlar
        dtypes: Beklenen veri tipleri
        custom_validators: Özel doğrulama fonksiyonları
        
        Returns:
        --------
        Dict: Doğrulama sonuçları
        """
        validation_results = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'statistics': {}
        }
        
        try:
            # Temel doğrulamalar
            self._validate_basic_requirements(df, required_columns, dtypes, validation_results)
            
            # Şema doğrulama
            if self.schema:
                self._validate_schema(df, validation_results)
            
            # İş kuralları kontrolü
            if self.business_rules:
                self._validate_business_rules(df, validation_results)
            
            # Özel doğrulayıcılar
            if custom_validators:
                self._run_custom_validators(df, custom_validators, validation_results)
            
            # Anomali tespiti
            if self.anomaly_detection:
                self._detect_anomalies(df, validation_results)
            
            # Tutarlılık kontrolü
            if self.consistency_check:
                self._check_data_consistency(df, validation_results)
            
            # İstatistiksel analizler
            self._calculate_statistics(df, validation_results)
            
        except Exception as e:
            validation_results['is_valid'] = False
            validation_results['errors'].append(str(e))
            
        return validation_results
        
    def _validate_basic_requirements(self,
                                   df: pd.DataFrame,
                                   required_columns: List[str],
                                   dtypes: Dict[str, Any],
                                   results: Dict) -> None:
        """Temel gereksinimleri doğrula"""
        # Boş DataFrame kontrolü
        if df.empty:
            results['is_valid'] = False
            results['errors'].append("DataFrame is empty")
            return
            
        # Gerekli kolonlar kontrolü
        if required_columns:
            missing_cols = set(required_columns) - set(df.columns)
            if missing_cols:
                results['is_valid'] = False
                results['errors'].append(f"Missing required columns: {missing_cols}")
                
        # Veri tipi kontrolü
        if dtypes:
            for col, dtype in dtypes.items():
                if col in df.columns:
                    if not pd.api.types.is_dtype_equal(df[col].dtype, dtype):
                        results['warnings'].append(
                            f"Column {col} has type {df[col].dtype}, expected {dtype}"
                        )
                        
    def _validate_schema(self,
                        df: pd.DataFrame,
                        results: Dict) -> None:
        """Şema doğrulama"""
        for column, rules in self.schema.items():
            if column not in df.columns:
                continue
                
            # Değer aralığı kontrolü
            if 'range' in rules:
                min_val, max_val = rules['range']
                if not df[column].between(min_val, max_val).all():
                    results['errors'].append(
                        f"Values in {column} outside range [{min_val}, {max_val}]"
                    )
                    
            # Regex pattern kontrolü
            if 'pattern' in rules and pd.api.types.is_string_dtype(df[column]):
                pattern = rules['pattern']
                mask = df[column].str.match(pattern, na=False)
                if not mask.all():
                    results['errors'].append(
                        f"Invalid patterns found in {column}"
                    )
                    
            # Unique değer kontrolü
            if rules.get('unique', False):
                if not df[column].is_unique:
                    results['errors'].append(
                        f"Duplicate values found in {column}"
                    )
                    
    def _validate_business_rules(self,
                               df: pd.DataFrame,
                               results: Dict) -> None:
        """İş kuralları kontrolü"""
        for rule_name, rule_func in self.business_rules.items():
            try:
                is_valid = rule_func(df)
                if not is_valid:
                    results['errors'].append(f"Business rule '{rule_name}' failed")
            except Exception as e:
                results['errors'].append(f"Error in business rule '{rule_name}': {str(e)}")
                
    def _detect_anomalies(self,
                         df: pd.DataFrame,
                         results: Dict) -> None:
        """Anomali tespiti"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            if col not in self.anomaly_detectors:
                # İzolasyon Ormanı
                iso_forest = IsolationForest(contamination=0.1, random_state=42)
                # Eliptik Zarf
                elliptic = EllipticEnvelope(contamination=0.1, random_state=42)
                
                self.anomaly_detectors[col] = {
                    'isolation_forest': iso_forest,
                    'elliptic_envelope': elliptic
                }
                
            # Anomali tespiti
            iso_forest_pred = self.anomaly_detectors[col]['isolation_forest'].fit_predict(
                df[col].values.reshape(-1, 1)
            )
            elliptic_pred = self.anomaly_detectors[col]['elliptic_envelope'].fit_predict(
                df[col].values.reshape(-1, 1)
            )
            
            # Anomali sayısı
            anomaly_count = sum(iso_forest_pred == -1)
            if anomaly_count > 0:
                results['warnings'].append(
                    f"Found {anomaly_count} anomalies in {col}"
                )
                
    def _check_data_consistency(self,
                              df: pd.DataFrame,
                              results: Dict) -> None:
        """Veri tutarlılık kontrolü"""
        # Tarih tutarlılığı
        date_cols = df.select_dtypes(include=['datetime64']).columns
        for col in date_cols:
            # Kronolojik sıra kontrolü
            if not df[col].is_monotonic:
                results['warnings'].append(
                    f"Dates in {col} are not in chronological order"
                )
                
            # Gelecek tarih kontrolü
            if (df[col] > pd.Timestamp.now()).any():
                results['warnings'].append(
                    f"Future dates found in {col}"
                )
                
        # Sayısal tutarlılık
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            # Negatif değer kontrolü (gerekiyorsa)
            if col.lower().contains(('price', 'amount', 'quantity')):
                if (df[col] < 0).any():
                    results['errors'].append(
                        f"Negative values found in {col}"
                    )
                    
        # İlişkisel tutarlılık
        if 'id' in df.columns and 'parent_id' in df.columns:
            self._check_hierarchical_consistency(df, results)
            
    def _check_hierarchical_consistency(self,
                                      df: pd.DataFrame,
                                      results: Dict) -> None:
        """Hiyerarşik veri tutarlılığı kontrolü"""
        # Çevrimsel referans kontrolü
        G = nx.DiGraph()
        for _, row in df.iterrows():
            if pd.notna(row['parent_id']):
                G.add_edge(row['id'], row['parent_id'])
                
        try:
            cycles = list(nx.simple_cycles(G))
            if cycles:
                results['errors'].append(
                    f"Circular references found: {cycles}"
                )
        except Exception as e:
            results['errors'].append(f"Error in hierarchy check: {str(e)}")
            
    def _calculate_statistics(self,
                            df: pd.DataFrame,
                            results: Dict) -> None:
        """İstatistiksel analizler"""
        stats = {}
        
        # Temel istatistikler
        stats['basic'] = {
            'row_count': len(df),
            'column_count': len(df.columns),
            'memory_usage': df.memory_usage(deep=True).sum()
        }
        
        # Eksik değer analizi
        missing_stats = df.isnull().sum()
        stats['missing'] = {
            col: count for col, count in missing_stats.items() if count > 0
        }
        
        # Korelasyon analizi
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 1:
            corr_matrix = df[numeric_cols].corr()
            high_corr = np.where(np.abs(corr_matrix) > 0.8)
            stats['high_correlations'] = [
                (numeric_cols[i], numeric_cols[j], corr_matrix.iloc[i, j])
                for i, j in zip(*high_corr) if i != j
            ]
            
        results['statistics'] = stats
        
    def add_business_rule(self,
                         name: str,
                         rule_func: Callable[[pd.DataFrame], bool]) -> None:
        """İş kuralı ekle"""
        self.business_rules[name] = rule_func
        
    def add_schema_rule(self,
                       column: str,
                       rules: Dict[str, Any]) -> None:
        """Şema kuralı ekle"""
        self.schema[column] = rules
        
    def validate_time_series(self,
                           df: pd.DataFrame,
                           time_col: str,
                           value_col: str,
                           frequency: str = 'D') -> Dict[str, Any]:
        """Zaman serisi doğrulama"""
        results = {
            'is_valid': True,
            'errors': [],
            'warnings': []
        }
        
        # Zaman indeksi kontrolü
        if not pd.api.types.is_datetime64_any_dtype(df[time_col]):
            try:
                df[time_col] = pd.to_datetime(df[time_col])
            except:
                results['errors'].append(f"Cannot convert {time_col} to datetime")
                return results
                
        # Frekans kontrolü
        expected_dates = pd.date_range(
            start=df[time_col].min(),
            end=df[time_col].max(),
            freq=frequency
        )
        missing_dates = set(expected_dates) - set(df[time_col])
        if missing_dates:
            results['warnings'].append(f"Missing dates: {missing_dates}")
            
        # Mevsimsellik kontrolü
        if len(df) >= 2 * 365:  # En az 2 yıllık veri
            decomposition = sm.tsa.seasonal_decompose(
                df[value_col],
                period=365 if frequency == 'D' else 12
            )
            results['seasonality'] = {
                'strength': np.std(decomposition.seasonal) / np.std(df[value_col])
            }
            
        return results
        
    def validate_categorical_distribution(self,
                                       df: pd.DataFrame,
                                       categorical_cols: List[str],
                                       threshold: float = 0.01) -> Dict[str, Any]:
        """Kategorik değişken dağılımı doğrulama"""
        results = {
            'is_valid': True,
            'warnings': []
        }
        
        for col in categorical_cols:
            value_counts = df[col].value_counts(normalize=True)
            
            # Nadir kategoriler
            rare_categories = value_counts[value_counts < threshold]
            if not rare_categories.empty:
                results['warnings'].append(
                    f"Rare categories in {col}: {dict(rare_categories)}"
                )
                
            # Kategori sayısı kontrolü
            if len(value_counts) > 100:  # Çok fazla kategori
                results['warnings'].append(
                    f"High cardinality in {col}: {len(value_counts)} categories"
                )
                
        return results
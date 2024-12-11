import numpy as np
import pandas as pd
from typing import Dict, List, Union, Optional
from sklearn.metrics import roc_auc_score, precision_recall_curve, average_precision_score
from scipy import stats
import statsmodels.api as sm
from lifelines import KaplanMeierFitter, CoxPHFitter

class AdvancedMarketingMetrics:
    """Gelişmiş Pazarlama Metrik Hesaplama Sınıfı"""
    
    def __init__(self):
        self.kmf = KaplanMeierFitter()
        self.cox_model = CoxPHFitter()
        
    def calculate_customer_metrics(self,
                                 customer_data: pd.DataFrame,
                                 monetary_col: str,
                                 frequency_col: str,
                                 time_col: str) -> Dict[str, float]:
        """
        Gelişmiş müşteri metrikleri hesaplama
        
        Parameters:
        -----------
        customer_data: Müşteri verileri
        monetary_col: Parasal değer kolonu
        frequency_col: Frekans kolonu
        time_col: Zaman kolonu
        
        Returns:
        --------
        Dict[str, float]: Hesaplanan metrikler
        """
        metrics = {}
        
        # Temel CLV hesaplama
        avg_purchase = customer_data[monetary_col].mean()
        purchase_freq = customer_data[frequency_col].mean()
        customer_lifetime = customer_data[time_col].max() - customer_data[time_col].min()
        
        metrics['basic_clv'] = avg_purchase * purchase_freq * customer_lifetime.days
        
        # Gelişmiş CLV metrikleri
        metrics['ltv_percentile_90'] = np.percentile(
            customer_data[monetary_col] * customer_data[frequency_col],
            90
        )
        
        # Müşteri yaşam süresi analizi
        self.kmf.fit(
            customer_data[time_col],
            event_observed=customer_data['churn_flag'],
            label='Survival Curve'
        )
        metrics['median_lifetime'] = self.kmf.median_survival_time_
        metrics['retention_rate'] = self.kmf.survival_function_.iloc[-1].values[0]
        
        return metrics
    
    def calculate_campaign_effectiveness(self,
                                      control_group: pd.DataFrame,
                                      treatment_group: pd.DataFrame,
                                      metric_col: str,
                                      confidence_level: float = 0.95) -> Dict[str, Union[float, Dict]]:
        """
        Kampanya etkinliği analizi
        
        Parameters:
        -----------
        control_group: Kontrol grubu verileri
        treatment_group: Test grubu verileri
        metric_col: Ölçüm yapılacak metrik kolonu
        confidence_level: Güven aralığı seviyesi
        
        Returns:
        --------
        Dict: Kampanya etkinlik metrikleri
        """
        results = {}
        
        # A/B Test analizi
        t_stat, p_value = stats.ttest_ind(
            control_group[metric_col],
            treatment_group[metric_col]
        )
        
        effect_size = (treatment_group[metric_col].mean() - control_group[metric_col].mean()) / \
                     control_group[metric_col].std()
                     
        # Güven aralığı hesaplama
        ci = stats.t.interval(
            confidence_level,
            len(control_group) + len(treatment_group) - 2,
            loc=effect_size,
            scale=stats.sem(treatment_group[metric_col])
        )
        
        results['effect_size'] = effect_size
        results['p_value'] = p_value
        results['confidence_interval'] = {'lower': ci[0], 'upper': ci[1]}
        results['lift'] = (treatment_group[metric_col].mean() / control_group[metric_col].mean() - 1) * 100
        
        return results
    
    def calculate_attribution_metrics(self,
                                   journey_data: pd.DataFrame,
                                   conversion_col: str,
                                   channel_col: str,
                                   value_col: str) -> Dict[str, Dict[str, float]]:
        """
        Gelişmiş atribüsyon metrikleri
        
        Parameters:
        -----------
        journey_data: Müşteri yolculuğu verileri
        conversion_col: Dönüşüm kolonu
        channel_col: Kanal kolonu
        value_col: Değer kolonu
        
        Returns:
        --------
        Dict: Kanal bazlı atribüsyon metrikleri
        """
        results = {}
        
        # First-touch attribution
        first_touch = journey_data.groupby(channel_col).agg({
            conversion_col: 'sum',
            value_col: 'sum'
        })
        
        # Last-touch attribution
        last_touch = journey_data.groupby(channel_col).agg({
            conversion_col: 'sum',
            value_col: 'sum'
        })
        
        # Linear attribution
        total_conversions = journey_data[conversion_col].sum()
        total_value = journey_data[value_col].sum()
        
        for channel in journey_data[channel_col].unique():
            results[channel] = {
                'first_touch_share': first_touch.loc[channel, value_col] / total_value,
                'last_touch_share': last_touch.loc[channel, value_col] / total_value,
                'linear_share': 1 / len(journey_data[channel_col].unique()),
                'conversion_rate': journey_data[journey_data[channel_col] == channel][conversion_col].mean()
            }
            
        return results
    
    def calculate_cohort_metrics(self,
                               cohort_data: pd.DataFrame,
                               time_col: str,
                               cohort_col: str,
                               metric_col: str) -> pd.DataFrame:
        """
        Kohort analizi metrikleri
        
        Parameters:
        -----------
        cohort_data: Kohort verileri
        time_col: Zaman kolonu
        cohort_col: Kohort kolonu
        metric_col: Metrik kolonu
        
        Returns:
        --------
        pd.DataFrame: Kohort analiz sonuçları
        """
        # Kohort matrisi oluştur
        cohort_matrix = cohort_data.pivot_table(
            index=cohort_col,
            columns=time_col,
            values=metric_col,
            aggfunc='mean'
        )
        
        # Retention oranları
        retention_matrix = cohort_matrix.div(cohort_matrix.iloc[:, 0], axis=0)
        
        # Büyüme oranları
        growth_matrix = cohort_matrix.pct_change(axis=1)
        
        return {
            'cohort_matrix': cohort_matrix,
            'retention_matrix': retention_matrix,
            'growth_matrix': growth_matrix
        }
    
    def calculate_predictive_metrics(self,
                                   actual: np.ndarray,
                                   predicted: np.ndarray,
                                   proba: Optional[np.ndarray] = None) -> Dict[str, float]:
        """
        Tahminsel metrikler
        
        Parameters:
        -----------
        actual: Gerçek değerler
        predicted: Tahmin edilen değerler
        proba: Olasılık değerleri (opsiyonel)
        
        Returns:
        --------
        Dict: Tahminsel metrikler
        """
        metrics = {}
        
        # Temel metrikler
        metrics['mape'] = np.mean(np.abs((actual - predicted) / actual)) * 100
        metrics['rmse'] = np.sqrt(np.mean((actual - predicted) ** 2))
        
        if proba is not None:
            # ROC AUC
            metrics['roc_auc'] = roc_auc_score(actual, proba)
            
            # Precision-Recall AUC
            metrics['pr_auc'] = average_precision_score(actual, proba)
            
            # Lift ve Gain metrikleri
            percentiles = np.percentile(proba, np.arange(0, 101, 10))
            lift_values = []
            
            for p in percentiles:
                selected = proba >= p
                if selected.sum() > 0:
                    lift = (actual[selected].mean() / actual.mean())
                    lift_values.append(lift)
            
            metrics['max_lift'] = max(lift_values)
            metrics['lift_curve'] = list(zip(np.arange(0, 101, 10), lift_values))
        
        return metrics
    
    def calculate_time_based_metrics(self,
                                   time_series_data: pd.DataFrame,
                                   metric_col: str,
                                   time_col: str) -> Dict[str, Union[float, Dict]]:
        """
        Zaman bazlı metrikler
        
        Parameters:
        -----------
        time_series_data: Zaman serisi verileri
        metric_col: Metrik kolonu
        time_col: Zaman kolonu
        
        Returns:
        --------
        Dict: Zaman bazlı metrikler
        """
        results = {}
        
        # Trend analizi
        X = sm.add_constant(np.arange(len(time_series_data)))
        model = sm.OLS(time_series_data[metric_col], X).fit()
        
        results['trend_coefficient'] = model.params[1]
        results['trend_p_value'] = model.pvalues[1]
        
        # Mevsimsellik analizi
        if len(time_series_data) >= 12:
            seasonal_decompose = sm.tsa.seasonal_decompose(
                time_series_data[metric_col],
                period=12
            )
            results['seasonality'] = {
                'trend': seasonal_decompose.trend.dropna().tolist(),
                'seasonal': seasonal_decompose.seasonal.dropna().tolist(),
                'residual': seasonal_decompose.resid.dropna().tolist()
            }
        
        # Büyüme metrikleri
        results['cagr'] = (
            (time_series_data[metric_col].iloc[-1] / time_series_data[metric_col].iloc[0]) ** 
            (1 / (len(time_series_data) / 12)) - 1
        ) * 100
        
        results['volatility'] = time_series_data[metric_col].std() / time_series_data[metric_col].mean()
        
        return results
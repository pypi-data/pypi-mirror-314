import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Union, Tuple
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
import networkx as nx
from sklearn.preprocessing import MinMaxScaler
import colorsys

class AdvancedMarketingVisualizer:
    """
    Gelişmiş Pazarlama Görselleştirme Sınıfı
    
    Özellikler:
    - İnteraktif grafikler
    - Çoklu görselleştirme
    - Özelleştirilebilir temalar
    - Otomatik raporlama
    - Animasyonlu grafikler
    """
    
    def __init__(self,
                 theme: str = 'modern',
                 color_palette: Optional[List[str]] = None,
                 interactive: bool = True):
        self.theme = theme
        self.color_palette = color_palette or self._get_default_palette()
        self.interactive = interactive
        self._set_theme()
        
    def _set_theme(self):
        """Tema ayarlarını yapılandır"""
        themes = {
            'modern': {
                'background_color': '#ffffff',
                'paper_color': '#f8f9fa',
                'font_family': 'Arial',
                'grid_color': '#e9ecef'
            },
            'dark': {
                'background_color': '#212529',
                'paper_color': '#343a40',
                'font_family': 'Helvetica',
                'grid_color': '#495057'
            },
            'minimal': {
                'background_color': '#ffffff',
                'paper_color': '#ffffff',
                'font_family': 'Roboto',
                'grid_color': '#dee2e6'
            }
        }
        
        self.theme_config = themes.get(self.theme, themes['modern'])
        
    def _get_default_palette(self) -> List[str]:
        """Varsayılan renk paleti"""
        return px.colors.qualitative.Set3
        
    def plot_customer_journey(self,
                            journey_data: pd.DataFrame,
                            channel_importance: Dict[str, float],
                            show_conversion_rates: bool = True) -> go.Figure:
        """
        Gelişmiş müşteri yolculuğu görselleştirmesi
        
        Parameters:
        -----------
        journey_data: Yolculuk verileri
        channel_importance: Kanal önem skorları
        show_conversion_rates: Dönüşüm oranlarını göster
        """
        # Sankey diyagramı
        fig = go.Figure(data=[
            go.Sankey(
                node=dict(
                    pad=15,
                    thickness=20,
                    line=dict(color="black", width=0.5),
                    label=list(channel_importance.keys()),
                    color=[self._adjust_color_opacity(c, channel_importance[ch])
                          for c, ch in zip(self.color_palette, channel_importance.keys())]
                ),
                link=dict(
                    source=journey_data['source'],
                    target=journey_data['target'],
                    value=journey_data['value'],
                    color=[self._adjust_color_opacity(self.color_palette[0], 0.3)
                          for _ in range(len(journey_data))]
                )
            )
        ])
        
        # Dönüşüm oranları
        if show_conversion_rates:
            conversion_rates = self._calculate_conversion_rates(journey_data)
            self._add_conversion_annotations(fig, conversion_rates)
            
        fig.update_layout(
            title="Customer Journey Analysis",
            font_family=self.theme_config['font_family'],
            paper_bgcolor=self.theme_config['paper_color'],
            plot_bgcolor=self.theme_config['background_color']
        )
        
        return fig
        
    def plot_segment_analysis(self,
                            segment_data: pd.DataFrame,
                            metrics: List[str],
                            segment_col: str = 'segment') -> go.Figure:
        """Segment analizi görselleştirmesi"""
        # Alt grafikler oluştur
        n_metrics = len(metrics)
        fig = make_subplots(
            rows=2,
            cols=2,
            subplot_titles=metrics,
            specs=[[{'type': 'domain'}, {'type': 'bar'}],
                  [{'type': 'box'}, {'type': 'scatter'}]]
        )
        
        # Segment büyüklükleri (Pasta grafik)
        segment_sizes = segment_data[segment_col].value_counts()
        fig.add_trace(
            go.Pie(
                labels=segment_sizes.index,
                values=segment_sizes.values,
                hole=0.4,
                marker_colors=self.color_palette[:len(segment_sizes)]
            ),
            row=1, col=1
        )
        
        # Metrik karşılaştırmaları (Bar grafik)
        for i, metric in enumerate(metrics):
            fig.add_trace(
                go.Bar(
                    x=segment_data.groupby(segment_col)[metric].mean().index,
                    y=segment_data.groupby(segment_col)[metric].mean().values,
                    name=metric,
                    marker_color=self.color_palette[i]
                ),
                row=1, col=2
            )
            
        # Dağılım analizi (Box plot)
        fig.add_trace(
            go.Box(
                x=segment_data[segment_col],
                y=segment_data[metrics[0]],
                marker_color=self.color_palette[0]
            ),
            row=2, col=1
        )
        
        # Trend analizi (Scatter plot)
        if 'date' in segment_data.columns:
            for segment in segment_data[segment_col].unique():
                segment_mask = segment_data[segment_col] == segment
                fig.add_trace(
                    go.Scatter(
                        x=segment_data[segment_mask]['date'],
                        y=segment_data[segment_mask][metrics[0]],
                        name=f"Segment {segment}",
                        mode='lines+markers'
                    ),
                    row=2, col=2
                )
                
        fig.update_layout(
            height=800,
            showlegend=True,
            title="Segment Analysis Dashboard",
            **self.theme_config
        )
        
        return fig
        
    def plot_price_elasticity(self,
                            prices: np.ndarray,
                            demand: np.ndarray,
                            elasticity: float,
                            confidence_interval: Optional[Tuple[float, float]] = None) -> go.Figure:
        """Fiyat esnekliği görselleştirmesi"""
        fig = go.Figure()
        
        # Scatter plot
        fig.add_trace(
            go.Scatter(
                x=prices,
                y=demand,
                mode='markers',
                name='Actual Data',
                marker=dict(
                    color=self.color_palette[0],
                    size=8
                )
            )
        )
        
        # Trend line
        z = np.polyfit(prices, demand, 1)
        p = np.poly1d(z)
        x_range = np.linspace(min(prices), max(prices), 100)
        
        fig.add_trace(
            go.Scatter(
                x=x_range,
                y=p(x_range),
                mode='lines',
                name='Trend Line',
                line=dict(
                    color=self.color_palette[1],
                    width=2
                )
            )
        )
        
        # Güven aralığı
        if confidence_interval:
            lower, upper = confidence_interval
            fig.add_trace(
                go.Scatter(
                    x=x_range,
                    y=p(x_range) + upper,
                    mode='lines',
                    line=dict(width=0),
                    showlegend=False
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=x_range,
                    y=p(x_range) + lower,
                    mode='lines',
                    line=dict(width=0),
                    fillcolor='rgba(68, 68, 68, 0.2)',
                    fill='tonexty',
                    name='95% CI'
                )
            )
            
        fig.update_layout(
            title=f"Price Elasticity Analysis (ε = {elasticity:.2f})",
            xaxis_title="Price",
            yaxis_title="Demand",
            **self.theme_config
        )
        
        return fig
        
    def plot_marketing_mix(self,
                          channel_data: pd.DataFrame,
                          metrics: List[str],
                          time_col: str = 'date') -> go.Figure:
        """Pazarlama karması görselleştirmesi"""
        fig = make_subplots(
            rows=2,
            cols=2,
            subplot_titles=["Channel Performance", "ROI Analysis",
                          "Time Series Analysis", "Channel Mix"]
        )
        
        # Kanal performansı (Bar chart)
        performance = channel_data.groupby('channel')[metrics[0]].sum()
        fig.add_trace(
            go.Bar(
                x=performance.index,
                y=performance.values,
                marker_color=self.color_palette
            ),
            row=1, col=1
        )
        
        # ROI analizi (Scatter plot)
        if 'cost' in channel_data.columns and 'revenue' in channel_data.columns:
            roi = (channel_data['revenue'] - channel_data['cost']) / channel_data['cost']
            fig.add_trace(
                go.Scatter(
                    x=channel_data['cost'],
                    y=roi,
                    mode='markers',
                    marker=dict(
                        size=10,
                        color=roi,
                        colorscale='Viridis',
                        showscale=True
                    )
                ),
                row=1, col=2
            )
            
        # Zaman serisi analizi
        for channel in channel_data['channel'].unique():
            channel_mask = channel_data['channel'] == channel
            fig.add_trace(
                go.Scatter(
                    x=channel_data[channel_mask][time_col],
                    y=channel_data[channel_mask][metrics[0]],
                    name=channel,
                    mode='lines'
                ),
                row=2, col=1
            )
            
        # Kanal karması (Pie chart)
        channel_mix = channel_data.groupby('channel')[metrics[0]].sum()
        fig.add_trace(
            go.Pie(
                labels=channel_mix.index,
                values=channel_mix.values,
                hole=0.4
            ),
            row=2, col=2
        )
        
        fig.update_layout(
            height=800,
            showlegend=True,
            title="Marketing Mix Analysis",
            **self.theme_config
        )
        
        return fig
        
    def create_dashboard(self,
                        data: Dict[str, pd.DataFrame],
                        metrics: List[str]) -> go.Figure:
        """İnteraktif dashboard oluştur"""
        fig = make_subplots(
            rows=3,
            cols=2,
            subplot_titles=["Overview", "Trends", "Segments",
                          "Channel Performance", "Customer Behavior", "Predictions"],
            specs=[[{'type': 'indicator'}, {'type': 'scatter'}],
                  [{'type': 'pie'}, {'type': 'bar'}],
                  [{'type': 'heatmap'}, {'type': 'scatter'}]]
        )
        
        # KPI göstergeleri
        for i, metric in enumerate(metrics[:4]):
            fig.add_trace(
                go.Indicator(
                    mode="number+delta",
                    value=data['metrics'][metric].iloc[-1],
                    delta={'reference': data['metrics'][metric].iloc[-2]},
                    title={'text': metric}
                ),
                row=1, col=1
            )
            
        # Diğer grafikler...
        
        fig.update_layout(
            height=1200,
            showlegend=True,
            title="Marketing Analytics Dashboard",
            **self.theme_config
        )
        
        return fig
        
    def _adjust_color_opacity(self,
                            color: str,
                            opacity: float) -> str:
        """Renk opaklığını ayarla"""
        rgb = px.colors.hex_to_rgb(color)
        return f"rgba{rgb + (opacity,)}"
        
    def _calculate_conversion_rates(self,
                                  journey_data: pd.DataFrame) -> Dict[str, float]:
        """Dönüşüm oranlarını hesapla"""
        conversion_rates = {}
        for source in journey_data['source'].unique():
            source_total = journey_data[journey_data['source'] == source]['value'].sum()
            conversions = journey_data[
                (journey_data['source'] == source) &
                (journey_data['target'] == 'conversion')
            ]['value'].sum()
            
            if source_total > 0:
                conversion_rates[source] = conversions / source_total
                
        return conversion_rates
        
    def _add_conversion_annotations(self,
                                  fig: go.Figure,
                                  conversion_rates: Dict[str, float]) -> None:
        """Dönüşüm oranı açıklamaları ekle"""
        for channel, rate in conversion_rates.items():
            fig.add_annotation(
                x=channel,
                y=1,
                text=f"{rate:.1%}",
                showarrow=False,
                font=dict(size=12)
            )
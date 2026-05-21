import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import plotly.express as px
import plotly.graph_objects as go

class DataScienceModels:
    """Aplica modelos de Data Science aos dados ambientais."""
    
    def __init__(self, df):
        self.df = df
        self.models = {}
        
    def forecast_impact(self, periods=12):
        """Previsão de impacto usando Holt-Winters (sazonalidade)."""
        # Agrega dados mensais
        monthly = self.df.groupby(['year', 'month'])['carbon_saved_tco2e'].sum().reset_index()
        monthly['date'] = pd.to_datetime(monthly[['year', 'month']].assign(day=1))
        monthly = monthly.set_index('date').sort_index()
        
        # Ajusta modelo
        model = ExponentialSmoothing(monthly['carbon_saved_tco2e'], 
                                     seasonal_periods=12, 
                                     trend='add', 
                                     seasonal='add')
        fit_model = model.fit()
        
        # Gera previsão
        forecast = fit_model.forecast(periods)
        
        # Cria dataframe da previsão
        last_date = monthly.index[-1]
        forecast_dates = pd.date_range(start=last_date + pd.DateOffset(months=1), periods=periods, freq='MS')
        forecast_df = pd.DataFrame({'date': forecast_dates, 'forecast_carbon_tco2e': forecast.values})
        
        # Visualização
        fig = px.line(title="📈 Previsão de Carbono Poupado (Próximos 12 Meses)")
        fig.add_scatter(x=monthly.index, y=monthly['carbon_saved_tco2e'], mode='lines+markers', name='Histórico')
        fig.add_scatter(x=forecast_df['date'], y=forecast_df['forecast_carbon_tco2e'], mode='lines+markers', name='Previsão', line=dict(dash='dash'))
        fig.update_layout(xaxis_title="Data", yaxis_title="Carbono Poupado (tCO₂e)")
        
        return forecast_df, fig
    
    def project_similarity_clustering(self):
        """Agrupa projetos por padrão de impacto usando K-Means."""
        # Agrega impacto total por projeto
        project_features = self.df.groupby('project_name')[['energy_produced_mwh', 'carbon_saved_tco2e']].sum()
        
        # Normaliza
        scaler = StandardScaler()
        features_scaled = scaler.fit_transform(project_features)
        
        # Aplica K-Means (k=3 clusters)
        kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
        clusters = kmeans.fit_predict(features_scaled)
        
        project_features['cluster'] = clusters
        project_features.reset_index(inplace=True)
        
        # Visualização 3D
        fig = px.scatter_3d(project_features, x='energy_produced_mwh', y='carbon_saved_tco2e', 
                            z='cluster', color='cluster', 
                            hover_name='project_name',
                            title="🎯 Agrupamento de Projetos por Similaridade de Impacto",
                            labels={'energy_produced_mwh': 'Energia (MWh)', 'carbon_saved_tco2e': 'Carbono (tCO₂e)'})
        return project_features, fig
    
    def feature_importance(self):
        """Determina quais fatores (tipo, região, tempo) mais impactam o carbono poupado."""
        # Prepara features
        df_ml = self.df.copy()
        df_ml['month_of_year'] = df_ml['date'].dt.month
        df_ml['years_since_start'] = (df_ml['date'].dt.year - 2016)
        
        # One-hot encoding para variáveis categóricas
        df_encoded = pd.get_dummies(df_ml, columns=['project_type', 'region'], drop_first=True)
        
        features = ['month_of_year', 'years_since_start'] + [c for c in df_encoded.columns if 'project_type_' in c or 'region_' in c]
        X = df_encoded[features]
        y = df_encoded['carbon_saved_tco2e']
        
        # Random Forest
        rf = RandomForestRegressor(n_estimators=100, random_state=42)
        rf.fit(X, y)
        
        # Importância
        importance_df = pd.DataFrame({'feature': features, 'importance': rf.feature_importances_})
        importance_df = importance_df.sort_values('importance', ascending=False)
        
        fig = px.bar(importance_df.head(10), x='importance', y='feature', orientation='h',
                     title="🔍 Importância das Features para o Carbono Poupado",
                     labels={'importance': 'Importância Relativa', 'feature': 'Variável'})
        return importance_df, fig
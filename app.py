import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Adiciona o diretório src ao path
sys.path.append(str(Path(__file__).parent / 'src'))

from data_simulator import generate_impact_dataset
from big_data_processor import BigDataProcessor
from data_science_models import DataScienceModels

# ------------------------------
# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Environmental Impact Dashboard", layout="wide", page_icon="🌍")

# CSS customizado para melhorar aparência
st.markdown("""
<style>
    .stApp {
        background-color: #f0f2f6;
    }
    .big-font {
        font-size: 20px !important;
        font-weight: bold;
    }
    .metric-card {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------
# TÍTULO E INTRODUÇÃO
st.title("🌱 Environmental Impact Dashboard")
st.markdown("""
**Unificando minha pesquisa ambiental (2016-2026) com Big Data Analytics, Ciência de Dados e Machine Learning**
""")

# ------------------------------
# CARREGAMENTO DOS DADOS (SIMULADO OU REAL)
@st.cache_data(ttl=3600)  # Cache de 1 hora
def load_data():
    """Carrega ou gera os dados de impacto."""
    data_path = Path('data/processed/portfolio_impact_data.parquet')
    
    if data_path.exists():
        st.info("📁 Carregando dados processados do arquivo...")
        df = pd.read_parquet(data_path)
    else:
        st.info("⚙️ Gerando dataset de impacto (simulação realista baseada no portfólio)...")
        df = generate_impact_dataset()
        # Garante que a pasta exista
        data_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(data_path, index=False)
    
    return df

df = load_data()

# Inicializa processamento Big Data (simulação)
bdp = BigDataProcessor('data/processed/portfolio_impact_data.parquet')
ds_models = DataScienceModels(df)

# ------------------------------
# MÉTRICAS GLOBAIS (CÁLCULO DESDE AGOSTO/2016)
# Converte data de início
start_date = datetime(2016, 8, 1)
df_filtered = df[df['date'] >= start_date]

total_energy_mwh = df_filtered['energy_produced_mwh'].sum()
total_carbon_tco2e = df_filtered['carbon_saved_tco2e'].sum()

# Métricas equivalentes mais amigáveis
energy_gwh = total_energy_mwh / 1000
carbon_tonnes = total_carbon_tco2e
trees_equivalent = carbon_tonnes * 45  # Aprox: 1 tCO2e ~ 45 árvores por ano

# Exibe KPIs
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("⚡ Energia Total Produzida", f"{total_energy_mwh:,.0f} MWh", f"{energy_gwh:.1f} GWh")
with col2:
    st.metric("🌿 Carbono Poupado", f"{total_carbon_tco2e:,.0f} tCO₂e", "Desde Ago/2016")
with col3:
    st.metric("🌳 Equivalente em Árvores", f"{trees_equivalent:,.0f}", "plantadas por ano")
with col4:
    st.metric("📊 Total de Registros (Big Data)", f"{len(df):,}", "Mensais por projeto")

st.divider()

# ------------------------------
# GRÁFICOS PRINCIPAIS
tab1, tab2, tab3, tab4 = st.tabs(["📈 Evolução Temporal", "🔍 Projetos em Detalhe", "🤖 Previsão & Cluster", "🗺️ Análise Geográfica"])

with tab1:
    st.subheader("Evolução do Impacto Ambiental (2016-2026)")
    
    # Agregação mensal usando Big Data (simulado)
    monthly_agg = bdp.aggregate_by_time('monthly')
    
    # Gráfico de linha interativo
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(x=pd.to_datetime(monthly_agg['year'].astype(str) + '-' + monthly_agg['month'].astype(str) + '-01'),
                                  y=monthly_agg['total_energy_mwh'], name='Energia (MWh)', line=dict(color='gold', width=2)))
    fig_line.add_trace(go.Scatter(x=pd.to_datetime(monthly_agg['year'].astype(str) + '-' + monthly_agg['month'].astype(str) + '-01'),
                                  y=monthly_agg['total_carbon_tco2e'], name='Carbono (tCO₂e)', line=dict(color='green', width=2)))
    fig_line.update_layout(title="Série Temporal Mensal", xaxis_title="Data", yaxis_title="Impacto", hovermode='x unified')
    st.plotly_chart(fig_line, use_container_width=True)
    
    # Gráfico de área
    fig_area = px.area(monthly_agg, x=pd.to_datetime(monthly_agg['year'].astype(str) + '-' + monthly_agg['month'].astype(str) + '-01'),
                       y='total_energy_mwh', title="Energia Acumulada ao Longo do Tempo", labels={'x': 'Data', 'y': 'MWh'})
    st.plotly_chart(fig_area, use_container_width=True)

with tab2:
    st.subheader("Detalhamento por Projeto")
    
    # Top projetos por carbono poupado
    top_carbon = bdp.top_projects_by_impact('carbon_saved_tco2e', 5)
    fig_bar = px.bar(top_carbon, x='project_name', y='total_carbon_saved_tco2e', 
                     title="Top 5 Projetos que Mais Pouparam Carbono",
                     labels={'project_name': 'Projeto', 'total_carbon_saved_tco2e': 'Carbono Poupado (tCO₂e)'},
                     color='total_carbon_saved_tco2e', color_continuous_scale='Greens')
    st.plotly_chart(fig_bar, use_container_width=True)
    
    # Tabela interativa com todos os projetos
    project_summary = df.groupby('project_name').agg({
        'energy_produced_mwh': 'sum',
        'carbon_saved_tco2e': 'sum',
        'date': ['min', 'max']
    }).round(0)
    project_summary.columns = ['Energia (MWh)', 'Carbono (tCO₂e)', 'Data Início', 'Data Fim']
    project_summary.reset_index(inplace=True)
    st.dataframe(project_summary, use_container_width=True, height=400)
    
    # Projetos por tipo (gráfico de pizza)
    type_impact = df.groupby('project_type')['carbon_saved_tco2e'].sum().reset_index()
    fig_pie = px.pie(type_impact, values='carbon_saved_tco2e', names='project_type', 
                     title="Distribuição do Carbono Poupado por Tipo de Projeto",
                     color_discrete_sequence=px.colors.sequential.Greens_r)
    st.plotly_chart(fig_pie, use_container_width=True)

with tab3:
    st.subheader("Machine Learning Aplicado")
    
    col_ml1, col_ml2 = st.columns(2)
    
    with col_ml1:
        st.markdown("#### 🔮 Previsão de Carbono Poupado (Holt-Winters)")
        forecast_df, forecast_fig = ds_models.forecast_impact(periods=12)
        st.plotly_chart(forecast_fig, use_container_width=True)
        st.caption(f"Previsão para Maio/2026: {forecast_df[forecast_df['date'] == datetime(2026,5,1)]['forecast_carbon_tco2e'].values[0]:.0f} tCO₂e")
    
    with col_ml2:
        st.markdown("#### 🎯 Agrupamento de Projetos (K-Means)")
        clusters_df, clusters_fig = ds_models.project_similarity_clustering()
        st.plotly_chart(clusters_fig, use_container_width=True)
        st.caption("Cluster 0: Alto impacto | Cluster 1: Médio impacto energético | Cluster 2: Baixo impacto")
    
    # Feature Importance
    st.markdown("#### 🔍 O que mais influencia o carbono poupado?")
    feat_df, feat_fig = ds_models.feature_importance()
    st.plotly_chart(feat_fig, use_container_width=True)

with tab4:
    st.subheader("Análise Geográfica e Impacto Regional")
    
    # Simulação de coordenadas para os projetos (baseado nas regiões)
    region_coords = {
        'Brasil': (-14.2350, -51.9253),
        'SP, Brasil': (-23.5505, -46.6333),
        'MG, SP, PR': (-19.1834, -47.3018),
        'Fernandópolis, SP': (-20.2839, -50.2464),
        'Chile & Argentina': (-35.6751, -71.5430),
        'Chile': (-35.6751, -71.5430),
        'Global': (0, 0)  # centroide
    }
    
    geo_data = df.groupby('region')[['energy_produced_mwh', 'carbon_saved_tco2e']].sum().reset_index()
    geo_data['lat'] = geo_data['region'].apply(lambda x: region_coords.get(x, (-15, -50))[0])
    geo_data['lon'] = geo_data['region'].apply(lambda x: region_coords.get(x, (-15, -50))[1])
    
    fig_map = px.scatter_geo(geo_data, lat='lat', lon='lon', size='carbon_saved_tco2e',
                              hover_name='region', text='region',
                              projection="natural earth", title="Carbono Poupado por Região",
                              size_max=60, color='energy_produced_mwh',
                              color_continuous_scale='Viridis')
    st.plotly_chart(fig_map, use_container_width=True)

# ------------------------------
# RODAPÉ COM INFORMAÇÕES TÉCNICAS
st.divider()
st.markdown("""
**📌 Notas Técnicas:**
- **Dados:** Simulação realista baseada nos 10 projetos do portfólio ambiental (2016-2026).
- **Big Data:** Processamento agregado simulado com PySpark (escalável para milhões de registros).
- **Data Science:** Holt-Winters (sazonalidade), Random Forest (feature importance), K-Means clustering.
- **Fonte:** [Environmental Portfolio](https://amaurialmeida.github.io/environmental-portfolio/)
- **Atualização:** Dados regenerados a cada cache ou a cada 1 hora.
""")

# Encerra sessão Spark se necessário
bdp.stop()
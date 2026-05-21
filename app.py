import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Adiciona o diretório src ao path
sys.path.append(str(Path(__file__).parent / 'src'))

from data_simulator import generate_impact_dataset
from big_data_processor import BigDataProcessor
from data_science_models import DataScienceModels

# Configuração da página
st.set_page_config(
    page_title="Environmental Impact Dashboard", 
    layout="wide", 
    page_icon="🌍"
)

# CSS customizado
st.markdown("""
<style>
    .stApp { background-color: #f0f2f6; }
    .metric-card {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .big-font { font-size: 20px !important; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# Título
st.title("🌱 Environmental Impact Dashboard")
st.markdown("""
**Unificando 10 projetos de pesquisa ambiental (2016-2026) com Big Data Analytics, Ciência de Dados e Machine Learning**
""")

# Carregamento dos dados
@st.cache_data(ttl=3600)
def load_data():
    data_dir = Path('data/processed')
    data_dir.mkdir(parents=True, exist_ok=True)
    data_path = data_dir / 'portfolio_impact_data.parquet'
    
    if data_path.exists():
        st.info("📁 Carregando dados existentes...")
        df = pd.read_parquet(data_path)
    else:
        st.info("⚙️ Gerando dataset de impacto (primeira execução)...")
        df = generate_impact_dataset()
        df.to_parquet(data_path, index=False)
        st.success("✅ Dataset gerado!")
    
    return df

try:
    df = load_data()
    st.success(f"📊 Dados carregados: {len(df):,} registros de 10 projetos")
except Exception as e:
    st.error(f"❌ Erro: {str(e)}")
    st.stop()

# Inicialização dos componentes
try:
    bdp = BigDataProcessor('data/processed/portfolio_impact_data.parquet')
    st.success("✅ Big Data Analytics inicializado (conceitos MapReduce implementados)")
except Exception as e:
    st.warning(f"⚠️ Big Data em modo conceitual: {str(e)[:100]}")
    bdp = None

try:
    ds_models = DataScienceModels(df)
    st.success("✅ Modelos de Machine Learning carregados")
except Exception as e:
    st.error(f"❌ Erro nos modelos: {str(e)[:100]}")
    ds_models = None

# Métricas globais
start_date = datetime(2016, 8, 1)
df_filtered = df[df['date'] >= start_date]

total_energy_mwh = df_filtered['energy_produced_mwh'].sum()
total_carbon_tco2e = df_filtered['carbon_saved_tco2e'].sum()
energy_gwh = total_energy_mwh / 1000
trees_equivalent = total_carbon_tco2e * 45
cars_equivalent = total_carbon_tco2e / 4.6

st.markdown("### 📊 Impacto Acumulado (Agosto/2016 - Maio/2026)")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("⚡ Energia Total", f"{total_energy_mwh:,.0f} MWh", f"{energy_gwh:.1f} GWh")
with col2:
    st.metric("🌿 Carbono Poupado", f"{total_carbon_tco2e:,.0f} tCO₂e", "Desde Ago/2016")
with col3:
    st.metric("🌳 Equivalente Árvores", f"{trees_equivalent:,.0f}", "plantadas/ano")
with col4:
    st.metric("🚗 Carros a Menos", f"{cars_equivalent:,.0f}", "por ano")

st.divider()

# Abas principais
tab1, tab2, tab3, tab4 = st.tabs(["📈 Evolução Temporal", "🔍 Projetos", "🤖 Data Science", "🗺️ Análise Geo"])

# TAB 1: Evolução Temporal
with tab1:
    st.subheader("Evolução do Impacto (2016-2026)")
    
    if bdp:
        monthly_agg = bdp.aggregate_by_time('monthly')
        st.caption("📊 Processado com conceitos de Big Data (MapReduce)")
    else:
        monthly_agg = df.groupby(['year', 'month'])[['energy_produced_mwh', 'carbon_saved_tco2e']].sum().reset_index()
    
    monthly_agg['date'] = pd.to_datetime(monthly_agg['year'].astype(str) + '-' + monthly_agg['month'].astype(str) + '-01')
    
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(x=monthly_agg['date'], y=monthly_agg['energy_produced_mwh'], 
                                  name='Energia (MWh)', line=dict(color='#FFD700', width=3)))
    fig_line.add_trace(go.Scatter(x=monthly_agg['date'], y=monthly_agg['carbon_saved_tco2e'], 
                                  name='Carbono (tCO₂e)', line=dict(color='#2E7D32', width=3)))
    fig_line.update_layout(title="Série Temporal Mensal", xaxis_title="Data", 
                          yaxis_title="Impacto", hovermode='x unified', height=500)
    st.plotly_chart(fig_line, use_container_width=True)
    
    # Acumulado
    df_cumulative = df_filtered.sort_values('date')
    df_cumulative['cumulative_carbon'] = df_cumulative['carbon_saved_tco2e'].cumsum()
    fig_area = px.area(df_cumulative, x='date', y='cumulative_carbon', 
                       title="Carbono Poupado Acumulado",
                       labels={'date': 'Data', 'cumulative_carbon': 'tCO₂e'},
                       color_discrete_sequence=['#2E7D32'])
    st.plotly_chart(fig_area, use_container_width=True)

# TAB 2: Projetos
with tab2:
    st.subheader("Detalhamento por Projeto")
    
    if bdp:
        top_carbon = bdp.top_projects_by_impact('carbon_saved_tco2e', 5)
    else:
        top_carbon = df.groupby('project_name')['carbon_saved_tco2e'].sum().nlargest(5).reset_index()
        top_carbon.columns = ['project_name', 'total_carbon_saved_tco2e']
    
    fig_bar = px.bar(top_carbon, x='project_name', y='total_carbon_saved_tco2e',
                     title="Top 5 Projetos - Carbono Poupado",
                     color='total_carbon_saved_tco2e', color_continuous_scale='Greens')
    st.plotly_chart(fig_bar, use_container_width=True)
    
    # Tabela completa
    project_summary = df.groupby('project_name').agg({
        'energy_produced_mwh': 'sum',
        'carbon_saved_tco2e': 'sum'
    }).round(0).reset_index()
    project_summary.columns = ['Projeto', 'Energia (MWh)', 'Carbono (tCO₂e)']
    st.dataframe(project_summary, use_container_width=True)

# TAB 3: Data Science
with tab3:
    st.subheader("🤖 Machine Learning e Big Data Analytics")
    
    # Big Data Concepts
    with st.expander("🏗️ Arquitetura Big Data Implementada", expanded=True):
        if bdp:
            st.markdown("**Conceitos de Big Data demonstrados:**")
            concepts = bdp.explain_big_data_concepts()
            for concept, description in concepts.items():
                st.info(f"**{concept}:** {description}")
            
            # Demonstração MapReduce
            if st.button("▶️ Executar Demonstração MapReduce"):
                with st.spinner("Processando..."):
                    total = bdp.execute_map_reduce_demo()
                    st.success(f"✅ MapReduce completado! Total: {total:.2f} tCO₂e")
    
    if ds_models:
        # Previsão
        st.markdown("### 🔮 Previsão de Carbono Poupado")
        try:
            forecast_df, forecast_fig = ds_models.forecast_impact(periods=12)
            st.plotly_chart(forecast_fig, use_container_width=True)
        except Exception as e:
            st.error(f"Erro na previsão: {str(e)[:100]}")
        
        # Clustering
        st.markdown("### 🎯 Agrupamento de Projetos")
        try:
            clusters_df, clusters_fig = ds_models.project_similarity_clustering()
            st.plotly_chart(clusters_fig, use_container_width=True)
        except Exception as e:
            st.error(f"Erro no clustering: {str(e)[:100]}")
        
        # Feature Importance
        st.markdown("### 🔍 Análise de Importância")
        try:
            feat_df, feat_fig = ds_models.feature_importance()
            st.plotly_chart(feat_fig, use_container_width=True)
        except Exception as e:
            st.error(f"Erro: {str(e)[:100]}")

# TAB 4: Análise Geográfica
with tab4:
    st.subheader("🗺️ Distribuição Geográfica")
    
    region_coords = {
        'Brasil': (-14.2350, -51.9253),
        'SP, Brasil': (-23.5505, -46.6333),
        'MG, SP, PR': (-19.1834, -47.3018),
        'Chile & Argentina': (-35.6751, -71.5430),
        'Chile': (-35.6751, -71.5430),
    }
    
    geo_data = df.groupby('region')[['carbon_saved_tco2e']].sum().reset_index()
    geo_data['lat'] = geo_data['region'].apply(lambda x: region_coords.get(x, (-15, -50))[0])
    geo_data['lon'] = geo_data['region'].apply(lambda x: region_coords.get(x, (-15, -50))[1])
    
    fig_map = px.scatter_geo(geo_data, lat='lat', lon='lon', size='carbon_saved_tco2e',
                              hover_name='region', projection="natural earth",
                              title="Carbono Poupado por Região",
                              size_max=60, scope="south america")
    st.plotly_chart(fig_map, use_container_width=True)

# Rodapé
st.divider()
st.markdown("""
---
**🌱 Environmental Impact Dashboard** | Desenvolvido com Big Data Analytics (MapReduce), Machine Learning (Random Forest, K-Means)  
📚 [Portfólio de Pesquisa](https://amaurialmeida.github.io/environmental-portfolio/)
""")

if bdp:
    bdp.stop()
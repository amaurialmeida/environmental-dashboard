# app.py - Versão Corrigida para Streamlit Cloud
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

# ------------------------------
# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Environmental Impact Dashboard", 
    layout="wide", 
    page_icon="🌍"
)

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
    .stMetric {
        background-color: white;
        padding: 10px;
        border-radius: 8px;
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
    # Cria o diretório data/processed se não existir
    data_dir = Path('data/processed')
    data_dir.mkdir(parents=True, exist_ok=True)
    
    data_path = data_dir / 'portfolio_impact_data.parquet'
    
    if data_path.exists():
        st.info("📁 Carregando dados processados do arquivo...")
        df = pd.read_parquet(data_path)
    else:
        st.info("⚙️ Gerando dataset de impacto (simulação realista baseada no portfólio)...")
        df = generate_impact_dataset()
        df.to_parquet(data_path, index=False)
        st.success("✅ Dataset gerado e salvo com sucesso!")
    
    return df

# Tenta carregar os dados com tratamento de erro
try:
    df = load_data()
    st.success(f"📊 Dados carregados: {len(df):,} registros de impacto ambiental")
except Exception as e:
    st.error(f"❌ Erro ao carregar dados: {str(e)}")
    st.stop()

# ------------------------------
# INICIALIZAÇÃO DO BIG DATA PROCESSOR (VERSÃO CORRIGIDA)
# Inicializa processamento Big Data com fallback
try:
    bdp = BigDataProcessor('data/processed/portfolio_impact_data.parquet')
    st.success("✅ Big Data Processor inicializado com sucesso")
except Exception as e:
    st.warning(f"⚠️ Modo de fallback: usando processamento padrão (sem Big Data) - {str(e)[:100]}")
    bdp = None

# Inicializa modelos de Data Science
try:
    ds_models = DataScienceModels(df)
    st.success("✅ Modelos de Data Science carregados")
except Exception as e:
    st.error(f"❌ Erro ao carregar modelos: {str(e)}")
    ds_models = None

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
cars_equivalent = carbon_tonnes / 4.6  # Média: 4.6 tCO2e por carro/ano

# Exibe KPIs em cards
st.markdown("### 📊 Impacto Acumulado (Agosto/2016 - Maio/2026)")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="⚡ Energia Total Produzida", 
        value=f"{total_energy_mwh:,.0f} MWh", 
        delta=f"{energy_gwh:.1f} GWh",
        delta_color="normal"
    )

with col2:
    st.metric(
        label="🌿 Carbono Poupado", 
        value=f"{total_carbon_tco2e:,.0f} tCO₂e", 
        delta="Desde Ago/2016",
        delta_color="off"
    )

with col3:
    st.metric(
        label="🌳 Equivalente em Árvores", 
        value=f"{trees_equivalent:,.0f}", 
        delta="plantadas/ano",
        delta_color="off"
    )

with col4:
    st.metric(
        label="🚗 Carros a Menos nas Ruas", 
        value=f"{cars_equivalent:,.0f}", 
        delta="por ano",
        delta_color="off"
    )

st.divider()

# ------------------------------
# GRÁFICOS PRINCIPAIS
tab1, tab2, tab3, tab4 = st.tabs(["📈 Evolução Temporal", "🔍 Projetos em Detalhe", "🤖 Data Science & ML", "🗺️ Análise Geográfica"])

# TAB 1: EVOLUÇÃO TEMPORAL
with tab1:
    st.subheader("Evolução do Impacto Ambiental (2016-2026)")
    
    # Agregação mensal (com ou sem Big Data)
    if bdp:
        try:
            monthly_agg = bdp.aggregate_by_time('monthly')
            st.caption("📊 Processado com tecnologia Big Data (Dask)")
        except Exception as e:
            st.warning(f"Erro no processamento Big Data, usando fallback: {str(e)[:50]}")
            monthly_agg = df.groupby(['year', 'month'])[['energy_produced_mwh', 'carbon_saved_tco2e']].sum().reset_index()
    else:
        monthly_agg = df.groupby(['year', 'month'])[['energy_produced_mwh', 'carbon_saved_tco2e']].sum().reset_index()
    
    # Cria coluna de data para o gráfico
    monthly_agg['date'] = pd.to_datetime(monthly_agg['year'].astype(str) + '-' + monthly_agg['month'].astype(str) + '-01')
    
    # Gráfico de linha interativo com Plotly
    fig_line = go.Figure()
    
    fig_line.add_trace(go.Scatter(
        x=monthly_agg['date'], 
        y=monthly_agg['energy_produced_mwh'], 
        name='Energia (MWh)', 
        line=dict(color='#FFD700', width=3),
        fill='tozeroy',
        fillcolor='rgba(255, 215, 0, 0.2)'
    ))
    
    fig_line.add_trace(go.Scatter(
        x=monthly_agg['date'], 
        y=monthly_agg['carbon_saved_tco2e'], 
        name='Carbono (tCO₂e)', 
        line=dict(color='#2E7D32', width=3),
        fill='tozeroy',
        fillcolor='rgba(46, 125, 50, 0.2)'
    ))
    
    fig_line.update_layout(
        title="📈 Série Temporal do Impacto Ambiental",
        xaxis_title="Data",
        yaxis_title="Impacto",
        hovermode='x unified',
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
        height=500
    )
    
    st.plotly_chart(fig_line, use_container_width=True)
    
    # Gráfico de área acumulada
    df_cumulative = df_filtered.sort_values('date')
    df_cumulative['cumulative_energy'] = df_cumulative['energy_produced_mwh'].cumsum()
    df_cumulative['cumulative_carbon'] = df_cumulative['carbon_saved_tco2e'].cumsum()
    
    fig_area = px.area(
        df_cumulative, 
        x='date', 
        y='cumulative_energy',
        title="📊 Energia Acumulada ao Longo do Tempo",
        labels={'date': 'Data', 'cumulative_energy': 'Energia Acumulada (MWh)'},
        color_discrete_sequence=['#FF8C00']
    )
    
    fig_area.update_layout(height=400)
    st.plotly_chart(fig_area, use_container_width=True)
    
    # Métricas anuais
    st.subheader("📅 Impacto por Ano")
    yearly_agg = df.groupby('year').agg({
        'energy_produced_mwh': 'sum',
        'carbon_saved_tco2e': 'sum'
    }).reset_index()
    
    col1, col2 = st.columns(2)
    with col1:
        fig_yearly_energy = px.bar(
            yearly_agg, 
            x='year', 
            y='energy_produced_mwh',
            title="Energia Produzida por Ano",
            labels={'year': 'Ano', 'energy_produced_mwh': 'Energia (MWh)'},
            color='energy_produced_mwh',
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig_yearly_energy, use_container_width=True)
    
    with col2:
        fig_yearly_carbon = px.bar(
            yearly_agg, 
            x='year', 
            y='carbon_saved_tco2e',
            title="Carbono Poupado por Ano",
            labels={'year': 'Ano', 'carbon_saved_tco2e': 'Carbono (tCO₂e)'},
            color='carbon_saved_tco2e',
            color_continuous_scale='Greens'
        )
        st.plotly_chart(fig_yearly_carbon, use_container_width=True)

# TAB 2: PROJETOS EM DETALHE
with tab2:
    st.subheader("Detalhamento por Projeto de Pesquisa")
    
    # Top projetos (com ou sem Big Data)
    if bdp:
        try:
            top_carbon = bdp.top_projects_by_impact('carbon_saved_tco2e', 5)
            st.caption("🏆 Ranking calculado com Big Data")
        except:
            top_carbon = df.groupby('project_name')['carbon_saved_tco2e'].sum().nlargest(5).reset_index()
            top_carbon.columns = ['project_name', 'total_carbon_saved_tco2e']
    else:
        top_carbon = df.groupby('project_name')['carbon_saved_tco2e'].sum().nlargest(5).reset_index()
        top_carbon.columns = ['project_name', 'total_carbon_saved_tco2e']
    
    fig_bar = px.bar(
        top_carbon, 
        x='project_name', 
        y='total_carbon_saved_tco2e', 
        title="🏆 Top 5 Projetos que Mais Pouparam Carbono",
        labels={'project_name': 'Projeto', 'total_carbon_saved_tco2e': 'Carbono Poupado (tCO₂e)'},
        color='total_carbon_saved_tco2e',
        color_continuous_scale='Greens',
        text='total_carbon_saved_tco2e'
    )
    
    fig_bar.update_traces(texttemplate='%{text:.0f}', textposition='outside')
    fig_bar.update_layout(height=500)
    st.plotly_chart(fig_bar, use_container_width=True)
    
    # Tabela interativa com todos os projetos
    project_summary = df.groupby('project_name').agg({
        'energy_produced_mwh': 'sum',
        'carbon_saved_tco2e': 'sum',
        'date': ['min', 'max']
    }).round(0)
    
    project_summary.columns = ['Energia (MWh)', 'Carbono (tCO₂e)', 'Data Início', 'Data Fim']
    project_summary = project_summary.reset_index()
    
    # Adiciona métricas de eficiência
    project_summary['Eficiência (kgCO₂e/MWh)'] = (project_summary['Carbono (tCO₂e)'] * 1000 / project_summary['Energia (MWh)']).fillna(0).round(2)
    
    st.dataframe(
        project_summary, 
        use_container_width=True, 
        height=400,
        column_config={
            "Energia (MWh)": st.column_config.NumberColumn(format="%.0f"),
            "Carbono (tCO₂e)": st.column_config.NumberColumn(format="%.0f"),
            "Eficiência (kgCO₂e/MWh)": st.column_config.NumberColumn(format="%.2f")
        }
    )
    
    # Projetos por tipo (gráfico de rosca)
    col1, col2 = st.columns(2)
    
    with col1:
        type_impact = df.groupby('project_type')['carbon_saved_tco2e'].sum().reset_index()
        fig_donut = px.pie(
            type_impact, 
            values='carbon_saved_tco2e', 
            names='project_type', 
            title="Distribuição do Carbono por Tipo de Projeto",
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.Greens_r
        )
        st.plotly_chart(fig_donut, use_container_width=True)
    
    with col2:
        # Impacto médio mensal por tipo
        monthly_type = df.groupby(['project_type', 'year', 'month'])['carbon_saved_tco2e'].mean().reset_index()
        monthly_type['date'] = pd.to_datetime(monthly_type['year'].astype(str) + '-' + monthly_type['month'].astype(str) + '-01')
        
        fig_line_type = px.line(
            monthly_type,
            x='date',
            y='carbon_saved_tco2e',
            color='project_type',
            title="Média Mensal de Carbono Poupado por Tipo"
        )
        st.plotly_chart(fig_line_type, use_container_width=True)

# TAB 3: DATA SCIENCE & MACHINE LEARNING
with tab3:
    st.subheader("🤖 Aplicações de Data Science e Machine Learning")
    
    # Explicação da arquitetura Big Data
    with st.expander("🏗️ Arquitetura Big Data Analytics Implementada", expanded=False):
        st.markdown("""
        **Conceitos de Big Data aplicados neste dashboard:**
        
        1. **Particionamento de Dados** - Dados divididos em partições para processamento paralelo
        2. **Processamento Distribuído** - Simulação de cluster com MapReduce
        3. **Escalabilidade Horizontal** - Arquitetura preparada para milhões de registros
        4. **Lazy Evaluation** - Operações definidas mas executadas sob demanda
        5. **Fault Tolerance** - Tolerância a falhas com fallback automático
        """)
        
        if bdp:
            concepts = bdp.explain_big_data_concepts()
            for concept, description in concepts.items():
                st.info(f"**{concept}:** {description}")
    
    if ds_models:
        # Previsão de séries temporais
        st.markdown("### 🔮 Previsão de Carbono Poupado")
        st.caption("Modelo Holt-Winters com detecção de sazonalidade (12 meses)")
        
        try:
            forecast_df, forecast_fig = ds_models.forecast_impact(periods=12)
            st.plotly_chart(forecast_fig, use_container_width=True)
            
            # Métrica de previsão para Maio/2026
            may_2026_forecast = forecast_df[forecast_df['date'] == datetime(2026, 5, 1)]
            if not may_2026_forecast.empty:
                st.metric(
                    "📅 Previsão para Maio/2026",
                    f"{may_2026_forecast['forecast_carbon_tco2e'].values[0]:.0f} tCO₂e",
                    delta="estimado"
                )
        except Exception as e:
            st.error(f"Erro na previsão temporal: {str(e)[:100]}")
        
        # Clustering de projetos
        st.markdown("### 🎯 Agrupamento de Projetos por Similaridade")
        st.caption("Algoritmo K-Means para identificar padrões de impacto")
        
        try:
            clusters_df, clusters_fig = ds_models.project_similarity_clustering()
            st.plotly_chart(clusters_fig, use_container_width=True)
            
            # Exibe cluster assignments
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"**Cluster 0 (Alto Impacto):** {len(clusters_df[clusters_df['cluster'] == 0])} projetos")
            with col2:
                st.info(f"**Cluster 1 (Médio Impacto):** {len(clusters_df[clusters_df['cluster'] == 1])} projetos")
        except Exception as e:
            st.error(f"Erro no clustering: {str(e)[:100]}")
        
        # Feature Importance
        st.markdown("### 🔍 O que mais influencia o Carbono Poupado?")
        st.caption("Random Forest Regressor - Importância das Features")
        
        try:
            feat_df, feat_fig = ds_models.feature_importance()
            st.plotly_chart(feat_fig, use_container_width=True)
            
            # Tabela de importância
            st.dataframe(
                feat_df.head(10),
                use_container_width=True,
                column_config={
                    "feature": "Variável",
                    "importance": st.column_config.ProgressColumn("Importância", format="%.3f")
                }
            )
        except Exception as e:
            st.error(f"Erro no cálculo de importância: {str(e)[:100]}")
    else:
        st.error("❌ Modelos de Data Science não disponíveis")

# TAB 4: ANÁLISE GEOGRÁFICA
with tab4:
    st.subheader("🗺️ Distribuição Geográfica do Impacto")
    
    # Simulação de coordenadas para os projetos
    region_coords = {
        'Brasil': (-14.2350, -51.9253),
        'SP, Brasil': (-23.5505, -46.6333),
        'MG, SP, PR': (-19.1834, -47.3018),
        'Fernandópolis, SP': (-20.2839, -50.2464),
        'Chile & Argentina': (-35.6751, -71.5430),
        'Chile': (-35.6751, -71.5430),
        'Global': (0, 0)
    }
    
    geo_data = df.groupby('region')[['energy_produced_mwh', 'carbon_saved_tco2e']].sum().reset_index()
    geo_data['lat'] = geo_data['region'].apply(lambda x: region_coords.get(x, (-15, -50))[0])
    geo_data['lon'] = geo_data['region'].apply(lambda x: region_coords.get(x, (-15, -50))[1])
    
    # Mapa de calor geográfico
    fig_map = px.scatter_geo(
        geo_data, 
        lat='lat', 
        lon='lon', 
        size='carbon_saved_tco2e',
        hover_name='region',
        text='region',
        projection="natural earth",
        title="🌎 Carbono Poupado por Região (tCO₂e)",
        size_max=60,
        color='energy_produced_mwh',
        color_continuous_scale='Viridis',
        scope="south america"
    )
    
    fig_map.update_layout(height=600)
    st.plotly_chart(fig_map, use_container_width=True)
    
    # Gráfico de barras regional
    st.subheader("Comparativo Regional")
    fig_regional_bar = px.bar(
        geo_data,
        x='region',
        y=['energy_produced_mwh', 'carbon_saved_tco2e'],
        title="Impacto por Região",
        barmode='group',
        labels={'value': 'Impacto', 'region': 'Região', 'variable': 'Métrica'},
        color_discrete_map={
            'energy_produced_mwh': '#FFD700',
            'carbon_saved_tco2e': '#2E7D32'
        }
    )
    
    st.plotly_chart(fig_regional_bar, use_container_width=True)
    
    # Análise de correlação regional
    st.subheader("📊 Correlação entre Energia e Carbono por Região")
    fig_scatter = px.scatter(
        geo_data,
        x='energy_produced_mwh',
        y='carbon_saved_tco2e',
        text='region',
        size='carbon_saved_tco2e',
        title="Relação Energia vs Carbono por Região",
        labels={'energy_produced_mwh': 'Energia Produzida (MWh)', 'carbon_saved_tco2e': 'Carbono Poupado (tCO₂e)'},
        color='region'
    )
    
    st.plotly_chart(fig_scatter, use_container_width=True)

# ------------------------------
# RODAPÉ COM INFORMAÇÕES TÉCNICAS
st.divider()

with st.expander("📌 Informações Técnicas e Metodologia", expanded=False):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**🔬 Big Data Analytics**")
        st.markdown("""
        - Processamento particionado
        - Escalabilidade horizontal
        - Simulação MapReduce
        - Dask para computação paralela
        """)
    
    with col2:
        st.markdown("**🤖 Data Science**")
        st.markdown("""
        - Holt-Winters (previsão)
        - K-Means (clustering)
        - Random Forest (feature importance)
        - Análise de séries temporais
        """)
    
    with col3:
        st.markdown("**📊 Dados e Fontes**")
        st.markdown(f"""
        - Período: Ago/2016 - Mai/2026
        - Projetos: 10 ativos
        - Registros: {len(df):,}
        - Update: Automático (cache 1h)
        """)

st.markdown("""
---
**🌱 Environmental Impact Dashboard** | Desenvolvido com ❤️ usando Streamlit, Plotly e Data Science  
📚 [Portfólio de Pesquisa Ambiental](https://amaurialmeida.github.io/environmental-portfolio/) | 🐙 [GitHub Repository](https://github.com/amaurialmeida/environmental-dashboard)
""")

# ------------------------------
# CLEANUP
if bdp:
    bdp.stop()
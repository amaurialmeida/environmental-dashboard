import streamlit as st

st.set_page_config(page_title="Greenlog • Environmental Intelligence", 
                   page_icon="🌱", layout="wide", initial_sidebar_state="collapsed")

html_code = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body { margin: 0; padding: 0; background: #050505; color: white; font-family: 'Segoe UI', sans-serif; overflow: hidden; }
        .header { text-align: center; padding: 25px 0 15px 0; border-bottom: 1px solid rgba(46,204,113,0.3); position: relative; }
        .title { 
            font-size: 4.8rem; 
            background: linear-gradient(90deg, #2ecc71, #3498db);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            margin: 0; letter-spacing: 6px;
        }
        .subtitle { color: #2ecc71; font-size: 1.75rem; margin: 8px 0 30px 0; }
        .lang-buttons {
            position: absolute; top: 35px; right: 40px; display: flex; gap: 8px;
        }
        .lang-btn {
            padding: 8px 16px; background: rgba(46,204,113,0.15); color: #2ecc71;
            border: 1px solid #2ecc71; border-radius: 30px; cursor: pointer;
            font-size: 0.95rem; transition: all 0.3s;
        }
        .lang-btn:hover, .lang-btn.active { background: #2ecc71; color: black; }

        .slide-container {
            display: flex; justify-content: center; align-items: center;
            min-height: 65vh; transition: opacity 0.8s;
        }
        .kpi-card {
            background: rgba(15, 25, 40, 0.95);
            border: 2px solid #2ecc71;
            border-radius: 20px;
            padding: 40px 30px;
            width: 360px;
            text-align: center;
            box-shadow: 0 0 40px rgba(46, 204, 113, 0.4);
            margin: 12px;
        }
        .kpi-number { font-size: 4.1rem; font-weight: bold; color: #2ecc71; margin: 15px 0; }
        .kpi-label { font-size: 1.3rem; color: #ddd; margin-bottom: 10px; }
        .delta { font-size: 1.55rem; font-weight: bold; }

        .bottom-bar {
            position: fixed; bottom: 0; left: 0; right: 0;
            background: rgba(10,20,35,0.95); padding: 14px 0;
            border-top: 2px solid #2ecc71; text-align: center;
            font-size: 0.95rem; color: #aaa;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="lang-buttons">
            <div class="lang-btn active" id="btn-pt" onclick="setLanguage('pt')">🇧🇷 PT</div>
            <div class="lang-btn" id="btn-en" onclick="setLanguage('en')">🇺🇸 EN</div>
            <div class="lang-btn" id="btn-es" onclick="setLanguage('es')">🇪🇸 ES</div>
        </div>
        <div class="title" id="main-title">GREENLOG</div>
        <div class="subtitle" id="main-subtitle">Dados para um planeta mais verde!</div>
    </div>
    
    <div id="slideContainer" class="slide-container"></div>

    <div class="bottom-bar" id="bottom-text">
        👇 Clique nos botões acima ou aguarde a transição automática
    </div>

    <script>
        let currentLang = 'pt';
        let currentSlide = 0;

        const translations = {
            pt: { title: "GREENLOG", subtitle: "Dados para um planeta mais verde!", bottom: "👇 Clique nos botões acima ou aguarde a transição automática" },
            en: { title: "GREENLOG", subtitle: "Data for a greener planet!", bottom: "👇 Click above or wait for automatic transition" },
            es: { title: "GREENLOG", subtitle: "¡Datos para un planeta más verde!", bottom: "👇 Haz clic arriba o espera la transición automática" }
        };

        const themes = [
            {name: {pt:"🌍 Temperaturas Globais", en:"🌍 Global Temperatures", es:"🌍 Temperaturas Globales"}, 
             kpis: [
                {label:{pt:"Temperatura Média Global",en:"Global Average Temperature",es:"Temperatura Media Global"}, value:14.92, unit:"°C", delta:"↑ 1.45%"},
                {label:{pt:"Ano Mais Quente",en:"Hottest Year",es:"Año Más Caliente"}, value:2025, unit:"", delta:"↑ 0.9%"},
                {label:{pt:"Anomalia Atual",en:"Current Anomaly",es:"Anomalía Actual"}, value:1.54, unit:"°C", delta:"↑ 15%"}
            ]},
            {name: {pt:"☀️ Energia Solar", en:"☀️ Solar Energy", es:"☀️ Energía Solar"}, 
             kpis: [
                {label:{pt:"Energia Gerada",en:"Energy Generated",es:"Energía Generada"}, value:390, unit:"MWh", delta:""},
                {label:{pt:"CO₂ Evitado",en:"CO₂ Avoided",es:"CO₂ Evitado"}, value:953, unit:"t", delta:""},
                {label:{pt:"Árvores Equivalentes",en:"Equivalent Trees",es:"Árboles Equivalentes"}, value:7250, unit:"", delta:""}
            ]},
            {name: {pt:"🐝 Colapso das Abelhas", en:"🐝 Bee Collapse", es:"🐝 Colapso de Abejas"}, 
             kpis: [
                {label:{pt:"Colmeias Perdidas",en:"Lost Hives",es:"Colmenas Perdidas"}, value:338, unit:"", delta:""},
                {label:{pt:"Abelhas Perdidas",en:"Bees Lost",es:"Abejas Perdidas"}, value:20000000, unit:"", delta:""},
                {label:{pt:"Colmeias RS (2024)",en:"RS Hives (2024)",es:"Colmenas RS (2024)"}, value:6300, unit:"", delta:""}
            ]},
            {name: {pt:"🐝 Abelhas sem Ferrão", en:"🐝 Stingless Bees", es:"🐝 Abejas sin Aguijón"}, 
             kpis: [
                {label:{pt:"Espécies Monitoradas",en:"Monitored Species",es:"Especies Monitoreadas"}, value:18, unit:"", delta:""},
                {label:{pt:"Registros GBIF",en:"GBIF Records",es:"Registros GBIF"}, value:24500, unit:"", delta:""},
                {label:{pt:"Estados Cobertos",en:"Covered States",es:"Estados Cubiertos"}, value:15, unit:"", delta:""},
                {label:{pt:"Espécies Ameaçadas",en:"Threatened Species",es:"Especies Amenazadas"}, value:4, unit:"VU", delta:""}
            ]},
            {name: {pt:"🌬️ Potencial Eólico", en:"🌬️ Wind Potential", es:"🌬️ Potencial Eólico"}, 
             kpis: [
                {label:{pt:"Velocidade Média",en:"Average Speed",es:"Velocidad Media"}, value:30.2, unit:"km/h", delta:""},
                {label:{pt:"Fator de Capacidade",en:"Capacity Factor",es:"Factor de Capacidad"}, value:60, unit:"%", delta:""},

import streamlit as st

st.set_page_config(page_title="Greenlog • Environmental Intelligence", 
                   page_icon="🌱", layout="wide", initial_sidebar_state="collapsed")

html_code = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body { 
            margin: 0; padding: 0; background: #050505; color: white; 
            font-family: 'Segoe UI', sans-serif; overflow: hidden;
        }
        .header { 
            text-align: center; 
            padding: 20px 0 10px 0;
            position: relative;
            z-index: 10;
            background: rgba(5, 5, 5, 0.7);
            backdrop-filter: blur(5px);
        }
        .main-title { 
            font-size: 2.7rem; 
            color: #2ecc71;
            margin: 8px 0 12px 0;
            font-weight: 500;
            text-shadow: 0 0 15px rgba(46, 204, 113, 0.5);
        }
        .lang-buttons {
            display: flex; 
            justify-content: center; 
            gap: 10px;
            margin-bottom: 20px;
        }
        .lang-btn {
            padding: 7px 16px; 
            background: rgba(46,204,113,0.12); 
            color: #2ecc71;
            border: 1px solid #2ecc71; 
            border-radius: 30px; 
            cursor: pointer;
            font-size: 0.9rem; 
            transition: all 0.3s;
            display: flex;
            align-items: center;
            gap: 7px;
        }
        .lang-btn:hover, .lang-btn.active { 
            background: #2ecc71; 
            color: black; 
        }

        /* Container do Mapa Windy */
        .map-background {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 1;
            opacity: 0.6; /* Ajuste para transparência do mapa */
            filter: hue-rotate(-15deg) brightness(0.8) contrast(1.2); /* Ajuste para tons mais verdes/azuis */
        }

        .slide-container {
            display: flex; 
            flex-direction: column;
            justify-content: center; 
            align-items: center;
            min-height: 70vh; 
            padding-top: 10px;
            position: relative;
            z-index: 5;
        }
        
        .kpi-wrapper {
            display: flex;
            gap: 18px;
            justify-content: center;
            flex-wrap: wrap;
            perspective: 1000px;
        }

        .kpi-card {
            background: rgba(10, 20, 35, 0.85);
            border: 2px solid #2ecc71;
            border-radius: 20px;
            padding: 35px 25px;
            width: 320px;
            text-align: center;
            box-shadow: 0 0 35px rgba(46, 204, 113, 0.3);
            margin: 8px;
            backdrop-filter: blur(10px);
            transition: transform 0.5s ease;
        }
        
        .kpi-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 0 50px rgba(46, 204, 113, 0.5);
        }

        .kpi-number { 
            font-size: 3.9rem; 
            font-weight: bold; 
            color: #2ecc71; 
            margin: 10px 0; 
            text-shadow: 0 0 10px rgba(46, 204, 113, 0.4);
        }
        .kpi-label { 
            font-size: 1.2rem; 
            color: #ddd; 
            margin-bottom: 8px; 
        }
        .delta { 
            font-size: 1.45rem; 
            font-weight: bold; 
        }

        .bottom-bar {
            position: fixed; 
            bottom: 0; left: 0; right: 0;
            background: rgba(10, 20, 35, 0.9); 
            padding: 12px 0;
            border-top: 2px solid #2ecc71; 
            text-align: center;
            font-size: 0.9rem; 
            color: #aaa;
            z-index: 10;
            backdrop-filter: blur(5px);
        }
        
        /* Overlay para escurecer o mapa e focar nos cards */
        .overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle, rgba(5,5,5,0.2) 0%, rgba(5,5,5,0.8) 100%);
            z-index: 2;
            pointer-events: none;
        }
    </style>
</head>
<body>
    <!-- Mapa Windy como Background -->
    <div class="map-background">
        <iframe 
            width="100%" 
            height="100%" 
            src="https://embed.windy.com/embed2.html?lat=-15.783&lon=-47.867&detailLat=-15.783&detailLon=-47.867&width=1200&height=800&zoom=3&level=surface&overlay=wind&product=ecmwf&menu=&message=&marker=&calendar=now&pressure=&type=map&location=coordinates&detail=&metricWind=km%2Fh&metricTemp=%C2%B0C&radarRange=-1" 
            frameborder="0"
            style="border:0;">
        </iframe>
    </div>
    
    <div class="overlay"></div>

    <div class="header">
        <div class="main-title" id="main-title">Dados para um planeta mais verde!</div>
        
        <div class="lang-buttons">
            <div class="lang-btn active" id="btn-pt" onclick="setLanguage('pt')">🇧🇷 Português</div>
            <div class="lang-btn" id="btn-en" onclick="setLanguage('en')">🇬🇧 English</div>
            <div class="lang-btn" id="btn-es" onclick="setLanguage('es')">🇪🇸 Español</div>
        </div>
    </div>
    
    <div id="slideContainer" class="slide-container"></div>

    <div class="bottom-bar" id="bottom-text">
        👇 Clique nos botões acima ou aguarde a transição automática
    </div>

    <script>
        let currentLang = 'pt';
        let currentSlide = 0;

        const translations = {
            pt: { title: "Dados para um planeta mais verde!", bottom: "👇 Clique nos botões acima ou aguarde a transição automática" },
            en: { title: "Data for a greener planet!", bottom: "👇 Click above or wait for automatic transition" },
            es: { title: "¡Datos para un planeta más verde!", bottom: "👇 Haz clic arriba o espera la transición automática" }
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
                {label:{pt:"Rajada Máxima",en:"Max Gust",es:"Ráfaga Máxima"}, value:130, unit:"km/h", delta:""},
                {label:{pt:"Potencial Total",en:"Total Potential",es:"Potencial Total"}, value:9500, unit:"MW", delta:""}
            ]},
            {name: {pt:"💧 Qualidade da Água", en:"💧 Water Quality", es:"💧 Calidad del Agua"}, 
             kpis: [
                {label:{pt:"IQA Médio",en:"Average IQA",es:"IQA Medio"}, value:81.9, unit:"", delta:""},
                {label:{pt:"Estações Excelente",en:"Excellent Stations",es:"Estaciones Excelentes"}, value:3, unit:"/18", delta:""},
                {label:{pt:"Rios Monitorados",en:"Monitored Rivers",es:"Ríos Monitoreados"}, value:10, unit:"", delta:""}
            ]},
            {name: {pt:"🌋 Monitoramento Sísmico", en:"🌋 Seismic Monitoring", es:"🌋 Monitoreo Sísmico"}, 
             kpis: [
                {label:{pt:"Magnitude",en:"Magnitude",es:"Magnitud"}, value:7.4, unit:"", delta:""},
                {label:{pt:"Profundidade",en:"Depth",es:"Profundidad"}, value:10, unit:"km", delta:""},
                {label:{pt:"Evacuados",en:"Evacuated",es:"Evacuados"}, value:1800, unit:"", delta:""},
                {label:{pt:"Réplicas",en:"Aftershocks",es:"Réplicas"}, value:50, unit:"+", delta:""}
            ]},
            {name: {pt:"🌿 Espécies Invasoras", en:"🌿 Invasive Species", es:"🌿 Especies Invasoras"}, 
             kpis: [
                {label:{pt:"Castores Estimados",en:"Estimated Beavers",es:"Castores Estimados"}, value:110000, unit:"+", delta:""},
                {label:{pt:"Hectares Devastados",en:"Devastated Hectares",es:"Hectáreas Devastadas"}, value:31000, unit:"ha", delta:""},
                {label:{pt:"Represas Construídas",en:"Dams Built",es:"Represas Construidas"}, value:70600, unit:"", delta:""}
            ]},
            {name: {pt:"🌊 El Niño 2026", en:"🌊 El Niño 2026", es:"🌊 El Niño 2026"}, 
             kpis: [
                {label:{pt:"Probabilidade",en:"Probability",es:"Probabilidad"}, value:98, unit:"%", delta:""},
                {label:{pt:"Niño 3.4 Atual",en:"Current Niño 3.4",es:"Niño 3.4 Actual"}, value:0.9, unit:"°C", delta:""},
                {label:{pt:"Previsão Pico",en:"Peak Forecast",es:"Previsión Pico"}, value:2.4, unit:"°C", delta:""},
                {label:{pt:"Super El Niño",en:"Super El Niño",es:"Super El Niño"}, value:33, unit:"%", delta:""}
            ]}
        ];

        function setLanguage(lang) {
            currentLang = lang;
            document.getElementById('main-title').textContent = translations[lang].title;
            document.getElementById('bottom-text').textContent = translations[lang].bottom;
            document.querySelectorAll('.lang-btn').forEach(btn => btn.classList.remove('active'));
            document.getElementById('btn-' + lang).classList.add('active');
            showSlide(currentSlide);
        }

        function animateCount(element, end, duration = 2000) {
            let start = 0;
            const startTime = Date.now();
            function update() {
                const now = Date.now();
                const progress = Math.min((now - startTime) / duration, 1);
                const value = (progress * (end - start) + start);
                
                // Formatação para decimais ou inteiros
                if (end % 1 !== 0) {
                    element.textContent = value.toFixed(2).replace('.', ',');
                } else {
                    element.textContent = Math.floor(value).toLocaleString('pt-BR');
                }
                
                if (progress < 1) requestAnimationFrame(update);
                else {
                    if (end % 1 !== 0) element.textContent = end.toFixed(2).replace('.', ',');
                    else element.textContent = end.toLocaleString('pt-BR');
                }
            }
            update();
        }

        function showSlide(index) {
            const container = document.getElementById('slideContainer');
            const theme = themes[index];
            const lang = currentLang;
            
            let html = `<h2 style="text-align:center; color:#2ecc71; margin-bottom:25px; text-shadow: 0 0 10px rgba(46, 204, 113, 0.4); font-size: 2rem;">${theme.name[lang]}</h2>`;
            html += '<div class="kpi-wrapper">';
            
            theme.kpis.forEach((kpi, i) => {
                html += `
                <div class="kpi-card">
                    <div class="kpi-number" id="num${index}_${i}">0</div>
                    <div class="kpi-label">${kpi.label[lang]} ${kpi.unit}</div>
                    <div class="delta" style="color:#2ecc71;">${kpi.delta}</div>
                </div>`;
            });
            html += '</div>';
            
            container.innerHTML = html;
            
            // Pequeno delay para a animação começar após o render
            setTimeout(() => {
                theme.kpis.forEach((kpi, i) => {
                    const el = document.getElementById(`num${index}_${i}`);
                    if (el) animateCount(el, kpi.value);
                });
            }, 300);
        }

        // Inicialização
        showSlide(0);

        // Timer de transição automática (15 segundos)
        setInterval(() => {
            currentSlide = (currentSlide + 1) % themes.length;
            showSlide(currentSlide);
        }, 15000);
    </script>
</body>
</html>
"""

st.components.v1.html(html_code, height=800, scrolling=False)

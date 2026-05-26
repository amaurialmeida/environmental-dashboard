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
            text-align: center; padding: 20px 0 10px 0; border-bottom: 1px solid rgba(46,204,113,0.3);
        }
        .title { 
            font-size: 4.8rem; 
            background: linear-gradient(90deg, #2ecc71, #3498db);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            margin: 0; letter-spacing: 6px;
        }
        .subtitle { 
            color: #2ecc71; font-size: 1.8rem; margin: 5px 0 25px 0;
        }
        .lang-buttons {
            position: absolute; top: 35px; right: 40px; display: flex; gap: 8px;
        }
        .lang-btn {
            padding: 8px 14px; background: rgba(46,204,113,0.15); color: #2ecc71;
            border: 1px solid #2ecc71; border-radius: 30px; cursor: pointer;
            font-size: 0.95rem; transition: all 0.3s;
        }
        .lang-btn:hover { background: #2ecc71; color: black; }

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
            margin: 10px;
        }
        .kpi-number {
            font-size: 4.1rem;
            font-weight: bold;
            color: #2ecc71;
            margin: 15px 0;
        }
        .kpi-label {
            font-size: 1.3rem;
            color: #ddd;
            margin-bottom: 10px;
        }
        .delta {
            font-size: 1.55rem;
            font-weight: bold;
        }
        .bottom-bar {
            position: fixed; bottom: 0; left: 0; right: 0;
            background: rgba(10,20,35,0.95); padding: 12px 0;
            border-top: 2px solid #2ecc71; text-align: center;
            font-size: 1.1rem; color: #2ecc71;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="lang-buttons">
            <div class="lang-btn" onclick="changeLang('pt')">🇧🇷 PT</div>
            <div class="lang-btn" onclick="changeLang('en')">🇺🇸 EN</div>
            <div class="lang-btn" onclick="changeLang('es')">🇪🇸 ES</div>
        </div>
        <div class="title">GREENLOG</div>
        <div class="subtitle">Dados para um planeta mais verde!</div>
    </div>
    
    <div id="slideContainer" class="slide-container"></div>

    <div class="bottom-bar">
        👇 Clique nos botões acima ou aguarde a transição automática • Projetos do Portfólio
    </div>

    <script>
        const themes = [
            {name: "🌍 Temperaturas Globais", kpis: [
                {label: "Temperatura Média Global", value: 14.92, unit: "°C", delta: "↑ 1.45%"},
                {label: "Ano Mais Quente", value: 2025, unit: "", delta: "↑ 0.9%"},
                {label: "Anomalia Atual", value: 1.54, unit: "°C", delta: "↑ 15%"}
            ]},
            {name: "☀️ Energia Solar", kpis: [
                {label: "Energia Gerada", value: 390, unit: "MWh", delta: ""},
                {label: "CO₂ Evitado", value: 953, unit: "t", delta: ""},
                {label: "Árvores Equivalentes", value: 7250, unit: "", delta: ""}
            ]},
            {name: "🐝 Colapso das Abelhas", kpis: [
                {label: "Colmeias Perdidas", value: 338, unit: "", delta: ""},
                {label: "Abelhas Perdidas", value: 20000000, unit: "", delta: ""},
                {label: "Colmeias RS (2024)", value: 6300, unit: "", delta: ""}
            ]},
            {name: "🐝 Abelhas sem Ferrão", kpis: [
                {label: "Espécies Monitoradas", value: 18, unit: "", delta: ""},
                {label: "Registros GBIF", value: 24500, unit: "", delta: ""},
                {label: "Estados Cobertos", value: 15, unit: "", delta: ""},
                {label: "Espécies Ameaçadas", value: 4, unit: "VU", delta: ""}
            ]},
            {name: "🌬️ Potencial Eólico", kpis: [
                {label: "Velocidade Média", value: 30.2, unit: "km/h", delta: ""},
                {label: "Fator de Capacidade", value: 60, unit: "%", delta: ""},
                {label: "Rajada Máxima", value: 130, unit: "km/h", delta: ""},
                {label: "Potencial Total", value: 9500, unit: "MW", delta: ""}
            ]},
            {name: "💧 Qualidade da Água", kpis: [
                {label: "IQA Médio", value: 81.9, unit: "", delta: ""},
                {label: "Estações Excelente", value: 3, unit: "/18", delta: ""},
                {label: "Rios Monitorados", value: 10, unit: "", delta: ""}
            ]},
            {name: "🌋 Monitoramento Sísmico", kpis: [
                {label: "Magnitude", value: 7.4, unit: "", delta: ""},
                {label: "Profundidade", value: 10, unit: "km", delta: ""},
                {label: "Evacuados", value: 1800, unit: "", delta: ""},
                {label: "Réplicas", value: 50, unit: "+", delta: ""}
            ]},
            {name: "🌿 Espécies Invasoras", kpis: [
                {label: "Castores Estimados", value: 110000, unit: "+", delta: ""},
                {label: "Hectares Devastados", value: 31000, unit: "ha", delta: ""},
                {label: "Represas Construídas", value: 70600, unit: "", delta: ""}
            ]},
            {name: "🌊 El Niño 2026", kpis: [
                {label: "Probabilidade", value: 98, unit: "%", delta: ""},
                {label: "Niño 3.4 Atual", value: 0.9, unit: "°C", delta: ""},
                {label: "Previsão Pico", value: 2.4, unit: "°C", delta: ""},
                {label: "Super El Niño", value: 33, unit: "%", delta: ""}
            ]}
        ];

        let currentSlide = 0;

        function animateCount(element, end, duration = 2000) {
            let start = 0;
            const startTime = Date.now();
            function update() {
                const now = Date.now();
                const progress = Math.min((now - startTime) / duration, 1);
                const value = Math.floor(progress * (end - start) + start);
                element.textContent = value.toLocaleString('pt-BR');
                if (progress < 1) requestAnimationFrame(update);
                else element.textContent = end.toLocaleString('pt-BR');
            }
            update();
        }

        function showSlide(index) {
            const container = document.getElementById('slideContainer');
            const theme = themes[index];
            
            let html = `<h2 style="text-align:center; color:#2ecc71; margin-bottom:40px;">${theme.name}</h2>`;
            html += '<div style="display:flex; gap:25px; justify-content:center; flex-wrap:wrap;">';
            
            theme.kpis.forEach((kpi, i) => {
                html += `
                <div class="kpi-card">
                    <div class="kpi-number" id="num${index}_${i}">0</div>
                    <div class="kpi-label">${kpi.label} ${kpi.unit}</div>
                    <div class="delta" style="color:#2ecc71;">${kpi.delta}</div>
                </div>`;
            });
            html += '</div>';
            container.innerHTML = html;

            setTimeout(() => {
                theme.kpis.forEach((kpi, i) => {
                    const el = document.getElementById(`num${index}_${i}`);
                    if (el) animateCount(el, kpi.value);
                });
            }, 400);
        }

        // Inicia o carrossel
        showSlide(0);
        setInterval(() => {
            currentSlide = (currentSlide + 1) % themes.length;
            showSlide(currentSlide);
        }, 15000);

        function changeLang(lang) {
            alert("Idioma alterado para: " + lang.toUpperCase() + " (em breve)");
        }
    </script>
</body>
</html>
"""

st.components.v1.html(html_code, height=850, scrolling=True)

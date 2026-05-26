import streamlit as st

st.set_page_config(page_title="Greenlog • Environmental Intelligence", 
                   page_icon="🌱", layout="wide", initial_sidebar_state="collapsed")

# ===================== HTML + CSS + JAVASCRIPT CUSTOMIZADO =====================
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
        .title { 
            font-size: 4.8rem; text-align: center; margin: 30px 0 10px 0;
            background: linear-gradient(90deg, #2ecc71, #3498db);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }
        .subtitle { text-align: center; color: #2ecc71; font-size: 1.8rem; margin-bottom: 40px; }
        
        .slide-container {
            display: flex; justify-content: center; align-items: center;
            min-height: 70vh; transition: opacity 0.8s;
        }
        .kpi-card {
            background: rgba(15, 25, 40, 0.95);
            border: 2px solid #2ecc71;
            border-radius: 20px;
            padding: 40px 30px;
            width: 380px;
            text-align: center;
            box-shadow: 0 0 40px rgba(46, 204, 113, 0.4);
        }
        .kpi-number {
            font-size: 4.2rem;
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
            font-size: 1.6rem;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="title">GREENLOG</div>
    <div class="subtitle">ENVIRONMENTAL INTELLIGENCE 2030</div>
    
    <div id="slideContainer" class="slide-container">
        <!-- Slides serão inseridos via JS -->
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
            // Adicione os outros temas aqui...
        ];

        let currentSlide = 0;

        function animateCount(element, end, duration = 1800) {
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
            html += '<div style="display:flex; gap:20px; justify-content:center; flex-wrap:wrap;">';
            
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

            // Animação de contagem
            setTimeout(() => {
                theme.kpis.forEach((kpi, i) => {
                    const el = document.getElementById(`num${index}_${i}`);
                    if (el) animateCount(el, kpi.value);
                });
            }, 300);
        }

        // Troca automática
        function autoAdvance() {
            currentSlide = (currentSlide + 1) % themes.length;
            showSlide(currentSlide);
        }

        // Inicia
        showSlide(0);
        setInterval(autoAdvance, 15000);
    </script>
</body>
</html>
"""

st.components.v1.html(html_code, height=800, scrolling=True)

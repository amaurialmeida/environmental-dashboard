import streamlit as st

st.set_page_config(page_title="Greenlog • Environmental Intelligence", 
                   page_icon="🌱", layout="wide", initial_sidebar_state="collapsed")

html_code = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        * { box-sizing: border-box; }
        html, body { 
            margin: 0; 
            padding: 0; 
            width: 100%; 
            height: 100%; 
            background: #050505; 
            color: white; 
            font-family: 'Segoe UI', sans-serif; 
            overflow: hidden;
        }
        .dashboard-wrapper {
            position: relative;
            width: 100%;
            height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            padding: 15px 20px;
        }
        .header { 
            text-align: center; 
            position: relative;
            z-index: 10;
            background: rgba(5, 5, 5, 0.65);
            backdrop-filter: blur(6px);
            padding-bottom: 8px;
        }
        .main-title { 
            font-size: 2.2rem; 
            color: #2ecc71;
            margin: 2px 0 8px 0;
            font-weight: 600;
            text-shadow: 0 0 15px rgba(46, 204, 113, 0.5);
        }
        .lang-buttons {
            display: flex; 
            justify-content: center; 
            gap: 6px;
            margin-bottom: 8px;
            flex-wrap: wrap;
        }
        .lang-btn {
            padding: 4px 10px; 
            background: rgba(46,204,113,0.12); 
            color: #2ecc71;
            border: 1px solid #2ecc71; 
            border-radius: 16px; 
            cursor: pointer;
            font-size: 0.75rem; 
            transition: all 0.3s;
            display: flex;
            align-items: center;
            gap: 4px;
        }
        .lang-btn:hover, .lang-btn.active { 
            background: #2ecc71; 
            color: black; 
            box-shadow: 0 0 10px rgba(46, 204, 113, 0.8);
        }

        /* Container do Mapa Windy (Marca d'água de fundo cobrindo 100%) */
        .map-background {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 1;
            opacity: 0.5;
            filter: hue-rotate(-15deg) brightness(0.75) contrast(1.2);
            pointer-events: none;
        }

        .slide-container {
            display: flex; 
            flex-direction: column;
            justify-content: center; 
            align-items: center;
            flex-grow: 1;
            position: relative;
            z-index: 5;
            width: 100%;
        }
        
        .kpi-wrapper {
            display: flex;
            gap: 16px;
            justify-content: center;
            align-items: center;
            flex-wrap: wrap;
            width: 100%;
            max-width: 1300px;
        }

        .kpi-card {
            background: rgba(10, 20, 35, 0.88);
            border: 2px solid #2ecc71;
            border-radius: 16px;
            padding: 22px 15px;
            flex: 1;
            min-width: 220px;
            max-width: 280px;
            text-align: center;
            box-shadow: 0 0 25px rgba(46, 204, 113, 0.25);
            backdrop-filter: blur(10px);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .kpi-card:hover {
            transform: translateY(-6px);
            box-shadow: 0 0 40px rgba(46, 204, 113, 0.6);
            border-color: #2ecc71;
        }

        .kpi-number { 
            font-size: 2.8rem; 
            font-weight: bold; 
            color: #2ecc71; 
            margin: 6px 0; 
            text-shadow: 0 0 10px rgba(46, 204, 113, 0.4);
        }
        .kpi-label { 
            font-size: 0.95rem; 
            color: #cbd5e1; 
            margin-bottom: 4px; 
            font-weight: 500;
        }
        .delta { 
            font-size: 1.1rem; 
            font-weight: bold; 
        }
        
        .bottom-bar {
            text-align: center;
            font-size: 0.8rem; 
            color: #94a3b8;
            z-index: 10;
            background: rgba(10, 20, 35, 0.8);
            padding: 8px 0;
            border-radius: 8px;
            border: 1px solid rgba(46, 204, 113, 0.3);
            backdrop-filter: blur(5px);
            width: 100%;
            max-width: 600px;
            margin: 0 auto;
        }
        
        .overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle, rgba(5,5,5,0.1) 0%, rgba(5,5,5,0.85) 100%);
            z-index: 2;
            pointer-events: none;
        }
    </style>
</head>
<body>
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

    <div class="dashboard-wrapper">
        <div class="header">
            <div class="main-title" id="main-title">Dados para um planeta mais verde!</div>
            
            <div class="lang-buttons">
                <div class="lang-btn active" id="btn-pt" onclick="setLanguage('pt')">🇧🇷 PT</div>
                <div class="lang-btn" id="btn-en" onclick="setLanguage('en')">🇬🇧 EN</div>
                <div class="lang-btn" id="btn-es" onclick="setLanguage('es')">🇪🇸 ES</div>
                <div class="lang-btn" id="btn-it" onclick="setLanguage('it')">🇮🇹 IT</div>
                <div class="lang-btn" id="btn-fr" onclick="setLanguage('fr')">🇫🇷 FR</div>
                <div class="lang-btn" id="btn-de" onclick="setLanguage('de')">🇩🇪 DE</div>
                <div class="lang-btn" id="btn-zh" onclick="setLanguage('zh')">🇨🇳 ZH</div>
                <div class="lang-btn" id="btn-ar" onclick="setLanguage('ar')">🇸🇦 AR</div>
            </div>
        </div>
        
        <div id="slideContainer" class="slide-container"></div>

        <div class="bottom-bar" id="bottom-text">
            👇 Clique nos botões acima ou aguarde a transição automática
        </div>
    </div>

    <script>
        let currentLang = 'pt';
        let currentSlide = 0;

        const translations = {
            pt: { title: "Dados para um planeta mais verde!", bottom: "👇 Clique nos botões acima ou aguarde a transição automática" },
            en: { title: "Data for a greener planet!", bottom: "👇 Click above or wait for automatic transition" },
            es: { title: "¡Datos para un planeta más verde!", bottom: "👇 Haz clic arriba o espera la transición automática" },
            it: { title: "Dati per un pianeta più verde!", bottom: "👇 Clicca sopra o attendi la transizione automatica" },
            fr: { title: "Des données pour une planète plus verte !", bottom: "👇 Cliquez ci-dessus ou attendez la transition automatique" },
            de: { title: "Daten für einen grüneren Planeten!", bottom: "👇 Klicken Sie oben oder warten Sie auf den automatischen Übergang" },
            zh: { title: "为更绿色的星球提供数据！", bottom: "👇 点击上方或等待自动切换" },
            ar: { title: "بيانات من أجل كوكب أكثر خضرة!", bottom: "👇 انقر أعلاه أو انتظر الانتقال التلقائي" }
        };

        const themes = [
            {
                name: {pt:"🌍 Temperaturas Globais", en:"🌍 Global Temperatures", es:"🌍 Temperaturas Globales", it:"🌍 Temperature Globali", fr:"🌍 Températures Mondiales", de:"🌍 Globale Temperaturen", zh:"🌍 全球气温", ar:"🌍 درجات الحرارة العالمية"}, 
                kpis: [
                    {label:{pt:"Temperatura Média Global",en:"Global Average Temperature",es:"Temperatura Media Global",it:"Temperatura Media Globale",fr:"Température Moyenne Mondiale",de:"Globale Durchschnittstemperatur",zh:"全球平均气温",ar:"متوسط درجة الحرارة العالمية"}, value:14.92, unit:"°C", delta:"↑ 1.45%"},
                    {label:{pt:"Ano Mais Quente",en:"Hottest Year",es:"Año Más Caliente",it:"Anno Più Caldo",fr:"Année la Plus Chaude",de:"Wärmstes Jahr",zh:"最热年份",ar:"السنة الأشد حرارة"}, value:2025, unit:"", delta:"↑ 0.9%"},
                    {label:{pt:"Anomalia Atual",en:"Current Anomaly",es:"Anomalía Actual",it:"Anomalia Attuale",fr:"Anomalie Actuelle",de:"Aktuelle Anomalie",zh:"当前异常",ar:"الشذوذ الحالي"}, value:1.54, unit:"°C", delta:"↑ 15%"}
                ]
            },
            {
                name: {pt:"☀️ Energia Solar", en:"☀️ Solar Energy", es:"☀️ Energía Solar", it:"☀️ Energia Solare", fr:"☀️ Énergie Solaire", de:"☀️ Solarenergie", zh:"☀️ 太阳能", ar:"☀️ الطاقة الشمسية"}, 
                kpis: [
                    {label:{pt:"Energia Gerada",en:"Energy Generated",es:"Energía Generada",it:"Energia Generata",fr:"Énergie Générée",de:"Erzeugte Energie",zh:"发电量",ar:"الطاقة المولدة"}, value:390, unit:"MWh", delta:""},
                    {label:{pt:"CO₂ Evitado",en:"CO₂ Avoided",es:"CO₂ Evitado",it:"CO₂ Evitato",fr:"CO₂ Évité",de:"Eingespartes CO₂",zh:"减少二氧化碳",ar:"تجنب انبعاثات ثاني أكسيد الكربون"}, value:953, unit:"t", delta:""},
                    {label:{pt:"Árvores Equivalentes",en:"Equivalent Trees",es:"Árboles Equivalentes",it:"Alberi Equivalenti",fr:"Arbres Équivalents",de:"Äquivalente Bäume",zh:"相当于植树",ar:"الأشجار المكافئة"}, value:7250, unit:"", delta:""}
                ]
            },
            {
                name: {pt:"🐝 Abelhas sem Ferrão", en:"🐝 Stingless Bees", es:"🐝 Abejas sin Aguijón", it:"🐝 Ape Senza Pungiglione", fr:"🐝 Abeilles sans Dard", de:"🐝 Stachellose Bienen", zh:"🐝 无刺蜂", ar:"🐝 النحل عديم اللسع"}, 
                kpis: [
                    {label:{pt:"Espécies Monitoradas",en:"Monitored Species",es:"Especies Monitoreadas",it:"Specie Monitorate",fr:"Espèces Suivies",de:"Überwachte Arten",zh:"监测物种",ar:"الأنواع المراقب"}, value:18, unit:"", delta:""},
                    {label:{pt:"Registros GBIF",en:"GBIF Records",es:"Registros GBIF",it:"Registri GBIF",fr:"Registres GBIF",de:"GBIF-Einträge",zh:"GBIF记录",ar:"سجلات GBIF"}, value:24500, unit:"", delta:""},
                    {label:{pt:"Estados Cobertos",en:"Covered States",es:"Estados Cubiertos",it:"Stati Coperti",fr:"États Couverts",de:"Abgedeckte Staaten",zh:"覆盖州数",ar:"الولايات المغطاة"}, value:15, unit:"", delta:""},
                    {label:{pt:"Espécies Ameaçadas",en:"Threatened Species",es:"Especies Amenazadas",it:"Specie Minacciate",fr:"Espèces Menacées",de:"Bedrohte Arten",zh:"受威胁物种",ar:"الأنواع المهددة بالانقراض"}, value:4, unit:"VU", delta:""}
                ]
            },
            {
                name: {pt:"🌬️ Potencial Eólico", en:"🌬️ Wind Potential", es:"🌬️ Potencial Eólico", it:"🌬️ Potenziale Eolico", fr:"🌬️ Potentiel Éolien", de:"🌬️ Windpotential", zh:"🌬️ 风能潜力", ar:"🌬️ الطاقة الريحية"}, 
                kpis: [
                    {label:{pt:"Velocidade Média",en:"Average Speed",es:"Velocidad Media",it:"Velocità Media",fr:"Vitesse Moyenne",de:"Durchschnittsgeschwindigkeit",zh:"平均风速",ar:"السرعة المتوسطة"}, value:30.2, unit:"km/h", delta:""},
                    {label:{pt:"Fator de Capacidade",en:"Capacity Factor",es:"Factor de Capacidad",it:"Fattore di Capacità",fr:"Facteur de Capacité",de:"Kapazitätsfaktor",zh:"容量因数",ar:"عامل السعة"}, value:60, unit:"%", delta:""},
                    {label:{pt:"Rajada Máxima",en:"Max Gust",es:"Ráfaga Máxima",it:"Raffica Massima",fr:"Rafale Maximale",de:"Maximale Böe",zh:"最大阵风",ar:"السرعة القصوى للرياح"}, value:130, unit:"km/h", delta:""},
                    {label:{pt:"Potencial Total",en:"Total Potential",es:"Potencial Total",it:"Potenziale Totale",fr:"Potentiel Total",de:"Gesamtpotential",zh:"总潜力",ar:"الإمكانات الكلية"}, value:9500, unit:"MW", delta:""}
                ]
            },
            {
                name: {pt:"💧 Qualidade da Água", en:"💧 Water Quality", es:"💧 Calidad del Agua", it:"💧 Qualità dell'Acqua", fr:"💧 Qualité de l'Eau", de:"💧 Wasserqualität", zh:"💧 水质", ar:"💧 جودة المياه"}, 
                kpis: [
                    {label:{pt:"IQA Médio",en:"Average IQA",es:"IQA Medio",it:"IQA Medio",fr:"IQA Moyen",de:"Durchschnittlicher IQA",zh:"平均水质指数",ar:"متوسط مؤشر جودة المياه"}, value:81.9, unit:"", delta:""},
                    {label:{pt:"Estações Excelente",en:"Excellent Stations",es:"Estaciones Excelentes",it:"Stazioni Eccellenti",fr:"Stations Excellentes",de:"Exzellente Stationen",zh:"优秀监测站",ar:"محطات ممتازة"}, value:3, unit:"/18", delta:""},
                    {label:{pt:"Rios Monitorados",en:"Monitored Rivers",es:"Ríos Monitoreados",it:"Fiumi Monitorati",fr:"Rivières Suivies",de:"Überwachte Flüsse",zh:"监测河流",ar:"الأنهار المراقب"}, value:10, unit:"", delta:""}
                ]
            },
            {
                name: {pt:"🌋 Monitoramento Sísmico", en:"🌋 Seismic Monitoring", es:"🌋 Monitoreo Sísmico", it:"🌋 Monitoraggio Sismico", fr:"🌋 Surveillance Sismique", de:"🌋 Seismische Überwachung", zh:"🌋 地震监测", ar:"🌋 الرصد الزلزالي"}, 
                kpis: [
                    {label:{pt:"Magnitude",en:"Magnitude",es:"Magnitud",it:"Magnitudo",fr:"Magnitude",de:"Magnitude",zh:"震级",ar:"القدر الزلزالي"}, value:7.4, unit:"", delta:""},
                    {label:{pt:"Profundidade",en:"Depth",es:"Profundidad",it:"Profondità",fr:"Profondeur",de:"Tiefe",zh:"深度",ar:"العمق"}, value:10, unit:"km", delta:""},
                    {label:{pt:"Réplicas",en:"Aftershocks",es:"Réplicas",it:"Repliche",fr:"Répliques",de:"Nachbeben",zh:"余震",ar:"الهزات الارتدادية"}, value:50, unit:"+", delta:""}
                ]
            },
            {
                name: {pt:"🌿 Espécies Invasoras", en:"🌿 Invasive Species", es:"🌿 Especies Invasoras", it:"🌿 Specie Invasive", fr:"🌿 Espèces Invasives", de:"🌿 Invasive Arten", zh:"🌿 入侵物种", ar:"🌿 الأنواع الغازية"}, 
                kpis: [
                    {label:{pt:"Castores Estimados",en:"Estimated Beavers",es:"Castores Estimados",it:"Castori Stimati",fr:"Castors Estimés",de:"Geschätzte Biber",zh:"估计海狸数",ar:"القنادس المقدرة"}, value:110000, unit:"+", delta:""},
                    {label:{pt:"Hectares Devastados",en:"Devastated Hectares",es:"Hectáreas Devastadas",it:"Ettari Devastati",fr:"Hectares Dévastés",de:"Zerstörte Hektar",zh:"受灾公顷数",ar:"الهكتارات المدمرة"}, value:31000, unit:"ha", delta:""}
                ]
            },
            {
                name: {pt:"🌊 El Niño 2026", en:"🌊 El Niño 2026", es:"🌊 El Niño 2026", it:"🌊 El Niño 2026", fr:"🌊 El Niño 2026", de:"🌊 El Niño 2026", zh:"🌊 2026 厄尔尼诺", ar:"🌊 إيل نينيو 2026"}, 
                kpis: [
                    {label:{pt:"Probabilidade",en:"Probability",es:"Probabilidad",it:"Probabilità",fr:"Probabilité",de:"Wahrscheinlichkeit",zh:"概率",ar:"الاحتمالية"}, value:98, unit:"%", delta:""},
                    {label:{pt:"Niño 3.4 Atual",en:"Current Niño 3.4",es:"Niño 3.4 Actual",it:"Niño 3.4 Attuale",fr:"Actuel Niño 3.4",de:"Aktueller Niño 3.4",zh:"当前尼尔o 3.4",ar:"إيل نينيو 3.4 الحالي"}, value:0.9, unit:"°C", delta:""},
                    {label:{pt:"Previsão Pico",en:"Peak Forecast",es:"Previsión Pico",it:"Previsione di Picco",fr:"Prévision Pic",de:"Höchststand-Prognose",zh:"峰值预测",ar:"ذروة التوقع"}, value:2.4, unit:"°C", delta:""}
                ]
            }
        ];

        function setLanguage(lang) {
            currentLang = lang;
            document.getElementById('main-title').textContent = translations[lang].title;
            document.getElementById('bottom-text').textContent = translations[lang].bottom;
            document.querySelectorAll('.lang-btn').forEach(btn => btn.classList.remove('active'));
            document.getElementById('btn-' + lang).classList.add('active');
            renderSlide(currentSlide);
        }

        function animateCount(element, end, unit) {
            let start = 0;
            const duration = 1600;
            const startTime = Date.now();
            
            function update() {
                const now = Date.now();
                const progress = Math.min((now - startTime) / duration, 1);
                const easeProgress = 1 - Math.pow(1 - progress, 3);
                const currentVal = easeProgress * (end - start) + start;
                
                if (end % 1 !== 0) {
                    element.textContent = currentVal.toFixed(2).replace('.', ',') + (unit ? ' ' + unit : '');
                } else {
                    element.textContent = Math.floor(currentVal).toLocaleString('pt-BR') + (unit ? ' ' + unit : '');
                }
                
                if (progress < 1) {
                    requestAnimationFrame(update);
                } else {
                    if (end % 1 !== 0) {
                        element.textContent = end.toFixed(2).replace('.', ',') + (unit ? ' ' + unit : '');
                    } else {
                        element.textContent = end.toLocaleString('pt-BR') + (unit ? ' ' + unit : '');
                    }
                }
            }
            update();
        }

        function renderSlide(index) {
            const theme = themes[index];
            const container = document.getElementById('slideContainer');
            
            let html = `
                <div style="font-size: 1.4rem; color: #2ecc71; margin-bottom: 12px; font-weight: 600; text-shadow: 0 0 10px rgba(46,204,113,0.4);">
                    ${theme.name[currentLang] || theme.name['pt']}
                </div>
                <div class="kpi-wrapper">
            `;
            
            theme.kpis.forEach((kpi, i) => {
                const labelText = kpi.label[currentLang] || kpi.label['pt'];
                html += `
                    <div class="kpi-card">
                        <div class="kpi-label">${labelText}</div>
                        <div class="kpi-number" id="val-${index}-${i}">0</div>
                        ${kpi.delta ? `<div class="delta" style="color: ${kpi.delta.includes('↑') ? '#2ecc71' : '#e74c3c'}">${kpi.delta}</div>` : ''}
                    </div>
                `;
            });
            
            html += `</div>`;
            container.innerHTML = html;
            
            theme.kpis.forEach((kpi, i) => {
                const el = document.getElementById(`val-${index}-${i}`);
                if (el) {
                    animateCount(el, kpi.value, kpi.unit);
                }
            });
        }

        setInterval(() => {
            currentSlide = (currentSlide + 1) % themes.length;
            renderSlide(currentSlide);
        }, 6000);

        renderSlide(0);
    </script>
</body>
</html>
"""

st.components.v1.html(html_code, height=520, scrolling=False)

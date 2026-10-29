"""Textos do hub Greenlog nos 9 idiomas do portfólio."""
LANGS = {"pt": "🇧🇷 PT", "en": "🇬🇧 EN", "es": "🇪🇸 ES", "it": "🇮🇹 IT", "zh": "🇨🇳 ZH",
         "fr": "🇫🇷 FR", "ar": "🇸🇦 AR", "de": "🇩🇪 DE", "el": "🇬🇷 EL"}

K = ["home", "router", "sec_main", "sec_projects", "lang", "open_app", "load_here", "hide", "preview", "no_preview",
     "heavy", "numbers", "embed_title"]
def _d(*v): return dict(zip(K, v))

UI = {
"pt": _d("Início", "Environmental Signal Router", "Greenlog", "Projetos", "Idioma", "Abrir app completo ↗", "▶ Carregar aqui", "✕ Fechar app",
         "Pré-visualização", "Pré-visualização em breve", "O app completo é pesado: só carrega quando você clica. Se demorar, o app pode estar acordando.", "Números-chave", "App completo"),
"en": _d("Home", "Environmental Signal Router", "Greenlog", "Projects", "Language", "Open full app ↗", "▶ Load here", "✕ Close app",
         "Preview", "Preview coming soon", "The full app is heavy: it only loads when you click. If it is slow, the app may be waking up.", "Key numbers", "Full app"),
"es": _d("Inicio", "Environmental Signal Router", "Greenlog", "Proyectos", "Idioma", "Abrir app completa ↗", "▶ Cargar aquí", "✕ Cerrar app",
         "Vista previa", "Vista previa próximamente", "La app completa es pesada: solo se carga al hacer clic. Si tarda, puede estar despertando.", "Cifras clave", "App completa"),
"it": _d("Home", "Environmental Signal Router", "Greenlog", "Progetti", "Lingua", "Apri l'app completa ↗", "▶ Carica qui", "✕ Chiudi app",
         "Anteprima", "Anteprima in arrivo", "L'app completa è pesante: si carica solo al clic. Se è lenta, potrebbe star ripartendo.", "Numeri chiave", "App completa"),
"zh": _d("首页", "Environmental Signal Router", "Greenlog", "项目", "语言", "打开完整应用 ↗", "▶ 在此加载", "✕ 关闭应用",
         "预览", "预览即将上线", "完整应用较重：仅在点击后加载。若较慢，应用可能正在唤醒。", "关键数据", "完整应用"),
"fr": _d("Accueil", "Environmental Signal Router", "Greenlog", "Projets", "Langue", "Ouvrir l'app complète ↗", "▶ Charger ici", "✕ Fermer l'app",
         "Aperçu", "Aperçu bientôt disponible", "L'app complète est lourde : elle ne se charge qu'au clic. Si c'est lent, elle se réveille peut-être.", "Chiffres clés", "App complète"),
"ar": _d("الرئيسية", "Environmental Signal Router", "Greenlog", "المشاريع", "اللغة", "فتح التطبيق الكامل ↗", "▶ تحميل هنا", "✕ إغلاق التطبيق",
         "معاينة", "المعاينة قريبًا", "التطبيق الكامل ثقيل: لا يُحمَّل إلا عند النقر. وإذا تأخر فقد يكون التطبيق يستيقظ.", "أرقام رئيسية", "التطبيق الكامل"),
"de": _d("Start", "Environmental Signal Router", "Greenlog", "Projekte", "Sprache", "Vollständige App öffnen ↗", "▶ Hier laden", "✕ App schließen",
         "Vorschau", "Vorschau folgt", "Die vollständige App ist schwer: Sie lädt erst nach einem Klick. Bei Verzögerung wacht sie evtl. gerade auf.", "Kennzahlen", "Vollständige App"),
"el": _d("Αρχική", "Environmental Signal Router", "Greenlog", "Έργα", "Γλώσσα", "Άνοιγμα πλήρους εφαρμογής ↗", "▶ Φόρτωση εδώ", "✕ Κλείσιμο εφαρμογής",
         "Προεπισκόπηση", "Προεπισκόπηση σύντομα", "Η πλήρης εφαρμογή είναι βαριά: φορτώνει μόνο με κλικ. Αν αργεί, ίσως ξυπνά.", "Βασικοί αριθμοί", "Πλήρης εφαρμογή"),
}

# Nomes dos projetos que não aparecem no carrossel
EXTRA_NAMES = {
 "bee-collapse": {"pt":"Colapso das Abelhas","en":"Bee Colony Collapse","es":"Colapso de las Colonias de Abejas","it":"Collasso delle Colonie di Api","zh":"蜂群崩溃","fr":"Effondrement des Colonies d'Abeilles","ar":"انهيار مستعمرات النحل","de":"Bienenvölker-Kollaps","el":"Κατάρρευση Αποικιών Μελισσών"},
 "road": {l: "Road to Patagonia" for l in LANGS},
 "carbon": {"pt":"Pegada de Carbono","en":"Carbon Footprint","es":"Huella de Carbono","it":"Impronta di Carbonio","zh":"碳足迹","fr":"Empreinte Carbone","ar":"البصمة الكربونية","de":"CO₂-Fußabdruck","el":"Αποτύπωμα Άνθρακα"},
 "santa-rita": {"pt":"Observatório do Rio Santa Rita","en":"Santa Rita River Observatory","es":"Observatorio del Río Santa Rita","it":"Osservatorio del Fiume Santa Rita","zh":"圣丽塔河观测站","fr":"Observatoire de la Rivière Santa Rita","ar":"مرصد نهر سانتا ريتا","de":"Santa-Rita-Flussobservatorium","el":"Παρατηρητήριο Ποταμού Santa Rita"},
}
assert all(len(v) == len(K) for v in UI.values())

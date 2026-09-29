# -*- coding: utf-8 -*-
"""CV de Daniel Martín: datos → plantilla HTML (estilo Orbit, barra lateral + columna) → PDF de una página, en español e inglés.

Uso: python build_cv.py   (necesita Microsoft Edge y PyMuPDF; ver README)
"""
import base64, subprocess, sys, tempfile, time, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT
PHOTO = ROOT / "foto.jpg"
EDGE = r"C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"

photo_b64 = base64.b64encode(PHOTO.read_bytes()).decode("ascii")

# ---------- iconos (feather, inline) ----------
def ico(d, size="3.4mm", stroke="currentColor"):
    return ('<svg viewBox="0 0 24 24" width="%s" height="%s" fill="none" stroke="%s" stroke-width="2" '
            'stroke-linecap="round" stroke-linejoin="round">%s</svg>') % (size, size, stroke, d)

I = {
 "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><polyline points="22,6 12,13 2,6"/>',
 "phone": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/>',
 "pin": '<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>',
 "globe": '<circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>',
 "github": '<path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"/>',
 "linkedin": '<path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"/><rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/>',
 "zap": '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>',
 "user": '<path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>',
 "folder": '<path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>',
 "brief": '<rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>',
 "book": '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>',
}

CSS = """
@page { size: A4; margin: 0; }
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }
body { font: 8.45pt/1.31 Roboto, "Segoe UI", Arial, sans-serif; color: #3F4650; background: #fff;
       -webkit-print-color-adjust: exact; print-color-adjust: exact; }
a { color: #1e3a6e; text-decoration: none; }
.wrapper { display: grid; grid-template-columns: 1fr 60mm; width: 210mm; min-height: 297mm; margin: 0 auto; }
/* ---- sidebar ---- */
.sidebar { background: #1e3a6e; color: #fff; order: 2; }
.sidebar a { color: #fff; }
.profile { background: rgba(0,0,0,.22); text-align: center; padding: 7mm 5mm 5mm; }
.avatar { width: 30mm; height: 30mm; border-radius: 50%; object-fit: cover; border: 1.2px solid rgba(255,255,255,.85);
          box-shadow: 0 1px 2px rgba(0,0,0,.25); margin-bottom: 3.5mm; }
.name { font-size: 18.5pt; font-weight: 900; margin: 0 0 1.5mm; line-height: 1.1; letter-spacing: -.005em; }
.tagline { font-size: 10pt; font-weight: 400; color: rgba(255,255,255,.72); margin: 0; }
.tagline2 { font-size: 8pt; color: rgba(255,255,255,.6); margin: 1mm 0 0; }
.block { padding: 4.6mm 6mm 0; }
.block:last-child { padding-bottom: 5mm; }
.block-title { text-transform: uppercase; font-size: 8.2pt; font-weight: 700; letter-spacing: .1em; margin: 0 0 2.2mm;
               padding-bottom: 1.2mm; border-bottom: 1px solid rgba(255,255,255,.18); }
.contact { list-style: none; margin: 0; padding: 0; }
.contact li { display: flex; align-items: center; gap: 2.2mm; margin: 0 0 2mm; font-size: 8.3pt; }
.contact svg { flex: 0 0 auto; opacity: .9; }
.pill { display: inline-flex; align-items: center; gap: 1.6mm; background: #c8692c; color: #fff; font-weight: 700;
        font-size: 7.6pt; letter-spacing: .06em; text-transform: uppercase; padding: 1.2mm 2.6mm; border-radius: 2mm; margin-top: .8mm; }
.lang { margin: 0; padding: 0; list-style: none; font-size: 8.3pt; }
.lang li { margin-bottom: 1.4mm; }
.lang .lvl { color: rgba(255,255,255,.62); }
.skill { margin: 0 0 2.4mm; font-size: 7.9pt; line-height: 1.34; }
.skill b { display: block; color: #fff; font-weight: 700; margin-bottom: .4mm; }
.skill span { color: rgba(255,255,255,.8); }
.interests { font-size: 8.3pt; color: rgba(255,255,255,.85); margin: 0; }
/* ---- main ---- */
.main { order: 1; background: #fff; padding: 6mm 7.5mm 3mm 9mm; }
.section { margin-bottom: 2.8mm; }
.section-title { display: flex; align-items: center; gap: 2.4mm; text-transform: uppercase; font-size: 9.8pt;
                 font-weight: 500; letter-spacing: .04em; color: #3f6fb5; margin: 0 0 1.8mm; }
.section-title .ic { display: inline-flex; align-items: center; justify-content: center; width: 6mm; height: 6mm;
                     border-radius: 50%; background: #1e3a6e; color: #fff; }
.hilo { font-style: italic; color: #1e3a6e; margin: 0 0 1.8mm; font-size: 9.2pt; }
p { margin: 0 0 1.6mm; }
.item { margin-bottom: 1.5mm; }
.upper { display: flex; justify-content: space-between; align-items: baseline; gap: 4mm; }
.job { font-size: 9.5pt; font-weight: 500; color: #2b323d; margin: 0; }
.job a { color: #1e3a6e; }
.job .url { font-weight: 400; color: #97AAC3; font-size: 8.2pt; margin-left: 1.4mm; }
.time { color: #97AAC3; white-space: nowrap; font-size: 8.4pt; }
.time a { color: #97AAC3; }
.time svg { vertical-align: -0.5mm; }
.company { color: #97AAC3; margin-bottom: .8mm; font-size: 8.5pt; }
.details { color: #3F4650; }
.n { color: #2f7a4c; font-weight: 600; }
.edu-line { display: flex; justify-content: space-between; gap: 4mm; margin-bottom: 1.2mm; }
.edu-line b { font-weight: 500; color: #2b323d; }
"""

def sidebar(d):
    contact = "".join('<li>%s<span>%s</span></li>' % (ico(I[k]), v) for k, v in d["contact"])
    langs = "".join('<li>%s <span class="lvl">%s</span></li>' % (a, b) for a, b in d["langs"])
    skills = "".join('<div class="skill"><b>%s</b><span>%s</span></div>' % (a, b) for a, b in d["skills"])
    return f"""
<aside class="sidebar">
  <div class="profile">
    <img class="avatar" src="data:image/jpeg;base64,{photo_b64}" alt="Daniel Martín">
    <h1 class="name">Daniel Martín</h1>
    <h3 class="tagline">{d['tagline']}</h3>
    <div class="tagline2">{d['tagline2']}</div>
  </div>
  <div class="block">
    <ul class="contact">{contact}</ul>
    <div class="pill">{ico(I['zap'], '3mm')} {d['avail']}</div>
  </div>
  <div class="block"><h2 class="block-title">{d['t_langs']}</h2><ul class="lang">{langs}</ul></div>
  <div class="block"><h2 class="block-title">{d['t_skills']}</h2>{skills}</div>
  <div class="block"><h2 class="block-title">{d['t_interests']}</h2><p class="interests">{d['interests']}</p></div>
</aside>"""

def sec(title, icon, body):
    return f'<section class="section"><h2 class="section-title"><span class="ic">{ico(I[icon], "3.3mm")}</span>{title}</h2>{body}</section>'

def main(d):
    gh = ico(I["github"], "2.9mm")
    projects = "".join(
        f'<div class="item"><div class="upper"><h3 class="job"><a href="https://github.com/{repo}">{name}</a></h3>'
        f'<span class="time"><a href="https://github.com/{repo}">{gh} {repo}</a> · {year}</span></div><div class="details">{desc}</div></div>'
        for name, repo, year, desc in d["projects"])
    exp = "".join(
        f'<div class="item"><div class="upper"><h3 class="job">{role}</h3><span class="time">{when}</span></div>'
        f'<div class="company">{company}</div><div class="details">{details}</div></div>'
        for role, when, company, details in d["experience"])
    edu = "".join(
        (f'<div class="item"><div class="upper"><h3 class="job">{deg}</h3><span class="time">{when}</span></div>'
         f'<div class="company">{org}</div><div class="details">{details}</div></div>') if details else
        f'<div class="edu-line"><b>{deg}</b><span class="time">{when}</span></div>'
        for deg, when, org, details in d["education"])
    return f"""
<main class="main">
  {sec(d['t_profile'], 'user', f'<p class="hilo">{d["hilo"]}</p><p>{d["summary"]}</p>')}
  {sec(d['t_projects'], 'folder', projects)}
  {sec(d['t_experience'], 'brief', exp)}
  {sec(d['t_education'], 'book', edu)}
</main>"""

def page(d):
    return f"""<!doctype html><html lang="{d['lang']}"><head><meta charset="utf-8"><title>CV Daniel Martín · {d['tagline']}</title>
<meta name="viewport" content="width=device-width, initial-scale=1"><style>{CSS}</style></head>
<body><div class="wrapper">{main(d)}{sidebar(d)}</div></body></html>"""

# ---------- contenido (variante AI Engineer) ----------
ES = {'lang': 'es',
 'tagline': 'AI Engineer',
 'tagline2': 'Soluciones de IA para procesos regulados',
 'contact': [('pin', 'Sevilla, España · remoto'),
             ('phone', '644 940 525'),
             ('mail', 'danielmartin@epifaneia.dev'),
             ('globe', '<a href="https://epifaneia.dev">epifaneia.dev</a>'),
             ('github', '<a href="https://github.com/epifaneia">github.com/epifaneia</a>'),
             ('linkedin', '<a href="https://www.linkedin.com/in/epifaneia/">linkedin.com/in/epifaneia</a>')],
 'avail': 'Disponibilidad inmediata',
 't_langs': 'Idiomas',
 'langs': [('Español', 'nativo'), ('Inglés', 'C1 · seis años trabajando en inglés')],
 't_skills': 'Competencias',
 'skills': [('IA aplicada',
             'Pipelines de LLM con salida estructurada, enum dinámico y verificación determinista. Modelos '
             'en local (Ollama, Qwen 7B/14B) y en nube (Gemini) bajo el mismo contrato. Recuperación BM25. '
             'Calibración y medida contra ground truth. Agentes con CrewAI (Flows y Crews con RAG) cuando el '
             'problema lo pide.'),
            ('Machine learning y datos',
             'Redes convolucionales con TensorFlow/Keras: preparación y balanceo de datos, partición '
             'train/validación/test, evaluación. Pandas, NumPy, Matplotlib, Jupyter, Streamlit. PDF '
             '(PyMuPDF, Docling, gmft), XML y ReqIF (lxml), SQLite.'),
            ('Código',
             'Python (FastAPI, Django, lxml), JavaScript y TypeScript (React Native, Expo), HTML y CSS. Git, '
             'Docker, Heroku, tests y cobertura. Desarrollo asistido por IA con revisión, verificación y '
             'guardarraíles propios.'),
            ('Regulación',
             'EU AI Act, ISO/IEC 42001, ISO/IEC 27001, RGPD, TISAX. Contexto ISO 26262 e ISO/SAE 21434. '
             'Polarion.')],
 't_interests': 'Intereses',
 'interests': 'Patinaje · Filosofía · Juegos de rol',
 't_profile': 'Perfil profesional',
 'hilo': 'La IA tiene riesgos. El código los acota. La norma responde de lo que queda.',
 'summary': 'Programador. Ocho años de estudio por mi cuenta y siete meses construyendo sin parar: pipelines '
            'de IA que corren sobre datos reales, con cifras medidas, limitaciones escritas y código '
            'público. Trabajo con una idea simple: cualquier aplicación con IA tiene cinco pasos y solo uno '
            'invoca un modelo; los otros cuatro son código. Cuando están bien hechos, lo que queda en medio '
            'cabe en una llamada, y el resultado es más barato, más potente y auditable.',
 't_projects': 'Proyectos públicos',
 'projects': [('CTSM',
               'epifaneia/ctsm',
               '2026',
               'Audita los requisitos de una especificación de cliente (ReqIF de Polarion) contra los '
               'manuales del proveedor y devuelve el mismo fichero con la evidencia y su página exacta. El '
               'modelo solo puede citar fragmentos de una lista cerrada; el código verifica cada cita contra '
               'la fuente y deriva la página del offset. <span class="n">9/9 contra ground truth · 8/9 con '
               'un modelo local de 14B en una GPU de 6 GB y cero falsos «cumple» · diff de ida y vuelta '
               'probado contra 5 sabotajes.</span>'),
              ('reqif-extractor',
               'epifaneia/reqif-extractor',
               '2026',
               'De un PDF de especificación a un ReqIF que Polarion importa a la primera: identificadores '
               'verbatim, jerarquía del documento, orden de página. Política determinista de identificadores '
               'y reconciliación de tipo contra la fuente. <span class="n">167 de 170 identificadores '
               'inventados por el modelo, detectados · 1/20 del coste de visión enrutando solo tablas y '
               'figuras · 12/12 documentos reales validados estructuralmente.</span>'),
              ('toolkit',
               'epifaneia/toolkit',
               '2026',
               'La parte reutilizable de cada pipeline: una herramienta por paso de diseño, guardarraíles '
               'genéricos y tres cables de integración con los sistemas de la empresa (identidad, registro '
               'de eventos, firma), con pruebas e integración documentada para Entra ID, SIEM y PKI.'),
              ('feasibility-study',
               'epifaneia/feasibility-study',
               '2026',
               'De un formulario de reunión a un estudio de viabilidad de IA en PDF: una investigación '
               'autónoma por cientos de páginas, convertida por código en un informe con nuestra narrativa y '
               'nuestro orden, con fuentes citadas. Formulario, servidor FastAPI, panel del consultor y '
               'revisión humana antes de enviar.'),
              ('Mildew Detection in Cherry Leaves',
               'cefeidas/Mildew-Detection-in-Cherry-Leaves',
               '2024',
               'Clasificador de imágenes que distingue hojas de cerezo sanas de las afectadas por oídio: red '
               'convolucional en TensorFlow/Keras entrenada sobre <span class="n">5.972 imágenes con clases '
               'balanceadas</span>, partición 70/10/20 y <span class="n">99,8 % de acierto en test</span>. '
               'Panel en Streamlit desplegado en Heroku.')],
 't_experience': 'Experiencia',
 'experience': [('Diseñador de soluciones de IA',
                 'marzo 2026 – actualidad',
                 'Epifaneia · Sevilla, remoto',
                 'Diseño e implantación de pipelines de IA con cadena de custodia para industria y procesos '
                 'regulados: los tres proyectos de arriba, una app móvil de conversación por voz con modelos '
                 'por etapa, y pruebas de concepto para empresas de automoción y alimentación.'),
                ('Gestor bilingüe',
                 '2025 – actualidad',
                 'Foundever · campaña de Airbnb · Sevilla',
                 'Atención al cliente avanzada en inglés, en paralelo a Epifaneia.'),
                ('Programador de automatizaciones y teleoperador',
                 'marzo – diciembre 2024',
                 'Konecta · Sevilla',
                 'Automatización de los informes del equipo con Python (Pandas, openpyxl) sobre '
                 'exportaciones de Metabase, en iteraciones revisadas por el equipo de análisis de datos.'),
                ('Análisis de riesgo, calidad y formación',
                 '2017 – 2023',
                 'TaskUs, Prepaid Financial Services, Media Interactiva, Field Management · Irlanda y España',
                 'Análisis de riesgo financiero, auditoría de calidad y formación de agentes en TaskUs, con '
                 'un programa de entrenamiento de modelos de IA; QA de software en Media Interactiva. Seis '
                 'años trabajando en inglés.')],
 't_education': 'Formación',
 'education': [('Diploma in Full Stack Software Development',
                '2023 – 2024',
                'Code Institute · crédito universitario (University of the West of Scotland)',
                'Único bootcamp online con créditos universitarios en Reino Unido y Europa. Cinco proyectos '
                'de portfolio en <a href="https://github.com/cefeidas">github.com/cefeidas</a>: web '
                'accesible (HTML, CSS), juego en JavaScript, juego en Python sobre la API de Google Sheets, '
                'biblioteca en Django con autenticación y reseñas, y la red convolucional de arriba.'),
               ('Formación autodidacta en IA, arquitectura de software y regulación',
                '2018 – actualidad',
                '',
                ''),
               ('Estudios universitarios de Filosofía y de Física', 'Universidad de Sevilla', '', '')]}

EN = {'lang': 'en',
 'tagline': 'AI Engineer',
 'tagline2': 'AI solutions for regulated processes',
 'contact': [('pin', 'Seville, Spain · remote'),
             ('phone', '+34 644 940 525'),
             ('mail', 'danielmartin@epifaneia.dev'),
             ('globe', '<a href="https://epifaneia.dev">epifaneia.dev</a>'),
             ('github', '<a href="https://github.com/epifaneia">github.com/epifaneia</a>'),
             ('linkedin', '<a href="https://www.linkedin.com/in/epifaneia/">linkedin.com/in/epifaneia</a>')],
 'avail': 'Available immediately',
 't_langs': 'Languages',
 'langs': [('Spanish', 'native'), ('English', 'C1 · six years working in English')],
 't_skills': 'Skills',
 'skills': [('Applied AI',
             'LLM pipelines with structured output, dynamic enums and deterministic verification. Local '
             'models (Ollama, Qwen 7B/14B) and cloud (Gemini) under one contract. BM25 retrieval. '
             'Calibration and measurement against ground truth. Agents with CrewAI (Flows and Crews with '
             'RAG) when the problem calls for them.'),
            ('Machine learning and data',
             'Convolutional networks with TensorFlow/Keras: data preparation and class balancing, '
             'train/validation/test split, evaluation. Pandas, NumPy, Matplotlib, Jupyter, Streamlit. PDF '
             '(PyMuPDF, Docling, gmft), XML and ReqIF (lxml), SQLite.'),
            ('Code',
             'Python (FastAPI, Django, lxml), JavaScript and TypeScript (React Native, Expo), HTML and CSS. '
             'Git, Docker, Heroku, tests and coverage. AI-assisted development with my own review, '
             'verification and guardrails.'),
            ('Regulation',
             'EU AI Act, ISO/IEC 42001, ISO/IEC 27001, GDPR, TISAX. ISO 26262 and ISO/SAE 21434 context. '
             'Polarion.')],
 't_interests': 'Interests',
 'interests': 'Skating · Philosophy · Role-playing',
 't_profile': 'Profile',
 'hilo': 'AI carries risk. Code bounds it. The standard answers for what remains.',
 'summary': 'Programmer. Eight years of self-directed study and seven months of non-stop building: AI '
            'pipelines that run on real data, with measured numbers, written limitations and public code. I '
            'work from one simple idea: every AI application has five steps and only one invokes a model; '
            'the other four are code. When those are done properly, what is left in the middle fits in one '
            'call, and the result is cheaper, stronger and auditable. I have worked with automotive and food '
            'companies where regulation rules and a silent error is expensive.',
 't_projects': 'Public projects',
 'projects': [('CTSM',
               'epifaneia/ctsm',
               '2026',
               'Audits the requirements of a customer specification (a Polarion ReqIF) against the '
               'supplier’s manuals and returns the same file with the evidence and its exact page. The model '
               'may only cite fragments from a closed list; code verifies every quote against the source and '
               'derives the page from the offset. <span class="n">9/9 against ground truth · 8/9 with a '
               'local 14B model on a 6 GB GPU and zero false "compliant" · round-trip diff tested against 5 '
               'sabotages.</span>'),
              ('reqif-extractor',
               'epifaneia/reqif-extractor',
               '2026',
               'From a specification PDF to a ReqIF that Polarion imports on the first attempt: verbatim '
               'identifiers, document hierarchy, page order. Deterministic identifier policy and type '
               'reconciliation against the source. <span class="n">167 of 170 model-invented identifiers '
               'caught · 1/20 of the vision cost by routing only tables and figures · 12/12 real documents '
               'structurally validated.</span>'),
              ('toolkit',
               'epifaneia/toolkit',
               '2026',
               'The reusable part of every pipeline: one tool per design step, generic guardrails and three '
               'integration wires to the company’s systems (identity, event ledger, sign-off), with tests '
               'and a documented integration for Entra ID, SIEM and PKI.'),
              ('feasibility-study',
               'epifaneia/feasibility-study',
               '2026',
               'From a meeting form to an AI feasibility study in PDF: an autonomous research run across '
               'hundreds of pages, turned by code into a report with our narrative and our order, with cited '
               'sources. Form, FastAPI server, consultant panel and human review before sending.'),
              ('Mildew Detection in Cherry Leaves',
               'cefeidas/Mildew-Detection-in-Cherry-Leaves',
               '2024',
               'Image classifier that tells healthy cherry leaves from those with powdery mildew: a '
               'convolutional network in TensorFlow/Keras trained on <span class="n">5,972 class-balanced '
               'images</span>, 70/10/20 split, <span class="n">99.8% accuracy on the test set</span>. '
               'Streamlit dashboard deployed on Heroku.')],
 't_experience': 'Experience',
 'experience': [('AI Solutions Designer',
                 'March 2026 – present',
                 'Epifaneia · Seville, remote',
                 'Design and delivery of AI pipelines with a chain of custody for industry and regulated '
                 'processes: the three projects above, a mobile voice-conversation app with a model per '
                 'stage, and proofs of concept for automotive and food companies.'),
                ('Bilingual account specialist',
                 '2025 – present',
                 'Foundever · Airbnb programme · Seville',
                 'Advanced customer support in English, in parallel with Epifaneia.'),
                ('Automation programmer and sales agent',
                 'March – December 2024',
                 'Konecta · Seville',
                 'Automated the team’s reporting with Python (Pandas, openpyxl) over Metabase exports, in '
                 'iterations reviewed by the data analysis team.'),
                ('Risk analysis, quality and training',
                 '2017 – 2023',
                 'TaskUs, Prepaid Financial Services, Media Interactiva, Field Management · Ireland and '
                 'Spain',
                 'Financial risk analysis, quality auditing and agent training at TaskUs, including an AI '
                 'model training programme; software QA at Media Interactiva. Six years working in '
                 'English.')],
 't_education': 'Education',
 'education': [('Diploma in Full Stack Software Development',
                '2023 – 2024',
                'Code Institute · university credit-rated (University of the West of Scotland)',
                'The only university credit-rated online coding bootcamp in the UK and Europe. Five '
                'portfolio projects at <a href="https://github.com/cefeidas">github.com/cefeidas</a>: an '
                'accessible website (HTML, CSS), a JavaScript game, a Python game on the Google Sheets API, '
                'a Django library with authentication and reviews, and the convolutional network above.'),
               ('Continuous self-directed study in AI, software architecture and regulation',
                '2018 – present',
                '',
                ''),
               ('University studies in Philosophy and in Physics', 'University of Seville', '', '')]}

def to_pdf(html_path: Path, pdf_path: Path):
    import os
    prof = Path(tempfile.mkdtemp(prefix="edgecv_"))
    tmp = pdf_path.with_name(pdf_path.stem + ".build.pdf")
    if tmp.exists():
        tmp.unlink()
    cmd = [EDGE, "--headless", "--disable-gpu", "--no-first-run", "--user-data-dir=" + str(prof),
           "--no-pdf-header-footer", "--print-to-pdf=" + str(tmp), html_path.as_uri()]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=90)
    for _ in range(60):
        if tmp.exists() and tmp.stat().st_size > 1000:
            break
        time.sleep(0.5)
    shutil.rmtree(prof, ignore_errors=True)
    if not tmp.exists():
        return False
    for i in range(10):
        try:
            os.replace(tmp, pdf_path)
            return True
        except PermissionError:
            time.sleep(1.5)
    print("AVISO: no se pudo sustituir", pdf_path.name, "(abierto en otro programa); la version nueva queda en", tmp.name)
    return True

if __name__ == "__main__":
    import fitz
    OUT.mkdir(parents=True, exist_ok=True)
    for d, suf in ((ES, "ES"), (EN, "EN")):
        html_path = OUT / f"Daniel_Martin_AI_Engineer_{suf}.html"
        pdf_path = OUT / f"Daniel_Martin_AI_Engineer_{suf}.pdf"
        html_path.write_text(page(d), encoding="utf-8")
        ok = to_pdf(html_path, pdf_path)
        doc = fitz.open(pdf_path if not (OUT / (pdf_path.stem + ".build.pdf")).exists() else OUT / (pdf_path.stem + ".build.pdf"))
        n = doc.page_count
        pix = doc[0].get_pixmap(dpi=96)
        png = Path(sys.argv[1]) / f"cv_{suf}.png" if len(sys.argv) > 1 else OUT / f"_preview_{suf}.png"
        pix.save(png)
        print(suf, "pdf ok" if ok else "PDF FAILED", "pages:", n, "->", png)

import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import base64

# Funciones para poder insertar las imagenes
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def get_img_with_href(local_img_path):
    img_format = local_img_path.split('.')[-1]
    binary_data = get_base64_of_bin_file(local_img_path)
    return f"data:image/{img_format};base64,{binary_data}"

# Configuración de la página
st.set_page_config(
    page_title="Dinastía de Bajo Costo | NFL Storytelling",
    page_icon="🏈",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS Global
st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,400&family=Source+Serif+4:ital,wght@0,300;0,400;0,600;1,300&display=swap" rel="stylesheet">
    <style>
    #MainMenu, footer, header { visibility: hidden; }
    /* Eliminar el espacio en blanco superior por defecto de Streamlit */
    [data-testid="block-container"] { padding-top: 0rem !important; }
    [data-testid="stAppViewContainer"] { background-color: "white"; font-family: 'Source Serif 4', Georgia, serif; }
    /* --- CORRECCIÓN DE TEXTO GENERAL --- */
    div[data-testid="stMarkdownContainer"] p, div[data-testid="stMarkdownContainer"] li { font-family: 'Source Serif 4', Georgia, serif !important; font-size: 1.15rem !important; line-height: 1.85 !important; color: #1a1a1a !important; font-weight: 300 !important; }
    /* --- CORRECCIÓN DE TÍTULOS --- */
    div[data-testid="stMarkdownContainer"] h1, div[data-testid="stMarkdownContainer"] h2, div[data-testid="stMarkdownContainer"] h3, div[data-testid="stMarkdownContainer"] h4 { font-family: 'Playfair Display', Georgia, serif !important; color: #1a1a1a !important; letter-spacing: -0.02em !important; }
    hr { border-top: 2px solid #1a1a1a; margin: 3rem 0 2rem; opacity: 0.15; }
    /* --- PULL QUOTE --- */
    .pull-quote { border-left: 5px solid #FFB81C; padding: 0.8rem 1.5rem; margin: 2rem 0; background: rgba(255, 244, 206, 0.4); border-radius: 0 4px 4px 0; }
    .pull-quote p { font-family: 'Playfair Display', serif !important; font-size: 1.3rem !important; font-style: italic !important; color: #1a1a1a !important; margin: 0 !important; }
    /* --- KPIS Y MÉTRICAS (Dimensiones homogéneas) --- */
    [data-testid="stMetric"] { background: #fff; border-radius: 4px; padding: 1rem 1.2rem; border-left: 4px solid #E31837; box-shadow: 0 2px 8px rgba(0,0,0,0.06); height: 100% !important; min-height: 140px; }
    [data-testid="stMetricValue"] { font-family: 'Playfair Display', serif !important; font-size: 1.7rem !important; }
    /* Forzar que el título del KPI baje de renglón atacando todas sus capas internas (*) */
    [data-testid="stMetricLabel"], [data-testid="stMetricLabel"] * { white-space: normal !important; overflow: visible !important; text-overflow: clip !important; line-height: 1.3 !important; }
    </style>
    """,
    unsafe_allow_html=True
)

# Carga de datos
@st.cache_data
def cargar_datos():
    df_pases = pd.read_csv('data/processed/nfl_storytelling_final.csv')
    df_hist_sb = pd.read_csv('data/processed/historico_superbowl_wr.csv')
    df_cap_spotrac = pd.read_csv('data/processed/cap_data_2022.csv')
    return df_pases, df_cap_spotrac, df_hist_sb

df_final, df_cap_spotrac, df_epilogo = cargar_datos()

# Configuración de los hover
estilo_hover = dict(
    bgcolor="#1b1b1b",
    font_size=13,
    font_family="Source Serif 4",
    font_color="white",
    bordercolor="#1b1b1b"
)

# Hero banner
hero_img_base64 = get_img_with_href('assets/hero_banner.jpg')
st.markdown(
    f"""
    <style>
    .hero-section {{
        background-image: linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.8)), url("{hero_img_base64}");
        background-size: cover; background-position: center top; height: 570px;
        display: flex; flex-direction: column; justify-content: flex-end; align-items: flex-start;
        color: white; margin-bottom: 2rem; 
        margin-top: -7rem; 
        padding: 2.5rem calc(50vw - 425px); 
        width: 100vw; position: relative; left: 50%; right: 50%; margin-left: -50vw; margin-right: -50vw;
        
        /* NUEVO: Colocamos el banner en la capa más alta para que oculte el índice al inicio */
        z-index: 200; 
    }}
    .hero-kicker {{ font-family: 'Source Serif 4', serif; font-size: 1rem; text-transform: uppercase; letter-spacing: 0.2em; color: #FFB81C; margin-bottom: 0.5rem; }}
    .hero-title {{ font-family: 'Playfair Display', serif; font-size: 6rem; font-weight: 900; line-height: 1.05; letter-spacing: -0.02em; text-shadow: 2px 4px 15px rgba(0,0,0,0.8); margin-bottom: 0.8rem; color: #fdfbf7; }}
    .hero-subtitle {{ font-family: 'Source Serif 4', serif; font-size: 2rem; font-style: italic; opacity: 0.9; max-width: 600px; line-height: 1.5; }}
    </style>
    <div class="hero-section">
        <div class="hero-kicker">NFL · Análisis Estratégico · 2022–2023</div>
        <div class="hero-title">DINASTÍA DE<br>BAJO COSTO</div>
        <div class="hero-subtitle">La paradoja de ganar el Super Bowl subestimando a los receptores estrella</div>
    </div>
    """, unsafe_allow_html=True)


# Firma (Byline)
st.markdown("""
    <style>
    .article-meta {
        max-width: 850px; margin: 0 auto 0rem auto; display: flex; align-items: center; 
        font-family: 'Source Serif 4', serif; padding-bottom: 2rem; border-bottom: 1px solid #eaeaea;
    }
    .author-avatar {
        width: 48px; height: 48px; border-radius: 50%; background-color: #1a1a1a; 
        display: flex; justify-content: center; align-items: center; margin-right: 15px; 
        font-weight: bold; color: #fdfbf7; font-family: 'Playfair Display', serif; font-size: 1.2rem;
    }
    .author-info { display: flex; flex-direction: column; justify-content: center; }
    .author-name { font-size: 1.1rem; color: #1a1a1a; }
    .article-date { font-size: 0.9rem; color: #8c8c8c; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 2px;}
    </style>
    
    <div class="article-meta">
        <div class="author-avatar">BR</div>
        <div class="author-info">
            <div class="author-name">Por <b>Bruno Gael Ramos Huerta</b></div>
            <div class="article-date">25 de abril de 2026</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Índice
st.markdown("""
    <style>
    /* 1. Hacemos que el contenedor invisible de Streamlit sea el "pegajoso" */
    div[data-testid="stElementContainer"]:has(.toc-container),
    div.element-container:has(.toc-container) {
        position: sticky !important;
        top: 150px !important; /* Dónde se detiene al hacer scroll hacia abajo */
        z-index: 100;
    }

    /* 2. El índice lo "empujamos" limpiamente hacia el margen izquierdo del texto */
    .toc-container {
        position: absolute;
        top: -30px;
        left: -240px;
        width: 170px;
        border-left: 2px solid #eaeaea;
        padding-left: 1.0rem;
    }

    .toc-title { font-family: 'Playfair Display', serif; font-weight: bold; font-size: 1.6rem; margin-bottom: 1rem; color: #1a1a1a; }
    
    /* Mantenemos tu color gris y el efecto rojo al pasar el ratón */
    .toc-container a.toc-link {
        display: block; 
        color: #8c8c8c !important; 
        text-decoration: none !important; 
        font-family: 'Source Serif 4', serif; 
        font-size: 1.0rem; margin-bottom: 0.8rem; transition: all 0.2s ease; line-height: 1.3;
    }
    .toc-container a.toc-link:hover { 
        color: #E31837 !important; 
        border-left: 2px solid #E31837; 
        padding-left: 5px; margin-left: -1rem; font-weight: 600; 
    }
    
    /* Lo ocultamos en pantallas pequeñas para que no choque con el texto */
    @media (max-width: 1150px) { .toc-container { display: none !important; } }
    </style>
    
    <div class="toc-container">
        <div class="toc-title">Índice</div>
        <a class="toc-link" href="#prologo">Prólogo</a>
        <a class="toc-link" href="#acto1">Acto 1: La Paradoja</a>
        <a class="toc-link" href="#transicion">La Estrategia</a>
        <a class="toc-link" href="#acto2">Acto 2: El Tablero</a>
        <a class="toc-link" href="#acto3">Acto 3: Jaque Mate</a>
        <a class="toc-link" href="#epilogo">Epílogo</a>
    </div>
""", unsafe_allow_html=True)

# Glosario Contextual
st.markdown("""
    <style>
    div[data-testid="stElementContainer"]:has(.glossary-container),
    div.element-container:has(.glossary-container) {
        position: sticky !important;
        top: 165px !important;
        z-index: 100;
    }
    .glossary-container {
        position: absolute;
        top: -50px;
        right: -240px;
        width: 170px;
        border-left: 2px solid #E31837;
        padding-left: 1.0rem;
    }
    .glossary-title { font-family: 'Playfair Display', serif; font-weight: bold; font-size: 1.6rem; margin-bottom: 1rem; color: #1a1a1a; }
    .g-term { color: #E31837; font-weight: 600; cursor: help; border-bottom: 1px dotted #E31837; transition: background-color 0.2s ease; }
    .g-term:hover { background-color: rgba(227, 24, 55, 0.1); }
    .glossary-default { display: block; font-family: 'Source Serif 4', serif; font-size: 0.95rem; color: #b3b3b3; font-style: italic; line-height: 1.4; }
    .glossary-def { display: none; font-family: 'Source Serif 4', serif; font-size: 0.95rem; color: #1a1a1a; line-height: 1.5; animation: fadeIn 0.3s ease; }
    .glossary-def b { font-family: 'Playfair Display', serif; font-size: 1.1rem; color: #E31837; display:block; margin-bottom:0.3rem;}
    @keyframes fadeIn { from { opacity: 0; transform: translateX(10px); } to { opacity: 1; transform: translateX(0); } }

    /* Lógica de visualización (Añadido term-wr) */
    :root:has(#term-hill:hover) .def-hill,
    :root:has(#term-reid:hover) .def-reid,
    :root:has(#term-mahomes:hover) .def-mahomes,
    :root:has(#term-air:hover) .def-air,
    :root:has(#term-epa:hover) .def-epa,
    :root:has(#term-cap:hover) .def-cap,
    :root:has(#term-wr:hover) .def-wr { display: block !important; }

    :root:has(.g-term:hover) .glossary-default { display: none !important; }

    @media (max-width: 1150px) { .glossary-container { display: none !important; } }
    </style>
    <div class="glossary-container">
        <div class="glossary-title">Contexto</div>
        <div class="glossary-default">Pasa el cursor sobre las palabras subrayadas en rojo para leer su definición.</div>
        <div class="glossary-def def-hill"><b>Tyreek Hill</b>Receptor estrella apodado "Cheetah". Considerado uno de los jugadores más rápidos y explosivos en la historia de la liga.</div>
        <div class="glossary-def def-reid"><b>Andy Reid</b>Entrenador en Jefe (Head Coach) de los Chiefs. Una de las mentes ofensivas y tácticas más brillantes del deporte.</div>
        <div class="glossary-def def-mahomes"><b>Patrick Mahomes</b>Quarterback de los Chiefs, múltiple ganador del MVP y el brazo ejecutor del sistema ofensivo.</div>
        <div class="glossary-def def-air"><b>Air Yards</b>Yardas Aéreas. La distancia exacta que viaja el balón en el aire desde la línea de golpeo hasta que el receptor lo atrapa.</div>
        <div class="glossary-def def-epa"><b>Métrica EPA</b>Expected Points Added. Métrica avanzada que calcula el valor real en puntos que una jugada específica aportó a la ofensiva.</div>
        <div class="glossary-def def-cap"><b>Tope Salarial</b>Salary Cap. Límite estricto de millones de dólares que cada equipo de la NFL tiene permitido gastar en salarios por temporada.</div>
        <div class="glossary-def def-wr"><b>Receptor Abierto</b>Wide Receiver (WR). Jugador ofensivo especializado en atrapar pases. Suelen alinearse en los extremos del campo para estirar la defensa.</div>
    </div>
""", unsafe_allow_html=True)

# --- Prólogo ---
st.markdown("<div id='prologo'></div>", unsafe_allow_html=True)
st.markdown("## Prólogo: La era de Tyreek Hill")

st.image("assets/tyreek_hill.jpg", caption="Tyreek Hill: El motor de la era explosiva de los Chiefs. From: www.pff.com", use_column_width=True)

st.markdown("""
Entre 2018 y 2021, la ofensiva de Kansas City tenía un nombre propio en las trayectorias profundas: <span class="g-term" id="term-hill">Tyreek Hill</span>. 
Su velocidad no solo generaba yardas, sino que condicionaba a toda la defensa rival. Para muchos analistas, Hill era el motor 
imprescindible que permitía a <span class="g-term" id="term-mahomes">Mahomes</span> arriesgar.

La siguiente visualización muestra el porcentaje de <span class="g-term" id="term-air">yardas aéreas (Air Yards)</span> que recaían exclusivamente en los hombros de Hill 
en comparación con todos los demás receptores del equipo.
""", unsafe_allow_html=True)

# ---

# Preparación de datos
kc_era_hill = df_final[(df_final['posteam'] == 'KC') & (df_final['season'] < 2022)].copy()
kc_era_hill['Jugador'] = kc_era_hill['receiver_player_name'].apply(
    lambda x: 'Tyreek Hill' if x == 'T.Hill' else 'Resto del Equipo'
    )
hill_share = kc_era_hill.groupby(['season', 'Jugador'])['air_yards'].sum().reset_index()
total_por_año = hill_share.groupby('season')['air_yards'].transform('sum')
hill_share['pct'] = (hill_share['air_yards'] / total_por_año * 100).round(1)

# Ordenar para que Hill quede en la base
hill_share['order'] = hill_share['Jugador'].map({'Tyreek Hill': 0, 'Resto del Equipo': 1})
hill_share = hill_share.sort_values(['season', 'order'])

# Gráfico
fig_hill = px.bar(
    hill_share, x='season', y='pct', color='Jugador', barmode='stack',
    title="Porcentaje de Yardas Aéreas: Hill vs. el Equipo",
    color_discrete_map={'Tyreek Hill': '#FFB81C', 'Resto del Equipo': '#E31837'},
    text='pct',
    custom_data=['air_yards']
)

# Estética
fig_hill.update_traces(
    texttemplate='<b>%{text:.0f}%</b>', textposition='inside', insidetextanchor='middle',
    textfont=dict(color='white', size=16), marker_line_width=0,
    hovertemplate='<b>%{fullData.name}</b><br>%{y:.1f}% de yardas aéreas<br>(%{customdata[0]:,.0f} yds totales)<extra></extra>'
)

fig_hill.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(title="", tickmode='array', tickvals=[2018, 2019, 2020, 2021], tickfont=dict(size=14)),
    yaxis=dict(visible=False, range=[0, 100]), 
    legend=dict(title="", orientation="h", yanchor="top", y=-0.15, xanchor="center", x=0.5),
    margin=dict(t=50, b=80, l=0, r=0),
    hoverlabel=estilo_hover
)

st.plotly_chart(fig_hill, use_container_width=True)

# ---

st.markdown("""
Hill no era un receptor más; era una pieza que acaparaba una porción masiva del arsenal aéreo. 
Su salida en 2022 hacia los *Miami Dolphins* dejó un vacío que, en teoría, era imposible de llenar con jugadores promedio.
""")

# Frase
st.markdown("""
<div class="pull-quote">
<p><b>"No buscamos otro Tyreek. Buscamos una forma de no necesitar otro Tyreek."</b></p>
</div>
""", unsafe_allow_html=True)

# --- Acto 1 ---
st.markdown("---")
st.markdown("<div id='acto1'></div>", unsafe_allow_html=True)
st.markdown("## Acto 1: La Paradoja Financiera")

st.markdown("""
¿Cómo respondes a la pérdida de una superestrella? La lógica dicta que deberías buscar un reemplazo igual de caro. 
Sin embargo, <span class="g-term" id="term-reid">Andy Reid</span> y la gerencia de los Chiefs hicieron todo lo contrario: **ahorraron dinero de su billetera**.

Mientras los equipos de la élite vaciaban millones de su <span class="g-term" id="term-cap">tope salarial (Salary Cap)</span> en 2022 para asegurar a sus estrellas, 
Kansas City se posicionó en el extremo opuesto del espectro financiero.
""", unsafe_allow_html=True)

# ---

# Top 5 y Kansas City del dataset de Spotrac
top_5 = df_cap_spotrac.head(5).copy()
kc_data = df_cap_spotrac[df_cap_spotrac['posteam'] == 'KC'].copy()
datos_salarios = pd.concat([top_5, kc_data])

# Logos oficiales basados en las siglas
logos = {
    'LAR': 'https://a.espncdn.com/i/teamlogos/nfl/500/lar.png',
    'NE': 'https://a.espncdn.com/i/teamlogos/nfl/500/ne.png',
    'NYG': 'https://a.espncdn.com/i/teamlogos/nfl/500/nyg.png',
    'LAC': 'https://a.espncdn.com/i/teamlogos/nfl/500/lac.png',
    'MIA': 'https://a.espncdn.com/i/teamlogos/nfl/500/mia.png',
    'KC': 'https://a.espncdn.com/i/teamlogos/nfl/500/kc.png'
}
datos_salarios['URL_Logo'] = datos_salarios['posteam'].map(logos)

# Creación del gráfico de barras
fig_cap = px.bar(
    datos_salarios, 
    x='posteam', 
    y='Gasto_WR_Millones',
    title="Top 5 Inversiones en Receptores vs. Kansas City (2022)",
    text='Gasto_WR_Millones'
)

# Colorear las barras
colores = ['#A5ACAF' if eq != 'KC' else '#E31837' for eq in datos_salarios['posteam']]
fig_cap.update_traces(
    marker_color=colores, 
    texttemplate='<b>%{text:.1f}M</b>', # Redondeamos a 1 decimal
    textposition='inside',
    textfont=dict(color='white', size=14),
    hovertemplate='<b>%{x}</b><br>Inversión: $%{y:.1f}M<extra></extra>'
)

# Insertar los Escudos
for i, row in datos_salarios.iterrows():
    fig_cap.add_layout_image(
        dict(
            source=row['URL_Logo'],
            xref="x", yref="y",
            x=row['posteam'], 
            y=row['Gasto_WR_Millones'] + 6,
            sizex=0.7, sizey=8,
            xanchor="center", yanchor="bottom"
        )
    )

# Ajustes de layout
fig_cap.update_layout(
    showlegend=False, 
    plot_bgcolor='rgba(0,0,0,0)', 
    yaxis=dict(title="Millones de USD", showgrid=True, gridcolor='#e6e6e6', range=[0, 55]),
    xaxis=dict(title="", tickfont=dict(size=14)),
    height=650,
    hoverlabel=estilo_hover 
)

st.plotly_chart(fig_cap, use_container_width=True)

# ---

st.markdown("""
**La apuesta fue:** El dinero ahorrado en una "estrella" se usaría para fortalecer la línea defensiva y la profundidad del roster, 
confiando en que el sistema de juego compensaría la falta de talento individual en los receptores.
""")

# --- Transición táctica ---
st.markdown("---")
st.markdown("<div id='transicion'></div>", unsafe_allow_html=True)
st.markdown("### La Estrategia: ¿Por qué no simplemente correr más?")

# ---

st.image("assets/mahomes_strategy.jpg", caption="Mahomes y Reid. From: www.foxsports.com" , use_column_width=True)

# ---

st.markdown("""
La respuesta común ante la falta de receptores es intentar "equilibrar" la ofensiva corriendo más el balón. 
Sin embargo, Andy Reid sabía que en la NFL moderna, **el juego terrestre es una inversión de bajo retorno.**

Para mantener la eficiencia, los Chiefs no corrieron más; simplemente aprendieron a pasar mejor a jugadores que 
normalmente son ignorados u opacados por otros. La siguiente gráfica justifica esta decisión: el valor esperado de un pase (<span class="g-term" id="term-epa">EPA</span>) 
siempre ha sido superior al de un acarreo, incluso con receptores "promedio".
""", unsafe_allow_html=True)

# ---

# 1. Procesamiento de datos
epa_stats = df_final.groupby(['season', 'play_type'])['epa'].mean().reset_index()
epa_stats['play_type'] = epa_stats['play_type'].map({'pass': 'Pase', 'run': 'Acarreo'})
 
# 2. Gráfico
fig_eficiencia = px.line(
    epa_stats,
    x='season',
    y='epa',
    color='play_type',
    markers=True,
    title="Eficiencia por Jugada: La superioridad del pase (2018-2023)",
    labels={'season': 'Temporada', 'epa': 'EPA Promedio', 'play_type': 'Tipo de Jugada'},
    color_discrete_map={'Pase': '#E31837', 'Acarreo': '#A5ACAF'}
)

# Línea de transición post-Hill
fig_eficiencia.add_vline(x=2021, line_dash="dash", line_color="#FFB81C", line_width=2.5, opacity=0.8)
fig_eficiencia.add_annotation(
    x=2021, y=0.22,
    text="<b>Salida de Tyreek Hill</b>",
    showarrow=False,
    font=dict(color='white', size=11),
    bgcolor="#FFB81C", borderpad=4, bordercolor="#FFB81C"
)


# 3. Estética
fig_eficiencia.update_traces(
    hovertemplate="EPA Promedio: %{y:.2f}           <extra></extra>"
)

fig_eficiencia.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    yaxis=dict(showgrid=True, gridcolor='#e6e6e6', zeroline=True, zerolinecolor='black'),
    hovermode="x unified",
    hoverlabel=estilo_hover
)

st.plotly_chart(fig_eficiencia, use_container_width=True)

# ---

st.markdown("""
Esta gráfica fue la base del éxito de los Chiefs: **el pase más ineficiente de Mahomes sigue siendo, en promedio, 
más productivo que un acarreo promedio.** Con esto en mente, el reto de Reid para 2022 no fue buscar a otro Tyreek Hill, sino diseñar un "nuevo tablero" 
donde el balón pudiera ir a cualquier parte del campo, volviendo a la ofensiva imposible de predecir.
""")

# --- Acto 2 ---
st.markdown("---")
st.markdown("<div id='acto2'></div>", unsafe_allow_html=True)
st.markdown("## Acto 2: El Nuevo Tablero")
st.markdown("""
Con este nuevo sistema de una ofensiva basada en la **entropía y la imprevisibilidad**. 
El campo dejó de ser una autopista vertical, se convirtió en un tablero de distribución horizontal.

Agrupar los datos por "eras" nos permite ver el cambio estructural: observa cómo la concentración de pases cambia de forma y cómo 
la carga de trabajo se reparte entre muchos más jugadores.
""")

# ---

# Control interactivo por épocas
era_seleccionada = st.radio(
    "Selecciona la era a visualizar:",
    options=["Era Tyreek Hill (2018-2021)", "El Nuevo Esquema (2022-2023)"],
    horizontal=True
)

# 1. Filtrar por la epoca que seleccionemos
if era_seleccionada == "Era Tyreek Hill (2018-2021)":
    df_kc_pases = df_final[(df_final['posteam'] == 'KC') & (df_final['play_type'] == 'pass') & (df_final['season'] <= 2021)].copy()
else:
    df_kc_pases = df_final[(df_final['posteam'] == 'KC') & (df_final['play_type'] == 'pass') & (df_final['season'] >= 2022)].copy()

df_kc_pases = df_kc_pases.dropna(subset=['pass_location', 'target_player'])

# Mapear ubicación a coordenadas X y agregar jitter
map_location = {'left': -1.5, 'middle': 0, 'right': 1.5}
df_kc_pases['x_base'] = df_kc_pases['pass_location'].map(map_location)
np.random.seed(42) # Utilizamos random para simular los pases
df_kc_pases['x_jitter'] = df_kc_pases['x_base'] + np.random.uniform(-0.45, 0.45, size=len(df_kc_pases))

# Cálculos para el receptor principal y KPIs
ranking_total = df_kc_pases['target_player'].value_counts()
receptor_top = ranking_total.index[0]
total_pases = len(df_kc_pases)
porcentaje_top1 = (ranking_total.iloc[0] / total_pases) * 100
porcentaje_top3 = (ranking_total.iloc[0:3].sum() / total_pases) * 100

df_kc_pases['Color'] = df_kc_pases['target_player'].apply(lambda x: receptor_top if x == receptor_top else 'Resto del Equipo')

# Métrocas KPI (Tarjetas HTML personalizadas)
# Calcular valores de la era contraria para el delta
if "2018" in era_seleccionada:
    df_otra_era = df_final[(df_final['posteam'] == 'KC') & (df_final['play_type'] == 'pass') & (df_final['season'] >= 2022)].dropna(subset=['pass_location', 'target_player'])
    delta_label = "vs. Era Post-Hill"
else:
    df_otra_era = df_final[(df_final['posteam'] == 'KC') & (df_final['play_type'] == 'pass') & (df_final['season'] <= 2021)].dropna(subset=['pass_location', 'target_player'])
    delta_label = "vs. Era Hill"

ranking_otra = df_otra_era['target_player'].value_counts()
pct_top1_otra = (ranking_otra.iloc[0] / len(df_otra_era) * 100)
pct_top3_otra = (ranking_otra.iloc[0:3].sum() / len(df_otra_era) * 100)

# Cálculos de diferencias
delta_val_1 = porcentaje_top1 - pct_top1_otra
delta_val_3 = porcentaje_top3 - pct_top3_otra

# Lógica de colores
clase_delta_1 = "delta-positivo" if delta_val_1 > 0 else "delta-negativo"
clase_delta_3 = "delta-positivo" if delta_val_3 > 0 else "delta-negativo"

# HTML y CSS inyectado
html_kpis = f"""
<style>
.kpi-row {{ display: flex; gap: 15px; margin-bottom: 2rem; justify-content: space-between; }}
.kpi-card {{ flex: 1; background: #fff; border-radius: 6px; padding: 1.0rem; border-left: 4px solid #E31837; box-shadow: 0 4px 10px rgba(0,0,0,0.05); display: flex; flex-direction: column; justify-content: space-between; box-sizing: border-box; }}
.kpi-title-container {{ display: flex; align-items: flex-start; justify-content: space-between; margin-bottom: 0.5rem; }}
.kpi-label {{ font-family: 'Source Serif 4', serif; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em; color: #666; font-weight: 600; line-height: 1.2; padding-right: 10px;}}
.kpi-val {{ font-family: 'Playfair Display', serif; font-size: 2.2rem; font-weight: 700; color: #1a1a1a; line-height: 1; margin-bottom: 0.5rem; }}
.kpi-delta {{ font-family: 'Source Serif 4', serif; font-size: 0.9rem; font-weight: 600; display: flex; align-items: baseline; gap: 5px; }}
.delta-positivo {{ color: #E31837; }} 
.delta-negativo {{ color: #2b7a4b; }} 
.delta-neutro {{ color: #8c8c8c; font-weight: 400; }}
.kpi-tooltip {{ position: relative; display: inline-block; cursor: help; color: #b3b3b3; font-size: 1rem; line-height: 1; }}
.kpi-tooltip .tooltiptext {{ visibility: hidden; width: 220px; background-color: #1b1b1b; color: #fff; text-align: center; border-radius: 6px; padding: 10px; position: absolute; z-index: 50; bottom: 130%; left: 50%; margin-left: -110px; opacity: 0; transition: opacity 0.2s; font-family: 'Source Serif 4', serif; font-size: 0.85rem; font-weight: 300; text-transform: none; letter-spacing: normal; line-height: 1.4; box-shadow: 0 4px 8px rgba(0,0,0,0.3); }}
.kpi-tooltip .tooltiptext::after {{ content: ""; position: absolute; top: 100%; left: 50%; margin-left: -5px; border-width: 5px; border-style: solid; border-color: #1b1b1b transparent transparent transparent; }}
.kpi-tooltip:hover .tooltiptext {{ visibility: visible; opacity: 1; }}
.kpi-tooltip:hover {{ color: #1a1a1a; }}
</style>
<div class="kpi-row">
    <div class="kpi-card">
        <div class="kpi-title-container">
            <div class="kpi-label">Jugador Principal</div>
            <div class="kpi-tooltip">ⓘ<span class="tooltiptext">El receptor que más pases recibió en esta era en particular.</span></div>
        </div>
        <div class="kpi-val">{receptor_top}</div>
        <div class="kpi-delta delta-neutro">Objetivo más buscado</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-title-container">
            <div class="kpi-label">Dependencia Top 1</div>
            <div class="kpi-tooltip">ⓘ<span class="tooltiptext">Porcentaje de todos los pases de la ofensiva dirigidos exclusivamente a su receptor principal.</span></div>
        </div>
        <div class="kpi-val">{porcentaje_top1:.1f}%</div>
        <div class="kpi-delta {clase_delta_1}">
            {'+' if delta_val_1 > 0 else ''}{delta_val_1:.1f}pp <span style="color:#8c8c8c; font-weight:400;">{delta_label}</span>
        </div>
    </div>
    <div class="kpi-card">
        <div class="kpi-title-container">
            <div class="kpi-label">Dependencia Top 3</div>
            <div class="kpi-tooltip">ⓘ<span class="tooltiptext">Porcentaje de pases dirigidos a los 3 jugadores más buscados. Entre menor sea, el balón se reparte mejor.</span></div>
        </div>
        <div class="kpi-val">{porcentaje_top3:.1f}%</div>
        <div class="kpi-delta {clase_delta_3}">
            {'+' if delta_val_3 > 0 else ''}{delta_val_3:.1f}pp <span style="color:#8c8c8c; font-weight:400;">{delta_label}</span>
        </div>
    </div>
</div>
"""
st.markdown(html_kpis, unsafe_allow_html=True)
st.write("")

# Gráficos
col1, col2 = st.columns([2, 1]) 

# Gráfico de Dispersión
with col1:
    fig_campo = px.scatter(
        df_kc_pases,
        x='x_jitter',
        y='air_yards',
        color='Color',
        custom_data=['target_player', 'epa'], # Usamos custom_data en lugar de hover_data
        title=f"Mapa de Pases de Mahomes ({era_seleccionada})",
        color_discrete_map={receptor_top: '#FFB81C', 'Resto del Equipo': '#E31837'},
        opacity=0.7 
    )

    # Línea de golpeo
    fig_campo.add_hline(
        y=0, line_dash="solid", line_width=3,
        line_color="white", 
        annotation_text="Línea de Golpeo", 
        annotation_position="bottom right",
        annotation_font=dict(color="white", size=12),
        annotation_bgcolor="#1e5433",
        annotation_borderpad=4
    )
    
    # Estética
    fig_campo.update_layout(
        plot_bgcolor="#2A7A4A", 
        xaxis=dict(title="", showgrid=False, zeroline=False, showticklabels=False, range=[-2.5, 2.5]),
        yaxis=dict(title="Profundidad del Pase (Yardas Aéreas)", gridcolor='rgba(255,255,255,0.2)', range=[-15, 75]),
        showlegend=False,
        margin=dict(l=0, r=0, t=40, b=0),
        hoverlabel=estilo_hover,
        height=650
    )
    
    # Configuración del hover
    fig_campo.update_traces(
        hovertemplate='<b>Receptor: %{customdata[0]}</b><br>Profundidad: %{y} yds<br>Eficiencia (EPA): %{customdata[1]:.2f}<extra></extra>'
    )
    
    st.plotly_chart(fig_campo, use_container_width=True)

# Gráfico de Barras
with col2:
    # Seleccionamos top 8 jugadores
    ranking_top = ranking_total.reset_index().head(8)
    ranking_top.columns = ['Jugador', 'Pases Recibidos']
    
    # Mapeo de colores: Dorado para el #1 y rojo para los demás
    colores_barras = [
        '#FFB81C' if jugador == receptor_top else '#E31837' for jugador in ranking_top['Jugador']
        ]
    
    fig_barras = px.bar(
        ranking_top,
        x='Pases Recibidos',
        y='Jugador',
        orientation='h',
        title="Top Objetivos"
    )
    
    # Configuración de colores y hover
    fig_barras.update_traces(
    marker_color=colores_barras,
    hovertemplate='<b>%{y}</b><br>Pases dirigidos: %{x}<extra></extra>'
    )

    fig_barras.update_layout(
        yaxis={'categoryorder':'total ascending'},
        xaxis=dict(title=""),
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        margin=dict(l=0, r=0, t=40, b=0),
        hoverlabel=estilo_hover,
        height=650
    )
    st.plotly_chart(fig_barras, use_container_width=True)
    
# ---
    
# --- Acto 3 ---
st.markdown("---")
st.markdown("<div id='acto3'></div>", unsafe_allow_html=True)
st.markdown("## Acto 3: El Jaque Mate Financiero")
st.markdown("""
*¿Valió la pena el riesgo?* Si cruzamos la inversión que se hizo con la eficiencia real en el campo, el panorama sale a la luz. 

El siguiente gráfico de cuadrantes posiciona a los 32 equipos de la NFL en 2022. 
* El **Eje X** representa los millones invertidos en la posición de receptor.
* El **Eje Y** representa la eficiencia ofensiva aérea (EPA por pase).

**Busca el logo de los Chiefs (KC).** Al revertir el eje del gasto, lo hemos posicionado en el cuadrante de ensueño: 
el mínimo costo a cambio del máximo rendimiento, aislado en el pico superior derecho de la liga.
""")

# ---

# Calculamos el EPA de todos los equipos en 2022
df_epa_2022 = df_final[(df_final['season'] == 2022) & (df_final['play_type'] == 'pass')].copy()
epa_por_equipo = df_epa_2022.groupby('posteam')['epa'].mean().reset_index()

# Merge en ambas tablas usando el dataset unificado de Spotrac
df_cuadrantes = pd.merge(epa_por_equipo, df_cap_spotrac, on='posteam')

# Medianas de la liga para trazar los cuadrantes
mediana_gasto = df_cuadrantes['Gasto_WR_Millones'].median()
mediana_epa = df_cuadrantes['epa'].median()

# Etiquetas y colores
df_cuadrantes['Color'] = df_cuadrantes['posteam'].apply(lambda x: 'rgba(0,0,0,0)' if x == 'KC' else '#A5ACAF')
df_cuadrantes['Etiqueta'] = df_cuadrantes['posteam'].apply(lambda x: '' if x == 'KC' else x)

# Límites
max_epa = df_cuadrantes['epa'].max() + 0.15
min_gasto = df_cuadrantes['Gasto_WR_Millones'].min() - 4 

# Extraer coordenadas de KC para posicionar el logo
kc_data = df_cuadrantes[df_cuadrantes['posteam'] == 'KC'].iloc[0]
kc_spend = kc_data['Gasto_WR_Millones']
kc_epa = kc_data['epa']

# Gráfico de dispersión
fig_cuadrantes = px.scatter(
    df_cuadrantes,
    x='Gasto_WR_Millones',
    y='epa',
    text='Etiqueta', 
    color='Color',
    color_discrete_map="identity",
    custom_data=['posteam'],
    title="Optimización de Recursos: Inversión en WR vs Eficiencia (2022)",
    labels={
        'Gasto_WR_Millones': 'Inversión en WRs (Millones USD)', 
        'epa': 'Eficiencia Aérea (EPA/Pase)'
        }
)

# Estilo
fig_cuadrantes.update_traces(
    textposition='top center', 
    marker=dict(size=10, opacity=0.8),
    hovertemplate="<b>%{customdata[0]}</b><br>Gasto: $%{x:.1f}M<br>Eficiencia (EPA): %{y:.2f}<extra></extra>"
)

# Ejes de los cuadrantes
fig_cuadrantes.add_vline(x=mediana_gasto, line_dash="dash", line_color="#8c8c8c", line_width=2)
fig_cuadrantes.add_hline(y=mediana_epa, line_dash="dash", line_color="#8c8c8c", line_width=2)

# Cuadrante ideal (ARRIBA-DERECHA)
fig_cuadrantes.add_shape(
    type="rect",
    x0=mediana_gasto, y0=mediana_epa, x1=min_gasto, y1=max_epa, # Rango del promedio al mínimo en X
    fillcolor="rgba(43, 122, 75, 0.1)", 
    layer="below",
    line_width=0
)

# Etiquetas de las esquinas
fig_cuadrantes.add_annotation(
    x=0.01, y=0.98, xref="paper", yref="paper",
    text="Alto Gasto / Alta Eficiencia",
    showarrow=False, align="left",
    font=dict(color="#333333", size=11),
    bgcolor="#f0f0f0", borderpad=4
)

fig_cuadrantes.add_annotation(
    x=0.99, y=0.98, xref="paper", yref="paper",
    text="<b>Bajo Gasto / Alta Eficiencia</b><br>El Cuadrante Ideal",
    showarrow=False, align="right",
    font=dict(color="white", size=13),
    bgcolor="#1e5433", borderpad=6, bordercolor="#1e5433", borderwidth=1
)

fig_cuadrantes.add_annotation(
    x=0.01, y=0.02, xref="paper", yref="paper",
    text="Alto Gasto / Baja Eficiencia",
    showarrow=False, align="left",
    font=dict(color="#333333", size=11),
    bgcolor="#f0f0f0", borderpad=4
)

fig_cuadrantes.add_annotation(
    x=0.99, y=0.02, xref="paper", yref="paper",
    text="Bajo Gasto / Baja Eficiencia",
    showarrow=False, align="right",
    font=dict(color="#333333", size=11),
    bgcolor="#f0f0f0", borderpad=4
)

# Insertamos el logo de KC
kc_logo_base64 = get_img_with_href('assets/kc_logo_alpha.png')
fig_cuadrantes.add_layout_image(
    dict(
        source=kc_logo_base64,
        xref="x", yref="y",
        x=kc_spend, y=kc_epa,
        sizex=3, sizey=1,
        xanchor="center", yanchor="middle"
    )
)

# Anotación para el logo de KC
fig_cuadrantes.add_annotation(
    x=kc_spend, y=kc_epa + 0.03, 
    text="<b>KC</b>",
    showarrow=False, font=dict(color="#E31837", size=14)
)

# Flecha Mayor Gasto (Hacia la izquierda)
fig_cuadrantes.add_annotation(
    x=0.02, y=-0.09, xref="paper", yref="paper",
    text="← <b>Mayor Gasto</b>", showarrow=False,
    font=dict(size=12, color="#8c8c8c")
)
# Flecha Menor Gasto (Hacia la derecha)
fig_cuadrantes.add_annotation(
    x=0.98, y=-0.09, xref="paper", yref="paper",
    text="<b>Menor Gasto</b> →", showarrow=False,
    font=dict(size=12, color="#8c8c8c")
)

# Layout finales y revertimos el eje X
fig_cuadrantes.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(
        showgrid=True, gridcolor='#e6e6e6', 
        # Forzamos el rango dinámico revertido: de max_gasto a min_gasto
        range=[df_cuadrantes['Gasto_WR_Millones'].max() + 4, min_gasto] 
    ),
    yaxis=dict(showgrid=True, gridcolor='#e6e6e6', range=[df_cuadrantes['epa'].min() - 0.05, max_epa]),
    height=650,
    margin=dict(t=50, b=50, l=50, r=50),
    hoverlabel=estilo_hover
)

st.plotly_chart(fig_cuadrantes, use_container_width=True)

# ---

st.markdown("""
El éxito del esquema de <span class="g-term" id="term-reid">Andy Reid</span> se basa en identificar ineficiencias en el mercado de la NFL. 
En lugar de sobrepagar por talento individual, optaron por distribuir el balón mediante un esquema complejo que eleva el valor 
de piezas de bajo costo, garantizando un rendimiento superior al resto de la liga.
""", unsafe_allow_html=True)

# --- Epílogo ---
st.markdown("---")
st.markdown("<div id='epilogo'></div>", unsafe_allow_html=True)
st.markdown("## Epílogo: El Estándar de Oro")

st.markdown("""
Es fácil pensar que la temporada 2022 de los Chiefs fue una anomalía, un "golpe de suerte" 
impulsado por la genialidad de <span class="g-term" id="term-mahomes">Patrick Mahomes</span>. Sin embargo, la historia reciente de la NFL nos cuenta una verdad incómoda 
para los equipos que gastan fortunas en la agencia libre.

La siguiente gráfica traza a los últimos 10 campeones del Super Bowl y su **Ranking de Inversión** dentro de los 
32 equipos en la posición de <span class="g-term" id="term-wr">Receptor Abierto (WR)</span>.
""", unsafe_allow_html=True)

# ---

# Aseguramos que la columna Campeón_Label exista para la etiqueta del hover
if 'Campeón_Label' not in df_epilogo.columns:
    df_epilogo['Campeón_Label'] = '<b>' + df_epilogo['Campeón'] + '</b>'

# Gráfico de línea
fig_epilogo = px.line(
    df_epilogo,
    x='Temporada',
    y='Ranking',
    hover_name='Campeón',
    title="El Umbral del Campeonato: Inversión en WRs del Ganador del Super Bowl"
)

# Ticks
fig_epilogo.update_yaxes(
    title="Ranking de Gasto",
    tickvals=[1, 8, 16, 24, 32],
    range=[36, 0],
    zeroline=False
)
fig_epilogo.update_xaxes(title="Temporada del Campeonato", dtick=1)

# Sombreamos el Top 5 en rojo tenue
fig_epilogo.add_shape(
    type="rect",
    x0=2013, x1=2024,
    y0=1, y1=5,
    fillcolor="rgba(227, 24, 55, 0.08)",
    layer="below",
    line_width=0
)

# Etiqueta de la zona roja
fig_epilogo.add_annotation(
    x=2018.5, y=3, 
    text="<b>Zona de Gasto de Élite (Top 5)</b><br>Solo 1 campeón en 10 años",
    showarrow=False,
    font=dict(color="#E31837", size=13) 
)

# Línea divisoria del Top 10
fig_epilogo.add_hline(y=10, line_dash="dash", line_color="#8c8c8c", line_width=2)

# Etiqueta
fig_epilogo.add_annotation(
    x=2023, y=10.7, 
    text="<i>El Umbral del Top 10</i>",
    showarrow=False, align="left",
    font=dict(color="white", size=12),
    bgcolor="#1e5433",
    borderpad=4
)

# Quitamos el texto y dejamos solo la línea y un área para el hover
fig_epilogo.update_traces(
    mode="lines+markers", 
    marker=dict(size=30, color="rgba(0,0,0,0)"), 
    line=dict(color="#A5ACAF", width=3),
    hovertemplate="<b>%{hovertext}</b><br>Temporada: %{x}<br>Ranking de Gasto: #%{y}<extra></extra>"
)

# Inyectamos de nuevo los escudos en cada nodo
for i, row in df_epilogo.iterrows():
    fig_epilogo.add_layout_image(
        dict(
            source=row['URL_Logo'],
            xref="x", yref="y",
            x=row['Temporada'],
            y=row['Ranking'],
            sizex=0.9, sizey=4.3,
            xanchor="center", yanchor="middle"
        )
    )

fig_epilogo.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=dict(showgrid=True, gridcolor="#e6e6e6"),
    xaxis=dict(showgrid=False),
    height=650, 
    margin=dict(t=50, b=50, l=50, r=50),
    hovermode="closest", 
    hoverlabel=estilo_hover
)

st.plotly_chart(fig_epilogo, use_container_width=True)

# ---

st.markdown("""
A pesar de la obsesión de la liga por encontrar un receptor estrella, la verdad es que **el gasto de élite no es un requisito para el campeonato.** 

En la última década, solo un equipo logró coronarse estando dentro del Top 5 de mayor inversión en receptores. Aún más impactante: *el 90% de los campeones construyeron sus plantillas fuera del Top 10*.

Las verdaderas dinastías, como los Patriots en su era de dominio, o como los actuales Chiefs, han monopolizado los anillos ubicándose constantemente cerca del **fondo del gasto**.

La reestructuración de Kansas City no fue un experimento desesperado; fue la prueba más directa para comprobar que **las dinastías no se compran con receptores caros, se construyen con sistemas inteligentes.**
""")

st.markdown("""
""")

# ---

st.image("assets/team_celebration.jpg", caption="Patrick Mahomes celebrando la victoria del Super Bowl LIV en 2020. From: cnnespanol.cnn.com", use_column_width=True)

# ---

st.markdown("""
<div class="pull-quote">
<p><b>En la NFL moderna, no pagas por la pieza. Pagas por el sistema.</b></p>
</div>
""", unsafe_allow_html=True)

# --- Bibliografía ---
st.markdown("---")
st.markdown("### *Fuentes de Datos*")
st.markdown("""
* **Datos de Campo (Play-by-Play & Rosters):** Extraídos mediante la API oficial de la NFL a través de la librería `nfl_data_py`. Se procesaron miles de registros para aislar el juego aéreo, medir la distribución de pases y calcular el *Expected Points Added (EPA)*.
* **Datos Financieros (Salary Cap):** La métrica de inversión utilizada corresponde al *Positional Cap Hit* de la unidad de Receptores Abiertos (WR). Estos datos fueron recopilados de los registros históricos oficiales de **Spotrac** y **Over The Cap**, plataformas estándar en la contabilidad deportiva.
* **Procesamiento:** Los datos fueron limpiados y cruzados utilizando `pandas`. Las visualizaciones interactivas fueron desarrolladas íntegramente con `plotly`.

***Aviso:*** Las fotografías e insignias de equipos utilizadas en este proyecto son propiedad de sus respectivos dueños y de la National Football League (NFL). Se utilizan aquí exclusivamente con fines educativos, de análisis de datos y bajo la doctrina de uso justo (Fair Use), sin fines de lucro.
""")
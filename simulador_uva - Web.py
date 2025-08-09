import streamlit as st
import pandas as pd
import requests
from PIL import Image
from bs4 import BeautifulSoup
import os


def format_num(n):
    return f"{int(round(n)):,}".replace(",", ".")
   
def cuota_sistema_frances(prestamo_maximo, interes_banco, total_cuotas):
    i = interes_banco / 12  # tasa mensual decimal
    cuota = prestamo_maximo * (i * (1 + i)**total_cuotas) / ((1 + i)**total_cuotas - 1)
    return cuota

valor_uva = st.cache_data(ttl=60*60*20)(lambda: int(float(next(tr.find_all('td')[2].text.strip().replace('.', '').replace(',', '.') for tr in BeautifulSoup(requests.get("https://www.bcra.gob.ar/PublicacionesEstadisticas/Principales_variables.asp", verify=False).text, 'html.parser').find_all('tr') if tr.find('td') and "Unidad de Valor Adquisitivo (UVA)" in tr.find('td').text))))()


# Configuración de página
st.set_page_config(page_title="Simulador Crédito UVA", layout="centered")


#dolares
oficial = st.cache_data(ttl=60*60*5)(lambda: requests.get("https://dolarapi.com/v1/dolares/oficial").json())()
blue = st.cache_data(ttl=60*60*5)(lambda: requests.get("https://dolarapi.com/v1/dolares/blue").json())()
uva = valor_uva
st.markdown(f"""
<style>
@media (max-width: 768px) {{
    .dolar-box {{
        position: relative !important;
        width: 90% !important;
        left: auto !important;
        top: auto !important;
        margin: 20px auto !important;
        font-size: 14px !important;
    }}
}}

.dolar-box {{
    position: fixed;
    left: 20px;
    top: 100px;
    background: white;
    padding: 15px;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    width: 250px;
    z-index: 999;
    font-size: 18px;
    font-weight: bold;
    color: #222222;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}}

.dolar-box > div {{
    color: #222222;
}}
</style>

<div class="dolar-box">
    <div style="padding:10px 15px; margin:5px 0; border-radius:5px; border-left:4px solid #4CAF50;">
        🏦 Oficial: ${oficial['venta']:,.0f}
    </div>
    <div style="padding:10px 15px; margin:5px 0; border-radius:5px; border-left:4px solid #2196F3;">
        💵 Blue: ${blue['venta']:,.0f}
    </div>
    <div style="padding:10px 15px; margin:5px 0; border-radius:5px; border-left:4px solid #FF9800;">
        📊 UVA: ${uva:,.0f}
    </div>
</div>
""", unsafe_allow_html=True)

# Tarjeta LinkedIn 
st.markdown(
    """
    <style>
    .creator-text {
        position: sticky;
        left: 20px;
        top: 60px;
        width: 250px;
        font-weight: bold;
        font-size: 14px;
        user-select: none;
        z-index: 999;
        color: black;
    }
    .creator-text a {
        color: black;
        text-decoration: underline;
    }
    @media (prefers-color-scheme: dark) {
        .creator-text {
            color: white;
        }
        .creator-text a {
            color: white;
        }
    }
    </style>

    <div class="creator-text">
        👨‍💻📊 Created by <a href="https://www.linkedin.com/in/nahuel-martin/" target="_blank">Nahuel Zanzi</a>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("""
    <style>
        .sidebar-nav {
            position: fixed;
            top: 100px;
            left: 20px;
            background: white;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            z-index: 999;
            width: 250px;
        }
        .sidebar-nav div {
            cursor: pointer;
            padding: 10px 15px;
            margin: 5px 0;
            font-size: 18px;
            font-weight: bold;
            border-radius: 5px;
            transition: all 0.3s;
        }
        .sidebar-nav div:hover {
            background-color: #f0f2f6;
            transform: translateX(5px);
        }
        
        .stButton>button {
            font-size: 18px !important;
            padding: 10px 24px !important;
            height: auto !important;
        }
        
        header > div:first-child {
            padding-top: 0px !important;
            padding-bottom: 0px !important;
        }
        .css-1v3fvcr h1 {
            margin-top: 0px !important;
            margin-bottom: 8px !important;
            text-align: left;
        }
        main > div.block-container {
            padding-left: 300px !important;
        }


        }
    </style>
""", unsafe_allow_html=True)

# Sección Simulador
st.markdown('<div id="simulador"></div>', unsafe_allow_html=True)
st.title("\n\n\n\n🏡 Simulador de Crédito UVA")
st.markdown(
    "¡Importante! Se trata de valores aproximados y **no representan el monto exacto que vas a pagar**.  \n"
    "Completá los valores abajo y presioná **Calcular**:"
)

valor_propiedad = st.number_input("💰 Valor de la propiedad (USD)", min_value=0, step=1000, format="%d")

col1, col2 = st.columns(2)

with col1:
    comision_inmobiliaria = st.number_input("🏠 Comisión inmobiliaria (%)", min_value=0.0, max_value=100.0, step=0.1, value=4.5, format="%.1f") / 100
    costo_gastos = st.number_input("📟 Costo gastos (escribano, sellos, etc.) (%)", min_value=0.0, max_value=100.0, step=0.1, value=4.5, format="%.1f") / 100
    interes_banco = st.number_input("🏦 Interés del banco (%)", min_value=0.0, max_value=100.0, step=0.1, value=4.5, format="%.1f") / 100

with col2:
    porcentaje_prestamo = st.number_input("💵 % que te presta el banco (%)", min_value=0, max_value=100, step=1, value=75, format="%d") / 100
    anios_credito = st.number_input("📅 Años del crédito", min_value=1, value=20)
    relacion_cuota_ingreso = st.number_input("⚖️ Relación cuota/ingreso (%)", min_value=0.0, max_value=100.0, step=0.1, value=25.0, format="%.1f") / 100

# Inicializar valores en session_state
if 'custom_dolar' not in st.session_state:
    st.session_state.custom_dolar = int(oficial['venta'])
if 'ver_en_pesos' not in st.session_state:
    st.session_state.ver_en_pesos = False
if 'mostrar_resultados' not in st.session_state:
    st.session_state.mostrar_resultados = False

# --- Controles Compactos ---
cols = st.columns([0.7, 2, 0.7]) s

with cols[0]: 
    if st.button("Calcular"): 
        st.session_state.mostrar_resultados = True

with cols[1]: 
    col_label, col_radio = st.columns([1, 3]) 
    with col_label:
        st.write("") 
    with col_radio:
        opcion_moneda = st.radio(
            "",  
            ["USD", "Pesos", "UVAs"],
            index=0,
            key="opcion_moneda",
            horizontal=True,
            label_visibility="collapsed"  
        )
        # Actualiza las variables de sesión
        st.session_state.ver_en_usd = (opcion_moneda == "USD")
        st.session_state.ver_en_pesos = (opcion_moneda == "Pesos")
        st.session_state.ver_en_uva = (opcion_moneda == "UVAs")


if st.session_state.mostrar_resultados:
    # Cálculos
    gastos = valor_propiedad * costo_gastos
    comision = valor_propiedad * comision_inmobiliaria
    total_con_gastos = valor_propiedad + gastos + comision
    prestamo_maximo = valor_propiedad * porcentaje_prestamo
    ahorro_necesario = total_con_gastos - prestamo_maximo
    total_cuotas = (12 * anios_credito)
    cuota_mensual = cuota_sistema_frances(prestamo_maximo, interes_banco, total_cuotas)
    ingresos_minimos = (cuota_mensual * st.session_state.custom_dolar) / relacion_cuota_ingreso

    st.markdown('<div id="resultados"></div>', unsafe_allow_html=True)

    st.subheader("📊 Resultados del cálculo")

# --- Función Format_Valor ---
    def format_valor(valor_usd):
        valor_pesos = valor_usd * st.session_state.custom_dolar
        if st.session_state.get('ver_en_pesos'): return f"ARS {format_num(int(valor_pesos))}"
        if st.session_state.get('ver_en_uva'): return f"UVA {format_num(valor_pesos/valor_uva)}"
        return f"USD {format_num(valor_usd)}"
    

    # Mostrar resultados
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="metric-label">🔧 Gastos estimados</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{format_valor(gastos)}</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-label">🏠 Comisión inmobiliaria</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{format_valor(comision)}</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-label">💸 Ahorro necesario</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{format_valor(ahorro_necesario)}</div>', unsafe_allow_html=True)

    col4, col5, col6 = st.columns(3)
    with col4:
        st.markdown('<div class="metric-label">🏷️ Total con gastos</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{format_valor(total_con_gastos)}</div>', unsafe_allow_html=True)
    with col5:
        st.markdown('<div class="metric-label">🏦 Préstamo máximo</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{format_valor(prestamo_maximo)}</div>', unsafe_allow_html=True)
    with col6:
        st.markdown('<div class="metric-label">📅 Cuota mensual</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{format_valor(cuota_mensual)}</div>', unsafe_allow_html=True)

    col_left, col_center, col_right = st.columns([1, 0.2, 90])
    with col_right:
        st.markdown('<div class="metric-label">💼 Ingresos mínimos requeridos</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">ARS {format_num(int(ingresos_minimos))}</div>', unsafe_allow_html=True)


# --- Variabilidad del tipo de cambio ---
st.markdown('<div id="variabilidad-cambio"></div>', unsafe_allow_html=True)
st.subheader("📈 Variabilidad del tipo de cambio")

dolar_esperado = st.number_input(
    "Valor del dólar esperado al momento de comprar:",
    min_value=1,
    value=int(oficial['venta']),  # Valor por defecto (dólar oficial actual)
    step=1,
    format="%d"
)

if st.button("Ver Variación"):
    if 'prestamo_maximo' in locals():
        # Calcular diferencia
        prestamo_pesos = prestamo_maximo * st.session_state.custom_dolar
        nuevo_valor_usd = prestamo_pesos / dolar_esperado
        diferencia = prestamo_maximo - nuevo_valor_usd
        
        if diferencia > 0:
            st.warning(f"⚠️ Con este valor del dólar te **faltarán** {format_num(abs(diferencia))} dólares")
        elif diferencia < 0:
            st.success(f"✅ Con este valor del dólar te **sobrarán** {format_num(abs(diferencia))} dólares")
        else:
            st.info("El valor del dólar no genera variación en tu préstamo")
    else:
        st.error("Primero debes calcular tu préstamo máximo usando el simulador")


# Info Bancos con fuente clickeable
st.markdown('<div id="info_banco"></div>', unsafe_allow_html=True)
st.markdown(
    """
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <h2 style="margin: 0;">🏦 Información por Banco</h2>
    </div>
    """,
    unsafe_allow_html=True
)


# Cargar datos
url_excel = "https://github.com/NahuelZanzi/creditos_uva/raw/main/Comprar%20Propiedad%20-%20Credito%20UVA.xlsx"
df = pd.read_excel(url_excel, sheet_name="Bancos")

bancos_disponibles = [col for col in df.columns if col not in ['Categoria']]

if bancos_disponibles:
    st.markdown("### Selecciona un banco para ver su información:")
    banco_seleccionado = st.selectbox(
        "",
        options=bancos_disponibles,
        label_visibility="collapsed"
    )
    
    df_filtrado = df[['Categoria', banco_seleccionado]].copy()
    df_filtrado.columns = ['Categoría', banco_seleccionado]


   # Mapeo banco -> ruta relativa a la carpeta del proyecto en git
    imagenes_bancos = {
        "galicia": "Imagenes Banco/galicia.png",
        "comafi": "Imagenes Banco/comafi.png",
        "bbva": "Imagenes Banco/bbva.png",
        "hipotecario": "Imagenes Banco/hipotecario.png",
        "supervielle": "Imagenes Banco/Supervielle.png",
        "banco nación": "Imagenes Banco/nacion.png",
        "banco ciudad": "Imagenes Banco/ciudad.png",
        "santander": "Imagenes Banco/santander.png",
        "patagonia": "Imagenes Banco/patagonia.png",
        "macro": "Imagenes Banco/macro.png",
        "brubank": "Imagenes Banco/Brubank.png",
        "icbc": "Imagenes Banco/ICBC.png",
        "credicoop": "Imagenes Banco/credicoop.png",
        "banco del sol": "Imagenes Banco/banco del sol.png"
    }

    banco_key = banco_seleccionado.lower()
    if banco_key in imagenes_bancos:
        try:
            imagen = Image.open(imagenes_bancos[banco_key])
            st.image(imagen, width=180, output_format="PNG")
        except Exception as e:
            st.error(f"No se pudo cargar la imagen de {banco_seleccionado}: {e}")

    st.dataframe(
        df_filtrado,
        height=min(400, 35 * (len(df_filtrado) + 1)),
        width=700,
        hide_index=True,
        column_config={
            'Categoría': st.column_config.TextColumn(width="medium"),
            banco_seleccionado: st.column_config.TextColumn(width="medium")
        }
    )
else:
    st.error("No se encontraron columnas de bancos en el archivo.")

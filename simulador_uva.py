import streamlit as st

# Configuración de página
st.set_page_config(page_title="Simulador Crédito UVA", layout="centered")

# CSS personalizado para ajustes visuales
st.markdown("""
    <style>
        /* Ajustar inputs font size */
        .stTextInput>div>div>input,
        .stNumberInput>div>div>input {
            font-size: 18px;
        }
        /* Estilo labels y valores resultado centrados */
        .metric-label {
            font-size: 20px !important;
            font-weight: bold;
            color: #444;
            text-align: center;
        }
        .metric-value {
            font-size: 20px !important;
            text-align: center;
        }
        /* Botón gris oscuro */
        .stButton>button {
            background-color: #555555;
            color: white;
            border-radius: 5px;
            font-size: 16px;
            padding: 6px 12px;
        }
        /* Mover título más arriba, a la izquierda y reducir margen arriba */
        .css-1v3fvcr h1 {
            margin-top: 5px !important;
            margin-bottom: 10px !important;
            text-align: left;
        }
        /* Reducir espacio blanco arriba de todo (header) para que no haya scroll */
        header > div:first-child {
            padding-top: 5px !important;
            padding-bottom: 5px !important;
        }
        /* Centrar contenido columnas resultados */
        .stColumns [class*="css-"] > div {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🏡 Simulador de Crédito UVA")

st.markdown("Calculadora interactiva de crédito hipotecario en UVA. Completá los valores abajo y presioná **Calcular**:")

# Entradas usuario
valor_propiedad = st.number_input("💰 Valor de la propiedad (USD)", min_value=0.0, step=1000.0)

col1, col2 = st.columns(2)

with col1:
    comision_inmobiliaria = round(st.number_input("🏠 Comisión inmobiliaria (%)", min_value=0.0, step=0.1, format="%.1f", value=4.5), 1) / 100
    costo_gastos = round(st.number_input("🧾 Costo gastos (escribano, sellos, etc.) (%)", min_value=0.0, step=0.1, format="%.1f", value=4.5), 1) / 100
    interes_banco = round(st.number_input("🏦 Interés del banco (%)", min_value=0.0, step=0.1, format="%.1f", value=4.5), 1) / 100

with col2:
    porcentaje_prestamo = round(st.number_input("💵 % que te presta el banco (%)", min_value=0.0, step=0.1, format="%.1f", value=75.0), 1) / 100
    anios_credito = st.number_input("📅 Años del crédito", min_value=1, value=20)

calcular = st.button("Calcular")

if calcular:
    gastos = valor_propiedad * costo_gastos
    comision = valor_propiedad * comision_inmobiliaria
    total_con_gastos = valor_propiedad + gastos + comision
    prestamo_maximo = valor_propiedad * porcentaje_prestamo
    ahorro_necesario = total_con_gastos - prestamo_maximo
    cuota_mensual = prestamo_maximo / (12 * anios_credito)

    # Formatear números sin decimales y con separador de miles '.'
    def format_num(n):
        return f"{int(round(n)):,}".replace(",", ".")

    st.markdown("---")
    st.subheader("📊 Resultados del cálculo")

    col_res1, col_res2, col_res3 = st.columns(3)
    with col_res1:
        st.markdown('<div class="metric-label">🔧 Gastos estimados</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">USD {format_num(gastos)}</div>', unsafe_allow_html=True)

    with col_res2:
        st.markdown('<div class="metric-label">🏠 Comisión inmobiliaria</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">USD {format_num(comision)}</div>', unsafe_allow_html=True)

    with col_res3:
        st.markdown('<div class="metric-label">💸 Ahorro necesario</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">USD {format_num(ahorro_necesario)}</div>', unsafe_allow_html=True)

    col_res4, col_res5, col_res6 = st.columns(3)
    with col_res4:
        st.markdown('<div class="metric-label">🏷️ Total con gastos</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">USD {format_num(total_con_gastos)}</div>', unsafe_allow_html=True)

    with col_res5:
        st.markdown('<div class="metric-label">🏦 Préstamo máximo</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">USD {format_num(prestamo_maximo)}</div>', unsafe_allow_html=True)

    with col_res6:
        st.markdown('<div class="metric-label">📅 Cuota mensual</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">USD {format_num(cuota_mensual)}</div>', unsafe_allow_html=True)

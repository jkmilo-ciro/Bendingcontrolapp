import streamlit as st
import math

# Configuración básica
st.set_page_config(page_title="Piping Control v1.0")

# Estilo de colores (Verde y Negro)
st.markdown("""
    <style>
    .stApp { background-color: #121212; color: #FFFFFF; }
    div.stButton > button {
        background-color: #00FF7F; color: black; font-weight: bold;
        width: 100%; border-radius: 10px; height: 50px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("PIPING CONTROL V1.0")
st.write("Maestría en Trazado y Cuadrantes")

# Entradas de datos
id_linea = st.text_input("ID DE JUNTA / LÍNEA")
diametro = st.number_input("Ø TUBO (PULG)", min_value=0.0)

col1, col2 = st.columns(2)
with col1:
    ang_a = st.number_input("ANG. HORIZ (A°)")
    sent_h = st.selectbox("SENTIDO H", ["DERECHA (CHD)", "IZQUIERDA (CHI)"])
with col2:
    ang_b = st.number_input("ANG. VERT (B°)")
    sent_v = st.selectbox("SENTIDO V", ["SUPERIOR (CS)", "INFERIOR (CI)"])

if st.button("CALCULAR Y POSICIONAR"):
    if diametro > 0:
        rad_a = math.radians(ang_a)
        rad_b = math.radians(ang_b)
        
        # Ángulo Combinado
        cos_c = max(-1, min(1, math.cos(rad_a) * math.cos(rad_b)))
        ang_c = math.degrees(math.acos(cos_c))
        
        # Giro en mm
        constante = (math.pi * diametro * 25.4) / 360
        giro_mm = 0.0
        if math.tan(rad_b) != 0:
            giro_deg = math.degrees(math.atan(math.sin(rad_a) / math.tan(rad_b)))
            giro_mm = abs(giro_deg * constante)

        # Resultados
        st.success(f"MEDIDA DE GIRO: {giro_mm:.2f} mm")
        st.write(f"Ángulo Combinado: {ang_c:.2f}°")
        
        # Lógica basada en tu dibujo manual
        ref = "SUPERIOR" if "INFERIOR" in sent_v else "INFERIOR"
        lado = "IZQUIERDA" if "DERECHA" in sent_h else "DERECHA"
        st.info(f"📍 MARCAR: Desde el eje **{ref}**, girar hacia la **{lado}**.")
    else:
        st.error("Introduce el diámetro del tubo.")
        

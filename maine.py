import streamlit as st
import math
import matplotlib.pyplot as plt

# Configuración visual estilo profesional
st.set_page_config(page_title="Piping Control v1.0", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #121212; color: #FFFFFF; }
    .title { color: #00FF7F; text-align: center; font-size: 30px; font-weight: bold; margin-bottom: 0px;}
    div.stButton > button {
        background-color: #00FF7F; color: black; font-weight: bold;
        width: 100%; border-radius: 10px; height: 50px; border: none;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="title">PIPING CONTROL V1.0</p>', unsafe_allow_html=True)
st.caption("MAESTRÍA EN TRAZADO Y CUADRANTES")

# Entradas de datos
id_linea = st.text_input("ID DE JUNTA / LÍNEA")
diametro = st.number_input("Ø TUBO (PULG)", min_value=0.0)

c1, c2 = st.columns(2)
with c1:
    ang_h = st.number_input("ANG. HORIZ (A°)")
    sent_h = st.selectbox("SENTIDO H", ["DERECHA (CHD)", "IZQUIERDA (CHI)"])
with c2:
    ang_v = st.number_input("ANG. VERT (B°)")
    sent_v = st.selectbox("SENTIDO V", ["SUPERIOR (CS)", "INFERIOR (CI)"])

if st.button("CALCULAR Y POSICIONAR"):
    if diametro > 0:
        # Cálculos
        rad_a, rad_b = math.radians(ang_h), math.radians(ang_v)
        cos_c = max(-1, min(1, math.cos(rad_a) * math.cos(rad_b)))
        ang_c = math.degrees(math.acos(cos_c))
        
        # Giro en mm
        constante = (math.pi * diametro * 25.4) / 360
        giro_deg = math.degrees(math.atan(math.sin(rad_a) / math.tan(rad_b))) if math.tan(rad_b) != 0 else 0
        giro_mm = abs(giro_deg * constante)

        # MOSTRAR RESULTADOS
        st.success(f"### GIRO: {giro_mm:.2f} mm")
        
        # --- DIBUJO DEL DIAGRAMA ---
        fig, ax = plt.subplots(figsize=(4, 4))
        fig.patch.set_facecolor('#121212')
        ax.set_facecolor('#121212')
        
        # Círculo del tubo
        circle = plt.Circle((0, 0), 1, color='#00FF7F', fill=False, lw=3)
        ax.add_artist(circle)
        
        # Ejes
        ax.axhline(0, color='#333', lw=1)
        ax.axvline(0, color='#333', lw=1)
        
        # Lógica de la flecha según tu dibujo
        # Partimos de arriba (CI) o de abajo (CS)
        start_angle = 90 if sent_v == "INFERIOR (CI)" else 270
        direction = -1 if sent_h == "DERECHA (CHD)" else 1
        end_angle = start_angle + (45 * direction) # 45 es representativo para la flecha
        
        # Dibujar flecha indicativa
        ax.annotate("", xy=(math.cos(math.radians(end_angle)), math.sin(math.radians(end_angle))),
                    xytext=(math.cos(math.radians(start_angle)), math.sin(math.radians(start_angle))),
                    arrowprops=dict(arrowstyle="->", color="#00FF7F", lw=4, connectionstyle="arc3,rad=.3"))
        
        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-1.2, 1.2)
        ax.axis('off')
        st.pyplot(fig)
        
        # Instrucción final
        ref = "SUPERIOR" if "INFERIOR" in sent_v else "INFERIOR"
        lado = "IZQUIERDA" if "DERECHA" in sent_h else "DERECHA"
        st.info(f"📍 MARCAR: Desde el eje **{ref}**, medir **{giro_mm:.2f} mm** hacia la **{lado}**.")
        

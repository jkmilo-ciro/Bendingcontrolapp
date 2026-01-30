import streamlit as st
import math
import matplotlib.pyplot as plt
import numpy as np

# Configuración y Estilo
st.set_page_config(page_title="Piping Control v1.0", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    div.stButton > button {
        background-color: #00FF7F; color: black; font-weight: bold;
        width: 100%; border-radius: 8px; height: 50px; border: none;
    }
    .res-box { background-color: #1E2631; padding: 15px; border-radius: 10px; border-left: 5px solid #00FF7F; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h2 style='color:#00FF7F; text-align:center;'>PIPING CONTROL V1.0</h2>", unsafe_allow_html=True)

# Entradas
id_linea = st.text_input("ID DE JUNTA / LÍNEA")
diam_p = st.number_input("Ø TUBO (PULG)", min_value=0.0, step=0.5, value=56.0)

c1, c2 = st.columns(2)
with c1:
    ang_h = st.number_input("ANG. HORIZ (A°)", value=0.0)
    sent_h = st.selectbox("SENTIDO H", ["DERECHA (CHD)", "IZQUIERDA (CHI)"])
with c2:
    ang_v = st.number_input("ANG. VERT (B°)", value=0.0)
    sent_v = st.selectbox("SENTIDO V", ["SUPERIOR (CS)", "INFERIOR (CI)"])

if st.button("CALCULAR Y POSICIONAR"):
    if diam_p > 0:
        rad_a, rad_b = math.radians(ang_h), math.radians(ang_v)
        circ = math.pi * diam_p * 25.4
        giro_deg = math.degrees(math.atan(math.sin(rad_a) / math.tan(rad_b))) if math.tan(rad_b) != 0 else 0
        giro_mm = abs(giro_deg * (circ / 360))

        # Resultados Visuales
        fig, ax = plt.subplots(figsize=(5, 5))
        fig.patch.set_facecolor('#0E1117')
        ax.set_facecolor('#0E1117')
        t = np.linspace(0, 2*np.pi, 100)
        ax.plot(np.cos(t), np.sin(t), color='#00FF7F', lw=3)
        ax.axhline(0, color='#333', lw=1, ls='--')
        ax.axvline(0, color='#333', lw=1, ls='--')

        # Lógica de flecha
        start_angle = 90 if "CI" in sent_v else 270
        sentido_f = (1 if "CHD" in sent_h else -1) if "CI" in sent_v else (-1 if "CHD" in sent_h else 1)
        ext = 55 * sentido_f
        arc_t = np.deg2rad(np.linspace(start_angle, start_angle + ext, 50))
        ax.plot(np.cos(arc_t)*1.15, np.sin(arc_t)*1.15, color='#00FF7F', lw=4)
        end_rad = np.deg2rad(start_angle + ext)
        ax.arrow(np.cos(end_rad)*1.15, np.sin(end_rad)*1.15, -0.03*sentido_f*np.sin(end_rad), 0.03*sentido_f*np.cos(end_rad), shape='full', head_width=0.09, color='#00FF7F')
        ax.set_xlim(-1.6, 1.6); ax.set_ylim(-1.6, 1.6); ax.axis('off')

        st.markdown(f"<div class='res-box'><h2 style='color:#00FF7F; margin:0;'>GIRO: {giro_mm:.2f} mm</h2></div>", unsafe_allow_html=True)
        st.pyplot(fig)
        
        ref = "SUPERIOR" if "CI" in sent_v else "INFERIOR"
        lado = "IZQUIERDA" if "CHD" in sent_h else "DERECHA"
        st.info(f"📍 MARCAR: Desde el eje {ref}, medir {giro_mm:.2f} mm hacia la {lado}.")

st.markdown("---")
# Botón para compartir enlace por WhatsApp
url_app = "https://bendingcontrolapp.streamlit.app" # Reemplaza con tu URL real si es distinta
st.markdown(f"""
    <a href="https://wa.me/?text=Hola!%20Te%20comparto%20la%20App%20de%20Piping%20Control%20para%20los%20cálculos%20de%20giro:%20{url_app}" target="_blank">
        <button style="width:100%; background-color:#25D366; color:white; font-weight:bold; border:none; border-radius:8px; height:45px; cursor:pointer;">
            📤 COMPARTIR APP POR WHATSAPP
        </button>
    </a>
""", unsafe_allow_html=True)

import streamlit as st
import math
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Piping Control v1.0", layout="centered")

# Estilo visual
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

# Entradas de datos
id_linea = st.text_input("ID DE JUNTA / LÍNEA")
diam_p = st.number_input("Ø TUBO (PULG)", min_value=0.0, step=0.5)

c1, c2 = st.columns(2)
with c1:
    ang_h = st.number_input("ANG. HORIZ (A°)")
    sent_h = st.selectbox("SENTIDO H", ["DERECHA (CHD)", "IZQUIERDA (CHI)"])
with c2:
    ang_v = st.number_input("ANG. VERT (B°)")
    sent_v = st.selectbox("SENTIDO V", ["SUPERIOR (CS)", "INFERIOR (CI)"])

if st.button("CALCULAR Y POSICIONAR"):
    if diam_p > 0:
        rad_a, rad_b = math.radians(ang_h), math.radians(ang_v)
        cos_c = max(-1, min(1, math.cos(rad_a) * math.cos(rad_b)))
        ang_c = math.degrees(math.acos(cos_c))
        
        circ = math.pi * diam_p * 25.4
        giro_deg = math.degrees(math.atan(math.sin(rad_a) / math.tan(rad_b))) if math.tan(rad_b) != 0 else 0
        giro_mm = abs(giro_deg * (circ / 360))

        st.markdown(f"""<div class='res-box'>
            <h2 style='color:#00FF7F; margin:0;'>GIRO: {giro_mm:.2f} mm</h2>
            <p style='color:#888; margin:0;'>Ángulo combinado: {ang_c:.2f}°</p>
        </div>""", unsafe_allow_html=True)

        # Gráfico corregido según diagrama manual
        fig, ax = plt.subplots(figsize=(5, 5))
        fig.patch.set_facecolor('#0E1117')
        ax.set_facecolor('#0E1117')
        
        t = np.linspace(0, 2*np.pi, 100)
        ax.plot(np.cos(t), np.sin(t), color='#00FF7F', lw=3)
        ax.axhline(0, color='#333', lw=1, ls='--')
        ax.axvline(0, color='#333', lw=1, ls='--')

        # LÓGICA DE FLECHA (Basada en 161104.jpg)
        # CI (Inferior) parte de arriba (90°); CS (Superior) parte de abajo (270°)
        start_angle = 90 if "CI" in sent_v else 270
        
        # CHD gira a la izquierda (antihorario +); CHI gira a la derecha (horario -)
        sentido_flecha = 1 if "CHD" in sent_h else -1
        arc_end = start_angle + (60 * sentido_flecha)

        # Dibujar arco y punta de flecha
        arc_t = np.deg2rad(np.linspace(start_angle, arc_end, 50))
        ax.plot(np.cos(arc_t)*1.15, np.sin(arc_t)*1.15, color='#00FF7F', lw=4)
        
        ax.arrow(np.cos(np.deg2rad(arc_end))*1.15, np.sin(np.deg2rad(arc_end))*1.15, 
                 -0.02*sentido_flecha*np.sin(np.deg2rad(arc_end)), 0.02*sentido_flecha*np.cos(np.deg2rad(arc_end)),
                 shape='full', head_width=0.08, color='#00FF7F')

        ax.set_xlim(-1.6, 1.6); ax.set_ylim(-1.6, 1.6); ax.axis('off')
        st.pyplot(fig)

        # Texto de instrucción
        ref = "SUPERIOR" if "CI" in sent_v else "INFERIOR"
        lado = "IZQUIERDA" if "CHD" in sent_h else "DERECHA"
        st.info(f"📍 MARCAR: Desde el eje {ref}, medir {giro_mm:.2f} mm hacia la {lado}.")

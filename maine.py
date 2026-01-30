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
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h2 style='color:#00FF7F; text-align:center;'>PIPING CONTROL V1.0</h2>", unsafe_allow_html=True)

# Entradas
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
        
        # Cálculo de giro
        circ = math.pi * diam_p * 25.4
        # Evitar división por cero si ang_v es 0
        giro_deg = math.degrees(math.atan(math.sin(rad_a) / math.tan(rad_b))) if math.tan(rad_b) != 0 else 0
        giro_mm = abs(giro_deg * (circ / 360))

        # --- LÓGICA DE GRÁFICO CORREGIDA ---
        fig, ax = plt.subplots(figsize=(5, 5))
        fig.patch.set_facecolor('#0E1117')
        ax.set_facecolor('#0E1117')
        
        # Círculo del tubo
        t = np.linspace(0, 2*np.pi, 100)
        ax.plot(np.cos(t), np.sin(t), color='#00FF7F', lw=3)
        ax.axhline(0, color='#333', lw=1, ls='--')
        ax.axvline(0, color='#333', lw=1, ls='--')

        # AJUSTE SEGÚN TU LIBRETA:
        # CI (Inferior) -> Empieza ARRIBA (90°)
        # CS (Superior) -> Empieza ABAJO (270°)
        if "CI" in sent_v:
            start_angle = 90
            # CHD gira a la izquierda (+), CHI a la derecha (-)
            sentido = 1 if "CHD" in sent_h else -1
        else: # Es CS
            start_angle = 270
            # En CS, CHD gira a la izquierda (+), CHI a la derecha (-)
            sentido = 1 if "CHD" in sent_h else -1

        # Dibujar arco de 60 grados para la flecha visual
        extent = 60 * sentido
        arc_t = np.deg2rad(np.linspace(start_angle, start_angle + extent, 50))
        ax.plot(np.cos(arc_t)*1.15, np.sin(arc_t)*1.15, color='#00FF7F', lw=4)
        
        # Punta de flecha
        end_rad = np.deg2rad(start_angle + extent)
        ax.arrow(np.cos(end_rad)*1.15, np.sin(end_rad)*1.15, 
                 -0.02*sentido*np.sin(end_rad), 0.02*sentido*np.cos(end_rad),
                 shape='full', head_width=0.08, color='#00FF7F')

        ax.set_xlim(-1.6, 1.6); ax.set_ylim(-1.6, 1.6); ax.axis('off')
        
        st.markdown(f"<h2 style='color:#00FF7F; text-align:center;'>GIRO: {giro_mm:.2f} mm</h2>", unsafe_allow_html=True)
        st.pyplot(fig)

        # Texto de instrucción dinámico
        ref = "SUPERIOR (Eje de doblado)" if "CI" in sent_v else "INFERIOR"
        lado = "IZQUIERDA" if "CHD" in sent_h else "DERECHA"
        st.info(f"📍 MARCAR: Desde el eje {ref}, medir {giro_mm:.2f} mm hacia la {lado}.")
            

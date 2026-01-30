import streamlit as st
import math
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Piping Control v1.0", layout="centered")

# Estilo visual oscuro y verde neón
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    .title { color: #00FF7F; text-align: center; font-size: 28px; font-weight: bold; margin-bottom: 20px; }
    div.stButton > button {
        background-color: #00FF7F; color: black; font-weight: bold;
        width: 100%; border-radius: 8px; height: 50px; border: none;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="title">PIPING CONTROL V1.0</p>', unsafe_allow_html=True)

# Entradas de datos
id_linea = st.text_input("ID DE JUNTA / LÍNEA", placeholder="Ej: L-100-ISO-01")
diam_pulg = st.number_input("Ø TUBO (PULG)", min_value=0.0, step=0.5)

col1, col2 = st.columns(2)
with col1:
    ang_h = st.number_input("ANG. HORIZ (A°)", min_value=0.0)
    sent_h = st.selectbox("SENTIDO H", ["DERECHA (CHD)", "IZQUIERDA (CHI)"])
with col2:
    ang_v = st.number_input("ANG. VERT (B°)", min_value=0.0)
    sent_v = st.selectbox("SENTIDO V", ["SUPERIOR (CS)", "INFERIOR (CI)"])

if st.button("CALCULAR Y POSICIONAR"):
    if diam_pulg > 0:
        rad_a, rad_b = math.radians(ang_h), math.radians(ang_v)
        
        # Ángulo Combinado
        cos_c = max(-1, min(1, math.cos(rad_a) * math.cos(rad_b)))
        ang_c = math.degrees(math.acos(cos_c))
        
        # Giro en mm
        circunferencia = math.pi * diam_pulg * 25.4
        giro_deg = math.degrees(math.atan(math.sin(rad_a) / math.tan(rad_b))) if math.tan(rad_b) != 0 else 0
        giro_mm = abs(giro_deg * (circunferencia / 360))

        # --- GENERAR GRÁFICO ---
        fig, ax = plt.subplots(figsize=(5, 5))
        fig.patch.set_facecolor('#0E1117')
        ax.set_facecolor('#0E1117')
        
        # Dibujar círculo (Tubo)
        theta = np.linspace(0, 2*np.pi, 100)
        ax.plot(np.cos(theta), np.sin(theta), color='#00FF7F', lw=3)
        
        # Ejes de referencia
        ax.axhline(0, color='#333', lw=1, ls='--')
        ax.axvline(0, color='#333', lw=1, ls='--')

        # Lógica de inicio (Superior para CI, Inferior para CS)
        # En matplotlib, 90° es arriba, 270° es abajo
        start_deg = 90 if sent_v == "INFERIOR (CI)" else 270
        
        # Sentido de giro (CHD hacia la izquierda (+), CHI hacia la derecha (-))
        direction = 1 if "CHD" in sent_h else -1
        # Usamos un arco de 45 grados para la flecha visual
        end_deg = start_deg + (45 * direction)
        
        # Dibujar flecha curva
        style = "Simple, tail_width=0.5, head_width=8, head_length=10"
        kw = dict(arrowstyle=style, color="#00FF7F")
        
        # Crear el arco de la flecha
        arrow_theta = np.deg2rad(np.linspace(start_deg, end_deg, 30))
        ax.plot(np.cos(arrow_theta)*1.1, np.sin(arrow_theta)*1.1, color="#00FF7F", lw=3)
        
        # Punta de la flecha
        ax.arrow(np.cos(np.deg2rad(end_deg))*1.1, np.sin(np.deg2rad(end_deg))*1.1, 
                 -0.01*direction*np.sin(np.deg2rad(end_deg)), 0.01*direction*np.cos(np.deg2rad(end_deg)),
                 shape='full', lw=0, length_includes_head=True, head_width=0.1, color='#00FF7F')

        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 1.5)
        ax.axis('off')
        
        # Mostrar el valor del giro en el centro
        st.markdown(f"<div style='background-color:#1E2631; padding:20px; border-radius:10px; border-left: 5px solid #00FF7F;'>"
                    f"<h2 style='color:#00FF7F; margin:0;'>GIRO: {giro_mm:.2f} mm</h2>"
                    f"<p style='margin:0; color:#888;'>Ángulo combinado: {ang_c:.2f}°</p></div>", unsafe_allow_html=True)
        
        st.pyplot(fig)
        
        # Instrucción dinámica
        eje_ref = "SUPERIOR" if "CI" in sent_v else "INFERIOR"
        lado_ref = "IZQUIERDA" if "CHD" in sent_h else "DERECHA"
        st.info(f"📍 MARCAR: Desde el eje {eje_ref}, medir {giro_mm:.2f} mm hacia la {lado_ref}.")
        


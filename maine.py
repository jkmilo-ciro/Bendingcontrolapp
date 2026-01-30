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
    .stTextInput input { background-color: #1E2631; color: white; border-radius: 5px; text-align: center; font-size: 18px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h2 style='color:#00FF7F; text-align:center;'>PIPING CONTROL V1.0</h2>", unsafe_allow_html=True)

# --- ENTRADAS (ID ELIMINADO) ---
diam_p_raw = st.text_input("Ø TUBO (PULG)", value="0") 

c1, c2 = st.columns(2)
with c1:
    ang_h_raw = st.text_input("ANG. HORIZ (A°)", value="0")
    sent_h = st.selectbox("SENTIDO H", ["DERECHA (CHD)", "IZQUIERDA (CHI)"])
with c2:
    ang_v_raw = st.text_input("ANG. VERT (B°)", value="0")
    sent_v = st.selectbox("SENTIDO V", ["SUPERIOR (CS)", "INFERIOR (CI)"])

def decimal_to_gms(decimal_deg):
    d = int(decimal_deg)
    m = int((decimal_deg - d) * 60)
    s = (decimal_deg - d - m/60) * 3600
    return f"{d}° {m}' {s:.2f}\""

if st.button("CALCULAR Y POSICIONAR"):
    try:
        diam_p = float(diam_p_raw.replace(',', '.'))
        A = float(ang_h_raw.replace(',', '.'))
        B = float(ang_v_raw.replace(',', '.'))

        if diam_p > 0:
            # NUEVA FÓRMULA: Cos-1(Cos A * Cos B)
            rad_A, rad_B = math.radians(A), math.radians(B)
            # Cálculo del ángulo resultante espacial (Giro en grados)
            res_rad = math.acos(math.cos(rad_A) * math.cos(rad_B))
            giro_deg = math.degrees(res_rad)
            
            # Conversión a GMS y mm
            gms_resultado = decimal_to_gms(giro_deg)
            circ = math.pi * diam_p * 25.4
            giro_mm = giro_deg * (circ / 360)

            # Resultados en pantalla
            st.markdown(f"""
            <div class='res-box'>
                <p style='color:#00FF7F; margin:0;'>DISTANCIA DE GIRO:</p>
                <h2 style='color:#00FF7F; margin:0;'>{giro_mm:.2f} mm</h2>
                <hr style='border-color:#333;'>
                <p style='margin:0;'>ÁNGULO RESULTANTE Espacial:</p>
                <h4 style='margin:0;'>Decimal: {giro_deg:.4f}°</h4>
                <h4 style='margin:0; color:#00FF7F;'>GMS: {gms_resultado}</h4>
            </div>
            """, unsafe_allow_html=True)

            # Gráfico de Trazado
            fig, ax = plt.subplots(figsize=(5, 5))
            fig.patch.set_facecolor('#0E1117')
            ax.set_facecolor('#0E1117')
            t = np.linspace(0, 2*np.pi, 100)
            ax.plot(np.cos(t), np.sin(t), color='#00FF7F', lw=3)
            ax.axhline(0, color='#333', lw=1, ls='--')
            ax.axvline(0, color='#333', lw=1, ls='--')

            # Posicionamiento de flecha según tu manual
            start_angle = 90 if "CI" in sent_v else 270
            sentido_f = (1 if "CHD" in sent_h else -1) if "CI" in sent_v else (-1 if "CHD" in sent_h else 1)
            ext = 55 * sentido_f
            arc_t = np.deg2rad(np.linspace(start_angle, start_angle + ext, 50))
            ax.plot(np.cos(arc_t)*1.15, np.sin(arc_t)*1.15, color='#00FF7F', lw=4)
            end_rad = np.deg2rad(start_angle + ext)
            ax.arrow(np.cos(end_rad)*1.15, np.sin(end_rad)*1.15, -0.03*sentido_f*np.sin(end_rad), 0.03*sentido_f*np.cos(end_rad), shape='full', head_width=0.09, color='#00FF7F')
            ax.set_xlim(-1.6, 1.6); ax.set_ylim(-1.6, 1.6); ax.axis('off')
            
            st.pyplot(fig)
            
            ref = "SUPERIOR" if "CI" in sent_v else "INFERIOR"
            lado = "IZQUIERDA" if "CHD" in sent_h else "DERECHA"
            st.info(f"📍 MARCAR: Desde el eje {ref}, medir {giro_mm:.2f} mm hacia la {lado}.")
        else:
            st.warning("El diámetro debe ser mayor a 0.")
    except ValueError:
        st.error("Por favor, introduce solo números.")
            

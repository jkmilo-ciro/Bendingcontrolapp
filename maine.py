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

# --- ENTRADAS (ID Eliminado) ---
diam_p_raw = st.text_input("Ø TUBO (PULG)", value="0") 

c1, c2 = st.columns(2)
with c1:
    ang_h_raw = st.text_input("ANG. HORIZ (A°)", value="0")
    sent_h = st.selectbox("SENTIDO H", ["DERECHA (CHD)", "IZQUIERDA (CHI)"])
with c2:
    ang_v_raw = st.text_input("ANG. VERT (B°)", value="0")
    sent_v = st.selectbox("SENTIDO V", ["SUPERIOR (CS)", "INFERIOR (CI)"])

# Función para convertir grados decimales a GMS
def decimal_to_gms(decimal_deg):
    d = int(decimal_deg)
    m = int((decimal_deg - d) * 60)
    s = (decimal_deg - d - m/60) * 3600
    return f"{d}° {m}' {s:.2f}\""

if st.button("CALCULAR Y POSICIONAR"):
    try:
        diam_p = float(diam_p_raw.replace(',', '.'))
        ang_h = float(ang_h_raw.replace(',', '.'))
        ang_v = float(ang_v_raw.replace(',', '.'))

        if diam_p > 0:
            # Sumatoria de los ángulos solicitada
            suma_angulos = ang_h + ang_v
            gms_suma = decimal_to_gms(suma_angulos)

            # Cálculo de giro original para el gráfico y distancia
            rad_a, rad_b = math.radians(ang_h), math.radians(ang_v)
            circ = math.pi * diam_p * 25.4
            giro_deg = math.degrees(math.atan(math.sin(rad_a) / math.tan(rad_b))) if math.tan(rad_b) != 0 else 0
            giro_mm = abs(giro_deg * (circ / 360))

            # Resultados
            st.markdown(f"""
            <div class='res-box'>
                <p style='color:#00FF7F; margin:0;'>DISTANCIA DE GIRO:</p>
                <h2 style='color:#00FF7F; margin:0;'>{giro_mm:.2f} mm</h2>
                <hr style='border-color:#333;'>
                <p style='margin:0;'>SUMATORIA DE ÁNGULOS (A° + B°):</p>
                <h4 style='margin:0;'>Decimal: {suma_angulos:.4f}°</h4>
                <h4 style='margin:0; color:#00FF7F;'>GMS: {gms_suma}</h4>
            </div>
            """, unsafe_allow_html=True)

            # Gráfico
            fig, ax = plt.subplots(figsize=(5, 5))
            fig.patch.set_facecolor('#0E1117')
            ax.set_facecolor('#0E1117')
            t = np.linspace(0, 2*np.pi, 100)
            ax.plot(np.cos(t), np.sin(t), color='#00FF7F', lw=3)
            ax.axhline(0, color='#333', lw=1, ls='--')
            ax.axvline(0, color='#333', lw=1, ls='--')

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
        st.error("Introduce solo números válidos.")

st.markdown("---")
url_app = "https://bendingcontrolapp.streamlit.app"
st.markdown(f"""<a href="https://wa.me/?text=App%20Piping%20Control:%20{url_app}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; font-weight:bold; border:none; border-radius:8px; height:45px;">📤 COMPARTIR APP POR WHATSAPP</button></a>""", unsafe_allow_html=True)
            

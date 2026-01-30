import streamlit as st
import math
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Piping Control v1.0", layout="centered")

# Estilo para campos limpios de solo escritura
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    div.stButton > button { background-color: #00FF7F; color: black; font-weight: bold; width: 100%; border-radius: 8px; }
    .stTextInput input { background-color: #1E2631; color: white; text-align: center; font-size: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h2 style='color:#00FF7F; text-align:center;'>PIPING CONTROL V1.0</h2>", unsafe_allow_html=True)

# Entradas en cero y sin botones +/-
id_linea = st.text_input("ID DE JUNTA", value="")
diam_p_raw = st.text_input("Ø TUBO (PULG)", value="0")
ang_h_raw = st.text_input("ANG. HORIZ (A°)", value="0")
sent_h = st.selectbox("SENTIDO H", ["DERECHA (CHD)", "IZQUIERDA (CHI)"])
ang_v_raw = st.text_input("ANG. VERT (B°)", value="0")
sent_v = st.selectbox("SENTIDO V", ["SUPERIOR (CS)", "INFERIOR (CI)"])

if st.button("CALCULAR"):
    try:
        diam_p = float(diam_p_raw.replace(',', '.'))
        if diam_p > 0:
            # (Aquí va el resto de tu lógica de cálculo y gráfico que ya funciona)
            st.success("Cálculo realizado con éxito")
    except:
        st.error("Ingresa números válidos")
        

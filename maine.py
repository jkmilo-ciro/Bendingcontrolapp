import streamlit as st
import math

# 1. CONFIGURACIÓN VISUAL (ESTILO PIPING CONTROL)
st.set_page_config(page_title="Piping Control v1.0", layout="centered")

# Aplicamos CSS para imitar la interfaz de la foto (Modo Oscuro y Verde Neón)
st.markdown("""
    <style>
    .stApp {
        background-color: #0E1117;
        color: #FFFFFF;
    }
    /* Estilo para los botones */
    div.stButton > button {
        background-color: #00FF7F;
        color: #000000;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        height: 3em;
        width: 100%;
    }
    div.stButton > button:hover {
        background-color: #00CC66;
        color: white;
    }
    /* Estilo para el título */
    .main-title {
        color: #00FF7F;
        text-align: center;
        font-size: 35px;
        font-weight: bold;
        margin-bottom: 0px;
    }
    .sub-title {
        color: #888888;
        text-align: center;
        font-size: 14px;
        margin-bottom: 30px;
    }
    /* Bordes verdes para los inputs */
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        border-color: #00FF7F;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. FUNCIONES DE CÁLCULO
def decimal_a_gms(decimal_grados):
    abs_grados = abs(decimal_grados)
    grados = int(abs_grados)
    minutos_float = (abs_grados - grados) * 60
    minutos = int(minutos_float)
    segundos = (minutos_float - minutos) * 60
    return grados, minutos, segundos

# 3. INTERFAZ DE USUARIO (UI)
st.markdown('<p class="main-title">PIPING CONTROL <span style="font-size:15
            

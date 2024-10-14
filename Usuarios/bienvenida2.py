import streamlit as st
import pandas as pd
import numpy as np


import streamlit as st


with open('style2.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


st.markdown('<style>div.block-container{margin-top:-6rem;}</style>',unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    st.write(' ')

with col2:
    st.image( "reportes/ESTRUCTURAS SOLANA - 04 (1).png", width=500)

with col3:
    st.write(' ')



st.markdown(f'<p style="display: block; text-align:center;margin-top:-1rem; font-size: 65px;color: #000;font-weight: bold;;">Hola {st.session_state["name"]} Bienvenido al</p>', unsafe_allow_html=True)
st.markdown('<p style="display: block; text-align:center; margin-top:-2rem; font-size: 70px;color: #000;font-weight: bold;">Sistema de Análisis de Soldadura</p>', unsafe_allow_html=True)


st.markdown('<p style="display: block; text-align:center; font-size: 35px;color: #000;">(Pagina para la realización de pruebas)</p>', unsafe_allow_html=True)

st.markdown('<p style="display: block; text-align:center; font-size: 25px;color: #000;font-weight: bold;">Derechos Reservados © 2024 SMARTEST</p>', unsafe_allow_html=True)


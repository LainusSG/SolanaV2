import streamlit as st
import pandas as pd
import numpy as np


import streamlit as st


with open('style2.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)


st.write('Sistema de Soldadura Versión. 1.1')
st.write('Copyright © 2023-2024, SMARTEST - El equipo de desarrollo del Sistema de Soldadura.')
st.write('')


st.markdown('<p style="display: block;  font-size: 25px;  font-weight:bold; color: #000;">LICENCIA</p>', unsafe_allow_html=True)
st.write('''El uso de productos de software o hardware de SMARTEST se basa en la licencia de software y ciertos términos y condiciones para el producto al momento de su compra. La aceptación de esos términos es obligatoria para instalar o usar el producto. Consulta la licencia con tu proveedor o comunícate con nuestra área comercial ventas@smartest.mx.''')
st.write('')


st.markdown('<p style="display: block;  font-size: 25px;  font-weight:bold; color: #000;">MARCAS</p>', unsafe_allow_html=True)
st.write('''El logotipo del Sistema de Soldadura y de SMARTEST son marcas registradas o marcas comerciales de SMARTEST en México.''')
st.write('')



st.markdown('<p style="display: block;  font-size: 25px;  font-weight:bold; color: #000;">POLÍTICAS Y AVISOS</p>', unsafe_allow_html=True)
st.write('''Los avisos, términos y condiciones pertenecientes a software, hardware o datos de terceros se encuentran en https://www.smartest.mx/.''')
st.write('')


st.markdown('<p style="display: block;  font-size: 25px;  font-weight:bold; color: #000;">DERECHOS Y PERMISOS</p>', unsafe_allow_html=True)
st.write('''La instalación y las adecuaciones del Sistema de Soldadura están limitadas a acciones de los técnicos de SMARTEST.''')
st.write('')


st.markdown('<p style="display: block;  font-size: 25px;  font-weight:bold; color: #000;">INTELIGENCIA ARTIFICIAL.</p>', unsafe_allow_html=True)
st.write('''El producto Sistema de Soldadura tiene inteligencia artificial ("IA"). Este es desarrollado por SMARTEST. La funcionalidad de la IA esta especificada en las características del producto o servicio. Las funciones de IA utilizan la información que el sistema recopila para mejorar los servicios que te proporcionamos o para mejorar la asistencia que te ofrecemos en relación con las operaciones del sistema.''')

st.write('')
st.markdown('<p style="display: block; text-align:center; font-size: 22px;  font-weight:bold;  text-align:center;color: #000;">El Sistema de Soldadura es creado por SMARTEST.</p>', unsafe_allow_html=True)

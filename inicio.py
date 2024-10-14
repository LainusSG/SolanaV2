import streamlit as st
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities.hasher import Hasher
import base64


st.set_page_config(page_title="SolanaIA", page_icon="reportes/lluvia.ico", layout="wide")


custom_css = """
<style>
 [alt=Logo] {
      height: 5rem;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

st.logo("reportes/LOGOS JUNTOS.png")
st.markdown(
    r"""
    <style>
    .stDeployButton {
            visibility: hidden;
        }
        .stMenuButton {
            visibility: hidden;
        }
    </style>
    """, unsafe_allow_html=True
)

# Pass the list of passwords directly to the 
# Hasher constructor and generate the hashes
# passwords_to_hash = ['fashion@123', 'increff@fashion']
# hashed_passwords = Hasher(passwords_to_hash).generate()

# print(hashed_passwords)



with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

    
#Hasher.hash_passwords(config['credentials'])
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)
name, authentication_status, username = authenticator.login()




bienvenida = st.Page(
    "bienvenida.py", title="Inicio", icon=":material/home:", default=True
)
IAImagenes = st.Page(
    "IAImagenes/IA_para_Imagenes.py", title="IA para Imagenes", icon=":material/image:"
)
Dashboard = st.Page(
    "reportes/dashboard2.py", title="Dashboard", icon=":material/dashboard:"
)

IAVideo = st.Page(
    "IAVideo/IA_para_videos.py", title="IA para procesar videos", icon=":material/camera:"
)
About = st.Page(
    "About.py", title="Acerca de", icon=":material/search:"
)



bienvenida2 = st.Page(
    "Usuarios/bienvenida2.py", title="BIenvenida", icon=":material/home:"
)

Pruebas = st.Page(
    "Usuarios/Usuarios.py", title="Pruebas de Imagen", icon=":material/image:"
)
Pruebas2 = st.Page(
    "Usuarios/videos.py", title="Pruebas de Video", icon=":material/camera:"
)


custom_css = """
<style>
div.stButton button {
    background-color: white;
    color:#000;
    width: 200px;
}

div.stButton button:hover {
    background-color: white ;
    color:#FF5000;
    width: 200px;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

if st.session_state["authentication_status"]:
    authenticator.logout('Salir', 'sidebar', key='unique_key')

    if username == 'user':
        pg = st.navigation(
        {
            "Inicio":[bienvenida2],
            "Pruebas de Imagen":[Pruebas],
            "Pruebas de Video":[Pruebas2],
        }
        )
        pg.run()
    elif username == 'casho':
        pg = st.navigation(
        {
            "Inicio":[bienvenida],
            "IAImagenes": [IAImagenes],
            "IAVideo": [IAVideo],
            "Reportes": [Dashboard],
            "About":[About]
        }
        )
        pg.run()
    elif username == 'solana':
        pg = st.navigation(
        {
            "Inicio":[bienvenida],
            "IAImagenes": [IAImagenes],
            "IAVideo": [IAVideo],
            "Reportes": [Dashboard],
            "About":[About]
        }
        )
        pg.run()
    elif username == 'david':
        pg = st.navigation(
        {
            "Inicio":[bienvenida],
            "IAImagenes": [IAImagenes],
            "IAVideo": [IAVideo],
            "Reportes": [Dashboard],
            "About":[About]
        }
        )
        pg.run()
    elif username == 'julio':
        pg = st.navigation(
        {
            "Inicio":[bienvenida],
            "IAImagenes": [IAImagenes],
            "IAVideo": [IAVideo],
            "Reportes": [Dashboard],
            "About":[About]
        }
        )
        pg.run()
    elif username == 'paola':
        pg = st.navigation(
        {
            "Inicio":[bienvenida],
            "IAImagenes": [IAImagenes],
            "IAVideo": [IAVideo],
            "Reportes": [Dashboard],
            "About":[About]
        }
        )
        pg.run()
    elif username == 'victor':
        pg = st.navigation(
        {
            "Inicio":[bienvenida],
            "IAImagenes": [IAImagenes],
            "IAVideo": [IAVideo],
            "Reportes": [Dashboard],
            "About":[About]
        }
        )
        pg.run()
    elif username == 'jonathan':
        pg = st.navigation(
        {
            "Inicio":[bienvenida],
            "IAImagenes": [IAImagenes],
            "IAVideo": [IAVideo],
            "Reportes": [Dashboard],
            "About":[About]
        }
        )
        pg.run()
    elif username == 'javier':
        pg = st.navigation(
        {
            "Inicio":[bienvenida],
            "IAImagenes": [IAImagenes],
            "IAVideo": [IAVideo],
            "Reportes": [Dashboard],
            "About":[About]
        }
        )
        pg.run()


   
elif st.session_state["authentication_status"] is False:
    st.error('Username/password es incorrecto')
elif st.session_state["authentication_status"] is None:
    st.warning('Por favor introduce tu username/password')




##################################################################################################################################################################
####################################################### bloque de estilos ########################################################################################
##################################################################################################################################################################

with open('style.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)




##################################################################################################################################################################
####################################################### bloque de estilos ########################################################################################
##################################################################################################################################################################

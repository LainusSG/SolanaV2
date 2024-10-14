import streamlit as st
from streamlit_webrtc import webrtc_streamer, RTCConfiguration
import av
from yolo_prediccion import YOLO_Pred
import datetime
import threading
from matplotlib import pyplot as plt

import cv2
from sqlalchemy import text


st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)
st.markdown(f'<p style="display: block; text-align:right; font-size: 24px;  margin-top:-2rem;  color: #000;font-weight: bold;"> Usuario: {st.session_state["name"]}</p>', unsafe_allow_html=True)
col1, col2,col3 = st.columns((3))
with col1:
    st.write("")
with col2:
    st.image('reportes/TM2.gif',caption=None, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")
with col3:
    st.write("")



yolo = YOLO_Pred('./models/best.onnx',
                  './models/data.yml')


lock = threading.Lock()
img_container = {"img": None, "data": ""}




def video_frame_callback(frame):
    
    img = frame.to_ndarray(format="bgr24")
    
    with lock:
        #flipped = img[::-1,:,:]
        [pred_img, falla_detectada] = yolo.predicciones(img)
        img_container["img"] = pred_img
        img_container["data"] = falla_detectada

        name = "imagenes/pred_img_obj.png"
        cv2.imwrite(name, img) 
    return av.VideoFrame.from_ndarray(pred_img, format="bgr24")



ctx = webrtc_streamer(key="example", video_frame_callback=video_frame_callback, rtc_configuration= {"iceServers": [{"urls":["stun:stun1.l.google.com:19302"]}]}, media_stream_constraints={"video":True, "audio": False})

fig_place = st.empty()
fig, ax = plt.subplots(1, 1)




def realizar_limpieza(valorfalla):
    valor2 =[]
    valor2_f=[]     
    total_fallas = []
    if len(valorfalla) > 0:
        for k in valorfalla:

            valor1 = k.split(':')
            try:
                valor3 = float(valor1[0])
                valor2.append(valor3)
                
        
            except:
                igual=False
                for kk in valor2_f:
                    if kk == valor1[0]:
                        igual=True
                if not igual:
                    valor2_f.append(valor1[0])
                
        nnn=0
        x=0
        for nn in valor2:
            nnn+=nn
            x+=1
        if x > 0:    
            calificacion = nnn/x
        else:
            calificacion = 0
        if len(valor2_f) > 0:
            for kkk in valor2_f:
                total_fallas.append([calificacion, kkk, 1])
        else:
            total_fallas.append([calificacion, 'No hay fallas', 0])
    else:
        total_fallas.append([0, 'No hay fallas', 0])
 
    return(total_fallas)







conn = st.connection("postgresql", type="sql")



def create_new_form():
    with st.form("myform", clear_on_submit=True):
        Fecha = st.date_input("Fecha", datetime.datetime.now(), format="DD/MM/YYYY")

        Obra = st.text_input("Obra", "")

        Cliente = st.text_input("Cliente", "")

        Tipo_Pieza = st.text_input("Tipo de Pieza", "")

        Pieza = st.text_input("Pieza", "")

        Categoria = st.text_input("Categoría", "")

        Tipo_soldadura = st.text_input("Tipo de Soldadura", "")
        submit = st.form_submit_button(label="Submit")
        if submit:
            total_fallas=[]
            valorfalla = []
            tamano = 0
            while ctx.state.playing:
                with lock:
                    img = img_container["img"]
                    for kk in img_container["data"]:
                        valor = kk.split(":")
                        if not valor[0] in total_fallas:
                            valorfalla.append(valor[0])
                            total_fallas= realizar_limpieza(valorfalla)
                            if len(total_fallas)>tamano:
                                tamano = len(total_fallas)
                                with conn.session as s:
                                    if len(total_fallas)<= 0:
                                        total_fallas. append([0,'No hay fallas',0])
                                    for [calificacion1, tipo_fallas1, fallas1] in total_fallas:
                                        import pyrebase

                                        ## configuraciones de la base de datos
                                        
                                        firebaseConfig = {
                                            "apiKey": "AIzaSyB3XiVjsPQMnlr4atYjU2xnL-NX9fk_2Mg",
                                            "authDomain": "solanaia.firebaseapp.com",
                                            "databaseURL": "https://solanaia-default-rtdb.firebaseio.com",
                                            "projectId": "solanaia",
                                            "storageBucket": "solanaia.appspot.com",
                                            "messagingSenderId": "781444992537",
                                            "appId": "1:781444992537:web:5986510634d48fc259e488",
                                            "measurementId": "G-Z1Q8XZ19SR"
                                            }


                                        firebase = pyrebase.initialize_app(firebaseConfig )
                                        ## declaracion de que funicion queremos usar, en este caso "storage" para almacenar ahi nuestras fotos dentro del bucket
                                        storage = firebase.storage()

                                        imgw= "imagenes/pred_img_obj.png"

                                        
                                        

                                        today = datetime.datetime.now()
                                        today3 = today.strftime("%H:%M:%S")
                                        today2 = today.strftime("%d-%m-%Y")

                                        ## el estorage child es el nombre con el que guardaremos el archivo en la base de datos
                                        ## no uncluiur "/" en el nombre, ya que el programa lo reconocé como rutas y crea sub carpetas


                                        ## la funcion put sube la variable o el archivo que este contenido entre parentesis en este caso la foto
                                        ## que siempre cambiara en cada analisís
                                        storage.child('IMAGENES/'+str(today2)+' - '+str(today3)).put(imgw)
                                        auth = firebase.auth()
                                        user = auth.sign_in_with_email_and_password(email='calidad@solana.mx', password='Calidad.2024*')
                                        url = storage.child('IMAGENES/'+str(today2)+' - '+str(today3)).get_url(user)  
                                        url2 = url.split("':")
                                        url3= url2[0]
                                        s.execute(text('INSERT INTO soldadura (fecha, calificacion, obra, cliente, tipo_pieza, pieza, categoria, tipo_soldadura, tipo_fallas, fallas, link) VALUES (:fecha, :calificacion, :obra, :cliente, :tipo_pieza, :pieza, :categoria, :tipo_soldadura, :tipo_fallas, :fallas, :link );'),
                                            params=dict(fecha=Fecha, calificacion=calificacion1, obra=Obra, cliente=Cliente,  tipo_pieza=Tipo_Pieza, pieza=Pieza, categoria=Categoria, tipo_soldadura=Tipo_soldadura, tipo_fallas=tipo_fallas1, fallas=fallas1, link=url3 )
                                                                    )
                                        s.commit()
                            


                if img is None:
                    continue
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                ax.cla()
                ax.hist(gray.ravel(), 256, [0, 256])
                fig_place.pyplot(fig)
    


                   

    


                

create_new_form()
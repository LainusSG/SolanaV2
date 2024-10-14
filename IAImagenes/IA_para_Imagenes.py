import streamlit as st
from yolo_prediccion import YOLO_Pred
from PIL import Image
import numpy as np
import datetime
from sqlalchemy import text

conn = st.connection("postgresql", type="sql")

#st.set_page_config(page_title="Detección calificación de soldadura de Imagen",
#                   layout="wide",
#                   page_icon="./imagenes/busquedaIA.jpg")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)
st.markdown(f'<p style="display: block; text-align:right; font-size: 24px;  margin-top:-2rem;  color: #000;font-weight: bold;"> Usuario: {st.session_state["name"]}</p>', unsafe_allow_html=True)
col1, col2,col3 = st.columns((3))
with col1:
    st.write("")
with col2:
    st.image('reportes/TM2.gif',caption=None, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")
with col3:
    st.write("")

# ##################################  OBTENER VALORES DE LA IA #######################################


st.title('Por favor sube una imagen para hacer detección/calificación')

with st.spinner('Por favor, espera que tu modelo esta cargando'):   
    yolo = YOLO_Pred(onnx_model='./models/best.onnx',
                    data_yaml='./models/data.yml')
    







#Subir imagen
def subir_imagen():
    archivo_imagen = st.file_uploader(label=":orange[Cargue la soldadura a analizar]")
    if archivo_imagen is not None:
        size_mb = archivo_imagen.size/(1024**2)
        detalles_archivo = {
            "filename": archivo_imagen.name,
            "filetype": archivo_imagen.type,
            "filesize": "{:,.2f} MB".format(size_mb)}
        #st.json(detalles_archivo)

        # Validando Archivo

        if detalles_archivo['filetype'] in ('image/png'):
            st.success('Tipos de Archivos de IMAGEN Válidos (png)')
            return {"archivo": archivo_imagen, "detalles": detalles_archivo}

        else:
            st.error('Tipo de archivo de imagen inválido')
            st.error('Subir solamente PNG')
            return None

def capturar_imagen():
    object = subir_imagen()
    if object:
        imagen_obj = Image.open(object['archivo'])

        col1, col2 = st.columns(2)

        with col1:
            st.info('Vista previa de la imagen')
            st.image(imagen_obj)
        with col2:
            st.subheader('Checa abajo los detalles del archivo')
            st.json(object['detalles'])
        return(imagen_obj)
    else:
        return None

def analisis_IA(imagen_obj):
    valorfalla=[]
    prediccion=False
    with st.spinner("""
            Detectando fallas de soldadura en la imagen. Por favor, paciencia
                    """):
        st.write('Se Generó Un Análisis')
        arreglo_imagen = np.array(imagen_obj)
        [pred_img, valorfalla] = yolo.predicciones(arreglo_imagen)
        pred_img_obj = Image.fromarray(pred_img)
        prediccion = True

    if prediccion:
        st.subheader(" Imagen analizada")
        st.caption("Detección de objetos con la IA")
        st.image(pred_img_obj)
        pred_img_obj.save("imagenes/pred_img_obj.png")
       
    return valorfalla





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


################################################## Conexion a la base de dato ################################################################################


def create_new_form(imagen):

    conn = st.connection("postgresql", type="sql")
    #df = pd.read_csv("reportes/Graficas3.csv", encoding = "ISO-8859-1")
    df= conn.query('select * from soldadura;', ttl="1s")

    col1, col2,col3 = st.columns((3), vertical_alignment="center")
    with col1:
        empresa_nueva = st.checkbox("Nueva Obra")
    with col2:
        cliente_nuevo = st.checkbox("Nuevo Cliente ")
    with col3:
        ClienteEmpresa_nuevo = st.checkbox("Cliente y Obra Nuevos")
    

    if not empresa_nueva and not cliente_nuevo and not ClienteEmpresa_nuevo:
        with st.form("1", clear_on_submit=True):
            Fecha = st.date_input("Fecha", datetime.datetime.now(), format="DD/MM/YYYY")
            
            Obra = st.selectbox("Obra", (df["obra"]))
            

            Cliente = st.selectbox("Cliente",  (df["cliente"]))
            

            Tipo_Pieza = st.text_input("Tipo de Pieza", "")

            Pieza = st.text_input("Pieza", "")

            Categoria = st.text_input("Categoría", "")

            Tipo_soldadura = st.text_input("Tipo de Soldadura", "")


            submit = st.form_submit_button(label="Submit")
            if submit:
                if imagen is not None:
                    valorfalla= analisis_IA(imagen)
                    TotalFallas= realizar_limpieza(valorfalla)
                    with conn.session as s:
                        for [calificacion1, tipo_fallas1, fallas1] in TotalFallas:
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
                            s.execute(text('INSERT INTO soldadura (fecha, calificacion, obra, cliente, tipo_pieza, pieza, categoria, tipo_soldadura, tipo_fallas, fallas, link) VALUES (:fecha, :calificacion, :obra, :cliente, :tipo_pieza, :pieza, :categoria, :tipo_soldadura, :tipo_fallas, :fallas, :link  );'),
                            params=dict(fecha=Fecha, calificacion =calificacion1, obra=Obra, cliente=Cliente,  tipo_pieza = Tipo_Pieza, pieza=Pieza, categoria=Categoria, tipo_soldadura=Tipo_soldadura, tipo_fallas=tipo_fallas1, fallas= fallas1, link=url3 )
                                        )
                        
                            s.commit()
            
    if empresa_nueva==True:
        with st.form("2", clear_on_submit=True):
            Fecha = st.date_input("Fecha", datetime.datetime.now(), format="DD/MM/YYYY")
            
            Obra = st.text_input("Obra", "")

            Cliente = st.selectbox("Cliente", (df["cliente"]))

            Tipo_Pieza = st.text_input("Tipo de Pieza", "")

            Pieza = st.text_input("Pieza", "")

            Categoria = st.text_input("Categoría", "")

            Tipo_soldadura = st.text_input("Tipo de Soldadura", "")


            submit = st.form_submit_button(label="Submit")
            if submit:
                if imagen is not None:
                    valorfalla= analisis_IA(imagen)
                    TotalFallas= realizar_limpieza(valorfalla)
                    with conn.session as s:
                        for [calificacion1, tipo_fallas1, fallas1] in TotalFallas:
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
                            s.execute(text('INSERT INTO soldadura (fecha, calificacion, obra, cliente, tipo_pieza, pieza, categoria, tipo_soldadura, tipo_fallas, fallas, link) VALUES (:fecha, :calificacion, :obra, :cliente, :tipo_pieza, :pieza, :categoria, :tipo_soldadura, :tipo_fallas, :fallas, :link  );'),
                            params=dict(fecha=Fecha, calificacion =calificacion1, obra=Obra, cliente=Cliente,  tipo_pieza = Tipo_Pieza, pieza=Pieza, categoria=Categoria, tipo_soldadura=Tipo_soldadura, tipo_fallas=tipo_fallas1, fallas= fallas1, link=url3 )
                                        )
                        
                            s.commit()
    
                        
    if cliente_nuevo==True:
        with st.form("3", clear_on_submit=True):
            Fecha = st.date_input("Fecha", datetime.datetime.now(), format="DD/MM/YYYY")
            
            Obra = st.selectbox("Obra", (df["obra"]))

            Cliente = st.text_input("Cliente", "")

            Tipo_Pieza = st.text_input("Tipo de Pieza", "")

            Pieza = st.text_input("Pieza", "")

            Categoria = st.text_input("Categoría", "")

            Tipo_soldadura = st.text_input("Tipo de Soldadura", "")


            submit = st.form_submit_button(label="Submit")
            if submit:
                if imagen is not None:
                    valorfalla= analisis_IA(imagen)
                    TotalFallas= realizar_limpieza(valorfalla)
                    with conn.session as s:
                        for [calificacion1, tipo_fallas1, fallas1] in TotalFallas:
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
                            s.execute(text('INSERT INTO soldadura (fecha, calificacion, obra, cliente, tipo_pieza, pieza, categoria, tipo_soldadura, tipo_fallas, fallas, link) VALUES (:fecha, :calificacion, :obra, :cliente, :tipo_pieza, :pieza, :categoria, :tipo_soldadura, :tipo_fallas, :fallas, :link  );'),
                            params=dict(fecha=Fecha, calificacion =calificacion1, obra=Obra, cliente=Cliente,  tipo_pieza = Tipo_Pieza, pieza=Pieza, categoria=Categoria, tipo_soldadura=Tipo_soldadura, tipo_fallas=tipo_fallas1, fallas= fallas1, link=url3 )
                                        )
                        
                            s.commit()
                
    if ClienteEmpresa_nuevo==True:
        with st.form("4", clear_on_submit=True):
            Fecha = st.date_input("Fecha", datetime.datetime.now(), format="DD/MM/YYYY")
            
            Obra = st.text_input("Obra", "")

            Cliente = st.text_input("Cliente", "")

            Tipo_Pieza = st.text_input("Tipo de Pieza", "")

            Pieza = st.text_input("Pieza", "")

            Categoria = st.text_input("Categoría", "")

            Tipo_soldadura = st.text_input("Tipo de Soldadura", "")


            submit = st.form_submit_button(label="Submit")
            if submit:
                if imagen is not None:
                    valorfalla= analisis_IA(imagen)
                    TotalFallas= realizar_limpieza(valorfalla)
                    with conn.session as s:
                        for [calificacion1, tipo_fallas1, fallas1] in TotalFallas:
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
                            s.execute(text('INSERT INTO soldadura (fecha, calificacion, obra, cliente, tipo_pieza, pieza, categoria, tipo_soldadura, tipo_fallas, fallas, link) VALUES (:fecha, :calificacion, :obra, :cliente, :tipo_pieza, :pieza, :categoria, :tipo_soldadura, :tipo_fallas, :fallas, :link  );'),
                            params=dict(fecha=Fecha, calificacion =calificacion1, obra=Obra, cliente=Cliente,  tipo_pieza = Tipo_Pieza, pieza=Pieza, categoria=Categoria, tipo_soldadura=Tipo_soldadura, tipo_fallas=tipo_fallas1, fallas= fallas1, link=url3 )
                                        )
                        
                            s.commit()

imagen=capturar_imagen()
create_new_form(imagen)






################################################## Conexion a la base de dato ################################################################################
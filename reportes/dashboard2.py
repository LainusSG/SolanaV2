import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
from fpdf import FPDF
import base64
import datetime

import plotly.figure_factory as ff
import time 



warnings.filterwarnings('ignore')

today = datetime.datetime.now()
today2 = today.strftime("%d/%m/%Y")

st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)
st.markdown(f'<p style="display: block; text-align:right; font-size: 24px;  margin-top:-2rem;  color: #000;font-weight: bold;"> Usuario: {st.session_state["name"]}</p>', unsafe_allow_html=True)
col1, col2,col3 = st.columns((3))
with col1:
    st.write("")
with col2:
    st.image('reportes/TM2.gif',caption=None, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")
with col3:
    st.write("")

# fl = st.file_uploader(":file_folder: Subir Archivo!",type=(["csv","txt","xlsx","xls"]))
# if fl is not None:
#     filename = fl.name
#     st.write(filename)
#     df = pd.read_csv(filename, encoding = "ISO-8859-1")
# else:
    #os.chdir(r"reportes")



########################################################################################   
########################################################################################   
########################################################################################   
conn = st.connection("postgresql", type="sql")
#df = pd.read_csv("reportes/Graficas3.csv", encoding = "ISO-8859-1")
df= conn.query('select * from soldadura;', ttl="1s")


########################################################################################   
    
col1, col2 = st.columns((2))
def convert(dt):
    try:
        return datetime.strptime(dt, '%m/%d/%Y').strftime('%d/%m/%Y')
    except ValueError:
        return dt
df["fecha"] = pd.to_datetime(df["fecha"])

# Getting the min and max date 
startDate = pd.to_datetime(df["fecha"]).min()
endDate = pd.to_datetime(df["fecha"]).max()

with col1:
    date1 = pd.to_datetime(st.date_input("Fecha de Inicio", startDate))
    today3 = date1.strftime("%d/%m/%Y")

with col2:
    date2 = pd.to_datetime(st.date_input("Fecha Final", endDate))
    today4 = date2.strftime("%d/%m/%Y")

df = df[(df["fecha"] >= date1) & (df["fecha"] <= date2)].copy()

########################################################################################   

col1, col2, col3, col4, col5 = st.columns((5))


# Create for Obra

with col1:
    Obra = st.multiselect("Elige una Obra", df["obra"].unique())
    if not Obra:
        df2 = df.copy()
    else:
        df2 = df[df["obra"].isin(Obra)]

# Create for Tipo de Fallas
with col2:
    Cliente = st.multiselect("Elige un Cliente", df2["cliente"].unique())
    if not Cliente:
        df3 = df2.copy()
    else:
        df3 = df2[df2["cliente"].isin(Cliente)]

# Create for Tipo de Pieza
with col3:
    Tipo_de_Pieza = st.multiselect("Elige un Material",df3["tipo_pieza"].unique())
    if not Tipo_de_Pieza:
        df4 = df3.copy()
    else:
        df4 = df3[df3["tipo_pieza"].isin(Tipo_de_Pieza)]

with col4:
    Pieza = st.multiselect("Elige una Pieza",df4["pieza"].unique())
    if not Pieza:
        df5 = df4.copy()
    else:
        df5 = df4[df4["pieza"].isin(Pieza)]

with col5:
    Falla = st.multiselect("Elige una Falla",df5["tipo_fallas"].unique())
   





if not Obra and not Cliente and not Tipo_de_Pieza and not Pieza  and not Falla:
    filtered_df = df
    

##################################################################################################################
elif not Cliente and not Tipo_de_Pieza and not Pieza and not Falla:
    filtered_df = df[df["obra"].isin(Obra)]

elif not Obra and not Tipo_de_Pieza and not Pieza and not Falla:
    filtered_df = df[df["CLIENTE"].isin(Cliente)]

elif not Falla and not Cliente and not Pieza and not Obra:
    filtered_df = df3[df3["tipo_pieza"].isin(Tipo_de_Pieza)]

elif not Obra and not Tipo_de_Pieza and not Cliente and not Falla:
    filtered_df = df[df["pieza"].isin(Pieza)]

elif not Obra and not Tipo_de_Pieza and not Cliente and not Pieza:
    filtered_df = df[df["tipo_fallas"].isin(Falla)]

##################################################################################################################
elif Obra and Cliente:
    filtered_df = df3[df["obra"].isin(Obra) & df3["cliente"].isin(Cliente)]

elif Obra and Tipo_de_Pieza:
    filtered_df = df3[df["obra"].isin(Obra) & df3["tipo_pieza"].isin(Tipo_de_Pieza)]

elif Obra and Pieza:
    filtered_df = df3[df["obra"].isin(Obra) & df3["pieza"].isin(Pieza)]

elif Obra and Falla:
    filtered_df = df3[df["obra"].isin(Obra) & df3["tipo_fallas"].isin(Falla)]


##################################################################################################################
elif Cliente and Tipo_de_Pieza:
    filtered_df = df3[df["cliente"].isin(Cliente) & df3["tipo_pieza"].isin(Tipo_de_Pieza)]

elif Cliente and Pieza:
    filtered_df = df3[df["cliente"].isin(Cliente) & df3["pieza"].isin(Pieza)]

elif Cliente and Falla:
    filtered_df = df3[df["cliente"].isin(Cliente) & df3["tipo_fallas"].isin(Falla)]

elif Cliente and Obra:
    filtered_df = df3[df["cliente"].isin(Cliente) & df3["obra"].isin(Obra)]

##################################################################################################################
elif Tipo_de_Pieza and Cliente:
    filtered_df = df3[df["tipo_pieza"].isin(Tipo_de_Pieza) & df3["cliente"].isin(Cliente)]

elif Tipo_de_Pieza and Pieza:
    filtered_df = df3[df["tipo_pieza"].isin(Tipo_de_Pieza) & df3["pieza"].isin(Pieza)]

elif Tipo_de_Pieza and Falla:
    filtered_df = df3[df["tipo_pieza"].isin(Tipo_de_Pieza) & df3["tipo_fallas"].isin(Falla)]

elif Tipo_de_Pieza and Obra:
    filtered_df = df3[df["tipo_pieza"].isin(Tipo_de_Pieza) & df3["obra"].isin(Obra)]


##################################################################################################################
elif Pieza and Cliente:
    filtered_df = df3[df["pieza"].isin(Pieza) & df3["cliente"].isin(Cliente)]

elif Pieza and Tipo_de_Pieza:
    filtered_df = df3[df["pieza"].isin(Pieza) & df3["tipo_pieza"].isin(Tipo_de_Pieza)]

elif Pieza and Falla:
    filtered_df = df3[df["pieza"].isin(Pieza) & df3["tipo_fallas"].isin(Falla)]

elif Pieza and Obra:
    filtered_df = df3[df["pieza"].isin(Pieza) & df3["obra"].isin(Obra)]


##################################################################################################################
elif Falla and Cliente:
    filtered_df = df3[df["tipo_fallas"].isin(Falla) & df3["cliente"].isin(Cliente)]

elif Falla and Tipo_de_Pieza:
    filtered_df = df3[df["tipo_fallas"].isin(Falla) & df3["tipo_pieza"].isin(Tipo_de_Pieza)]

elif Falla and Pieza:
    filtered_df = df3[df["tipo_fallas"].isin(Falla) & df3["pieza"].isin(Pieza)]

elif Falla and Obra:
    filtered_df = df3[df["tipo_fallas"].isin(Falla) & df3["obra"].isin(Obra)]


##################################################################################################################
else:
    filtered_df = df3[df3["obra"].isin(Obra) & df3["cliente"].isin(Cliente) & df3["tipo_pieza"].isin(Tipo_de_Pieza) & df3["pieza"].isin(Pieza) & df3["tipo_fallas"].isin(Falla)]


##################################################################################################################
category_df = filtered_df.groupby(by = ["tipo_pieza"], as_index = False)["fallas"].sum()

category2_df = filtered_df.groupby(by = ["obra"], as_index = False)["fallas"].sum()

category3_df = filtered_df.groupby(by = ["pieza"], as_index = False)["fallas"].sum()


##################################################################################################################
with st.expander("Fallas en Obras"):
    fig12 = px.bar(category2_df, x = "obra", y = "fallas",
                    template ="ggplot2")
    fig12.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    fig12.update_traces(marker_color='#FF8000')
    st.plotly_chart(fig12,use_container_width=True, height = 200)
    
col1, col2= st.columns((2))


with col1:
    st.write('<p style="font-size:25px; font-weight:bold; text-align:center;"> Fallas por Pieza</p>', unsafe_allow_html=True)
    fig1 = px.bar(category_df, x = "tipo_pieza", y = "fallas")
    fig1.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    fig1.update_traces(marker_color='#FF8000')
    st.plotly_chart(fig1,use_container_width=True, height = 200)


with col2:
    st.write('<p style="font-size:25px; font-weight:bold; text-align:center;">Fallas por Tipo de Soldadura</p>', unsafe_allow_html=True)
    fig2 = px.pie(filtered_df, values = "fallas", names = "tipo_soldadura", hole = 0.5, template ="presentation")
    fig2.update_traces(text = filtered_df["categoria"], textposition = "outside")
    fig2.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    
    st.plotly_chart(fig2,use_container_width=True)

with st.expander("Por Pieza"):
    fig11 = px.bar(category3_df, x = "pieza", y = "fallas")
    fig11.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    fig11.update_traces(marker_color='#FF8000')
    st.plotly_chart(fig11,use_container_width=True, height = 200)

chart1, chart2 = st.columns((2))
with chart1:
    st.write('<p style="font-size:25px; font-weight:bold; text-align:center;"> Fallas por Pieza</p>', unsafe_allow_html=True)
    fig3 = px.pie(filtered_df, values = "fallas", names = "tipo_pieza", template ="presentation")
    fig3.update_traces(text = filtered_df["tipo_pieza"], textposition = "inside")
    fig3.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    st.plotly_chart(fig3,use_container_width=True)

with chart2:
    st.write('<p style="font-size:25px; font-weight:bold; text-align:center;"> Fallas por Tipo de Soldadura</p>', unsafe_allow_html=True)
    fig4 = px.pie(filtered_df, values = "fallas", names = "tipo_soldadura", template ="presentation")
    fig4.update_traces(text = filtered_df["tipo_fallas"], textposition = "inside")
    fig4.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    st.plotly_chart(fig4,use_container_width=True)

########################################################################################   
cl1, cl2 = st.columns((2))
with cl1:
    with st.expander("Fallas por PIeza"):
        st.write(category_df.style.background_gradient(cmap="Oranges"))
        csv = category_df.to_csv(index = False).encode('utf-8')
        st.download_button("Descargar", data = csv, file_name = "Tipo de Pieza.csv", mime = "text/csv",
                            help = 'Haz click para descargar la información')
        
        
        
    
with cl2:
    with st.expander("Fallas por Tipo de Soldadura"):
        calificacion = filtered_df.groupby(by = "categoria", as_index = False)["fallas"].sum()
        st.write(calificacion.style.background_gradient(cmap="Oranges"))
        csv = calificacion.to_csv(index = False).encode('utf-8')
        st.download_button("Descargar", data = csv, file_name = "Categoria.csv", mime = "text/csv",
                        help = 'Haz click para descargar la información')
        
        





col1, col2 = st.columns((2))

########################################################################################           
with col1:
    filtered_df["Año"] = filtered_df["fecha"].dt.to_period("Y")
    st.write('<p style="font-size:25px; font-weight:bold; text-align:center;"> Fallas por Año</p>', unsafe_allow_html=True)

    linechart = pd.DataFrame(filtered_df.groupby(filtered_df["Año"].dt.strftime("%Y"))["fallas"].sum()).reset_index()
    fig5 = px.line(linechart, x = "Año", y="fallas", labels = {"fallas": "Cantidad"},height=500, width = 1000,template="ggplot2")
    fig5.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    fig5.update_traces(marker_color='#FF8000')
    st.plotly_chart(fig5,use_container_width=True)

    with st.expander("Fallas Por Año"):
        st.write(linechart.T.style.background_gradient(cmap="Blues"))
        csv = linechart.to_csv(index=False).encode("utf-8")
        st.download_button('Descargar', data = csv, file_name = "Fallas por Año.csv", mime ='text/csv',
                        help = 'Haz click para descargar la información')



########################################################################################           
with col2:
    filtered_df["Mes"] = filtered_df["fecha"].dt.to_period("M")
    st.write('<p style="font-size:25px; font-weight:bold; text-align:center;"> Fallas por Mes</p>', unsafe_allow_html=True)

    linechart = pd.DataFrame(filtered_df.groupby(filtered_df["Mes"].dt.strftime("%B"))["fallas"].sum()).reset_index()
    fig6 = px.line(linechart, x = "Mes", y="fallas", labels = {"fallas": "Cantidad"},height=500, width = 1000,template="ggplot2")
    fig6.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    fig6.update_traces(marker_color='#FF8000')
    st.plotly_chart(fig6,use_container_width=True)

    with st.expander("Fallas Por Mes"):
        st.write(linechart.T.style.background_gradient(cmap="Blues"))
        csv = linechart.to_csv(index=False).encode("utf-8")
        st.download_button('Descargar', data = csv, file_name = "Fallas por Mes.csv", mime ='text/csv',
                        help = 'Haz click para descargar la información')


########################################################################################   


col1, col2 = st.columns((2))

########################################################################################           
with col1:
    filtered_df["Semana"] = filtered_df["fecha"].dt.to_period("W")
    st.write('<p style="font-size:25px; font-weight:bold; text-align:center;"> Fallas por Semana</p>', unsafe_allow_html=True)

    linechart = pd.DataFrame(filtered_df.groupby(filtered_df["Semana"].dt.strftime("%W"))["fallas"].sum()).reset_index()
    fig9 = px.line(linechart, x = "Semana", y="fallas", labels = {"fallas": "Cantidad"},height=500, width = 1000,template="ggplot2")
    fig9.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    fig9.update_traces(marker_color='#FF8000')
    st.plotly_chart(fig9,use_container_width=True)

    with st.expander("Fallas Por Semana"):
        st.write(linechart.T.style.background_gradient(cmap="Blues"))
        csv = linechart.to_csv(index=False).encode("utf-8")
        st.download_button('Descargar', data = csv, file_name = "Fallas por Semana.csv", mime ='text/csv',
                        help = 'Haz click para descargar la información')


with col2:
    filtered_df["Dia"] = filtered_df["fecha"].dt.to_period("D")
    st.write('<p style="font-size:25px; font-weight:bold; text-align:center;"> Fallas por Dia</p>', unsafe_allow_html=True)

    linechart = pd.DataFrame(filtered_df.groupby(filtered_df["Dia"].dt.strftime("%D"))["fallas"].sum()).reset_index()
    fig10 = px.line(linechart, x = "Dia", y="fallas", labels = {"fallas": "Cantidad"},height=500, width = 1000,template="ggplot2")
    fig10.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    fig10.update_traces(marker_color='#FF8000')
    st.plotly_chart(fig10,use_container_width=True)

    with st.expander("Fallas Por Dia"):
        st.write(linechart.T.style.background_gradient(cmap="Blues"))
        csv = linechart.to_csv(index=False).encode("utf-8")
        st.download_button('Descargar', data = csv, file_name = "Fallas por Dia.csv", mime ='text/csv',
                        help = 'Haz click para descargar la información')




st.write('<p style="font-size:25px; font-weight:bold; text-align:center;"> Fallas</p>', unsafe_allow_html=True)
with st.expander("Organización de Fallas"):
    fig7 = px.treemap(filtered_df, path = ["categoria","tipo_fallas","tipo_pieza", "calificacion"], values = "fallas",hover_data = ["fallas"],template="presentation")
    fig7.update_layout(width = 800, height = 800)
    fig7.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        })
    st.plotly_chart(fig7, use_container_width=True)


########################################################################################   

st.write('<p style="font-size:25px; font-weight:bold; text-align:center;">Tabla de Datos</p>', unsafe_allow_html=True)
with st.expander("Reporte de Obra"):
    df_sample = filtered_df[["fecha", "obra", "cliente", "tipo_pieza", "pieza", "tipo_soldadura", "tipo_fallas", "categoria", "calificacion","fallas"]]
    
    df_sample["fecha"] = [
        datetime.datetime.strptime(
            str(target_date).split(" ")[0], '%Y-%m-%d').date()
        for target_date in df_sample["fecha"]
    ]
    fig8 = ff.create_table(df_sample, colorscale = "hot")
    fig8.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    st.plotly_chart(fig8, use_container_width=True)



    fotos = filtered_df[["link"]]
    piezas = filtered_df[["pieza"]]

######################################################################################## 
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1]) 
with col1:
    st.write("")
with col2:
    csv = df.to_csv(index = False).encode('utf-8')
    st.download_button('Descargar Archivo', data = csv, file_name = "Data.csv",mime = "text/csv")
with col3:
    st.write("")
with col4:
    export_as_pdf = st.button("Reporte Cliente")
with col5:
    st.write("")



fig1.write_image("reportes/images/fig1.png")
fig2.write_image("reportes/images/fig2.png")
fig3.write_image("reportes/images/fig3.png")
fig4.write_image("reportes/images/fig4.png")
fig9.write_image("reportes/images/fig5.png")
fig10.write_image("reportes/images/fig6.png")
fig8.write_image("reportes/images/fig7.png")



def create_download_link(val, filename):
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Descargar PDF</a>'





if export_as_pdf:
    class PDF(FPDF):
        # Page footer
        def header(self):
            # Position at 1.5 cm from bottom
            self.image('reportes/images/ENCABEZADOSOLANA.png',0, 0, 217, 0, 'PNG')
            self.ln(34)
            self.set_font('Arial', 'B', 10)
            self.cell(35, 10, 'Nombre de la Obra:',0,0,'L')
            self.set_font('Arial', 'I', 10)
            self.cell(90, 10, str(Obra[0]),0,0,'L')
             
            self.ln(8)
            self.set_font('Arial', 'B', 10)
            self.cell(12, 10, 'Fecha:',0,0,'L')
            self.set_font('Arial', 'I', 10)
            self.cell(90, 10, str(today2) ,0,0,'L')
            
            self.ln(8)
            self.set_font('Arial', 'B', 10)
            self.cell(112, 10, '' ,0,0,'L')
            self.cell(33, 10, 'Rango de Fechas:',0,0,'L')
            self.set_font('Arial', 'I', 10)
            self.cell(20, 10, str(today3) ,0,0,'L')
            self.cell(6, 10, ' - ' ,0,0,'L')
            self.cell(20, 10, str(today4) ,0,0,'L')
            pdf.ln(10)
            
        def footer(self):
            # Position at 1.5 cm from bottom
            self.set_y(-15)
            # Arial italic 8
            self.set_font('Arial', 'I', 8)
            # Page number
            self.cell(0, 10, 'Página ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

    # Instantiation of inherited class
    pdf = PDF('P','mm','Letter')
    pdf.alias_nb_pages()
    pdf.add_page()
    
   
    
    

    pdf.set_font('Arial', 'B', 12)
    pdf.cell(190, 10, 'Fallas por Pieza',0,0,'L')
    pdf.ln(8)
    pdf.image('reportes/images/fig1.png', 20, 77, 90, 0, 'PNG')
    pdf.image('reportes/images/fig3.png', 100, 77, 90, 0, 'PNG')
    
    
    pdf.ln(65)
    pdf.cell(190, 10, 'Fallas por Tipo de Soldadura',0,0,'L')
    pdf.image('reportes/images/fig2.png', 20, 150, 90, 0, 'PNG')
    pdf.image('reportes/images/fig4.png', 105, 150, 90, 0, 'PNG')
    
    
    pdf.ln(70)
    pdf.cell(190, 10, 'Fallas Semanales y Diarias',0,0,'L')
    pdf.image('reportes/images/fig5.png', 20, 220, 90, 0, 'PNG')
    pdf.image('reportes/images/fig6.png', 105, 220, 90, 0, 'PNG')
    
    
    
    pdf.add_page()
        

    pdf.set_font('Arial', 'B', 10)
    pdf.cell(190, 10, 'Reporte de Obra',0,0,'L')
    pdf.ln(13)
    
    pdf.set_font('Arial', 'B', 6)
    pdf.set_fill_color(255, 178, 102)
    pdf.cell(19.6,10, 'Fecha', 1,0,'C', True)
    pdf.cell(19.6,10, 'Obra', 1,0,'C', True)
    pdf.cell(19.6,10, 'Cliente', 1,0,'C', True)
    pdf.cell(19.6,10, 'Tipo de Pieza', 1,0,'C', True)
    pdf.cell(19.6,10, 'Pieza', 1,0,'C', True)
    pdf.cell(19.6,10, 'Tipo de Soldadura', 1,0,'C', True)
    pdf.cell(19.6,10, 'Tipo de Falla', 1,0,'C', True)
    pdf.cell(19.6,10, 'Categoría', 1,0,'C', True)
    pdf.cell(19.6,10, 'Calificación', 1,0,'C', True)
    pdf.cell(19.6,10, 'Fallas', 1,0,'C', True)
    pdf.ln()
    
    pdf.set_font('Arial', '', 4)

    columnNameList = list(df_sample)
    for row in range(0, len (df_sample)):
        for col_num, col_name in enumerate(columnNameList):
            if col_num != len(columnNameList) - 1 :
                pdf.cell(19.6,10, str(df_sample['%s' % (col_name)].iloc[row]), 1,0,'C')
            else: 
                pdf.cell(19.6,10, str(df_sample['%s' % (col_name)].iloc[row]), 1,2,'C')
                pdf.cell(-176.4)
                
    pdf.cell(35,10,'',0,2)
    pdf.cell(20)






    x=0
    y=0
    pdf.add_page()
    pdf.ln(15)
    columnNameList = list(fotos)
    columnNameList2 = list(piezas)
    for row in range(0, len (fotos)):
        for col_num2, col_name2 in enumerate(columnNameList2):
            for col_num, col_name in enumerate(columnNameList):
                if col_num != len(columnNameList) - 1 :
                    pdf.image(str(fotos['%s' % (col_name)].iloc[row]), pdf.get_x(), pdf.get_y(), 90, 70, 'PNG')
                else: 
                    pdf.image(str(fotos['%s' % (col_name)].iloc[row]), pdf.get_x(), pdf.get_y(), 90, 70, 'PNG')
                    pdf.set_font('Arial', '', 12)
                    pdf.text(pdf.get_x(), pdf.get_y()+75, str(piezas['%s' % (col_name2)].iloc[row]))
                    if x < 5: 
                        pdf.cell(105)
                        x=x+1
                        
                    if x==2: 
                        pdf.ln(90)
                    if x==4: 
                        pdf.add_page()
                        pdf.ln(15)
                        x=0
                        
                    
                
                
                    
                    
                    

               

                   

                
                    
                    
                
                
                
                



   
    
    
    
    html = create_download_link(pdf.output(dest="S").encode("latin-1"), 'Obra '+str(Obra[0])+ '_'+str(today2) )
    

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
    storage = firebase.storage()



    #pred_img_obj.save("imagenes/pred_img_obj.png")
    #imgw= "imagenes/pred_img_obj.png"

    today = datetime.datetime.now()
    today3 = today.strftime("%H:%M:%S")
    today2 = today.strftime("%d-%m-%Y")

    

    st.markdown(html, unsafe_allow_html=True)
    storage.child('REPORTE/'+'Obra '+str(Obra[0])+ '_'+str(today2) ).put(pdf.output(dest="S").encode("latin-1"))










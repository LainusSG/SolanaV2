import streamlit as st
from streamlit_webrtc import webrtc_streamer, RTCConfiguration
import av
from yolo_prediccion import YOLO_Pred
import datetime
import threading
from matplotlib import pyplot as plt
from PIL import Image
import numpy as np
import cv2
from sqlalchemy import text
import tempfile

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


confidence_slider = 0.25
video_file = st.file_uploader('Sube vídeo', type=['mp4'])
if video_file:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(video_file.read())
    cap = cv2.VideoCapture(tfile.name)
    col1, col2 = st.columns(2)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter('IAVideo/video-sample.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30, (frame_width, frame_height))
    stframe = st.empty()
    progress_bar = st.progress(0)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    with col1:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            if yolo:
                results = yolo(img_rgb, conf=confidence_slider)
                if results:
                    annotated_frame = results[0].plot()
                    out.write(cv2.cvtColor(annotated_frame, cv2.COLOR_RGB2BGR))
                    stframe.image(annotated_frame, channels="RGB", use_column_width=True)  # Ajusta el uso del ancho de la columna
            progress_bar.progress(min(cap.get(cv2.CAP_PROP_POS_FRAMES) / frame_count, 1.0))
        cap.release()
        out.release()
        st.success('Procesamiento de vídeo completo.')

    with col2:
        st.video('output.mp4')

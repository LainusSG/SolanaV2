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
img_container = {"img": None}
total_fallas=[]




def video_frame_callback(frame):
    img = frame.to_ndarray(format="bgr24")
    with lock:
        #flipped = img[::-1,:,:]
        [pred_img, falla_detectada] = yolo.predicciones(img)

        total_fallas.append(falla_detectada)
    return av.VideoFrame.from_ndarray(pred_img, format="bgr24")


ctx = webrtc_streamer(key="example", video_frame_callback=video_frame_callback, rtc_configuration= {"iceServers": [{"urls":["stun:stun1.l.google.com:19302"]}]}, media_stream_constraints={"video":True, "audio": False})



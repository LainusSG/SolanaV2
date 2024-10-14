import cv2
import numpy as np
import os
import yaml
from yaml.loader import SafeLoader

class YOLO_Pred():
    def __init__(self,onnx_model, data_yaml):
        with open(data_yaml, mode='r') as f:
            data_yaml = yaml.load(f,Loader=SafeLoader)
        self.labels = data_yaml['names']
        self.nc =  data_yaml['nc']

        # Cargar el modelo YOLO

        self.yolo = cv2.dnn.readNetFromONNX(onnx_model)
        self.yolo.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        self.yolo.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

    def predicciones(self, image):
# Cargar la imagen
#img = cv2.imread('58cf2807-IMG_1506.jpg')
#image = img.copy()

        row, col, d = image.shape

        valorfalla=[

        ]

        #Paso 1: Convertir imagen en una imagen cuadrada
        max_rc = max(row, col)
        input_image = np.zeros((max_rc, max_rc, 3), dtype=np.uint8)
        input_image[0:row,0:col] = image

        #Paso 2: Predecir desde un arreglo cuadrado
        INPUT_WH_YOLO = 640
        blob = cv2.dnn.blobFromImage(input_image, 1/255,(INPUT_WH_YOLO, INPUT_WH_YOLO), swapRB=True, crop=False)
        self.yolo.setInput(blob)
        preds = self.yolo.forward() # deteccion y predicción con yolo

        detecciones = preds[0]
        boxes = []
        confidences = []
        clases = []

        imagen_w, imagen_h = input_image.shape[:2]
        x_factor = imagen_w/INPUT_WH_YOLO
        y_factor = imagen_h/INPUT_WH_YOLO

        for i in range(len(detecciones)):
            row = detecciones[i]
            confidence = row[4]
            if confidence > 0.4:
                class_score  = row[5:].max() #la probabilidad máxima del objeto de los 14 objectos
                class_id = row[5:].argmax() # trae el indice donde ocurre la máxima probabilidad

                if class_score > 0.25:
                    cx, cy, w, h = row[0:4]
                    # costruir la caja
                    left = int((cx-0.5*w)*x_factor)
                    top = int((cy-0.5*h)*y_factor)
                    width = int(w*x_factor)
                    height = int(h*y_factor)

                    box = np.array([left, top, width, height])

                    confidences.append(confidence)
                    boxes.append(box)
                    clases.append(class_id)

        # Limpiando

        boxes_np = np.array(boxes).tolist()
        confidences_np = np.array(confidences).tolist()

        #NMS

        index = cv2.dnn.NMSBoxes(boxes_np, confidences_np, 0.25, 0.45)

        for ind in index:
            # extraer bordes
            x,y,w,h = boxes_np[ind]
            bb_conf = int(confidences_np[ind]*100)
            class_id = clases[ind]
            class_name = self.labels[class_id]
            colors = self.generar_color(class_id)

            text = f'{class_name}: {bb_conf}%'
            valorfalla.append(text)
            cv2.rectangle(image, (x,y),(x+w,y+h), colors,2)
            cv2.rectangle(image,(x,y-30),(x+w,y),colors,-1)
            cv2.putText(image, text,(x,y-10), cv2.FONT_HERSHEY_PLAIN,5,(0,255,0),8)
        return [image, valorfalla] 
    def generar_color(self, ID):
        np.random.seed(10)
        colors = np.random.randint(100, 255, size=(self.nc, 3)).tolist()
        return tuple(colors[ID])




        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

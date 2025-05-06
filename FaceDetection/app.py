import cv2
import dlib
import numpy as np
import streamlit as st
from PIL import Image
import imutils

# Carregar o detector de faces e o preditor de forma
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Função para detectar círculos no rosto
def detect_circles(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 1)
    
    for rect in rects:
        shape = predictor(gray, rect)
        shape = imutils.face_utils.shape_to_np(shape)
        
        # Desenhar círculos ao redor da cabeça e dos olhos
        for (x, y) in shape:
            cv2.circle(image, (x, y), 2, (0, 255, 0), -1)
        
        # Círculo ao redor da cabeça
        (x, y, w, h) = imutils.face_utils.rect_to_bb(rect)
        cv2.circle(image, (x + w//2, y + h//2), max(w, h)//2, (255, 0, 0), 2)
        
        # Círculos ao redor dos olhos
        for (i, (x, y)) in enumerate(shape[36:48]):
            if i in [0, 3, 6, 9]:  # Pontos ao redor dos olhos
                cv2.circle(image, (x, y), 10, (0, 0, 255), 2)
    
    return image

# Configurar a interface do Streamlit
st.title("Detecção de Círculos no Rosto")
uploaded_file = st.file_uploader("Escolha uma imagem...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    image = np.array(image)
    
    st.image(image, caption='Imagem Original', use_column_width=True)
    
    # Detectar círculos na imagem
    result_image = detect_circles(image)
    
    st.image(result_image, caption='Imagem com Círculos Detectados', use_column_width=True)

import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io
import matplotlib.pyplot as plt

def load_image(uploaded_file):
    if uploaded_file is not None:
        image_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)
        return image
    return None

def convert_color_space(image, color_space='HSV'):
    if color_space == 'HSV':
        return cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    elif color_space == 'YCrCb':
        return cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
    elif color_space == 'Lab':
        return cv2.cvtColor(image, cv2.COLOR_BGR2Lab)
    return image

def detect_skin(image, color_space, thresholds):
    converted_image = convert_color_space(image, color_space)
    
    if color_space == 'HSV':
        lower = np.array([thresholds['h_min'], thresholds['s_min'], thresholds['v_min']])
        upper = np.array([thresholds['h_max'], thresholds['s_max'], thresholds['v_max']])
    elif color_space == 'YCrCb':
        lower = np.array([thresholds['y_min'], thresholds['cr_min'], thresholds['cb_min']])
        upper = np.array([thresholds['y_max'], thresholds['cr_max'], thresholds['cb_max']])
    elif color_space == 'Lab':
        lower = np.array([thresholds['l_min'], thresholds['a_min'], thresholds['b_min']])
        upper = np.array([thresholds['l_max'], thresholds['a_max'], thresholds['b_max']])
    
    mask = cv2.inRange(converted_image, lower, upper)
    result = cv2.bitwise_and(image, image, mask=mask)
    return mask, result

def main():
    st.title("Detector de Pele em Imagens")
    st.write("Upload uma imagem para detectar regiões de pele")
    
    uploaded_file = st.file_uploader("Escolha uma imagem...", type=['jpg', 'jpeg', 'png'])
    
    if uploaded_file is not None:
        image = load_image(uploaded_file)
        if image is not None:
            st.write("Dimensões da imagem:", image.shape)
            
            color_space = st.selectbox(
                "Selecione o espaço de cor",
                ['HSV', 'YCrCb', 'Lab']
            )
            
            st.write("Ajuste os parâmetros de detecção:")
            
            if color_space == 'HSV':
                col1, col2, col3 = st.columns(3)
                with col1:
                    h_min = st.slider('H min', 0, 180, 0)
                    h_max = st.slider('H max', 0, 180, 25)
                with col2:
                    s_min = st.slider('S min', 0, 255, 30)
                    s_max = st.slider('S max', 0, 255, 255)
                with col3:
                    v_min = st.slider('V min', 0, 255, 50)
                    v_max = st.slider('V max', 0, 255, 255)
                thresholds = {
                    'h_min': h_min, 'h_max': h_max,
                    's_min': s_min, 's_max': s_max,
                    'v_min': v_min, 'v_max': v_max
                }
            
            elif color_space == 'YCrCb':
                col1, col2, col3 = st.columns(3)
                with col1:
                    y_min = st.slider('Y min', 0, 255, 0)
                    y_max = st.slider('Y max', 0, 255, 255)
                with col2:
                    cr_min = st.slider('Cr min', 0, 255, 133)
                    cr_max = st.slider('Cr max', 0, 255, 173)
                with col3:
                    cb_min = st.slider('Cb min', 0, 255, 77)
                    cb_max = st.slider('Cb max', 0, 255, 127)
                thresholds = {
                    'y_min': y_min, 'y_max': y_max,
                    'cr_min': cr_min, 'cr_max': cr_max,
                    'cb_min': cb_min, 'cb_max': cb_max
                }
            
            else:  # Lab
                col1, col2, col3 = st.columns(3)
                with col1:
                    l_min = st.slider('L min', 0, 255, 20)
                    l_max = st.slider('L max', 0, 255, 200)
                with col2:
                    a_min = st.slider('a min', 0, 255, 130)
                    a_max = st.slider('a max', 0, 255, 170)
                with col3:
                    b_min = st.slider('b min', 0, 255, 130)
                    b_max = st.slider('b max', 0, 255, 170)
                thresholds = {
                    'l_min': l_min, 'l_max': l_max,
                    'a_min': a_min, 'a_max': a_max,
                    'b_min': b_min, 'b_max': b_max
                }
            
            mask, result = detect_skin(image, color_space, thresholds)
            
            col1, col2, col3 = st.columns(3)
            
            # Convert BGR to RGB for display
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            result_rgb = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
            
            with col1:
                st.write("Imagem Original")
                st.image(image_rgb, use_column_width=True)
            
            with col2:
                st.write("Máscara de Pele")
                st.image(mask, use_column_width=True)
            
            with col3:
                st.write("Resultado")
                st.image(result_rgb, use_column_width=True)

if __name__ == '__main__':
    main()

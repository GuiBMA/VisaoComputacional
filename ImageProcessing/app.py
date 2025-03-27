import streamlit as st
import numpy as np
from PIL import Image

# Função para aplicar o filtro da média (Blur)
def mean_filter(image, kernel_size):
    img_array = np.array(image)
    padded_img = np.pad(img_array, ((kernel_size//2, kernel_size//2), (kernel_size//2, kernel_size//2), (0, 0)), mode='constant')
    filtered_img = np.zeros_like(img_array)
    
    # Aplicar o filtro da média
    for i in range(img_array.shape[0]):
        for j in range(img_array.shape[1]):
            for k in range(img_array.shape[2]):
                filtered_img[i, j, k] = np.mean(padded_img[i:i+kernel_size, j:j+kernel_size, k])
    
    return Image.fromarray(filtered_img)

# Função para realçar a imagem
def enhance_image(image, factor):
    img_array = np.array(image)
    enhanced_img = np.clip(img_array * factor, 0, 255)
    return Image.fromarray(enhanced_img.astype(np.uint8))

# Função para aplicar o filtro da mediana
def median_filter(image, kernel_size):
    img_array = np.array(image)
    padded_img = np.pad(img_array, ((kernel_size//2, kernel_size//2), (kernel_size//2, kernel_size//2), (0, 0)), mode='constant')
    filtered_img = np.zeros_like(img_array)
    
    # Aplicar o filtro da mediana
    for i in range(img_array.shape[0]):
        for j in range(img_array.shape[1]):
            for k in range(img_array.shape[2]):
                filtered_img[i, j, k] = np.median(padded_img[i:i+kernel_size, j:j+kernel_size, k])
    
    return Image.fromarray(filtered_img)

# Função para obter as bordas da imagem usando o filtro da média
def get_edges(image, kernel_size):
    img_array = np.array(image)
    blurred_img = np.array(mean_filter(image, kernel_size))
    edges = np.clip(img_array - blurred_img, 0, 255)
    return Image.fromarray(edges.astype(np.uint8))

# Função para reforçar as bordas da imagem usando o filtro da média
def reinforce_edges(image, kernel_size):
    img_array = np.array(image)
    edges = np.array(get_edges(image, kernel_size))
    reinforced_img = np.clip(img_array + edges, 0, 255)
    return Image.fromarray(reinforced_img.astype(np.uint8))

# Função para aplicar erosão na imagem
def erode_image(image, kernel_size):
    img_array = np.array(image)
    padded_img = np.pad(img_array, ((kernel_size//2, kernel_size//2), (kernel_size//2, kernel_size//2), (0, 0)), mode='constant')
    eroded_img = np.zeros_like(img_array)
    
    # Aplicar erosão
    for i in range(img_array.shape[0]):
        for j in range(img_array.shape[1]):
            for k in range(img_array.shape[2]):
                eroded_img[i, j, k] = np.min(padded_img[i:i+kernel_size, j:j+kernel_size, k])
    
    return Image.fromarray(eroded_img)

# Função para aplicar dilatação na imagem
def dilate_image(image, kernel_size):
    img_array = np.array(image)
    padded_img = np.pad(img_array, ((kernel_size//2, kernel_size//2), (kernel_size//2, kernel_size//2), (0, 0)), mode='constant')
    dilated_img = np.zeros_like(img_array)
    
    # Aplicar dilatação
    for i in range(img_array.shape[0]):
        for j in range(img_array.shape[1]):
            for k in range(img_array.shape[2]):
                dilated_img[i, j, k] = np.max(padded_img[i:i+kernel_size, j:j+kernel_size, k])
    
    return Image.fromarray(dilated_img)

# Interface do Streamlit
st.title("Processamento de Imagens com Streamlit")

# Carregar a imagem
uploaded_file = st.file_uploader("Escolha uma imagem...", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Imagem Original', use_column_width=True)

    # Selecionar parâmetros
    kernel_size = st.slider("Tamanho do Kernel", 3, 15, 3)
    factor = st.slider("Fator de Realce", 1.0, 3.0, 1.5)

    # Aplicar filtros e operações
    filtered_image = mean_filter(image, kernel_size)
    st.image(filtered_image, caption='Imagem Filtrada (Filtro da Média)', use_column_width=True)

    enhanced_image = enhance_image(image, factor)
    st.image(enhanced_image, caption='Imagem Realçada', use_column_width=True)

    median_filtered_image = median_filter(image, kernel_size)
    st.image(median_filtered_image, caption='Imagem Filtrada (Filtro da Mediana)', use_column_width=True)

    edges_image = get_edges(image, kernel_size)
    st.image(edges_image, caption='Bordas da Imagem', use_column_width=True)

    reinforced_image = reinforce_edges(image, kernel_size)
    st.image(reinforced_image, caption='Bordas Reforçadas', use_column_width=True)

    eroded_image = erode_image(image, kernel_size)
    st.image(eroded_image, caption='Imagem Erodida', use_column_width=True)

    dilated_image = dilate_image(image, kernel_size)
    st.image(dilated_image, caption='Imagem Diltada', use_column_width=True)
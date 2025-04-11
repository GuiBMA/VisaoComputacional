import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os


def prewitt_edge_detection(image):
    """
    Detecção de bordas utilizando operadores Prewitt (primeira derivada).
    É necessário criar os kernels manualmente, pois o OpenCV não tem Prewitt nativo.
    """
    # Converte para escala de cinza caso não esteja
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Kernels Prewitt
    kernelx = np.array([[-1,  0,  1],
                        [-1,  0,  1],
                        [-1,  0,  1]], dtype=np.float32)
    kernely = np.array([[ 1,  1,  1],
                        [ 0,  0,  0],
                        [-1, -1, -1]], dtype=np.float32)
    
    # Convolução (a saída geralmente vem em uint8 se a imagem de entrada for uint8)
    img_prewittx = cv2.filter2D(gray, cv2.CV_32F, kernelx)
    img_prewitty = cv2.filter2D(gray, cv2.CV_32F, kernely)
    
    # Agora temos duas imagens em float32. Podemos calcular a magnitude:
    # Opção 1 (usando as funções do OpenCV):
    prewitt = cv2.sqrt(cv2.addWeighted(cv2.pow(img_prewittx, 2.0), 1.0,
                                       cv2.pow(img_prewitty, 2.0), 1.0, 0.0))

    # Opção 2 (usando Numpy):
    # prewitt = np.sqrt(img_prewittx**2 + img_prewitty**2)

    # Retorna a matriz resultante em float32
    # Se precisar exibir como imagem, normalizar e converter para uint8:
    # prewitt_disp = cv2.normalize(prewitt, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    
    return prewitt

def prewitt_compass_edge_detection(image):
    """
    Detecção de bordas utilizando o operador Prewitt Compass.
    Nesse método, usamos várias máscaras (orientações) e pegamos o máximo.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = np.float32(gray)
    
    # Máscaras (kernels) nas 8 direções
    kernels = []
    kernels.append(np.array([[ -1,  0,  1],
                             [ -1,  0,  1],
                             [ -1,  0,  1]], dtype=np.float32)) # 0° / 180°
    kernels.append(np.array([[  0,  1,  1],
                             [ -1,  0,  1],
                             [ -1, -1,  0]], dtype=np.float32)) # 45°
    kernels.append(np.array([[  1,  1,  1],
                             [  0,  0,  0],
                             [ -1, -1, -1]], dtype=np.float32)) # 90°
    kernels.append(np.array([[  1,  1,  0],
                             [  1,  0, -1],
                             [  0, -1, -1]], dtype=np.float32)) # 135°
    kernels.append(np.array([[  1,  0, -1],
                             [  1,  0, -1],
                             [  1,  0, -1]], dtype=np.float32)) # 180°
    kernels.append(np.array([[  0, -1, -1],
                             [  1,  0, -1],
                             [  1,  1,  0]], dtype=np.float32)) # 225°
    kernels.append(np.array([[ -1, -1, -1],
                             [  0,  0,  0],
                             [  1,  1,  1]], dtype=np.float32)) # 270°
    kernels.append(np.array([[ -1, -1,  0],
                             [ -1,  0,  1],
                             [  0,  1,  1]], dtype=np.float32)) # 315°

    # Aplica cada kernel e pega o valor máximo
    compass_images = [cv2.filter2D(gray, -1, k) for k in kernels]
    # Tira o valor absoluto para realçar as bordas (ou pode pegar o valor bruto se preferir)
    compass_images_abs = [np.abs(ci) for ci in compass_images]
    
    # Faz um stack e pega o máximo por pixel
    stacked = np.stack(compass_images_abs, axis=-1)
    compass_result = np.max(stacked, axis=-1)
    
    return compass_result


def sobel_edge_detection(image):
    """
    Detecção de bordas utilizando operador Sobel (primeira derivada).
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Sobel nas direções x e y
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    # Magnitude
    sobel_mag = cv2.magnitude(sobelx, sobely)
    
    return sobel_mag


def sobel_compass_edge_detection(image):
    """
    Implementa lógica semelhante ao compass, mas usando Sobel em múltiplas orientações (H/V é o mais comum).
    Aqui, mostraremos apenas H/V (pois Sobel normalmente é 2 direções), mas para 'compass'
    poderíamos combinar mais ângulos. Ilustramos com horizontal e vertical.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Sobel horizontal (y=0, x=1)
    sobel_h = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    # Sobel vertical (y=1, x=0)
    sobel_v = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    
    # Podemos combinar tirando o máximo
    sobel_h_abs = np.abs(sobel_h)
    sobel_v_abs = np.abs(sobel_v)
    
    combined = np.maximum(sobel_h_abs, sobel_v_abs)
    return combined


def successive_gaussians_edge_detection(image):
    """
    Exemplo simples de 'Successive Gaussians' ou Diferença de Gaussiana (DoG).
    Aplica duas Gaussianas com sigmas diferentes e subtrai uma da outra.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Gaussian blur com duas sigmas diferentes
    blur1 = cv2.GaussianBlur(gray, (5,5), 1)
    blur2 = cv2.GaussianBlur(gray, (5,5), 2)
    
    dog = blur1 - blur2
    # Convertendo para valor absoluto para realçar bordas
    dog_abs = np.abs(dog)
    
    return dog_abs


def canny_edge_detection(image, low_threshold=100, high_threshold=200):
    """
    Detecção de bordas utilizando Canny, que faz:
    1) Suavização por Gaussiana
    2) Gradiente (1ª derivada)
    3) Non-maximum suppression
    4) Histerese
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, low_threshold, high_threshold)
    return edges


def gaussian_blur(image, kernel_size=5, sigma=1):
    """
    Aplica um Kernel Gaussiano básico para suavização.
    """
    return cv2.GaussianBlur(image, (kernel_size, kernel_size), sigma)


# --------------------------------------------------
# Função principal do Streamlit
# --------------------------------------------------

def main():
    st.title("Comparação de Detectores de Borda com Streamlit")

    st.write("""
    Este aplicativo compara diferentes métodos de detecção de bordas em imagens, 
    incluindo Prewitt, Sobel, Canny e variações com filtros gaussianos.
    """)

    # Opção para escolher imagens pré-definidas ou upload
    option = st.sidebar.selectbox(
        "Escolha uma imagem de entrada",
        ("Mortal no Lago", "Caveirão", "Senegal", 
         "Guarda-Chuva", "Crianças na Agua", "Bicicleta", 
         "Banho de Mangueira", "Altinha", "Parede do Chaves","Salto de Fé","Fazer upload...")
    )

    if option == "Mortal no Lago":
        img_path = "images/AP1VisãoComputacional_TércioTeixeira.jpg"
        image = Image.open(img_path)
    elif option == "Caveirão":
        img_path = "images/AP1VisãoComputacional1_TércioTeixeira.jpg"
        image = Image.open(img_path)
    elif option == "Senegal":
        img_path = "images/AP1VisãoComputacional2_TércioTeixeira.jpg"
        image = Image.open(img_path)
    elif option == "Guarda-Chuva":
        img_path = "images/AP1VisãoComputacional3_TércioTeixeira.jpg"
        image = Image.open(img_path)
    elif option == "Crianças na Agua":
        img_path = "images/AP1VisãoComputacional4_TércioTeixeira.jpg"
        image = Image.open(img_path)
    elif option == "Bicicleta":
        img_path = "images/AP1VisãoComputacional5_TércioTeixeira.jpg"
        image = Image.open(img_path)
    elif option == "Banho de Mangueira":
        img_path = "images/AP1VisãoComputacional6_TércioTeixeira.jpg"
        image = Image.open(img_path)
    elif option == "Altinha":
        img_path = "images/AP1VisãoComputacional7_TércioTeixeira.jpg"
        image = Image.open(img_path)
    elif option == "Parede do Chaves":
        img_path = "images/AP1VisãoComputacional8_TércioTeixeira.jpg"
        image = Image.open(img_path)
    elif option == "Salto de Fé":
        img_path = "images/AP1VisãoComputacional9_TércioTeixeira.jpg"
        image = Image.open(img_path)
    else:
        uploaded_file = st.sidebar.file_uploader("Faça upload da imagem", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
        else:
            st.warning("Por favor, faça upload de uma imagem ou selecione uma opção padrão.")
            return

    # Converte para OpenCV (numpy array)
    opencv_image = np.array(image.convert("RGB"))
    opencv_image = cv2.cvtColor(opencv_image, cv2.COLOR_RGB2BGR)

    st.subheader("Imagem Original")
    st.image(image, use_container_width=True)

    st.markdown("---")
    st.subheader("Comparação dos Detectores de Borda")

    # Aplica cada método
    prewitt = prewitt_edge_detection(opencv_image)
    prewitt_compass = prewitt_compass_edge_detection(opencv_image)
    sobel = sobel_edge_detection(opencv_image)
    sobel_compass = sobel_compass_edge_detection(opencv_image)
    canny = canny_edge_detection(opencv_image)
    dog = successive_gaussians_edge_detection(opencv_image)
    
    # Para exibir, podemos normalizar as imagens (para Prewitt, Sobel, etc.)
    # ou converter para uint8 caso sejam floats.
    prewitt_disp = cv2.normalize(prewitt, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    prewitt_compass_disp = cv2.normalize(prewitt_compass, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    sobel_disp = cv2.normalize(sobel, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    sobel_compass_disp = cv2.normalize(sobel_compass, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    dog_disp = cv2.normalize(dog, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    # Canny já está em formato uint8

    # Exibição lado a lado (cada detecção ao lado da imagem suavizada)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("**Prewitt (Primeira Derivada)**")
        st.image(prewitt_disp, use_container_width=True)
        
        st.write("**Sobel (Primeira Derivada)**")
        st.image(sobel_disp, use_container_width=True)

    with col2:
        st.write("**Prewitt Compass**")
        st.image(prewitt_compass_disp, use_container_width=True)
        
        st.write("**Sobel Compass (H/V)**")
        st.image(sobel_compass_disp, use_container_width=True)

    with col3:
        st.write("**Canny**")
        st.image(canny, use_container_width=True)
        
        st.write("**Diferença de Gaussiana**")
        st.image(dog_disp, use_container_width=True)

    st.markdown("---")
    st.subheader("Aplicar Kernel Gaussiano")

    kernel_size = st.slider("Tamanho do Kernel", min_value=3, max_value=15, step=2, value=5)
    sigma_value = st.slider("Sigma", min_value=1, max_value=10, value=1)
    
    # Aplica Gaussian
    gaussed_img = gaussian_blur(opencv_image, kernel_size, sigma_value)
    
    # Cria duas colunas para mostrar as imagens lado a lado
    col1, col2 = st.columns(2)
    with col1:
        st.image(cv2.cvtColor(opencv_image, cv2.COLOR_BGR2RGB), caption="Imagem Original", use_container_width=True)
    with col2:
        st.image(cv2.cvtColor(gaussed_img, cv2.COLOR_BGR2RGB), caption="Imagem suavizada com Kernel Gaussiano", use_container_width=True)


if __name__ == "__main__":
    main()

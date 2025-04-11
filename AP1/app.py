import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os

# =========================
# Funções de detecção de bordas
# =========================


def prewitt_edge_detection(image):
    """Detecção de bordas usando Prewitt (com kernel personalizado)."""
    # Converte para escala de cinza
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Kernels clássicos do Prewitt
    kernelx = np.array([[-1, 0, 1],
                        [-1, 0, 1],
                        [-1, 0, 1]], dtype=np.float32)

    kernely = np.array([[1, 1, 1],
                        [0, 0, 0],
                        [-1, -1, -1]], dtype=np.float32)

    # Aplica os filtros
    img_prewittx = cv2.filter2D(gray, cv2.CV_32F, kernelx)
    img_prewitty = cv2.filter2D(gray, cv2.CV_32F, kernely)

    # Calcula a magnitude do gradiente
    prewitt = cv2.magnitude(img_prewittx, img_prewitty)

    return prewitt


def prewitt_compass_edge_detection(image):
    """Prewitt Compass (direções fixas)."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = np.float32(gray)
    
    kernels = [
        np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], dtype=np.float32),
        np.array([[0, 1, 1], [-1, 0, 1], [-1, -1, 0]], dtype=np.float32),
        np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]], dtype=np.float32),
        np.array([[1, 1, 0], [1, 0, -1], [0, -1, -1]], dtype=np.float32),
        np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]], dtype=np.float32),
        np.array([[0, -1, -1], [1, 0, -1], [1, 1, 0]], dtype=np.float32),
        np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]], dtype=np.float32),
        np.array([[-1, -1, 0], [-1, 0, 1], [0, 1, 1]], dtype=np.float32)
    ]

    compass_images = [np.abs(cv2.filter2D(gray, -1, k)) for k in kernels]
    stacked = np.stack(compass_images, axis=-1)
    return np.max(stacked, axis=-1)


def sobel_edge_detection(image, kernel_size):
    """Detecção de bordas usando Sobel."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=kernel_size)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=kernel_size)
    return cv2.magnitude(sobelx, sobely)


def sobel_compass_edge_detection(image, kernel_size):
    """Sobel Compass usando máximo entre horizontal e vertical."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    sobel_h = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=kernel_size)
    sobel_v = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=kernel_size)
    return np.maximum(np.abs(sobel_h), np.abs(sobel_v))


def laplacian_edge_detection(image, kernel_size):
    """Detecção de bordas usando Laplaciano."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    laplacian = cv2.Laplacian(gray, cv2.CV_64F, ksize=kernel_size)
    return np.abs(laplacian)


def roberts_edge_detection(image):
    """Detecção de bordas usando Roberts Cross (kernel fixo 2x2)."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    kernelx = np.array([[1, 0], [0, -1]], dtype=np.float32)
    kernely = np.array([[0, 1], [-1, 0]], dtype=np.float32)
    img_robertsx = cv2.filter2D(gray, -1, kernelx)
    img_robertsy = cv2.filter2D(gray, -1, kernely)
    return cv2.magnitude(img_robertsx.astype(float), img_robertsy.astype(float))


def successive_gaussians_edge_detection(image):
    """DoG (Diferença de Gaussianas). Não depende do slider."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur1 = cv2.GaussianBlur(gray, (5, 5), 1)
    blur2 = cv2.GaussianBlur(gray, (5, 5), 2)
    return np.abs(blur1 - blur2)


def canny_edge_detection(image, low_threshold=100, high_threshold=200):
    """Detecção de bordas usando Canny."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return cv2.Canny(gray, low_threshold, high_threshold)


def gaussian_blur(image, kernel_size, sigma):
    """Aplica Gaussian Blur."""
    return cv2.GaussianBlur(image, (kernel_size, kernel_size), sigma)


# --------------------------------------------------
# Função principal do Streamlit
# --------------------------------------------------

def main():
    st.title("Comparação de Detectores de Borda com Streamlit")

    st.write("""
    Este aplicativo compara diferentes métodos de detecção de bordas em imagens, 
    incluindo Prewitt, Sobel, Canny, Roberts, Laplaciano e variações com filtros gaussianos.
    """)

    # ==== Menu lateral completo ====
    st.sidebar.header("Configurações")

    option = st.sidebar.selectbox(
        "Escolha uma imagem de entrada",
        ("Mortal no Lago", "Caveirão", "Senegal", 
         "Guarda-Chuva", "Crianças na Agua", "Bicicleta", 
         "Banho de Mangueira", "Altinha", "Parede do Chaves", 
         "Salto de Fé","Mickey 8-bit","Jogo Baixa Qualidade", "Jogo Alta Qualidade", 'Carro', "Fazer upload...")
    )

    uploaded_file = None
    if option == "Fazer upload...":
        uploaded_file = st.sidebar.file_uploader("Faça upload da imagem", type=["jpg", "jpeg", "png"])

    # Slider global para kernel dos detectores
    kernel_global = st.sidebar.slider("Tamanho do Kernel Global (detectores)", min_value=3, max_value=31, step=2, value=3)

    st.sidebar.markdown("---")
    st.sidebar.subheader("Configuração Gaussian Blur (Suavização)")
    kernel_size = st.sidebar.slider("Tamanho do Kernel Gaussiano", min_value=3, max_value=31, step=2, value=5)
    sigma_value = st.sidebar.slider("Desvio Padrão (Sigma)", min_value=1, max_value=10, value=1)
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("Comparação Interativa")
    
    detector_names = [
        "Prewitt (3×3 fixo)",
        "Prewitt Compass (direções)",
        "Sobel (kernel variável)",
        "Sobel Compass (H/V)",
        "Laplaciano (kernel variável)",
        "Roberts (2×2 fixo)",
        "Canny (avançado)",
        "Diferença de Gaussianas (DoG)"
    ]

    selected_sem = st.sidebar.selectbox(
        "Escolha um detector SEM suavização",
        detector_names
    )

    selected_com = st.sidebar.selectbox(
        "Escolha um detector COM suavização",
        detector_names
    )


    # ==== Carregamento da imagem mantendo if / elif / else ====
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
    elif option == "Mickey 8-bit":
        img_path = "images/mickey2.png"
        image = Image.open(img_path) 
    elif option == "Jogo Baixa Qualidade":
        img_path = "images/celeste2.jpeg"
        image = Image.open(img_path)
    elif option == "Jogo Alta Qualidade":
        img_path = "images/celeste3.jpg"
        image = Image.open(img_path)   
    elif option == "Carro":
        img_path = "images/carro.jpg"
        image = Image.open(img_path)         
    else:
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
        else:
            st.warning("Por favor, faça upload de uma imagem ou selecione uma opção padrão.")
            return

    # Converte para OpenCV
    opencv_image = np.array(image.convert("RGB"))
    opencv_image = cv2.cvtColor(opencv_image, cv2.COLOR_RGB2BGR)

    # Aplica Gaussian Blur (para a comparação com suavização)
    gaussed_image = gaussian_blur(opencv_image, kernel_size, sigma_value)

    # Função utilitária para normalizar imagens para exibição
    def normalize_display(img):
        return cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8) if img.dtype != np.uint8 else img

    # ==== Detectores (Sem suavização) ====
    st.markdown("---")
    st.subheader("Detectores de Borda **SEM** Suavização")

    # Aplica cada método na imagem original
    detectors_original = {
        "Prewitt (3×3 fixo)": prewitt_edge_detection(opencv_image),
        "Prewitt Compass (direções)": prewitt_compass_edge_detection(opencv_image),
        "Sobel (kernel variável)": sobel_edge_detection(opencv_image, kernel_global),
        "Sobel Compass (H/V)": sobel_compass_edge_detection(opencv_image, kernel_global),
        "Laplaciano (kernel variável)": laplacian_edge_detection(opencv_image, kernel_global),
        "Roberts (2×2 fixo)": roberts_edge_detection(opencv_image),
        "Canny (avançado)": canny_edge_detection(opencv_image),
        "Diferença de Gaussianas (DoG)": successive_gaussians_edge_detection(opencv_image),
    }

    col1, col2 = st.columns(2)
    for idx, (name, result) in enumerate(detectors_original.items()):
        with (col1 if idx % 2 == 0 else col2):
            st.write(f"**{name}**")
            st.image(normalize_display(result), use_container_width=True)

    # ==== Detectores (Com suavização) ====
    st.markdown("---")
    st.subheader("Detectores de Borda **COM** Suavização (Gaussian Blur)")

    # Aplica cada método na imagem suavizada
    detectors_smooth = {
        "Prewitt (3×3 fixo)": prewitt_edge_detection(gaussed_image),
        "Prewitt Compass (direções)": prewitt_compass_edge_detection(gaussed_image),
        "Sobel (kernel variável)": sobel_edge_detection(gaussed_image, kernel_global),
        "Sobel Compass (H/V)": sobel_compass_edge_detection(gaussed_image, kernel_global),
        "Laplaciano (kernel variável)": laplacian_edge_detection(gaussed_image, kernel_global),
        "Roberts (2×2 fixo)": roberts_edge_detection(gaussed_image),
        "Canny (avançado)": canny_edge_detection(gaussed_image),
        "Diferença de Gaussianas (DoG)": successive_gaussians_edge_detection(gaussed_image),
    }

    col1, col2 = st.columns(2)
    for idx, (name, result) in enumerate(detectors_smooth.items()):
        with (col1 if idx % 2 == 0 else col2):
            st.write(f"**{name}**")
            st.image(normalize_display(result), use_container_width=True)

    # ==== Exibe imagem original e suavizada separadamente ====
    st.markdown("---")
    st.subheader("Visualização da Suavização Aplicada")

    col1, col2 = st.columns(2)
    with col1:
        st.image(cv2.cvtColor(opencv_image, cv2.COLOR_BGR2RGB), caption="Imagem Original", use_container_width=True)
    with col2:
        st.image(cv2.cvtColor(gaussed_image, cv2.COLOR_BGR2RGB), caption="Imagem com Gaussian Blur", use_container_width=True)
        
        st.markdown("---")
    st.subheader("Comparação Interativa entre Detectores")

    # Pega as imagens correspondentes aos detectores selecionados
    image_sem_suavizacao = normalize_display(detectors_original[selected_sem])
    image_com_suavizacao = normalize_display(detectors_smooth[selected_com])

    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**{selected_sem} - SEM Suavização**")
        st.image(image_sem_suavizacao, use_container_width=True)

    with col2:
        st.write(f"**{selected_com} - COM Suavização**")
        st.image(image_com_suavizacao, use_container_width=True)


if __name__ == "__main__":
    main()

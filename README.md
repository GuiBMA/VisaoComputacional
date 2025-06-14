# Visão Computacional

**Autores:**
- *Guilherme Barros*
- *Ivo Lavacek*
- *Pedro Lustosaa*
- *Gustavo Raia*
- *André Silveira*

## 1. Introdução

Este projeto contém uma série de trabalhos práticos desenvolvidos na disciplina de Visão Computacional, demonstrando diferentes técnicas e aplicações de processamento de imagem e visão computacional.

## 2. Estrutura do Projeto

O projeto está organizado nas seguintes atividades:

### AP1 - Detecção de Bordas
Demonstração de diferentes técnicas de detecção de bordas em imagens, incluindo:
- Prewitt (primeira derivada)
- Prewitt Compass
- Sobel
- Sobel Compass (H/V)
- Diferença de Gaussiana (DoG)
- Canny

### AP2 - Detecção de Movimento
Implementação de algoritmos para detecção de movimento em vídeos.

### AC1 - Processamento de Imagem
Aplicações básicas de processamento de imagem, incluindo:
- Transformações geométricas
- Filtros espaciais
- Operações morfológicas
- Histogramas e equalização

### AC2 - Detecção de Pele
Implementação de algoritmos para detecção de pele em imagens utilizando diferentes espaços de cor.

### AC3 - Detecção Facial
Sistema para detecção de faces em imagens utilizando:
- Cascade Classifiers
- Deep Learning (opcional)

### AC4 - Detecção de Círculos
Implementação de algoritmos para detecção de círculos em imagens:
- Transformada de Hough
- Detecção de círculos com OpenCV

### AC5 - Detecção de Texto
Sistema para detecção e reconhecimento de texto em imagens utilizando:
- OCR (Optical Character Recognition)
- Tesseract
- Pytesseract

### AC6 - Detecção de Objetos
Implementação de algoritmos para detecção de objetos em imagens:
- YOLO (You Only Look Once)
- Deep Learning para detecção de objetos

## 3. Tecnologias e Bibliotecas Utilizadas

- **Python 3.7+**
- **OpenCV (cv2) 4.5.0+** para processamento de imagens
- **Streamlit 1.0.0+** para criação de interface web
- **NumPy 1.20.0+** para manipulações em arrays
- **PIL (Pillow) 8.0.0+** para carregamento de imagens
- **Matplotlib 3.3.0+** para visualização de dados
- **Tesseract OCR** para reconhecimento de texto
- **YOLO** para detecção de objetos

## 4. Estrutura de Pastas

```plaintext
├── AP1/
│   ├── app.py
│   ├── resumo_slides/
│   └── images/
├── AP2/
│   ├── Cartas/
│   ├── documentclass_PT_BR_NaoFinalizado.txt
│   └── app.py
├── AC1_ImageProcessing/
│   └── app.py
├── AC2_SkinDetection/
│   └── app.py
├── AC3_FaceDetection/
│   └── app.py
├── AC4_CircleDedection/
│   └── app.py
├── AC5_TextDetection/
│   └── app.py
├── AC6_DetecçãoDeObjetos/
│   └── app.py
├── venv/
├── README.md
├── requirements.txt
└── .gitignore
```

## 5. Instruções de Uso

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/seu-usuario/VisaoComputacional.git
   cd VisaoComputacional
   ```

2. **Crie e ative um ambiente virtual** (recomendado):
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute o aplicativo desejado**:
   ```bash
   streamlit run [pasta]/app.py
   ```
   Exemplo: `streamlit run AP1/app.py`

## 6. Requisitos Adicionais

Algumas funcionalidades podem requerer instalações adicionais:

- **Tesseract OCR**: Necessário para AC5 (Detecção de Texto)
  - Windows: Baixe o instalador em https://github.com/UB-Mannheim/tesseract/wiki
  - Linux: `sudo apt-get install tesseract-ocr`
  - Mac: `brew install tesseract`

- **YOLO**: Necessário para AC6 (Detecção de Objetos)
  - Siga as instruções específicas na pasta AC6_DetecçãoDeObjetos

## 7. Referências

- ALMEIDA, J. G. et al. *Digital Image Edge Detection: A Systematic Review*, 2019 19th International Conference on Advanced Robotics (ICAR), 2019.
- GONZALEZ, R. C.; WOODS, R. E. *Digital Image Processing*. 4. ed. New York: Pearson, 2018.
- Documentação do [OpenCV](https://docs.opencv.org/master/)
- Documentação do [Streamlit](https://docs.streamlit.io/)
- Documentação do [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- Documentação do [YOLO](https://github.com/ultralytics/yolov5)
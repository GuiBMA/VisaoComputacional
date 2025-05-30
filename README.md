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

### AC1 - Processamento de Imagem
Aplicações básicas de processamento de imagem.

### AC2 - Detecção de Pele
Implementação de algoritmos para detecção de pele em imagens.

### AC3 - Detecção Facial
Sistema para detecção de faces em imagens.

### AC4 - Detecção de Círculos
Implementação de algoritmos para detecção de círculos em imagens.

### AC5 - Detecção de Texto
Sistema para detecção e reconhecimento de texto em imagens.

## 3. Tecnologias e Bibliotecas Utilizadas

- **Python 3.7+**
- **OpenCV (cv2)** para processamento de imagens
- **Streamlit** para criação de interface web
- **NumPy** para manipulações em arrays
- **PIL (Pillow)** para carregamento de imagens
- **Matplotlib** para visualização de dados

## 4. Estrutura de Pastas

```plaintext
├── AP1/
│   ├── app.py
│   ├── resumo_slides/
│   └── images/
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
├── README.md
└── requirements.txt
```

## 5. Instruções de Uso

1. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Execute o aplicativo desejado**:
   ```bash
   streamlit run [pasta]/app.py
   ```
   Exemplo: `streamlit run AP1/app.py`

## 6. Referências

- ALMEIDA, J. G. et al. *Digital Image Edge Detection: A Systematic Review*, 2019 19th International Conference on Advanced Robotics (ICAR), 2019.
- GONZALEZ, R. C.; WOODS, R. E. *Digital Image Processing*. 4. ed. New York: Pearson, 2018.
- Documentação do [OpenCV](https://docs.opencv.org/master/)
- Documentação do [Streamlit](https://docs.streamlit.io/)
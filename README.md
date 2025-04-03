# Visão Computacional

**Autores:**
- *Guilherme Barros de Melo Almeida*
- *Ivo lavaseck*
- *Pedro Lustroza*
- *Gustavo*
- *André*

## 1. Introdução

Este projeto tem como objetivo demonstrar o uso de diferentes técnicas na matéria de Visão Computacional. A pasta AP1 mostra diversas formas na detecção de bordas em imagens, comparando métodos clássicos da literatura, como Prewitt, Sobel e Canny, além de variações como Prewitt Compass, Sobel Compass e Diferença de Gaussiana (Sucessive Gaussians).

Estes softwares foram desenvolvidos em Python, utilizando a biblioteca [Streamlit](https://streamlit.io/) para criar a interface gráfica de comparação dos resultados.

## 2. Descrição do Software AP1

O aplicativo permite que o usuário selecione imagens de entrada de duas maneiras:
1. **Imagens padrão**: três exemplos de imagens fornecidas para comparação imediata.
2. **Upload de imagem**: permite o envio de uma imagem local no formato JPG ou PNG.

Após a seleção da imagem, o usuário pode visualizar:
- **Detecção de bordas com Prewitt** (primeira derivada, implementado manualmente);
- **Prewitt Compass** (várias máscaras em diferentes orientações);
- **Detecção de bordas com Sobel** (primeira derivada utilizando OpenCV);
- **Sobel Compass (H/V)** (detecção enfatizando direções horizontal e vertical);
- **Diferença de Gaussiana (DoG)** (Successive Gaussians);
- **Canny** (algoritmo que combina suavização gaussiana, gradiente e histerese).

Adicionalmente, o usuário pode aplicar **suavização por kernel gaussiano** (parâmetros ajustados via *sliders*).

## 3. Tecnologias e Bibliotecas Utilizadas

- **Python 3.7+** (ou superior)
- **OpenCV (cv2)** para processamento de imagens
- **Streamlit** para criação de interface web
- **NumPy** para manipulações em arrays
- **PIL** (Pillow) para carregamento de imagens

## 4. Estrutura de Pastas

```plaintext
├── AP1/
│   ├── app.py
│   ├── resumo_slides/
│   │   ├── 1.md
│   │   ├── 2.md
│   │   ├── 3.md
│   │   └── 4.md
│   └── images/
│       ├── AP1VisãoComputacional_TércioTeixeira.jpg
│       ├── AP1VisãoComputacional1_TércioTeixeira.jpg
│       └── AP1VisãoComputacional2_TércioTeixeira.jpg
├── ImageProcessing/
│   └── app.py
├── SkinDetection/
│   └── app.py
├── README.md
└── requirements.txt
```

## 5. Instruções de Uso

1. **Instale as dependências** (caso não as possua):  
   ```bash
   pip install -r requirements.txt
   ```

2. **Execute o comando** (na pasta em que se encontra o arquivo):  
   ```bash
   streamlit run app.py
   ```

## 6. Observações Importantes

- Prewitt não está disponível diretamente no OpenCV, então foi implementado via convolução manual utilizando kernels de Prewitt.
- Prewitt Compass foi implementado aplicando oito máscaras em diferentes orientações.
- Sobel e Sobel Compass ilustram a variação de orientações (mais simples com H/V).
- Sucessive Gaussians (Diferença de Gaussiana, ou Difference of Gaussian - DoG) faz a subtração de duas imagens com diferentes sigmas.
- Canny utiliza o método padrão do OpenCV.
- Foi adicionada a possibilidade de kernel gaussiano opcional, controlado por sliders no Streamlit.

## 7. Referências

- ALMEIDA, J. G. et al. *Digital Image Edge Detection: A Systematic Review*, 2019 19th International Conference on Advanced Robotics (ICAR), 2019. Disponível em: <https://ieeexplore.ieee.org/document/8854060>.  
- GONZALEZ, R. C.; WOODS, R. E. *Digital Image Processing*. 4. ed. New York: Pearson, 2018.  
- Documentação do [OpenCV](https://docs.opencv.org/master/)  
- Documentação do [Streamlit](https://docs.streamlit.io/)
- TEIXEIRA, Tércio. AP1VisãoComputacional_TércioTeixeira.jpg. [Fotografia]. 2025. Acervo pessoal. Disponível em: [Instagram](https://www.instagram.com/tercioteixeira1/?igsh=NTk2OTlpODJrMDZl#). Acesso em: 30 mar. 2025.
- TEIXEIRA, Tércio. AP1VisãoComputacional1_TércioTeixeira.jpg. [Fotografia]. 2025. Acervo pessoal. Disponível em: [Instagram](https://www.instagram.com/tercioteixeira1/?igsh=NTk2OTlpODJrMDZl#). Acesso em: 30 mar. 2025.
- TEIXEIRA, Tércio. AP1VisãoComputacional2_TércioTeixeira.jpg. [Fotografia]. 2025. Acervo pessoal. Disponível em: [Instagram](https://www.instagram.com/tercioteixeira1/?igsh=NTk2OTlpODJrMDZl#). Acesso em: 30 mar. 2025.
- TEIXEIRA, Tércio. AP1VisãoComputacional3_TércioTeixeira.jpg. [Fotografia]. 2025. Acervo pessoal. Disponível em: [Instagram](https://www.instagram.com/tercioteixeira1/?igsh=NTk2OTlpODJrMDZl#). Acesso em: 30 mar. 2025.
- TEIXEIRA, Tércio. AP1VisãoComputacional4_TércioTeixeira.jpg. [Fotografia]. 2025. Acervo pessoal. Disponível em: [Instagram](https://www.instagram.com/tercioteixeira1/?igsh=NTk2OTlpODJrMDZl#). Acesso em: 30 mar. 2025.
- TEIXEIRA, Tércio. AP1VisãoComputacional5_TércioTeixeira.jpg. [Fotografia]. 2025. Acervo pessoal. Disponível em: [Instagram](https://www.instagram.com/tercioteixeira1/?igsh=NTk2OTlpODJrMDZl#). Acesso em: 30 mar. 2025.
- TEIXEIRA, Tércio. AP1VisãoComputacional6_TércioTeixeira.jpg. [Fotografia]. 2025. Acervo pessoal. Disponível em: [Instagram](https://www.instagram.com/tercioteixeira1/?igsh=NTk2OTlpODJrMDZl#). Acesso em: 30 mar. 2025.
- TEIXEIRA, Tércio. AP1VisãoComputacional7_TércioTeixeira.jpg. [Fotografia]. 2025. Acervo pessoal. Disponível em: [Instagram](https://www.instagram.com/tercioteixeira1/?igsh=NTk2OTlpODJrMDZl#). Acesso em: 30 mar. 2025.
- TEIXEIRA, Tércio. AP1VisãoComputacional8_TércioTeixeira.jpg. [Fotografia]. 2025. Acervo pessoal. Disponível em: [Instagram](https://www.instagram.com/tercioteixeira1/?igsh=NTk2OTlpODJrMDZl#). Acesso em: 30 mar. 2025.
- TEIXEIRA, Tércio. AP1VisãoComputacional9_TércioTeixeira.jpg. [Fotografia]. 2025. Acervo pessoal. Disponível em: [Instagram](https://www.instagram.com/tercioteixeira1/?igsh=NTk2OTlpODJrMDZl#). Acesso em: 30 mar. 2025.
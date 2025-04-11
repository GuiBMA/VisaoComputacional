## 1. Imagem Digital
- Uma imagem contém uma quantidade discreta de elementos chamados pixels.
- Cada pixel possui um valor (intensidade para os casos de tons de cinza).

## 2. Representação de Imagens
- São normalmente discretas, representadas numa matriz regular de valores inteiros quantizados.

## 3. Imagem como Função
- Teoricamente, imagens são funções de R² a R M do brilho refletido de uma cena.
- f(x,y) fornece o valor de intensidade numa posição (x,y).
- O processo envolve as etapas de amostragem e quantização.

## 4. Amostragem
- Amostra a função 2D contínua para um conjunto de elementos discretos (pontos da imagem).
- Possui relação direta com a quantidade de nitidez que seja necessário na imagem coletada.

## 5. Quantização
- Define a dimensão de cor dos pontos da imagem, e.g., sinal em 3 bits.
- Define a dimensão de cores presentes em um ponto da imagem.
- Normalmente representada em bits.

## 6. Colorida x Tons de Cinza
- Tons de cinza: apenas Luminância (intensidade de luz - escala de cinza).
    - Representação simples.
    - Humanos podem entender.
- Coloridas: Luminância + Crominância.
    - Múltiplos canais (normalmente 3).
    - Processamento mais complexo.

## 7. Imagens RGB
- Red-Green-Blue: Mais comum.
- Canais correspondem aproximadamente às seguintes frequências:
    - R: 700nn
    - G: 546nn
    - B: 436nn

## 8. Imagens CMY
- Cyan-Magenta-Yellow: Cores secundárias baseadas na distância do branco.
- Toma como base o sistema subtrativo:
    - C = 255 - R
    - M = 255 - G
    - Y = 255 - B
- Usado em impressoras.

## 9. Imagens HSL
- Hue-Saturation-Luminance: Tom-Saturação-Luminância.
- Separa o que é cor do que é luminância num sistema cilíndrico:
    - Hue: 0..360
    - Luminância: 0..1
    - Saturation: 0..1

## 10. Imagens YCrCb
- Dedicado ao vídeo analógico.
- Y = Luminância.
- Cr = Crominância em vermelho em relação a um valor de referência.
- Cb = Crominância em azul em relação a um valor de referência.

## 11. Quantização Uniforme

## 12. Detecção de Pele
- Segmentação de pele com espaço de cor YCbCr e tracking de mão:
    - 85 ≤ Cb ≤ 135
    - 135 ≤ Cr ≤ 180
    - Y ≥ 80

## 13. Detecção de Olho Vermelho
- Detecção usando espaço de cor HSL:
    - (L >= 0.25) AND (S >= 0.4) AND (0.5 < L/S <1.5) AND (H <=14º OR H >=324º)

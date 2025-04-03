## 1. Filtragem
- Operações que visam extrair informações importantes da imagem:
    - Características: canto, bordas, agrupamentos.
    - Melhoramento: retirada de ruídos, aumento de contraste, etc.
- O processo de filtragem forma uma nova imagem, uma combinação dos pixels da imagem original.

## 2. Filtro da Média
- Um filtro da média pode ser definido como uma janela NxN que se move através de uma vizinhança de pixels:
    - (f∗h)[m,n] = 1/9 ⅀f[k,l] h[m-k,n-l]
    - ∗ representa a convolução de duas funções: f e h.
    - k varia de n-1 a n+1, l varia de m-1 a m+1.
    - m e n são as dimensões da imagem f.

## 3. Processo de Filtragem por Média
- Visualização do funcionamento de um filtro em imagens.

## 4. Convolução em Imagens
- Etapas desse processamento:
    - Posicionar um filtro h[n,m] num pixel (posição central).
    - Multiplicar cada valor dos pixels da imagem f[k,l] pelo valor do filtro h[n,m].
    - h[n,m] ∗ f[k,l].
    - Somar todos os elementos da multiplicação.
    - Repetir o processo para todos os pontos da imagem.

## 5. Filtro Gaussiano
- GaussianBlur(imgOriginal, imgSaida, Size(3,3),1,1):
    - Últimos dois parâmetros: desvio padrão em x e desvio padrão em y.
    - Caso queira o filtro em si, use a função getGaussianKernel.

## 6. Filtro da Mediana
- Redução de ruído impulsivo:
    - Ordenar os elementos do kernel em ordem crescente.
    - Mediana será os m elementos do centro desse conjunto ordenado.
    - salt(imgOriginal, 3000) %método para adicionar ruído impulsivo.
    - medianBlur(imgOriginal, imgSaida, 3) %remover ruído com o filtro.

## 7. Filtro Genérico
- Além dos filtros específicos para processamento da imagem, existe função para especificar um filtro genérico:
    - filter2d(imgOriginal, imgSaida, depth, kernel).

## 8. Bordas da Imagem
- Somente será computado pixels que tenham representantes completos dentro do filtro.
- Estratégias que podem ser adotadas:
    - Replicar borda.
    - Adicionar zeros (zero padding).

## 9. Filtros Morfológicos
- Conversor de imagens em tons de cinza para uma imagem binária para processamento.
- Operações como erosão, dilatação, abertura e fechamento:
    - Implementações dessas funções no OpenCV: cv.erode(), cv.dilate(), cv.morphologyEx().
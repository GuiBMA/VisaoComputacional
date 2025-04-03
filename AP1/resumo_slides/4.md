## 1. Importância dos Contornos
- Contornos são importantes para detectar descontinuidades repentinas nas imagens (mudanças).
- Limites e fronteiras (Edges) possuem a maioria da informação semântica presente numa imagem.
- Representação mais compacta do que pixels.
- Objetivo principal: Detectar bordas com a máxima precisão.

## 2. Origens da Detecção de Bordas
- Descontinuidade de:
    - Superfície
    - Profundidade
    - Superfície
    - Iluminação

## 3. Bordas
- Local na imagem onde aconteceu rápida mudança de tonalidades.
- Medida: Derivada.

## 4. Gradiente de uma Imagem

## 5. Efeitos Causados por Ruído
- O ruído faz com que bordas não sejam corretamente obtidas:
    - Pixels muito próximos possuem comportamentos aleatórios.
    - Mudanças súbitas de cor.
- Remover ruídos com filtros.

## 6. Implementação de Detectores de Borda
- Somente o gradiente pode gerar contornos grossos e que não refletem as bordas da imagem original.

## 7. Bom Detector de Bordas
- Precisa satisfazer três propriedades:
    - Detecção: minimizar falso positivos.
    - Localização: devem estar ou ser a própria borda.
    - Resposta atômica: o mínimo possível de contornos.

## 8. Opções de Detectores de Borda
- Roberts: primeira derivada, sensível a ruído, melhor aplicado em imagens binárias.
- Prewitt: primeira derivada, compass, derivadas parciais realizadas nas 8 direções básicas.
- Sobel: primeira derivada, compass (H/V).
- Canny: sucessivas Gaussianas, alta precisão na detecção de bordas.
- Laplaciano.

## 9. Thresholding
- Elimina valores intermediários e pode ser usado para transformar imagens em tons de cinza para imagens binárias.

## 10. Efeitos do Kernel Gaussiano
- Quanto maior o desvio, menor será a quantidade de detalhes capturada.

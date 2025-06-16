# Contador Automático de Medicamentos por Imagem

Este projeto é uma aplicação desenvolvida com Python e YOLOv8 que realiza a **detecção e contagem automática de medicamentos** (caixas, frascos e ampolas) em imagens, com uma interface gráfica interativa em Tkinter.

# Técnicas Aplicadas
- YOLOv8 (You Only Look Once)
Rede neural especializada em detecção de objetos em tempo real, usada aqui para identificar medicamentos em imagens.

- Aprendizado Supervisionado
Utilização de imagens rotuladas para treinar o modelo, com divisão em conjuntos de treino, validação e teste.

- Transfer Learning
Aproveitamento de um modelo pré-treinado (yolov8m.pt) para reduzir tempo de treinamento e melhorar desempenho com poucos dados.

- OpenCV para Pré e Pós-processamento
Conversão de cores (BGR → RGB), redimensionamento e renderização das detecções com bounding boxes.

- Interface Gráfica com Tkinter
GUI simples e eficiente, com carregamento de imagens, contagem automatizada, visualização e reset da contagem.

- Tratamento de Exceções
Detecção de falhas ao carregar ou processar arquivos inválidos, com feedback visual ao usuário.

# Funcionalidades
- Permite ao usuário escolher uma imagem do computador para análise.
- Detecta automaticamente os medicamentos presentes na imagem.
- Soma os medicamentos detectados em múltiplas imagens durante uma sessão.
- Exibe as caixas delimitadoras (bounding boxes) desenhadas nas imagens com os objetos detectados.
- Mostra uma versão ajustada da imagem com detecções diretamente na interface.
- Permite abrir a imagem detectada ampliada em uma nova janela.

# Tecnologias Utilizadas e Requisitos
- Python 3.11 +
- Tkinter 
- OpenCV 4.9.0
- Ultralytics YOLOv8 8.1.25
- Pillow 10.2.0

# Instalação
1. Clone o repositório
```
git clone https://github.com/seuusuario/repositorio.git
cd repositorio
```
2. Instale as dependências necessárias
```
$ pip install ultralytics==8.1.34
$ pip install opencv-python==4.9.0.80
$ pip install Pillow==10.2.0
```
3. Como executar

Após instalar as dependências, execute o seguinte comando:

```
python contador_medicamentos.py
```
> Certifique-se de que o arquivo best.pt (modelo treinado) esteja corretamente localizado no caminho definido no código. Por padrão, ele está na pasta train15.















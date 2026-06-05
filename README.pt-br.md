# 🖐 HandsDetectionProject

🇺🇸 [English version](README.md)

Controle o computador usando apenas gestos das mãos — sem mouse. Este projeto usa visão computacional para detectar os pontos de referência da mão em tempo real e traduzi-los em movimentos do cursor, cliques e scroll.

> Desenvolvido com MediaPipe, OpenCV e PyAutoGUI.

---

<!-- Adicione um gif de demonstração aqui depois de gravar -->
<!-- ![Demo](assets/demo.gif) -->

---

## ✨ Funcionalidades

- **Controle do mouse** — move o cursor com o dedo indicador
- **Clique** — gesto de pinça (polegar + indicador)
- **Scroll** — levanta indicador e médio, move a mão para cima/baixo
- **Movimento suavizado** — média móvel exponencial (EMA) para reduzir o tremor do cursor
- **Congelamento do cursor** — o cursor trava enquanto o gesto de pinça está se formando, evitando cliques acidentais
- **HUD na câmera** — indicador do modo atual e barra de progresso da pinça em tempo real

---

## 🗂 Estrutura do Projeto

```
HandsDetectionProject/
├── main.py                 # Ponto de entrada
├── detector_maos.py        # Lógica de detecção e desenho
├── controlador_mouse.py    # Lógica de controle do mouse
├── requirements.txt
├── README.md
├── README.pt-br.md
├── models/
│    └── hand_landmarker.task   # Baixado automaticamente na primeira execução
└── assets/
     ├── demo.gif
     └── screenshot.png
```

---

## 🚀 Como Rodar

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/HandsDetectionProject.git
cd HandsDetectionProject
```

### 2. Crie e ative o ambiente virtual
```bash
python -m venv myvenv

# Windows
myvenv\Scripts\activate

# macOS/Linux
source myvenv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Execute
```bash
python main.py
```

> O modelo de detecção do MediaPipe (~9MB) será baixado automaticamente na primeira execução.

---

## 🤚 Referência de Gestos

| Gesto | Ação |
|---|---|
| Indicador levantado | Mover cursor |
| Pinça polegar + indicador | Clique esquerdo |
| Indicador + médio levantados | Modo scroll |
| Mão para cima (modo scroll) | Scroll para cima |
| Mão para baixo (modo scroll) | Scroll para baixo |

---

## ⚙️ Configuração

Você pode ajustar os parâmetros do controlador em `main.py`:

```python
controlador = ControladorMouse(
    largura_cam,
    altura_cam,
    margem=100,       # Margem da zona ativa em pixels (exclui bordas da câmera)
    limiar_pinca=40,  # Distância limite da pinça em pixels
)
```

E o fator de suavização em `controlador_mouse.py`:

```python
self.alpha = 0.17  # Menor = mais suave mas mais lento (range: 0.1 – 0.4)
```

---

## 🛠 Tecnologias

- [MediaPipe](https://mediapipe.dev/) — detecção de landmarks da mão
- [OpenCV](https://opencv.org/) — captura de vídeo e desenho na imagem
- [PyAutoGUI](https://pyautogui.readthedocs.io/) — controle do mouse

---

## 📄 Licença

Licença MIT. Sinta-se livre para usar, modificar e distribuir.

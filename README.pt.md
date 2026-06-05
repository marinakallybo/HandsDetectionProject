# 🖐 HandsDetectionProject

🇺🇸 [English version](README.md)

Controle o computador usando apenas gestos das mãos — sem mouse. Este projeto usa visão computacional para detectar os pontos de referência da mão em tempo real e traduzi-los em movimentos do cursor, cliques, scroll e até desenho.

> Desenvolvido com MediaPipe, OpenCV e PyAutoGUI.

---

<!-- Adicione um gif de demonstração aqui depois de gravar -->
<!-- ![Demo](assets/demo.gif) -->

---

## ✨ Funcionalidades

- **Controle do mouse** — move o cursor com o dedo indicador
- **Clique** — gesto de pinça (polegar + indicador)
- **Scroll** — levanta indicador e médio, move a mão para cima/baixo
- **Modo pintura** — alterna com `P`; levanta o indicador para desenhar, pinça para clicar
- **Movimento suavizado** — média móvel exponencial (EMA) para reduzir o tremor do cursor
- **Congelamento do cursor** — o cursor trava enquanto o gesto de pinça está se formando, evitando cliques acidentais
- **HUD na câmera** — indicador do modo atual e barra de progresso da pinça em tempo real

---

## 🗂 Estrutura do Projeto

```
HandsDetectionProject/
├── main.py                 # Ponto de entrada e loop principal
├── detector_maos.py        # Detecção de mãos, desenho de landmarks e HUD
├── controlador_mouse.py    # Controle do mouse, scroll, clique e pintura
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

| Gesto | Modo | Ação |
|---|---|---|
| Indicador levantado | Mouse | Mover cursor |
| Pinça polegar + indicador | Mouse | Clique esquerdo |
| Indicador + médio levantados | Mouse | Modo scroll |
| Mão para cima (modo scroll) | Mouse | Scroll para cima |
| Mão para baixo (modo scroll) | Mouse | Scroll para baixo |
| Pressionar `P` | — | Alternar modo pintura |
| Indicador levantado | Pintura | Desenhar |
| Pinça polegar + indicador | Pintura | Clique esquerdo |
| Abaixar indicador | Pintura | Parar de desenhar |

---

## ⚙️ Configuração

Você pode ajustar os parâmetros do controlador em `main.py`:

```python
controlador = ControladorMouse(
    largura_cam,
    altura_cam,
    margem=100,       # Margem da zona ativa em pixels (exclui bordas da câmera)
    limiar_pinca=47,  # Distância limite da pinça em pixels
)
```

E o fator de suavização em `controlador_mouse.py`:

```python
self.alpha = 0.17   # Modo mouse: menor = mais suave mas mais lento (range: 0.1 – 0.4)
self.alpha = 0.55   # Modo pintura: maior = mais responsivo para desenhar
```

---

## 🛠 Tecnologias

- [MediaPipe](https://mediapipe.dev/) — detecção de landmarks da mão
- [OpenCV](https://opencv.org/) — captura de vídeo e desenho na imagem
- [PyAutoGUI](https://pyautogui.readthedocs.io/) — controle do mouse

---

## 📄 Licença

Licença MIT. Sinta-se livre para usar, modificar e distribuir.

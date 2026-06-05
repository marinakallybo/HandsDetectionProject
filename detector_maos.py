import cv2 ## Importa a biblioteca OpenCV para processamento de imagens e vídeo
import mediapipe as mp ## Importa a biblioteca MediaPipe para detecção de mãos e outros recursos de visão computacional
from mediapipe.tasks import python ## Entra na sub-biblioteca de tarefas (tasks.python) do MediaPipe para usar modelos pré-treinados
from mediapipe.tasks.python import vision ## Entra em media.taks.python e pega somente o vision, que é onde está o modelo de detecção de mãos
from mediapipe.framework.formats import landmark_pb2 ## Entra em mediapipe.framework.formats e pega o módulo landmark_pb2, que é usado para lidar com os pontos de referência das mãos
import urllib.request ## Biblioteca nativa do Python para fazer requisições de internet. Usada aqui para baixar o modelo de detecção de mãos se ele não estiver presente no sistema.
import os ## Biblioteca nativa do Python para interagir com o sistema operacional, usada aqui para verificar se o modelo de detecção de mãos já existe no sistema antes de baixá-lo.
import math
from controlador_mouse import ControladorMouse

## Essa função abaixo é responsável por: Verificar se o modelo já existe -> Se não existir -> Baixar o modelo automaticamente -> Retornar o caminho do arquivo
def baixar_modelo(): 
    """Baixa o modelo do hand landmarker se não existir"""
    url = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task" ## Guarda o endereço do modelo treinado
    caminho = "models/hand_landmarker.task" ## hand_landmarker.task - Modelo do Google MediaPipe já treinado
    ## caminho - Local onde o arquivo vai ficar no computador
    if not os.path.exists(caminho): ## Caso o arquivo não exista no caminho:
        print("Baixando modelo...")
        urllib.request.urlretrieve(url, caminho) ## Baixa o modelo do endereço e salva no caminho
        print("Modelo baixado!")
    return caminho


class DetectorMaos:
    """Classe responsável pela detecção das mãos"""
    
    NOMES_DEDOS = {
        4: "Polegar", 8: "Indicador", 12: "Medio", 16: "Anelar", 20: "Minimo"
    }
    
    ## __init__ is a special built-in method used as an initializer to set up a new object's attributes when a class is instantiated.
    def __init__(self, max_maos=2, deteccao_confianca=0.5,
                 rastreio_confianca=0.5, cor_pontos=(0, 0, 255), cor_conexoes=(255, 255, 255)):

        """
        Função responsável por inicializar a classe.
        :param max_maos: Quantidade máxima de mãos para serem detectadas.
        :param deteccao_confianca: Percentual da taxa de detecção da mão. Se for menos do que este limite,
        a detecção não ocorre.
        :param rastreio_confianca: Percentual da taxa de rastreio dos pontos da mão. Se for menos que esta
        limite, o rastreio dos pontos não é realizado.
        :param cor_pontos: Cor dos pontos.
        :param cor_conexoes: Cor das conexões.
        """

        # --- Inicializar os parâmetros --- #
        self.cor_pontos = cor_pontos 
        self.cor_conexoes = cor_conexoes
        self.resultado = None
        self.frame_num = 0 ## Serve como contador, pois estamos usando o vision.RunningMode.VIDEO e precisamos passar o número do frame para o método detect_for_video() do MediaPipe.

        # --- Baixar e carregar o modelo --- #
        caminho_modelo = baixar_modelo()

        # --- Inicializar o detector com a nova API --- #
        base_options = python.BaseOptions(model_asset_path=caminho_modelo) ## Aqui estamos dizendo qual modelo queremos usar
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            num_hands=max_maos,
            min_hand_detection_confidence=deteccao_confianca,
            min_tracking_confidence=rastreio_confianca,
            running_mode=vision.RunningMode.VIDEO
        ) ## Aqui estamos configurando as opções do detector, como o número máximo de mãos, os limiares de confiança para detecção e rastreamento, e o modo de execução (neste caso, vídeo).
        self.detector = vision.HandLandmarker.create_from_options(options) ## Onde é criado o detector de mãos

        # --- Inicializar os módulos de detecção das mãos --- #
        self.maos_mp = mp.solutions.hands ## Aqui estamos inicializando o módulo de detecção de mãos do MediaPipe, que contém as conexões entre os pontos das mãos e outras funcionalidades relacionadas à detecção de mãos.

        # --- Função para desenhar os pontos nas mãos --- #
        self.desenho_mp = mp.solutions.drawing_utils ## Aqui pegamos ferramentas de desenho


    def encontrar_maos(self, imagem, desenho=True):
        """
        Função responsável por detectar a(s) mão(s).
        :param imagem: Imagem capturada.
        :param desenho: Desenhar os pontos e as conexões na(s) mão(s)
        :return: Retorna a imagem com a detecção.
        """

        # --- Converter a imagem de BGR para RGB --- #
        imagem_rgb = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
        ## Isso serve porque o OpenCV lê imagens como BGR (Blue, Green, Red), enquanto o Media Pipe
        ## espera as imagens no formato RGB (Red, Green, Bluee)

        # --- Passar a imagem convertida para o detector --- #
        mp_imagem = mp.Image(image_format=mp.ImageFormat.SRGB, data=imagem_rgb) ## Aqui estamos convertendo a imagem para o formato que o MediaPipe espera, que é um objeto mp.Image com o formato de cor SRGB (Red, Green, Blue) e os dados da imagem RGB. Isso é necessário para que o detector possa processar a imagem corretamente.
        self.frame_num += 1
        self.resultado = self.detector.detect_for_video(mp_imagem, self.frame_num) ## Passando a imagem convertida para o método detect_for_video() do detector, junto com o número do frame. O resultado da detecção é armazenado na variável self.resultado, que conterá as informações sobre as mãos detectadas, como os pontos de referência e as conexões entre eles.

        # --- Verificar se alguma mão foi detectada --- #
        if desenho and self.resultado.hand_landmarks: ## Se: desenho == True & Há lanfmarks detectados, então: desenhar os pontos e conexões na mão
            for landmarks in self.resultado.hand_landmarks:

                # Converter para o formato do drawing_utils
                hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
                hand_landmarks_proto.landmark.extend([
                    landmark_pb2.NormalizedLandmark(
                        x=lm.x, 
                        y=lm.y, 
                        z=lm.z
                    )
                    for lm in landmarks
                ])

                # --- Desenhar os pontos e conexões na mão --- #
                self.desenho_mp.draw_landmarks(
                    imagem,
                    hand_landmarks_proto,
                    self.maos_mp.HAND_CONNECTIONS,
                    self.desenho_mp.DrawingSpec(color=self.cor_pontos),
                    self.desenho_mp.DrawingSpec(color=self.cor_conexoes)
                )

        # retorna imagem
        return imagem

    
    def encontrar_posicoes(self, imagem):
        """
        Retorna as posições dos landmarks em pixels.
        :param imagem: Imagem capturada (para pegar largura e altura).
        :return: Lista de dicts com id e coordenadas (x, y) em pixels, ou [] se não houver mão.
        """
        posicoes = []

        if self.resultado and self.resultado.hand_landmarks:
            altura, largura, _ = imagem.shape  # Pega dimensões reais da imagem

            for landmarks in self.resultado.hand_landmarks:
                for id, lm in enumerate(landmarks):
                    # lm.x e lm.y são valores de 0.0 a 1.0 — multiplicamos pelas dimensões reais
                    cx = int(lm.x * largura)
                    cy = int(lm.y * altura)
                    posicoes.append({'id': id, 'x': cx, 'y': cy})

        return posicoes
    
    def calcular_distancia(self, posicoes, id1, id2):
        """Retorna a distância em pixels entre dois landmarks."""
        p1 = next((p for p in posicoes if p['id'] == id1), None)
        p2 = next((p for p in posicoes if p['id'] == id2), None)
        if p1 and p2:
            return math.sqrt((p1['x'] - p2['x'])**2 + (p1['y'] - p2['y'])**2)
        return None

    def desenhar_nomes_dedos(self, imagem, posicoes):
        """Escreve o nome de cada dedo na ponta correspondente."""
        for id, nome in self.NOMES_DEDOS.items():
            ponto = next((p for p in posicoes if p['id'] == id), None)
            if ponto:
                cv2.putText(imagem, nome, (ponto['x'] - 30, ponto['y'] - 15),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        return imagem
    
    def desenhar_hud(self, imagem, modo, distancia=None, limiar=47):
        """
        Desenha o HUD na câmera com o modo atual e informações úteis.
        :param modo: String com o modo atual ('mouse' ou 'scroll')
        :param distancia: Distância atual entre landmarks 4 e 8 (opcional)
        :param limiar: Limiar para a distância da pinça (opcional)
        """
        altura, largura, _ = imagem.shape

        # --- Fundo semi-transparente no topo --- #
        overlay = imagem.copy()
        cv2.rectangle(overlay, (0, 0), (largura, 50), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.4, imagem, 0.6, 0, imagem)  # transparência

        # --- Modo atual --- #
        if modo == 'scroll':
            texto_modo = '[ SCROLL ]'
            cor_modo = (0, 255, 180)   # verde água
        elif modo == 'pinca':
            texto_modo = '[ CLIQUE ]'
            cor_modo = (0, 255, 0)     # verde
        else:
            texto_modo = '[ MOUSE ]'
            cor_modo = (255, 255, 255) # branco

        cv2.putText(imagem, texto_modo, (15, 33),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, cor_modo, 2)

        # --- Distância da pinça (barra de progresso) --- #
        if distancia is not None:
            limiar = limiar
            barra_x = largura - 220
            cv2.putText(imagem, 'PINCA', (barra_x, 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (180, 180, 180), 1)

            # fundo da barra
            cv2.rectangle(imagem, (barra_x, 28), (barra_x + 150, 40), (60, 60, 60), -1)

            # preenchimento — quanto menor a distância, mais cheia
            progresso = max(0.0, min(1.0, 1 - (distancia / (limiar * 2))))
            fill = int(150 * progresso)
            cor_barra = (0, 255, 0) if distancia < limiar else (100, 200, 255)
            cv2.rectangle(imagem, (barra_x, 28), (barra_x + fill, 40), cor_barra, -1)

        # --- Instrução de saída --- #
        cv2.putText(imagem, 'Q: sair', (largura - 75, altura - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (120, 120, 120), 1)

        return imagem
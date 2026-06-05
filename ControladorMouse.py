import pyautogui
import time
from collections import deque

pyautogui.FAILSAFE = False  # desativa a trava de mover para o canto

class ControladorMouse:
    """Classe responsável por controlar o mouse com os gestos da mão."""

    def __init__(self, largura_cam, altura_cam, margem=100, limiar_pinca=40):
        """
        :param largura_cam: Largura do frame da câmera em pixels.
        :param altura_cam: Altura do frame da câmera em pixels.
        :param margem: Zona ativa da câmera (exclui as bordas para mais precisão).
        :param limiar_pinca: Distância em px abaixo da qual considera pinça fechada.
        """
        self.larg_cam = largura_cam
        self.alt_cam = altura_cam
        self.margem = margem
        self.limiar_pinca = limiar_pinca
        
        self.larg_tela, self.alt_tela = pyautogui.size()  # resolução real da tela

        self.clicando = False       # controle de estado do clique
        self.ultimo_clique = 0      # evita cliques duplos acidentais

        # --- Smoothing: guarda as últimas N posições --- #
        self.x_suave = None
        self.y_suave = None
        self.alpha = 0.17 # fator de suavização (0.2 = 20% da nova posição, 80% da antiga)

        # --- Congelamento durante pinça --- #
        self.cursor_congelado = False
        self.pos_congelada = (0, 0)  # posição onde o cursor fica congelado



    def mover(self, posicoes, distancia):
        """
        Move o cursor baseado na posição do landmark 8 (ponta do indicador).
        :param posicoes: Lista de dicts retornada por encontrar_posicoes().
        :param distancia: Distância entre os landmarks 4 e 8.
        """
        p = next((p for p in posicoes if p['id'] == 8), None)
        if not p:
            return
        
        # Congela o cursor quando a pinça está fechada
        zona_congelamento = self.limiar_pinca * 1.4 # começa a congelar cerca de 40% antes do limiar de clique
        if distancia and distancia < zona_congelamento:
            if not self.cursor_congelado:
                self.cursor_congelado = True
                self.pos_congelada = pyautogui.position()  # salva posição atual do cursor
            pyautogui.moveTo(*self.pos_congelada)  # mantém o cursor congelado
            return
        
        self.cursor_congelado = False  # descongela quando a pinça abre

        # Limita o ponto dentro da zona ativa (exclui bordas)
        x_cam = max(self.margem, min(p['x'], self.larg_cam - self.margem))
        y_cam = max(self.margem, min(p['y'], self.alt_cam - self.margem))

        # Mapeia zona ativa da câmera para a tela inteira
        x_tela = int((x_cam - self.margem) /
                     (self.larg_cam - 2 * self.margem) * self.larg_tela)
        y_tela = int((y_cam - self.margem) /
                     (self.alt_cam - 2 * self.margem) * self.alt_tela)

        # Smoothing: Aplica suavização à posição
        if self.x_suave is None:
            self.x_suave = x_tela  # inicializa na primeira posição
            self.y_suave = y_tela
        else:
            self.x_suave = int(self.alpha * x_tela + (1 - self.alpha) * self.x_suave)
            self.y_suave = int(self.alpha * y_tela + (1 - self.alpha) * self.y_suave)

        pyautogui.moveTo(self.x_suave, self.y_suave)

    def verificar_clique(self, distancia):
        """
        Clica se a pinça estiver fechada. Evita cliques repetidos.
        :param distancia: Valor retornado por calcular_distancia(4, 8).
        """
        agora = time.time()

        if distancia and distancia < self.limiar_pinca:
            if not self.clicando and (agora - self.ultimo_clique) > 0.5:
                pyautogui.click()
                self.clicando = True
                self.ultimo_clique = agora
        else:
            self.clicando = False  # reseta quando a pinça abre

    def verificar_scroll(self, posicoes):
        """
        Scrolla quando indicador e médio estão levantados.
        Usa a posição Y do landmark 8 para determinar direção e velocidade.
        """
        # Pega os pontos necessários
        p8  = next((p for p in posicoes if p['id'] == 8),  None)  # ponta indicador
        p6  = next((p for p in posicoes if p['id'] == 6),  None)  # base indicador
        p12 = next((p for p in posicoes if p['id'] == 12), None)  # ponta médio
        p10 = next((p for p in posicoes if p['id'] == 10), None)  # base médio

        if not all([p8, p6, p12, p10]):
            return False

        indicador_levantado = p8['y'] < p6['y']   # ponta acima da base = levantado
        medio_levantado     = p12['y'] < p10['y']

        if indicador_levantado and medio_levantado:
            # Usa a posição Y do indicador para definir velocidade e direção
            # Centro da câmera = zona morta, acima = scroll up, abaixo = scroll down
            centro = self.alt_cam // 2
            distancia_centro = p8['y'] - centro  # positivo = abaixo, negativo = acima

            zona_morta = 20  # px de zona morta no centro para evitar scroll acidental

            if abs(distancia_centro) > zona_morta:
                velocidade = int((abs(distancia_centro) - zona_morta) / 4)  # 0 a ~4
                velocidade = max(1, min(velocidade, 120))  # limita entre 1 e 5

                if distancia_centro < 0:
                    pyautogui.scroll(velocidade)   # scroll up
                else:
                    pyautogui.scroll(-velocidade)  # scroll down

            return True  # está em modo scroll

        return False  # não está em modo scroll
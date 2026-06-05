import cv2
from detector_maos import DetectorMaos
from controlador_mouse import ControladorMouse


def main():
    # capturar o vídeo pela webcam
    cap = cv2.VideoCapture(0)

    # --- Instanciar a classe do detector --- #
    detector = DetectorMaos()

    largura_cam = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    altura_cam = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    controlador = ControladorMouse(largura_cam, altura_cam)

    # realizar a captura
    while True:
        # obtenção da imagem
        _, imagem = cap.read() ## Aqui estamos lendo um frame do vídeo capturado pela webcam. A função cap.read() retorna dois valores: o primeiro é um booleano que indica se a leitura foi bem-sucedida (True ou False), e o segundo é a imagem capturada (armazenada na variável imagem). O caractere de sublinhado (_) é usado para ignorar o valor booleano, já que não precisamos dele neste caso.

        # inverter a imagem
        imagem = cv2.flip(imagem, 1)

        # --- Realizar a detecção das mãos --- #
        imagem = detector.encontrar_maos(imagem)
        posicoes = detector.encontrar_posicoes(imagem)

        if posicoes:
            imagem = detector.desenhar_nomes_dedos(imagem, posicoes)
            distancia = detector.calcular_distancia(posicoes, 4, 8)
            
            em_scroll = controlador.verificar_scroll(posicoes)  # checa scroll primeiro
            
            if not em_scroll:  # só move o mouse se não estiver scrollando
                controlador.mover(posicoes, distancia)
                controlador.verificar_clique(distancia)
                
             # --- Determina o modo para o HUD --- #
            if em_scroll:
                modo = 'scroll'
            elif distancia and distancia < 47:
                modo = 'pinca'
            else:
                modo = 'mouse'

            imagem = detector.desenhar_hud(imagem, modo, distancia)

        else:
            # Mesmo sem mão detectada, mostra o HUD básico
            imagem = detector.desenhar_hud(imagem, 'mouse')
    
        # mostrar a imagem de captura
        cv2.imshow('Captura', imagem)

        # tempo de att da captura — pressione 'q' para sair
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        
    cap.release() ## Libera a captura de vídeo, ou seja, libera a webcam para que outros programas possam usá-la e para encerrar a captura de forma adequada.
    cv2.destroyAllWindows() ## Libera a captura de vídeo e fecha todas as janelas do OpenCV para encerrar o programa de forma limpa.


if __name__ == '__main__': ## Verifica se o script está sendo executado diretamente (em vez de importado como um módulo) e, se for o caso, chama a função main() para iniciar a execução do programa.
    main()
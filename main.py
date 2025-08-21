import cv2
import mediapipe as mp
import os
import csv

# Inicializa o módulo de detecção de mãos do Mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

# Captura de vídeo da webcam
cap = cv2.VideoCapture(0)

# Pasta principal onde estão armazenados os arquivos CSV de sinais
pasta_principal = 'C:/Users/Steffany/OneDrive/Área de Trabalho/senai_projetoia'

# Variáveis para rastrear coordenadas e etapas
coordenadas_mao_em_tempo_real = []
nome_arquivo_anterior = ""
etapas_completas = []

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    # Detecta mãos no frame atual
    results = hands.process(frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            coordenadas_mao = []
            # Extrai coordenadas (x, y) de cada ponto da mão
            for landmark in hand_landmarks.landmark:
                coordenadas_mao.extend([landmark.x, landmark.y])
            coordenadas_mao_em_tempo_real = coordenadas_mao

            # Desenha a mão e conexões na tela
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Percorre as pastas dentro da pasta principal
            for pasta_sinal in os.listdir(pasta_principal):
                if os.path.isdir(os.path.join(pasta_principal, pasta_sinal)):
                    # Percorre os arquivos CSV dentro da pasta
                    for arquivo_csv in os.listdir(os.path.join(pasta_principal, pasta_sinal)):
                        if arquivo_csv.endswith(".csv"):
                            nome_arquivo = os.path.splitext(arquivo_csv)[0].split('.')[0]  # Pega apenas o nome base
                            caminho_csv = os.path.join(pasta_principal, pasta_sinal, arquivo_csv)

                            # Lê o arquivo CSV
                            with open(caminho_csv, newline='') as csvfile:
                                reader = csv.reader(csvfile)
                                next(reader)  # Pula a linha de cabeçalho
                                correspondencia_encontrada = True
                                etapas_completas = []  # Limpa as etapas anteriores

                                # Conta quantas etapas existem no CSV
                                numero_de_etapas = sum(1 for row in reader)

                                # Retorna para o início do arquivo (depois do cabeçalho)
                                csvfile.seek(0)
                                next(reader)

                                # Percorre cada etapa do CSV
                                for row in reader:
                                    etapa = float(row[0])
                                    sinal = float(row[1])

                                    # Compara os pontos da mão em tempo real com os pontos do CSV
                                    for ponto_idx in range(0, 20):
                                        x_csv = float(row[ponto_idx * 2 + 2])
                                        y_csv = float(row[ponto_idx * 2 + 3])

                                        x_real = coordenadas_mao_em_tempo_real[ponto_idx * 2]
                                        y_real = coordenadas_mao_em_tempo_real[ponto_idx * 2 + 1]

                                        # Calcula a "distância" entre os pontos (critério de similaridade)
                                        distancia_entre_pontos = ((x_csv - x_real) * 2 + (y_csv - y_real) * 2) ** 0.5

                                        # Define os critérios com base no número de etapas
                                        if numero_de_etapas == 1:  
                                            # Critério para apenas 1 etapa
                                            distancia_maxima_possivel = 1.0
                                            limite_correspondencia_percentual = 0.85
                                        else:  
                                            # Critério para mais de 1 etapa
                                            distancia_maxima_possivel = 1.0
                                            limite_correspondencia_percentual = 0.75

                                        # Calcula a porcentagem de correspondência
                                        correspondencia_percentual = 1 - (distancia_entre_pontos / distancia_maxima_possivel)

                                        if correspondencia_percentual < limite_correspondencia_percentual:
                                            correspondencia_encontrada = False
                                            break
                                    etapas_completas.append(correspondencia_encontrada)
                                
                                # Se todas as etapas foram correspondidas e não é repetição do último arquivo
                                if all(etapas_completas) and nome_arquivo != nome_arquivo_anterior:
                                    print(nome_arquivo)
                                    nome_arquivo_anterior = nome_arquivo

    # Exibe a janela com a mão detectada
    cv2.imshow("Hand Tracking", frame)

    # Pressione ESC para sair
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Libera a câmera e fecha janelas
cap.release()
cv2.destroyAllWindows()

import cv2
import mediapipe as mp
import os
import csv

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

pasta_principal = 'C:/Users/Steffany/OneDrive/Área de Trabalho/senai_projetoia'

# Initialize variables to track real-time coordinates
coordenadas_mao_em_tempo_real = []
nome_arquivo_anterior = ""
etapas_completas = []

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    # Detect hands
    results = hands.process(frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            coordenadas_mao = []
            for landmark in hand_landmarks.landmark:
                coordenadas_mao.extend([landmark.x, landmark.y])
            coordenadas_mao_em_tempo_real = coordenadas_mao

            # Draw hand landmarks with numbers
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Consult CSV files in folders within the main folder
            for pasta_sinal in os.listdir(pasta_principal):
                if os.path.isdir(os.path.join(pasta_principal, pasta_sinal)):
                    for arquivo_csv in os.listdir(os.path.join(pasta_principal, pasta_sinal)):
                        if arquivo_csv.endswith(".csv"):
                            nome_arquivo = os.path.splitext(arquivo_csv)[0].split('.')[0]  # Get only the base name
                            caminho_csv = os.path.join(pasta_principal, pasta_sinal, arquivo_csv)

                            # Read the CSV file
                            with open(caminho_csv, newline='') as csvfile:
                                reader = csv.reader(csvfile)
                                next(reader)  # Skip the header row
                                correspondencia_encontrada = True
                                etapas_completas = []  # Limpar etapas completas

                                # Contar o número de etapas no arquivo CSV
                                numero_de_etapas = sum(1 for row in reader)

                                # Volte para o início do arquivo para a verificação
                                csvfile.seek(0)
                                next(reader)  # Skip the header row

                                for row in reader:
                                    etapa = float(row[0])
                                    sinal = float(row[1])

                                    # Compare real-time hand coordinates with CSV file
                                    for ponto_idx in range(0, 20):
                                        x_csv = float(row[ponto_idx * 2 + 2])
                                        y_csv = float(row[ponto_idx * 2 + 3])

                                        x_real = coordenadas_mao_em_tempo_real[ponto_idx * 2]
                                        y_real = coordenadas_mao_em_tempo_real[ponto_idx * 2 + 1]

                                        # Calculate the distance between points
                                        distancia_entre_pontos = ((x_csv - x_real) * 2 + (y_csv - y_real) * 2) ** 0.5

                                        # Defina os critérios com base no número de etapas
                                        if numero_de_etapas == 1:  # Um critério para 1 etapa
                                            distancia_maxima_possivel = 1.0
                                            limite_correspondencia_percentual = 0.85
                                        else:  # Outro critério para mais de 1 etapa
                                            distancia_maxima_possivel = 1.0
                                            limite_correspondencia_percentual = 0.75

                                        # Calculate the percentage match
                                        correspondencia_percentual = 1 - (distancia_entre_pontos / distancia_maxima_possivel)

                                        if correspondencia_percentual < limite_correspondencia_percentual:
                                            correspondencia_encontrada = False
                                            break
                                    etapas_completas.append(correspondencia_encontrada)
                                
                                # Verifique se todas as etapas foram correspondidas antes de imprimir
                                if all(etapas_completas) and nome_arquivo != nome_arquivo_anterior:
                                    print(nome_arquivo)
                                    nome_arquivo_anterior = nome_arquivo

    cv2.imshow("Hand Tracking", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # Press Esc to exit
        break

cap.release()
cv2.destroyAllWindows()
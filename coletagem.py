import cv2
import mediapipe as mp
import csv

# Inicializa o módulo de detecção de mãos do Mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

# Pergunta ao usuário quantas etapas o sinal terá e o nome do sinal
numero_etapas = int(input("Quantas etapas o sinal terá? "))
nome_sinal = input("Qual é o nome do sinal? ")

# Nome do arquivo CSV onde os dados serão salvos
nome_arquivo_csv = f"{nome_sinal}.csv"

# Cabeçalhos básicos do CSV
fieldnames = ["Etapa", "Sinal"]

# Cria o arquivo CSV com cabeçalho inicial
with open(nome_arquivo_csv, mode='w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Captura das etapas
    for etapa in range(1, numero_etapas + 1):
        cap = cv2.VideoCapture(0)  # Abre a webcam
        coordenadas_etapa = []

        input(f"Pressione Enter para iniciar a Etapa {etapa}...")

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Processa a imagem da mão
            results = hands.process(frame)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    coordenadas_mao = []
                    # Percorre todos os pontos da mão detectada
                    for idx, landmark in enumerate(hand_landmarks.landmark):
                        coordenadas_mao.extend([landmark.x, landmark.y])  # Salva coordenadas normalizadas

                        # Desenha pontos e índices na tela
                        h, w, c = frame.shape
                        cx, cy = int(landmark.x * w), int(landmark.y * h)
                        cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)
                        cv2.putText(frame, str(idx), (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

                    # Salva a lista de coordenadas da etapa
                    coordenadas_etapa.append(coordenadas_mao)

            # Mostra a captura da mão
            cv2.imshow("Hand Tracking", frame)

            # Pressione Enter para encerrar a captura da etapa
            if cv2.waitKey(1) == 13:
                break

        # Número de pontos detectados na mão
        num_pontos = len(coordenadas_etapa[0]) // 2

        # Define os cabeçalhos com os pontos da mão (X e Y de cada ponto)
        fieldnames = ["Etapa", "Sinal"]
        for i in range(1, num_pontos + 1):
            fieldnames.extend([f"Ponto{i}_X", f"Ponto{i}_Y"])

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # "Achata" a lista de coordenadas em uma linha única
        coordenadas_etapa_flattened = [item for sublist in coordenadas_etapa for item in sublist]

        # Monta o dicionário com etapa, sinal e coordenadas
        coordenada_dict = {"Etapa": etapa, "Sinal": nome_sinal}
        coordenada_dict.update({fieldnames[i]: coordenadas_etapa_flattened[i] for i in range(len(fieldnames) - 2)})

        # Salva os dados no CSV
        writer.writerow(coordenada_dict)

        print(f"Coordenadas da Etapa {etapa} salvas em {nome_arquivo_csv}")

        # Fecha a câmera e a janela da etapa
        cap.release()
        cv2.destroyAllWindows()

import cv2
import mediapipe as mp
import csv

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

numero_etapas = int(input("Quantas etapas o sinal terá? "))
nome_sinal = input("Qual é o nome do sinal? ")

nome_arquivo_csv = f"{nome_sinal}.csv"

fieldnames = ["Etapa", "Sinal"]

with open(nome_arquivo_csv, mode='w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for etapa in range(1, numero_etapas + 1):
        cap = cv2.VideoCapture(0)
        coordenadas_etapa = []

        input(f"Pressione Enter para iniciar a Etapa {etapa}...")

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            results = hands.process(frame)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    coordenadas_mao = []
                    for idx, landmark in enumerate(hand_landmarks.landmark):
                        coordenadas_mao.extend([landmark.x, landmark.y])
                        h, w, c = frame.shape
                        cx, cy = int(landmark.x * w), int(landmark.y * h)
                        cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)
                        cv2.putText(frame, str(idx), (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                    coordenadas_etapa.append(coordenadas_mao)

            cv2.imshow("Hand Tracking", frame)

            if cv2.waitKey(1) == 13:
                break

        num_pontos = len(coordenadas_etapa[0]) // 2
        fieldnames = ["Etapa", "Sinal"]
        for i in range(1, num_pontos + 1):
            fieldnames.extend([f"Ponto{i}_X", f"Ponto{i}_Y"])

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        coordenadas_etapa_flattened = [item for sublist in coordenadas_etapa for item in sublist]

        coordenada_dict = {"Etapa": etapa, "Sinal": nome_sinal}
        coordenada_dict.update({fieldnames[i]: coordenadas_etapa_flattened[i] for i in range(len(fieldnames) - 2)})

        writer.writerow(coordenada_dict)

        print(f"Coordenadas da Etapa {etapa} salvas em {nome_arquivo_csv}")

        cap.release()
        cv2.destroyAllWindows()
import os
import numpy as np
import cv2 as cv

# Inicializa el clasificador
rostro = cv.CascadeClassifier('haarcascade_frontalface_alt.xml')
cap = cv.VideoCapture(0)
i = 0

output_dir = 'rostros-dataset'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

while True:
    ret, frame = cap.read()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    rostros = rostro.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)
    print("Rostros detectados:", len(rostros))

    for (x, y, w, h) in rostros:
        # Dibuja un rectángulo alrededor del rostro
        frame = cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Recorta el rostro y redimensiona a 100x100
        rostro_100x100 = cv.resize(frame[y:y+h, x:x+w], (100, 100), interpolation=cv.INTER_AREA)
        _, binarizada_100x100 = cv.threshold(cv.cvtColor(rostro_100x100, cv.COLOR_BGR2GRAY), 127, 255, cv.THRESH_BINARY)
        bin_img_100x100_path = os.path.join(output_dir, f'bin_rostro_100x100_{i}.jpg')
        cv.imwrite(bin_img_100x100_path, binarizada_100x100)
        
        # Redimensiona el mismo rostro a 80x80
        rostro_80x80 = cv.resize(frame[y:y+h, x:x+w], (80, 80), interpolation=cv.INTER_AREA)
        _, binarizada_80x80 = cv.threshold(cv.cvtColor(rostro_80x80, cv.COLOR_BGR2GRAY), 127, 255, cv.THRESH_BINARY)
        bin_img_80x80_path = os.path.join(output_dir, f'bin_rostro_80x80_{i}.jpg')
        cv.imwrite(bin_img_80x80_path, binarizada_80x80)

        # Opcional: muestra uno de los tamaños en pantalla
        cv.imshow('Binarizada 100x100', binarizada_100x100)
        
        # Incrementa el contador
        i += 1

    # Muestra el cuadro con los rostros detectados
    cv.imshow('rostros', frame)

    # Presiona 'Esc' para salir
    if cv.waitKey(1) == 27:
        break

cap.release()
cv.destroyAllWindows()

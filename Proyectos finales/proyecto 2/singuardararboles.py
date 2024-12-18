import pygame
import random
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from joblib import dump, load
import sys

# Inicializar Pygame
pygame.init()

# Dimensiones de la pantalla
w, h = 800, 400
pantalla = pygame.display.set_mode((w, h))
pygame.display.set_caption("Juego: Disparo de Bala, Salto, Nave y Menú")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Variables del jugador, bala, nave, fondo, etc.
jugador = None
bala = None
fondo = None
nave = None
menu = None

# Variables de salto
salto = False
salto_altura = 15  # Velocidad inicial de salto
gravedad = 1
en_suelo = True

# Variables de pausa y menú
pausa = False
fuente = pygame.font.SysFont('Arial', 24)
menu_activo = True
modo_auto = False  # Indica si el modo de juego es automático

# Lista para guardar los datos de velocidad, distancia y salto (target)
datos_modelo = []

# Variable global para el modelo (árbol de decisión)
model = None

# Cargar las imágenes
try:
    jugador_frames = [
        pygame.image.load('assets/sprites/mono_frame_1.png'),
        pygame.image.load('assets/sprites/mono_frame_2.png'),
        pygame.image.load('assets/sprites/mono_frame_3.png'),
        pygame.image.load('assets/sprites/mono_frame_4.png')
    ]
    bala_img = pygame.image.load('assets/sprites/purple_ball.png')
    fondo_img = pygame.image.load('assets/game/fondo2.png')
    nave_img = pygame.image.load('assets/game/ufo.png')
    menu_img = pygame.image.load('assets/game/menu.png')
except pygame.error as e:
    print(f"Error al cargar las imágenes: {e}")
    pygame.quit()
    sys.exit()

# Escalar la imagen de fondo para que coincida con el tamaño de la pantalla
fondo_img = pygame.transform.scale(fondo_img, (w, h))

# Crear el rectángulo del jugador, bala, nave
jugador = pygame.Rect(50, h - 100, 32, 48)
bala = pygame.Rect(w - 50, h - 90, 16, 16)
nave = pygame.Rect(w - 100, h - 100, 64, 64)
menu_rect = pygame.Rect(w // 2 - 135, h // 2 - 90, 270, 180)  # Tamaño del menú

# Variables para la animación del jugador
current_frame = 0
frame_speed = 10  # Cuántos frames antes de cambiar a la siguiente imagen
frame_count = 0

# Variables para la bala
velocidad_bala = -10  # Velocidad de la bala hacia la izquierda
bala_disparada = False

# Variables para el fondo en movimiento
fondo_x1 = 0
fondo_x2 = w

def disparar_bala():
    global bala_disparada, velocidad_bala
    if not bala_disparada:
        velocidad_bala = random.randint(-8, -3)  # Velocidad aleatoria negativa para la bala
        bala_disparada = True

def reset_bala():
    global bala, bala_disparada
    bala.x = w - 50  # Reiniciar la posición de la bala
    bala_disparada = False

def manejar_salto():
    global jugador, salto, salto_altura, gravedad, en_suelo

    if salto:
        jugador.y -= salto_altura  # Mover al jugador hacia arriba
        salto_altura -= gravedad  # Aplicar gravedad

        # Si el jugador llega al suelo, detener el salto
        if jugador.y >= h - 100:
            jugador.y = h - 100
            salto_altura = 15
            salto = False
            en_suelo = True

def update():
    global bala, velocidad_bala, current_frame, frame_count, fondo_x1, fondo_x2

    # Mover el fondo
    fondo_x1 -= 1
    fondo_x2 -= 1

    # Fondo infinito
    if fondo_x1 <= -w:
        fondo_x1 = w
    if fondo_x2 <= -w:
        fondo_x2 = w

    pantalla.blit(fondo_img, (fondo_x1, 0))
    pantalla.blit(fondo_img, (fondo_x2, 0))

    # Animación del jugador
    frame_count += 1
    if frame_count >= frame_speed:
        current_frame = (current_frame + 1) % len(jugador_frames)
        frame_count = 0

    pantalla.blit(jugador_frames[current_frame], (jugador.x, jugador.y))
    pantalla.blit(nave_img, (nave.x, nave.y))

    # Mover y dibujar la bala
    if bala_disparada:
        bala.x += velocidad_bala

    if bala.x < 0:
        reset_bala()

    pantalla.blit(bala_img, (bala.x, bala.y))

    # Colisión entre la bala y el jugador
    if jugador.colliderect(bala):
        print("Colisión detectada!")
        reiniciar_juego()

def guardar_datos():
    global jugador, bala, velocidad_bala, salto
    distancia = abs(jugador.x - bala.x)
    salto_hecho = 1 if salto else 0
    # Guardar velocidad_bala, distancia, salto_hecho
    datos_modelo.append((velocidad_bala, distancia, salto_hecho))

def pausa_juego():
    global pausa
    pausa = not pausa
    if pausa:
        print("Juego pausado. Datos registrados hasta ahora:", datos_modelo)
    else:
        print("Juego reanudado.")

def mostrar_menu():
    global menu_activo, modo_auto, datos_modelo
    pantalla.fill(NEGRO)
    texto = fuente.render("Presiona 'A' para Auto, 'M' para Manual, o 'Q' para Salir", True, BLANCO)
    pantalla.blit(texto, (w // 4, h // 2))
    pygame.display.flip()

    while menu_activo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_a:
                    print("Juego terminado. Datos recopilados:", datos_modelo)
                    entrenar_arbol_decision()
                    modo_auto = True
                    menu_activo = False
                elif evento.key == pygame.K_m:
                    datos_modelo = []
                    modo_auto = False
                    menu_activo = False
                elif evento.key == pygame.K_q:

                    pygame.quit()
                    exit()

def reiniciar_juego():
    global menu_activo, jugador, bala, nave, bala_disparada, salto, en_suelo
    menu_activo = True
    jugador.x, jugador.y = 50, h - 100
    bala.x = w - 50
    nave.x, nave.y = w - 100, h - 100
    bala_disparada = False
    salto = False
    en_suelo = True
    print("Datos recopilados para el modelo: ", datos_modelo)
    mostrar_menu()

# Función para entrenar el modelo con árbol de decisión
# Función para entrenar el modelo con árbol de decisión
def entrenar_arbol_decision():
    global datos_modelo, model
    if len(datos_modelo) < 10:
        print("No hay suficientes datos para entrenar el modelo.")
        return

    datos = np.array(datos_modelo)
    X = datos[:, :2]  # velocidad_bala, distancia
    y = datos[:, 2]   # salto_hecho

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = DecisionTreeClassifier()
    print("Entrenando el árbol de decisión con los datos recopilados...")
    model.fit(X_train, y_train)

    # Evaluar el modelo
    accuracy = model.score(X_test, y_test)
    print(f"Precisión en el conjunto de prueba: {accuracy:.2f}")

    # El modelo entrenado se mantiene en memoria y no se guarda en disco
    print("Modelo entrenado y listo para usar en memoria.")

    if len(X_test) > 0:
        nuevo_dato = X_test[0].reshape(1, -1)
        prediccion = model.predict(nuevo_dato)
        print(f"Predicción para {nuevo_dato}: {prediccion[0]}")

# Función para controlar automáticamente al jugador usando el modelo
def control_auto():
    global model, salto, en_suelo, velocidad_bala, jugador, bala

    if model is None:
        print("Modelo no entrenado. No se puede controlar automáticamente.")
        return

    if not en_suelo:
        return

    if bala.x < jugador.x:
        return

    velocidad_bala_current = velocidad_bala
    distancia_current = abs(jugador.x - bala.x)
    input_data = np.array([[velocidad_bala_current, distancia_current]])

    prediccion = model.predict(input_data)
    # Si la predicción indica que debería saltar (1), y está en el suelo, saltar
    if prediccion[0] == 1 and bala.x < 700 and bala.x > 30:
        print(f'Salta bala {bala.x}, jugador {jugador.x}')
        salto = True
        en_suelo = False


# Función para cargar el modelo entrenado si existe
def cargar_modelo():
    global model

def main():
    global salto, en_suelo, bala_disparada, modo_auto, model

    # Intentar cargar el modelo si existe
    cargar_modelo()

    reloj = pygame.time.Clock()
    mostrar_menu()  # Mostrar el menú al inicio
    correr = True

    while correr:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                correr = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and en_suelo and not pausa and not modo_auto:
                    salto = True
                    en_suelo = False
                if evento.key == pygame.K_p:
                    pausa_juego()
                if evento.key == pygame.K_q:
                    print("Juego terminado. Datos recopilados:", datos_modelo)
                    entrenar_arbol_decision()
                    pygame.quit()
                    exit()

        if not pausa:
            if modo_auto:
                control_auto()

            if salto:
                manejar_salto()

            # Guardar datos (tanto en manual como auto, se registran)
            guardar_datos()

            if not bala_disparada:
                disparar_bala()
            update()

        pygame.display.flip()
        reloj.tick(30)  # 30 FPS

    pygame.quit()

if __name__ == "__main__":
    main()

import os
import cv2

# Directorio raíz donde están las imágenes originales
input_directory = "tonos/dataColorsRotadas"
# Directorio raíz donde se guardarán las imágenes redimensionadas
output_directory = "tonos/dataColors50"
# Tamaño objetivo para las imágenes
target_size = (50, 50)

# Crear el directorio de salida si no existe
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

def process_images(input_dir, output_dir):
    for root, dirs, files in os.walk(input_dir):
        # Crear la misma estructura de directorios en el directorio de salida
        relative_path = os.path.relpath(root, input_dir)
        output_path = os.path.join(output_dir, relative_path)
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        # Procesar cada archivo en el directorio actual
        for file in files:
            input_file_path = os.path.join(root, file)
            output_file_path = os.path.join(output_path, file)

            # Verificar si el archivo es una imagen
            if file.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".gif")):
                # Leer la imagen
                image = cv2.imread(input_file_path)
                if image is not None:
                    # Escalar la imagen a 50x50
                    resized_image = cv2.resize(image, target_size, interpolation=cv2.INTER_AREA)
                    # Guardar la imagen redimensionada en el directorio correspondiente
                    cv2.imwrite(output_file_path, resized_image)
                    print(f"Imagen escalada guardada en: {output_file_path}")
                else:
                    print(f"Error al leer la imagen: {input_file_path}")

# Ejecutar la función
process_images(input_directory, output_directory)

import os
from PIL import Image

# Ruta de entrada y salida
input_folder = "tonos/dataColors"
output_folder = "tonos/dataColorsRotadas"

# Asegurarse de que la carpeta de salida exista
os.makedirs(output_folder, exist_ok=True)

# Recorrer las carpetas dentro de la carpeta "images"
for subfolder in os.listdir(input_folder):
    subfolder_path = os.path.join(input_folder, subfolder)
    if os.path.isdir(subfolder_path):
        # Crear la misma subcarpeta en "dataset"
        output_subfolder_path = os.path.join(output_folder, subfolder)
        os.makedirs(output_subfolder_path, exist_ok=True)

        # Recorrer cada imagen en la subcarpeta
        for image_name in os.listdir(subfolder_path):
            image_path = os.path.join(subfolder_path, image_name)
            if os.path.isfile(image_path):
                try:
                    # Abrir la imagen
                    img = Image.open(image_path)

                    # Convertir la imagen a modo RGB si tiene transparencia
                    if img.mode == "RGBA":
                        img = img.convert("RGB")

                    for angle in [0, 90, 180, 270]:
                        rotated_img = img.rotate(angle, expand=True)
                        new_image_name = f"{os.path.splitext(image_name)[0]}_{angle}.jpg"
                        rotated_img.save(os.path.join(output_subfolder_path, new_image_name))

                except Exception as e:
                    print(f"Error procesando la imagen {image_path}: {e}")

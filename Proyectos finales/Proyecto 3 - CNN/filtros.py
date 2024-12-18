from PIL import Image, ImageEnhance
import numpy as np
import os

# Directorios
input_dir = "tonos/dataColors"
output_dir = "tonos/datafiltros"
os.makedirs(output_dir, exist_ok=True)

# Función para aplicar opacidad
def apply_opacity(image, opacity):
    alpha = image.split()[-1]  # Extraer canal alfa
    alpha = alpha.point(lambda p: p * opacity)
    image.putalpha(alpha)
    return image

# Función para cambiar temperatura de color
def apply_temperature(image, temperature):

    if temperature == "warm":
        r, g, b = 1.2, 1.1, 0.9
    elif temperature == "cool":
        r, g, b = 0.9, 1.1, 1.2
    elif temperature == "sepia":
        r, g, b = 1.3, 1.1, 0.8
    elif temperature == "cold_warm":
        r, g, b = 1.1, 1.0, 1.3
    elif temperature == "desaturate":
        r, g, b = 0.8, 0.8, 0.8
    else:
        r, g, b = 1.0, 1.0, 1.0
    return image.point(lambda p: p * r if p < 256 else p * g if p < 512 else p * b)

# Función para cambiar el tono (hue)

# Parámetros de filtros
opacities = [0.3, 0.7]
saturations = [ 2.0, 3]
brightness_levels = [1.5, 2.5]
contrasts = [0.5, 1.5, 2.5]
temperatures = ["desaturate"]

# Aplicar filtros a todas las imágenes en la estructura de carpetas
for root, dirs, files in os.walk(input_dir):
    for file in files:
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            input_path = os.path.join(root, file)
            relative_path = os.path.relpath(root, input_dir)
            output_folder = os.path.join(output_dir, relative_path)
            os.makedirs(output_folder, exist_ok=True)

            # Cargar la imagen
            image = Image.open(input_path).convert("RGBA")

            # Aplicar filtros y guardar
            for opacity in opacities:
                img_opacity = apply_opacity(image.copy(), opacity)
                img_opacity.save(os.path.join(output_folder, f"{file}_opacity_{opacity:.1f}.png"))

            for saturation in saturations:
                enhancer = ImageEnhance.Color(image.copy())
                img_saturation = enhancer.enhance(saturation)
                img_saturation.save(os.path.join(output_folder, f"{file}_saturation_{saturation:.1f}.png"))

            for brightness in brightness_levels:
                enhancer = ImageEnhance.Brightness(image.copy())
                img_brightness = enhancer.enhance(brightness)
                img_brightness.save(os.path.join(output_folder, f"{file}_brightness_{brightness:.1f}.png"))

            for contrast in contrasts:
                enhancer = ImageEnhance.Contrast(image.copy())
                img_contrast = enhancer.enhance(contrast)
                img_contrast.save(os.path.join(output_folder, f"{file}_contrast_{contrast:.1f}.png"))

            for temperature in temperatures:
                img_temperature = apply_temperature(image.copy(), temperature)
                img_temperature.save(os.path.join(output_folder, f"{file}_temperature_{temperature}.png"))

print(f"Filtros aplicados y guardados en la carpeta: {output_dir}")

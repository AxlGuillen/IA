from PIL import Image
import numpy as np
import os


# Función para cambiar el tono (hue)
def apply_hue(image, hue_shift):
    img = image.convert("RGB")
    img_array = np.array(img) / 255.0
    r, g, b = img_array[..., 0], img_array[..., 1], img_array[..., 2]
    max_val = np.max(img_array, axis=-1)
    min_val = np.min(img_array, axis=-1)
    delta = max_val - min_val
    delta[delta == 0] = 1e-6

    hue = np.zeros_like(max_val)
    mask_r = (max_val == r)
    mask_g = (max_val == g)
    mask_b = (max_val == b)

    hue[mask_r] = (60 * ((g[mask_r] - b[mask_r]) / delta[mask_r]) + 360) % 360
    hue[mask_g] = (60 * ((b[mask_g] - r[mask_g]) / delta[mask_g]) + 120) % 360
    hue[mask_b] = (60 * ((r[mask_b] - g[mask_b]) / delta[mask_b]) + 240) % 360

    hue = (hue + hue_shift) % 360

    c = delta
    x = c * (1 - np.abs((hue / 60) % 2 - 1))
    m = min_val
    rgb_array = np.zeros_like(img_array)
    h_section = (hue // 60).astype(int)

    for i in range(6):
        mask = (h_section == i)
        if i == 0:
            rgb_array[mask] = np.stack([c[mask], x[mask], np.zeros_like(c[mask])], axis=-1)
        elif i == 1:
            rgb_array[mask] = np.stack([x[mask], c[mask], np.zeros_like(c[mask])], axis=-1)
        elif i == 2:
            rgb_array[mask] = np.stack([np.zeros_like(c[mask]), c[mask], x[mask]], axis=-1)
        elif i == 3:
            rgb_array[mask] = np.stack([np.zeros_like(c[mask]), x[mask], c[mask]], axis=-1)
        elif i == 4:
            rgb_array[mask] = np.stack([x[mask], np.zeros_like(c[mask]), c[mask]], axis=-1)
        elif i == 5:
            rgb_array[mask] = np.stack([c[mask], np.zeros_like(c[mask]), x[mask]], axis=-1)

    rgb_array += m[..., None]
    rgb_array = (rgb_array * 255).astype(np.uint8)
    return Image.fromarray(rgb_array)


# Directorios de entrada y salida
# Directorios de entrada y salida
def apply_tones(input_dir, output_dir, tones):
    for root, _, files in os.walk(input_dir):
        relative_path = os.path.relpath(root, input_dir)
        current_output_dir = os.path.join(output_dir, relative_path)
        os.makedirs(current_output_dir, exist_ok=True)

        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                input_path = os.path.join(root, file)
                image = Image.open(input_path).convert("RGBA")

                for tone in tones:
                    img_tone = apply_hue(image.copy(), tone)
                    output_path = os.path.join(current_output_dir, f"{os.path.splitext(file)[0]}_tone_{tone}.png")
                    img_tone.save(output_path)
                    print(f"Guardado: {output_path}")


# Parámetros del usuario
input_dir = "newOldData"
output_dir = "tonos/dataColors"
os.makedirs(output_dir, exist_ok=True)
tones = [20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360]


# Ejecución
apply_tones(input_dir, output_dir, tones)
print(f"Proceso completado. Archivos guardados en {output_dir}")

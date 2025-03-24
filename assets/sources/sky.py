from PIL import Image, ImageDraw
import random

# Crear una imagen de 400x600 con fondo azul cielo
width, height = 400, 600
sky_color = (135, 206, 235)  # Azul cielo
img = Image.new("RGB", (width, height), sky_color)
draw = ImageDraw.Draw(img)

# Función para dibujar una nube más grande estilo pixel art
def draw_large_pixel_cloud(x, y, draw):
    cloud_color = (255, 255, 255)
    cloud_pixels = [
        (0, 3), (1, 2), (1, 3), (1, 4),
        (2, 1), (2, 2), (2, 3), (2, 4), (2, 5),
        (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6),
        (4, 1), (4, 2), (4, 3), (4, 4), (4, 5),
        (5, 2), (5, 3), (5, 4),
        (6, 3)
    ]
    for px, py in cloud_pixels:
        draw.rectangle(
            [(x + px * 10, y + py * 10), (x + px * 10 + 9, y + py * 10 + 9)],
            fill=cloud_color
        )

# Dibujar varias nubes grandes en posiciones aleatorias
for _ in range(5):
    x = random.randint(0, width - 100)
    y = random.randint(0, height - 100)
    draw_large_pixel_cloud(x, y, draw)

# Guardar la nueva imagen
output_path = "sky_pixel_art_large_clouds.png"
img.save(output_path)
output_path

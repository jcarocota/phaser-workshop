from PIL import Image, ImageDraw
import math

# Parámetros del spritesheet
frame_width = 50
frame_height = 50
num_frames = 4
sheet_width = frame_width * num_frames
sheet_height = frame_height

# Crear el spritesheet con fondo transparente
sheet = Image.new("RGBA", (sheet_width, sheet_height), (0, 0, 0, 0))
draw_sheet = ImageDraw.Draw(sheet)

# Función para dibujar un frame de explosión
def draw_explosion_frame(draw, x_offset, frame_index):
    # Centro de la explosión en el frame
    center_x = x_offset + frame_width // 2
    center_y = frame_height // 2

    # Parámetros que varían con el frame para simular la expansión
    # El radio del círculo central aumenta en cada frame
    radius = 5 + frame_index * 3  
    # La longitud de las chispas también aumenta
    extension = 3 + frame_index * 2

    # Dibujar el círculo central (explosión)
    bbox = [center_x - radius, center_y - radius, center_x + radius, center_y + radius]
    draw.ellipse(bbox, fill=(255, 255, 0, 255))  # Amarillo

    # Dibujar 8 chispas radiales
    for angle in range(0, 360, 45):
        rad = math.radians(angle)
        # Punto de partida en el borde del círculo
        start_x = center_x + radius * math.cos(rad)
        start_y = center_y + radius * math.sin(rad)
        # Punto final extendido
        end_x = center_x + (radius + extension) * math.cos(rad)
        end_y = center_y + (radius + extension) * math.sin(rad)
        draw.line([(start_x, start_y), (end_x, end_y)], fill=(255, 140, 0, 255), width=1)  # Naranja

# Dibujar cada uno de los 4 frames en el spritesheet
for i in range(num_frames):
    x_offset = i * frame_width
    draw_explosion_frame(draw_sheet, x_offset, i)

# Guardar la imagen resultante
output_path = "boom_spritesheet.png"
sheet.save(output_path)
print("Spritesheet guardado en:", output_path)

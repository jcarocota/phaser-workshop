from PIL import Image, ImageDraw, ImageFont

# Crear una imagen de 200x200 px con fondo transparente
img = Image.new("RGBA", (200, 200), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Dibujar el letrero: un rectángulo amarillo con borde rojo
rect_coords = [20, 80, 180, 140]  # [x0, y0, x1, y1]
draw.rectangle(rect_coords, fill=(255, 255, 0, 255), outline=(255, 0, 0, 255), width=4)

# Función para dibujar una chispa (pequeño cruce) en pixel art
def draw_spark(draw, x, y):
    spark_color = (255, 215, 0, 255)  # Dorado
    # Dibujar un pequeño signo de más
    draw.line([(x-2, y), (x+2, y)], fill=spark_color, width=1)
    draw.line([(x, y-2), (x, y+2)], fill=spark_color, width=1)

# Agregar chispas arriba del letrero
spark_positions_above = [(40, 70), (80, 65), (120, 75), (160, 68)]
for pos in spark_positions_above:
    draw_spark(draw, pos[0], pos[1])

# Agregar chispas abajo del letrero
spark_positions_below = [(40, 150), (80, 155), (120, 148), (160, 152)]
for pos in spark_positions_below:
    draw_spark(draw, pos[0], pos[1])

# Texto a dibujar
text = "¡kaboom!"

# Cargar la fuente desde el archivo local con tamaño 28
font = ImageFont.truetype("PressStart2P-Regular.ttf", 18)

# Obtener el tamaño del texto usando textbbox
bbox = draw.textbbox((0, 0), text, font=font)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]

# Calcular la posición para centrar el texto en el rectángulo
rect_width = rect_coords[2] - rect_coords[0]
rect_height = rect_coords[3] - rect_coords[1]
text_x = rect_coords[0] + (rect_width - text_width) // 2
text_y = rect_coords[1] + (rect_height - text_height) // 2

# Dibujar el texto en color negro
draw.text((text_x, text_y), text, fill=(0, 0, 0, 255), font=font)

# Dibujar el texto en color negro
draw.text((text_x, text_y), text, fill=(0, 0, 0, 255), font=font)
# Guardar la imagen
output_path = "kaboom_sign.png"
img.save(output_path)
print("Imagen guardada en:", output_path)

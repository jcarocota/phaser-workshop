from PIL import Image, ImageDraw

# Dimensiones de la imagen
width, height = 50, 300

# Crear imagen con fondo transparente
img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Definir colores
main_color = (34, 139, 34, 255)    # Verde principal
highlight  = (50, 205, 50, 255)     # Verde más claro para resaltar
shadow     = (0, 100, 0, 255)        # Verde oscuro para sombrear y detalles
border     = (0, 0, 0, 255)          # Negro para el borde

# Rellenar el área principal (dejando 1px para el borde)
draw.rectangle([1, 1, width-2, height-2], fill=main_color)

# Dibujar borde exterior
draw.rectangle([0, 0, width-1, height-1], outline=border)

# Agregar highlight en el borde izquierdo (columna 1)
for y in range(1, height-1):
    draw.point((1, y), fill=highlight)

# Agregar sombra en el borde derecho (columna width-2)
for y in range(1, height-1):
    draw.point((width-2, y), fill=shadow)

# Agregar una línea horizontal de "seam" en el centro (3px de grosor)
seam_start = height // 2 - 1
seam_end = height // 2 + 1
for y in range(seam_start, seam_end+1):
    for x in range(1, width-1):
        #draw.point((x, y), fill=shadow)
        pass

# Agregar detalles horizontales adicionales cada 30 píxeles
for y in range(20, height-20, 30):
    # Línea horizontal interna de 1px, dejando márgenes a los lados
    for x in range(5, width-5):
        draw.point((x, y), fill=shadow)
    # Dibujar pequeños "rivets" a los costados para simular uniones
    # Rivet izquierdo
    draw.rectangle([3, y-1, 5, y+1], fill=highlight)
    # Rivet derecho
    draw.rectangle([width-6, y-1, width-4, y+1], fill=highlight)

# Guardar la imagen
output_path = "C:\imgs\pipe_segment_50x300.png"
img.save(output_path)
print(output_path)

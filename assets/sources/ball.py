from PIL import Image, ImageDraw

# Dimensiones y configuración
width, height = 128, 128
radius = 60
center_x, center_y = width // 2, height // 2

# Crear imagen transparente
img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
pixels = img.load()

# Definir colores para el degradado de la pelota
center_color = (255, 100, 100, 255)  # Color brillante en el centro
outer_color = (150, 0, 0, 255)        # Color más oscuro en el borde

# Dibujar la pelota con degradado radial
for x in range(width):
    for y in range(height):
        dx = x - center_x
        dy = y - center_y
        dist = (dx * dx + dy * dy) ** 0.5
        if dist <= radius:
            factor = dist / radius
            r = int(outer_color[0] * factor + center_color[0] * (1 - factor))
            g = int(outer_color[1] * factor + center_color[1] * (1 - factor))
            b = int(outer_color[2] * factor + center_color[2] * (1 - factor))
            pixels[x, y] = (r, g, b, 255)

# Agregar efecto de brillo (highlight) en la parte superior izquierda
draw = ImageDraw.Draw(img)
highlight_radius = 10
highlight_center = (center_x - 20, center_y - 20)
draw.ellipse(
    (
        highlight_center[0] - highlight_radius,
        highlight_center[1] - highlight_radius,
        highlight_center[0] + highlight_radius,
        highlight_center[1] + highlight_radius,
    ),
    fill=(255, 255, 255, 128)
)

# Guardar la imagen
img.save("ball.png")
img.show()

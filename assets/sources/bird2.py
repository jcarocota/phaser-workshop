from PIL import Image, ImageDraw

# Dimensiones de cada frame y del spritesheet (duplicado)
frame_width = 68
frame_height = 48
num_frames = 3
sheet_width = frame_width * num_frames
sheet_height = frame_height

# Crear el spritesheet con fondo transparente
sheet = Image.new("RGBA", (sheet_width, sheet_height), (0, 0, 0, 0))
draw_sheet = ImageDraw.Draw(sheet)

def draw_bird_frame(draw, x_offset, frame):
    """
    Dibuja un pájaro pixel art en un frame.
    x_offset: posición horizontal en el spritesheet.
    frame: índice del frame (0, 1 o 2) para variar la posición del ala.
    """
    # Colores
    body_color = (255, 255, 0, 255)       # Amarillo para el cuerpo
    wing_color = (255, 165, 0, 255)        # Naranja para el ala
    outline_color = (0, 0, 0, 255)         # Contorno en negro
    eye_color = (0, 0, 0, 255)
    
    # Dibujar cuerpo (un rectángulo simple)
    # Originalmente: [x_offset+6, 8, x_offset+26, 18] --> Duplicado: [x_offset+12, 16, x_offset+52, 36]
    #draw.rectangle([x_offset+12, 16, x_offset+52, 36], fill=body_color, outline=outline_color)
    draw.ellipse([x_offset+12, 16, x_offset+52, 36], fill=body_color, outline=outline_color)
    
    # Dibujar cabeza (una elipse pequeña)
    # Originalmente: [x_offset+2, 10, x_offset+10, 18] --> Duplicado: [x_offset+4, 20, x_offset+20, 36]
    draw.ellipse([x_offset+4, 20, x_offset+20, 36], fill=body_color, outline=outline_color)
    
    # Dibujar ala según el frame
    if frame == 0:
        # Ala "arriba": originalmente: [(x_offset+12, 10), (x_offset+20, 4), (x_offset+22, 10)]
        # Duplicado: [(x_offset+24, 20), (x_offset+40, 8), (x_offset+44, 20)]
        wing_points = [(x_offset+24, 20), (x_offset+40, 4), (x_offset+44, 20)]
    elif frame == 1:
        # Ala "media": originalmente: [(x_offset+12, 12), (x_offset+20, 8), (x_offset+22, 12)]
        # Duplicado: [(x_offset+24, 24), (x_offset+40, 16), (x_offset+44, 24)]
        wing_points = [(x_offset+24, 24), (x_offset+40, 16), (x_offset+44, 24)]
    elif frame == 2:
        # Ala "abajo": originalmente: [(x_offset+12, 16), (x_offset+20, 20), (x_offset+22, 16)]
        # Duplicado: [(x_offset+24, 32), (x_offset+40, 40), (x_offset+44, 32)]
        wing_points = [(x_offset+24, 32), (x_offset+40, 44), (x_offset+44, 32)]
    
    draw.polygon(wing_points, fill=wing_color, outline=outline_color)
    
    # Dibujar un ojo en la cabeza
    # Originalmente: en (x_offset+4, 14) --> Duplicado: (x_offset+8, 28)
    draw.point((x_offset+8, 28), fill=eye_color)

# Dibujar los 3 frames en el spritesheet
for i in range(num_frames):
    draw_bird_frame(draw_sheet, i * frame_width, i)

sheet.transpose(Image.Transpose.FLIP_LEFT_RIGHT)

# Guardar la imagen resultante
output_path = "bird_anim.png"
sheet.save(output_path)
print("Spritesheet guardado en:", output_path)

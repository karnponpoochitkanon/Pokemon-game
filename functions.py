import pygame
from os.path import join

def character_importer(cols, rows, *path):
    full_path = join(*path)
    sheet = pygame.image.load(full_path).convert_alpha()
    frame_dict = {}

    # ขนาด 128x128
    frame_width = 128
    frame_height = 128

    directions = ['down', 'left', 'right', 'up']
    for row_index, direction in enumerate(directions):
        frames = []
        for col in range(cols):
            x = col * frame_width
            y = row_index * frame_height
            frame = sheet.subsurface(pygame.Rect(x, y, frame_width, frame_height))
            frames.append(frame)
        frame_dict[direction] = frames
    return frame_dict
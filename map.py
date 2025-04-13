import pytmx
import pygame
from setting import *

class Map:
    def __init__(self, filename):
        self.tmx_data = pytmx.load_pygame(filename, pixelalpha=True)
        self.grass_rects = self.get_grass_rects()  # ✅ โหลดพื้นที่หญ้า
        print("📍 Grass zones loaded:", len(self.grass_rects))  # ✅ แสดงจำนวน

    def get_grass_rects(self):
        grass_rects = []
        for obj in self.tmx_data.objects:
            if obj.name == "grass":
                rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                grass_rects.append(rect)
        return grass_rects

    def draw(self, screen):
        # วาด tile layers
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        screen.blit(tile, (x * TILE_SIZE, y * TILE_SIZE))

        # ถ้ามี tile แบบวาดเองจาก object layer (ปกติอาจไม่ต้องใช้)
        for obj in self.tmx_data.objects:
            if obj.name == "grass" and hasattr(obj, 'gid'):
                tile = self.tmx_data.get_tile_image_by_gid(obj.gid)
                if tile:
                    screen.blit(tile, (obj.x, obj.y))
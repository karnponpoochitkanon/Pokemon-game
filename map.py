import pytmx
import pygame
from setting import *

class Map:
    def __init__(self, filename):
        self.tmx_data = pytmx.load_pygame(filename, pixelalpha=True)
        self.grass_rects = self.get_grass_rects()
        print("📍 Grass zones loaded:", len(self.grass_rects))

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

        # วาด object ที่มี gid เช่น hospital, door, healtree, yim
        for obj in self.tmx_data.objects:
            if hasattr(obj, 'gid'):
                tile = self.tmx_data.get_tile_image_by_gid(obj.gid)
                if tile:
                    screen.blit(tile, (obj.x, obj.y))

    def get_blocking_rects(self):
        block_rects = []
        for obj in self.tmx_data.objects:
            if obj.name in ["tree", "healtree", "yim"]:  # ✅ เพิ่ม yim ด้วย
                rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                block_rects.append(rect)
        return block_rects

    @property
    def block_rects(self):
        return self.get_blocking_rects()
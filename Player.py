import pygame
from pygame.math import Vector2 as Vector
import sys
from setting import *
from functions import character_importer
from pokemon import Pokemon

class Player:
    def __init__(self, image_path):
        self.frames = character_importer(3, 4, image_path)
        self.direction = Vector(0, 0)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.status = 'down'
        self.image = self.frames[self.status][0]
        self.pos = Vector(20, 220)

    def update(self, keys, block_rects):
        self.direction = Vector(0, 0)

        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.status = 'down'
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = 'left'
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = 'right'

        walked = 0  # ✅ เพิ่มตัวแปรนับระยะทาง

        if self.direction.length() != 0:
            next_pos = self.pos + self.direction
            next_rect = pygame.Rect(next_pos.x + 48, next_pos.y + 48, 32, 32)

            if not any(next_rect.colliderect(block) for block in block_rects):
                walked = self.direction.length()  # ✅ เดินได้เท่าไหร่
                self.pos = next_pos
                self.frame_index += self.animation_speed
                if self.frame_index >= len(self.frames[self.status]):
                    self.frame_index = 0
                self.image = self.frames[self.status][int(self.frame_index)]
            else:
                self.image = self.frames[self.status][0]
        else:
            self.image = self.frames[self.status][0]

        return walked  # ✅ คืนค่าระยะทางที่เดินได้

    def draw(self, screen):
        screen.blit(self.image, self.pos)

    @property
    def rect(self):
        return pygame.Rect(self.pos.x + 40, self.pos.y + 40, 48, 48)  # ใหญ่กว่าเดิมนิด

class CharacterSelectMenu:
    def __init__(self, screen, player_name):
        self.screen = screen
        self.player_name = player_name
        self.clock = pygame.time.Clock()
        self.characters = [
            ("Grass Boss", "image/player/grass_boss.png"),
            ("Purple Girl", "image/player/purple_girl.png"),
            ("Straw", "image/player/straw.png")
        ]
        self.font = pygame.font.Font("Fonts/Arabica/ttf/Arabica.ttf", 40)
        self.title_font = pygame.font.Font("Fonts/Arabica/ttf/Arabica.ttf", 60)
        self.hi_font = pygame.font.Font("Fonts/Arabica/ttf/Arabica.ttf", 80)  # ขนาดใหญ่สำหรับ Hi
        self.selected = 0

    def draw(self):
        self.screen.fill((24, 24, 72))

        # ข้อความทักทาย
        hi_text = self.hi_font.render(f"Hi, {self.player_name}!", True, (255, 255, 255))
        hi_rect = hi_text.get_rect(center=(WINDOW_WIDTH // 2, 60))
        self.screen.blit(hi_text, hi_rect)

        # หัวข้อเลือกตัวละคร
        title = self.title_font.render("Select Your Character", True, (255, 255, 255))
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 120))
        self.screen.blit(title, title_rect)


        # รายการตัวละคร
        for i, (name, _) in enumerate(self.characters):
            y = 200 + i * 60
            is_selected = i == self.selected

            box_width, box_height = 300, 50
            box_x = WINDOW_WIDTH // 2 - box_width // 2
            box_rect = pygame.Rect(box_x, y, box_width, box_height)

            if is_selected:
                pygame.draw.rect(self.screen, (255, 255, 255, 100), box_rect, border_radius=10)
                pygame.draw.rect(self.screen, (255, 0, 0), box_rect, 3, border_radius=10)

            label_color = (255, 0, 0) if is_selected else (200, 200, 200)
            label = self.font.render(name, True, label_color)
            label_rect = label.get_rect(center=box_rect.center)
            self.screen.blit(label, label_rect)

        _, preview_path = self.characters[self.selected]
        sheet = pygame.image.load(preview_path).convert_alpha()

        frame = sheet.subsurface(pygame.Rect(0, 0, 128, 128))

        preview = pygame.transform.scale(frame, (230, 230))
        preview_rect = preview.get_rect(center=(WINDOW_WIDTH // 2, 500))
        self.screen.blit(preview, preview_rect)


        pygame.display.flip()

    def run(self):
        while True:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected = (self.selected - 1) % len(self.characters)
                    elif event.key == pygame.K_DOWN:
                        self.selected = (self.selected + 1) % len(self.characters)
                    elif event.key == pygame.K_RETURN:
                        _, path = self.characters[self.selected]
                        return path
            self.clock.tick(30)

class PlayerTrainer:
    def __init__(self, name):
        self.name = name
        self.team = []
        self.add_pokemon(Pokemon("pikachu", "Normal"))

    def add_pokemon(self, pokemon):
        self.team.append(pokemon)

    def show_team(self):
        print(f"{self.name}'s Team:")
        for i, p in enumerate(self.team):
            print(f"{i+1}. {p.name} ({p.element_type})")

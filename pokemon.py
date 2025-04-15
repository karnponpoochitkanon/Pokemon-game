import pygame
from typing import List
from setting import WINDOW_WIDTH, WINDOW_HEIGHT
import sys

class Pokemon:
    def __init__(self, name, element_type="Normal"):
        self.name = name
        self.element_type = element_type
        self.max_hp = 200
        self.hp = 200
        self.base_attack = 50

    def __repr__(self):
        return f"{self.name} ({self.element_type})"


class PlayerMonsters:
    def __init__(self):
        self.monsters = [
            Pokemon("hitokage", "Fire"),
            Pokemon("zenigame", "Water"),
            Pokemon("fushigidane", "Grass"),
            Pokemon("eevee", "Normal"),
            Pokemon("pikachu", "Normal"),
            Pokemon("furin", "Normal"),
            Pokemon("gus", "Normal"),
            Pokemon("squirrel", "Grass"),  # ✅ เพิ่มตรงนี้
            Pokemon("cute", "Normal"),
            Pokemon("beagle", "Water"),
            Pokemon("firefox", "Fire")
        ]

    def get_available_monsters(self):
        return [
            Pokemon("hitokage", "Fire"),
            Pokemon("zenigame", "Water"),
            Pokemon("fushigidane", "Grass"),
            Pokemon("eevee", "Normal"),
            Pokemon("furin", "Normal"),
            Pokemon("gus", "Normal"),
            Pokemon("squirrel", "Grass"),   # ✅ ใหม่
            Pokemon("cute", "Normal"),      # ✅ ใหม่
            Pokemon("beagle", "Water"),
            Pokemon("firefox", "Fire")
        ]

class PokemonSelectionPopup:
    def __init__(self, screen, pokemon_list, font_path="Fonts/Arabica/ttf/Arabica.ttf"):
        self.screen = screen
        self.pokemon_list = pokemon_list
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(font_path, 28)
        self.selected_index = 0

        self.card_width = 160
        self.card_height = 240
        self.padding = 20
        self.sprite_scale = 100
        self.cards_per_page = 3
        self.page = 0

        self.modal_width = self.cards_per_page * (self.card_width + self.padding) + self.padding
        self.modal_height = self.card_height + 100
        self.modal_rect = pygame.Rect(
            (screen.get_width() - self.modal_width) // 2,
            (screen.get_height() - self.modal_height) // 2,
            self.modal_width,
            self.modal_height
        )

    def draw_type_label(self, element_type, x, y):
        color_map = {
            "Fire": (255, 100, 50),
            "Water": (100, 180, 255),
            "Grass": (100, 255, 100),
            "Normal": (200, 200, 200),
        }
        label_font = pygame.font.SysFont(None, 24)
        text = label_font.render(element_type.upper(), True, (0, 0, 0))
        label_width = 80
        label_height = text.get_height() + 6
        label_rect = pygame.Rect(x + (self.card_width - label_width) // 2, y, label_width, label_height)

        pygame.draw.rect(self.screen, color_map.get(element_type, (180, 180, 180)), label_rect, border_radius=6)
        pygame.draw.rect(self.screen, (0, 0, 0), label_rect, 1, border_radius=6)
        self.screen.blit(text, text.get_rect(center=label_rect.center))

    def draw(self):
        pygame.draw.rect(self.screen, (255, 255, 255), self.modal_rect, border_radius=16)
        title = self.font.render("CHOOSE YOUR POKEMON TO FIGHT", True, (0, 0, 0))
        self.screen.blit(title, (self.modal_rect.centerx - title.get_width() // 2, self.modal_rect.y + 20))

        start_index = self.page * self.cards_per_page
        end_index = min(start_index + self.cards_per_page, len(self.pokemon_list))
        visible_pokemon = self.pokemon_list[start_index:end_index]

        start_x = self.modal_rect.x + self.padding
        y = self.modal_rect.y + 60

        for i, pokemon in enumerate(visible_pokemon):
            index = start_index + i
            x = start_x + i * (self.card_width + self.padding)
            card_rect = pygame.Rect(x, y, self.card_width, self.card_height)

            if pokemon.hp <= 0:
                inner_color = (255, 220, 220)
            else:
                inner_color = (255, 255, 255)

            if pokemon.hp <= 0 and index == self.selected_index:
                border_color = (255, 0, 0)
            elif index == self.selected_index:
                border_color = (255, 204, 0)
            else:
                border_color = (0, 0, 0)

            pygame.draw.rect(self.screen, inner_color, card_rect, border_radius=12)
            pygame.draw.rect(self.screen, border_color, card_rect, 3, border_radius=12)

            sprite = pygame.image.load(f"image/pokemon/{pokemon.name}.png").convert_alpha()
            sprite = pygame.transform.scale(sprite, (self.sprite_scale, self.sprite_scale))
            self.screen.blit(sprite, (x + (self.card_width - self.sprite_scale) // 2, y + 10))

            name_surf = self.font.render(pokemon.name.upper(), True, (0, 0, 0))
            self.screen.blit(name_surf, (x + (self.card_width - name_surf.get_width()) // 2, y + 120))

            self.draw_type_label(pokemon.element_type, x, y + 155)

            # Draw HP bar
            hp_ratio = pokemon.hp / pokemon.max_hp
            hp_bar_x = x + 10
            hp_bar_y = y + 190
            hp_bar_width = self.card_width - 20
            pygame.draw.rect(self.screen, (0, 0, 0), (hp_bar_x, hp_bar_y, hp_bar_width, 10))
            pygame.draw.rect(self.screen, (0, 255, 0), (hp_bar_x, hp_bar_y, hp_bar_width * hp_ratio, 10))
            hp_text = self.font.render(f"{pokemon.hp}/{pokemon.max_hp} HP", True, (0, 0, 0))
            self.screen.blit(hp_text, (x + (self.card_width - hp_text.get_width()) // 2, hp_bar_y + 12))

    def run(self):
        total_pages = (len(self.pokemon_list) - 1) // self.cards_per_page + 1
        error_message = ""
        error_timer = 0

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.selected_index = (self.selected_index - 1) % len(self.pokemon_list)
                        self.page = self.selected_index // self.cards_per_page
                    elif event.key == pygame.K_RIGHT:
                        self.selected_index = (self.selected_index + 1) % len(self.pokemon_list)
                        self.page = self.selected_index // self.cards_per_page
                    elif event.key == pygame.K_RETURN:
                        selected = self.pokemon_list[self.selected_index]
                        if selected.hp > 0:
                            return selected
                        else:
                            error_message = "This Pokémon has no HP!"
                            error_timer = pygame.time.get_ticks()

            self.draw()

            # Error box
            if error_message and pygame.time.get_ticks() - error_timer < 2000:
                font = pygame.font.Font("Fonts/Arabica/ttf/Arabica.ttf", 32)
                msg = font.render(error_message, True, (255, 0, 0))
                box_width = msg.get_width() + 60
                box_height = msg.get_height() + 30
                box = pygame.Surface((box_width, box_height))
                box.fill((255, 240, 240))
                pygame.draw.rect(box, (255, 0, 0), box.get_rect(), 4)
                box_rect = box.get_rect(center=(WINDOW_WIDTH // 2, self.modal_rect.bottom + 40))
                self.screen.blit(box, box_rect)
                self.screen.blit(msg, msg.get_rect(center=box_rect.center))

            page_text = self.font.render(f"PAGE {self.page + 1} / {total_pages}", True, (50, 50, 50))
            page_rect = page_text.get_rect(center=(self.modal_rect.centerx, self.modal_rect.bottom - 10))
            self.screen.blit(page_text, page_rect)
            pygame.display.update()
            self.clock.tick(60)


class TeamStatusPopup:
    def __init__(self, screen, pokemon_list, draw_background_fn=None):
        self.screen = screen
        self.pokemon_list = pokemon_list
        self.selected_index = 0
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("Fonts/Arabica/ttf/Arabica.ttf", 28)
        self.draw_background_fn = draw_background_fn  # ✅ ใช้พื้นหลังแผนที่

        self.page_size = 4
        self.page = 0

        self.left_width = 220
        self.right_width = 400
        self.height = 320
        self.modal_rect = pygame.Rect(
            (WINDOW_WIDTH - (self.left_width + self.right_width)) // 2,
            (WINDOW_HEIGHT - self.height) // 2,
            self.left_width + self.right_width,
            self.height,
        )

        self.colors = {
            "Grass": (152, 251, 152),   # PaleGreen
            "Fire": (255, 99, 71),      # Tomato
            "Water": (135, 206, 235),   # SkyBlue
            "Normal": (240, 240, 240)
        }

    def draw(self):
        pygame.draw.rect(self.screen, (255, 255, 255), self.modal_rect, border_radius=16)

        left_rect = pygame.Rect(self.modal_rect.x, self.modal_rect.y, self.left_width, self.height)
        right_rect = pygame.Rect(left_rect.right, self.modal_rect.y, self.right_width, self.height)

        pygame.draw.rect(self.screen, (255, 255, 255), left_rect)
        pygame.draw.rect(self.screen, (245, 245, 245), right_rect)

        # 🔹 วาดฝั่งซ้าย (รายชื่อโปเกม่อน)
        start = self.page * self.page_size
        end = min(start + self.page_size, len(self.pokemon_list))
        for i in range(start, end):
            mon = self.pokemon_list[i]
            y = self.modal_rect.y + 10 + (i - start) * 70
            entry_rect = pygame.Rect(left_rect.x + 10, y, self.left_width - 20, 60)

            if i == self.selected_index:
                pygame.draw.rect(self.screen, (255, 255, 200), entry_rect)
                pygame.draw.rect(self.screen, (200, 200, 0), entry_rect, 2)
            else:
                pygame.draw.rect(self.screen, (255, 255, 255), entry_rect)
                pygame.draw.rect(self.screen, (0, 0, 0), entry_rect, 1)

            sprite = pygame.image.load(f"image/pokemon/{mon.name}.png").convert_alpha()
            sprite = pygame.transform.scale(sprite, (40, 40))
            self.screen.blit(sprite, (entry_rect.x + 8, entry_rect.y + 10))

            name_text = self.font.render(mon.name.upper(), True, (0, 0, 0))
            self.screen.blit(name_text, (entry_rect.x + 60, entry_rect.y + 15))

        # 🔹 วาดฝั่งขวา (รายละเอียด)
        if self.pokemon_list:
            selected = self.pokemon_list[self.selected_index]
            bg_color = self.colors.get(selected.element_type, (240, 240, 240))
            pygame.draw.rect(self.screen, bg_color, right_rect)

            sprite = pygame.image.load(f"image/pokemon/{selected.name}.png").convert_alpha()
            sprite = pygame.transform.scale(sprite, (100, 100))
            self.screen.blit(sprite, (right_rect.centerx - 50, right_rect.y + 20))

            name = self.font.render(selected.name.upper(), True, (0, 0, 0))
            self.screen.blit(name, (right_rect.centerx - name.get_width() // 2, right_rect.y + 130))

            hp_text = self.font.render(f"{selected.hp}/{selected.max_hp} HP", True, (0, 0, 0))
            self.screen.blit(hp_text, (right_rect.centerx - hp_text.get_width() // 2, right_rect.y + 170))

            ratio = selected.hp / selected.max_hp
            bar_width, bar_height = 180, 18
            bar_x = right_rect.centerx - bar_width // 2
            bar_y = right_rect.y + 200
            pygame.draw.rect(self.screen, (0, 0, 0), (bar_x, bar_y, bar_width, bar_height), 2)
            pygame.draw.rect(self.screen, (0, 255, 0), (bar_x + 2, bar_y + 2, int((bar_width - 4) * ratio), bar_height - 4))

            type_text = self.font.render(f"TYPE: {selected.element_type.upper()}", True, (0, 0, 0))
            self.screen.blit(type_text, (right_rect.centerx - type_text.get_width() // 2, bar_y + 30))

        # 🔹 หมายเลขหน้า
        total_pages = (len(self.pokemon_list) - 1) // self.page_size + 1
        page_text = self.font.render(f"PAGE {self.page + 1} / {total_pages}", True, (50, 50, 50))
        self.screen.blit(page_text, (self.modal_rect.centerx - page_text.get_width() // 2, self.modal_rect.bottom - 30))

    def next_page(self):
        max_page = (len(self.pokemon_list) - 1) // self.page_size
        if self.page < max_page:
            self.page += 1

    def prev_page(self):
        if self.page > 0:
            self.page -= 1

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_ESCAPE, pygame.K_LSHIFT, pygame.K_RSHIFT):
                        running = False
                    elif event.key == pygame.K_UP:
                        self.selected_index = (self.selected_index - 1) % len(self.pokemon_list)
                        self.page = self.selected_index // self.page_size
                    elif event.key == pygame.K_DOWN:
                        self.selected_index = (self.selected_index + 1) % len(self.pokemon_list)
                        self.page = self.selected_index // self.page_size

            if self.draw_background_fn:
                self.draw_background_fn()
            else:
                self.screen.fill((0, 0, 0))  # fallback

            self.draw()
            pygame.display.update()
            self.clock.tick(60)


class CatchPopup:
    def __init__(self, screen, pokemon_name):
        self.screen = screen
        self.name = pokemon_name
        self.sprite = pygame.image.load(f"image/pokemon/{self.name}.png").convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (100, 100))
        self.font = pygame.font.Font("Fonts/Arabica/ttf/Arabica.ttf", 36)
        self.duration = 1200  # ⏱ แสดง 1.2 วินาที

    def show(self):
        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time < self.duration:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # กล่อง popup
            box_width = 350
            box_height = 200
            box = pygame.Surface((box_width, box_height))
            box.fill((255, 255, 255))  # พื้นหลังกล่อง

            # ขอบชมพู #FF9999
            border_rect = box.get_rect()
            pygame.draw.rect(box, (255, 153, 153), border_rect, 4)

            # ข้อความด้านบน
            text = self.font.render(f"YOU CAUGHT {self.name.upper()}!", True, (0, 100, 0))
            text_rect = text.get_rect(center=(box_width // 2, 40))
            box.blit(text, text_rect)

            # รูปโปเกม่อน
            box.blit(self.sprite, (
                box_width // 2 - self.sprite.get_width() // 2,
                80
            ))

            # แสดงตรงกลางหน้าจอ
            box_rect = box.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            self.screen.blit(box, box_rect)

            pygame.display.update()
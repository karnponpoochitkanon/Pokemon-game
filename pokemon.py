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


class PokemonTeamPopup:
    def __init__(self, screen, team, font_path="Fonts/Arabica/ttf/Arabica.ttf"):
        self.screen = screen
        self.team = team
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(font_path, 24)
        self.title_font = pygame.font.Font(font_path, 32)

        self.card_width = 220
        self.card_height = 70
        self.padding = 20
        self.cols = 3
        self.rows = 2
        self.cards_per_page = self.cols * self.rows
        self.page = 0

        self.modal_width = self.cols * (self.card_width + self.padding) + self.padding
        self.modal_height = self.rows * (self.card_height + self.padding) + 120
        self.modal_rect = pygame.Rect(
            (WINDOW_WIDTH - self.modal_width) // 2,
            (WINDOW_HEIGHT - self.modal_height) // 2,
            self.modal_width,
            self.modal_height
        )

    def draw(self):
        pygame.draw.rect(self.screen, (255, 255, 255), self.modal_rect, border_radius=16)
        pygame.draw.rect(self.screen, (0, 0, 0), self.modal_rect, 3, border_radius=16)

        title = self.title_font.render("YOUR POKEMON TEAM", True, (0, 0, 0))
        self.screen.blit(title, (self.modal_rect.centerx - title.get_width() // 2, self.modal_rect.y + 20))

        start_x = self.modal_rect.x + self.padding
        start_y = self.modal_rect.y + 70

        start_index = self.page * self.cards_per_page
        end_index = min(start_index + self.cards_per_page, len(self.team))
        visible_team = self.team[start_index:end_index]

        for i, pokemon in enumerate(visible_team):
            row = i // self.cols
            col = i % self.cols

            x = start_x + col * (self.card_width + self.padding)
            y = start_y + row * (self.card_height + self.padding)
            card_rect = pygame.Rect(x, y, self.card_width, self.card_height)

            pygame.draw.rect(self.screen, (245, 255, 245), card_rect, border_radius=12)
            pygame.draw.rect(self.screen, (0, 100, 0), card_rect, 3, border_radius=12)

            name_text = self.font.render(pokemon.name.upper(), True, (0, 0, 0))
            self.screen.blit(name_text, (x + 10, y + 8))

            bar_width = self.card_width - 20
            bar_height = 18
            bar_x = x + 10
            bar_y = y + 35
            ratio = pokemon.hp / pokemon.max_hp
            pygame.draw.rect(self.screen, (0, 0, 0), (bar_x, bar_y, bar_width, bar_height), 2)
            pygame.draw.rect(self.screen, (0, 255, 0), (bar_x, bar_y, bar_width * ratio, bar_height))

            hp_text = self.font.render(f"{pokemon.hp}/{pokemon.max_hp} HP", True, (0, 0, 0))
            self.screen.blit(hp_text, (x + 10, bar_y + 17))

        # Page number
        page_text = self.font.render(f"PAGE {self.page + 1} / {(len(self.team)-1)//self.cards_per_page + 1}", True, (0, 0, 0))
        self.screen.blit(page_text, (self.modal_rect.centerx - page_text.get_width() // 2, self.modal_rect.bottom - 35))

        # Arrows
        arrow_y = self.modal_rect.centery
        arrow_size = 20
        if self.page > 0:
            left_points = [
                (self.modal_rect.left + 10, arrow_y),
                (self.modal_rect.left + 10 + arrow_size, arrow_y - arrow_size // 2),
                (self.modal_rect.left + 10 + arrow_size, arrow_y + arrow_size // 2),
            ]
            pygame.draw.polygon(self.screen, (0, 0, 0), left_points)

        if end_index < len(self.team):
            right_points = [
                (self.modal_rect.right - 10, arrow_y),
                (self.modal_rect.right - 10 - arrow_size, arrow_y - arrow_size // 2),
                (self.modal_rect.right - 10 - arrow_size, arrow_y + arrow_size // 2),
            ]
            pygame.draw.polygon(self.screen, (0, 0, 0), right_points)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_ESCAPE, pygame.K_LSHIFT, pygame.K_RSHIFT]:
                        running = False
                    elif event.key == pygame.K_RIGHT:
                        max_page = (len(self.team) - 1) // self.cards_per_page
                        self.page = min(self.page + 1, max_page)
                    elif event.key == pygame.K_LEFT:
                        self.page = max(self.page - 1, 0)

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
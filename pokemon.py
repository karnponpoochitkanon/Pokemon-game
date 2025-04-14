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
        self.card_height = 220
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
        label_rect = pygame.Rect(x, y, text.get_width() + 12, text.get_height() + 6)
        pygame.draw.rect(self.screen, color_map.get(element_type, (180, 180, 180)), label_rect, border_radius=6)
        pygame.draw.rect(self.screen, (0, 0, 0), label_rect, 1, border_radius=6)
        self.screen.blit(text, (x + 6, y + 3))

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

            # ✅ กำหนดพื้นหลัง
            if pokemon.hp <= 0:
                inner_color = (255, 220, 220)  # แดงอ่อนถ้าเลือดหมด
            else:
                inner_color = (255, 255, 255)

            # ✅ กำหนดสีกรอบ
            if pokemon.hp <= 0 and index == self.selected_index:
                border_color = (255, 0, 0)  # เลือก + เลือดหมด = กรอบแดง
            elif index == self.selected_index:
                border_color = (255, 204, 0)  # เลือกปกติ = กรอบเหลือง
            else:
                border_color = (0, 0, 0)  # ไม่เลือก = ดำ

            pygame.draw.rect(self.screen, inner_color, card_rect, border_radius=12)
            pygame.draw.rect(self.screen, border_color, card_rect, 3, border_radius=12)

            # ภาพโปเกม่อน
            sprite = pygame.image.load(f"image/pokemon/{pokemon.name}.png").convert_alpha()
            sprite = pygame.transform.scale(sprite, (self.sprite_scale, self.sprite_scale))
            self.screen.blit(sprite, (x + (self.card_width - self.sprite_scale) // 2, y + 10))

            # ชื่อ
            name_surf = self.font.render(pokemon.name.upper(), True, (0, 0, 0))
            self.screen.blit(name_surf, (x + (self.card_width - name_surf.get_width()) // 2, y + 120))

            # ธาตุ
            self.draw_type_label(pokemon.element_type, x + (self.card_width - 60) // 2, y + 160)

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

            # วาดกรอบโปเกม่อนพร้อมไฮไลต์
            start_index = self.page * self.cards_per_page
            end_index = min(start_index + self.cards_per_page, len(self.pokemon_list))
            visible_pokemon = self.pokemon_list[start_index:end_index]
            start_x = self.modal_rect.x + self.padding
            y = self.modal_rect.y + 60

            for i, pokemon in enumerate(visible_pokemon):
                index = start_index + i
                x = start_x + i * (self.card_width + self.padding)
                card_rect = pygame.Rect(x, y, self.card_width, self.card_height)

                if pokemon.hp <= 0 and index == self.selected_index:
                    border_color = (255, 0, 0)
                    bg_color = (255, 230, 230)
                elif pokemon.hp <= 0:
                    border_color = (0, 0, 0)
                    bg_color = (255, 230, 230)
                elif index == self.selected_index:
                    border_color = (255, 204, 0)
                    bg_color = (255, 255, 255)
                else:
                    border_color = (0, 0, 0)
                    bg_color = (255, 255, 255)

                pygame.draw.rect(self.screen, bg_color, card_rect, border_radius=12)
                pygame.draw.rect(self.screen, border_color, card_rect, 3, border_radius=12)

                sprite = pygame.image.load(f"image/pokemon/{pokemon.name}.png").convert_alpha()
                sprite = pygame.transform.scale(sprite, (self.sprite_scale, self.sprite_scale))
                self.screen.blit(sprite, (x + (self.card_width - self.sprite_scale) // 2, y + 10))

                name_surf = self.font.render(pokemon.name.upper(), True, (0, 0, 0))
                self.screen.blit(name_surf, (x + (self.card_width - name_surf.get_width()) // 2, y + 120))

                self.draw_type_label(pokemon.element_type, x + (self.card_width - 60) // 2, y + 160)

            # กล่อง error message
            if error_message and pygame.time.get_ticks() - error_timer < 2000:
                font = pygame.font.Font("Fonts/Arabica/ttf/Arabica.ttf", 32)
                msg_text = "This Pokemon has no HP!"
                msg = font.render(msg_text, True, (255, 0, 0))

                box_width = msg.get_width() + 60
                box_height = msg.get_height() + 30
                box = pygame.Surface((box_width, box_height))
                box.fill((255, 240, 240))
                pygame.draw.rect(box, (255, 0, 0), box.get_rect(), 4)

                # 👇 ปรับตำแหน่งให้กล่องอยู่กลางพอดี
                box_rect = box.get_rect(center=(WINDOW_WIDTH // 2, self.modal_rect.bottom + 40))
                self.screen.blit(box, box_rect)
                self.screen.blit(msg, msg.get_rect(center=box_rect.center))

            pygame.display.update()
            self.clock.tick(60)

class PokemonTeamPopup:
    def __init__(self, screen, team, font_path="Fonts/Arabica/ttf/Arabica.ttf"):
        self.screen = screen
        self.team = team
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(font_path, 28)
        self.title_font = pygame.font.Font(font_path, 32)

        self.card_width = 200
        self.card_height = 100
        self.padding = 20
        self.rows = 2
        self.cols = 3

        self.modal_width = self.cols * (self.card_width + self.padding) + self.padding
        self.modal_height = self.rows * (self.card_height + self.padding) + self.padding + 60
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

        for i, pokemon in enumerate(self.team):
            row = i // self.cols
            col = i % self.cols

            x = start_x + col * (self.card_width + self.padding)
            y = start_y + row * (self.card_height + self.padding)
            card_rect = pygame.Rect(x, y, self.card_width, self.card_height)

            # พื้นหลัง
            pygame.draw.rect(self.screen, (245, 255, 245), card_rect, border_radius=12)
            pygame.draw.rect(self.screen, (0, 100, 0), card_rect, 3, border_radius=12)

            # ชื่อ
            name_text = self.font.render(pokemon.name.upper(), True, (0, 0, 0))
            self.screen.blit(name_text, (x + 10, y + 10))

            # แถบ HP
            bar_width = self.card_width - 20
            bar_height = 18
            bar_x = x + 10
            bar_y = y + 50
            ratio = pokemon.hp / pokemon.max_hp
            pygame.draw.rect(self.screen, (0, 0, 0), (bar_x, bar_y, bar_width, bar_height), 2)
            pygame.draw.rect(self.screen, (0, 255, 0), (bar_x, bar_y, bar_width * ratio, bar_height))

            hp_text = self.font.render(f"{pokemon.hp}/{pokemon.max_hp} HP", True, (0, 0, 0))
            self.screen.blit(hp_text, (x + 10, bar_y + 24))

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                        running = False

            self.draw()
            pygame.display.update()
            self.clock.tick(60)
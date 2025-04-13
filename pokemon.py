import pygame
from typing import List
from setting import WINDOW_WIDTH, WINDOW_HEIGHT
import sys

class Pokemon:
    def __init__(self, name, element_type="Normal"):
        self.name = name
        self.element_type = element_type

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
        ]

    def get_available_monsters(self):
        return [
            Pokemon("hitokage", "Fire"),
            Pokemon("zenigame", "Water"),
            Pokemon("fushigidane", "Grass"),
            Pokemon("eevee", "Normal"),
            Pokemon("furin", "Normal"),
            Pokemon("gus", "Normal")
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
        # Modal background
        pygame.draw.rect(self.screen, (255, 255, 255), self.modal_rect, border_radius=16)

        # Title
        title = self.font.render("CHOOSE YOUR POKEMON TO FIGHT", True, (0, 0, 0))
        self.screen.blit(title, (self.modal_rect.centerx - title.get_width() // 2, self.modal_rect.y + 20))

        # Draw each pokemon on current page
        start_index = self.page * self.cards_per_page
        end_index = min(start_index + self.cards_per_page, len(self.pokemon_list))
        visible_pokemon = self.pokemon_list[start_index:end_index]

        start_x = self.modal_rect.x + self.padding
        y = self.modal_rect.y + 60

        for i, pokemon in enumerate(visible_pokemon):
            index = start_index + i
            x = start_x + i * (self.card_width + self.padding)
            card_rect = pygame.Rect(x, y, self.card_width, self.card_height)

            border_color = (255, 204, 0) if index == self.selected_index else (0, 0, 0)
            pygame.draw.rect(self.screen, (255, 255, 255), card_rect, border_radius=12)
            pygame.draw.rect(self.screen, border_color, card_rect, 3, border_radius=12)

            sprite = pygame.image.load(f"image/pokemon/{pokemon.name}.png").convert_alpha()
            sprite = pygame.transform.scale(sprite, (self.sprite_scale, self.sprite_scale))
            self.screen.blit(sprite, (x + (self.card_width - self.sprite_scale) // 2, y + 10))

            name_surf = self.font.render(pokemon.name.upper(), True, (0, 0, 0))
            self.screen.blit(name_surf, (x + (self.card_width - name_surf.get_width()) // 2, y + 120))

            self.draw_type_label(pokemon.element_type, x + (self.card_width - 60) // 2, y + 160)

    def run(self):
        total_pages = (len(self.pokemon_list) - 1) // self.cards_per_page + 1

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
                        return self.pokemon_list[self.selected_index]

            self.draw()
            pygame.display.update()
            self.clock.tick(60)

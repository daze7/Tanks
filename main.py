import pygame
import sys
import os

pygame.init()
size = width, height = 800, 800
screen = pygame.display.set_mode(size)


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def print_text(message, x, y, font_color=(255, 255, 255), font_type='data/EE-Bellflower.ttf', font_size=30):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    screen.blit(text, (x, y))


class Button(pygame.sprite.Sprite):
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.inactive_color = (0, 0, 0)
        self.active_color = (150, 150, 150)

    def draw(self, x, y, message, action=None, font_size=50):
        click = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if x + self.w > mouse_pos[0] > x and y + self.h > mouse_pos[1] > y:
            pygame.draw.rect(screen, self.active_color, (x, y, self.w, self.h))
            if click[0] == 1:
                if action is not None:
                    action()
        else:
            pygame.draw.rect(screen, self.inactive_color, (x, y, self.w, self.h))
        print_text(message=message, x=x + 10, y=y + 10, font_size=font_size)


def main_menu():
    start_btn = Button(290, 70)
    settings_btn = Button(255, 70)
    quit_btn = Button(160, 70)
    main_menu_background = pygame.image.load("data/main_menu_background.png")
    show = True
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.blit(main_menu_background, (0, 0))
        print_text('Танчики', 50, 100, (255, 255, 255), 'data/EE-Bellflower.ttf', 100)
        start_btn.draw(50, 300, 'Начать игру', start_game)
        settings_btn.draw(50, 400, 'Настройки', options_menu)
        quit_btn.draw(50, 500, 'Выход', terminate)
        pygame.display.update()


def start_game():
    pass


def options_menu():
    pass


main_menu()
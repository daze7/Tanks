import pygame
import sys
import os
import tkinter as tk
from tkinter import *
from tkinter import ttk

pygame.init()
size = width, height = 800, 800
screen = pygame.display.set_mode(size)
fps = 60
current_volume = 1
show_main_menu = False
show_optoins_menu = False
show_game = False

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

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
    global show_main_menu
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
                    show_main_menu = False
                    action()
        else:
            pygame.draw.rect(screen, self.inactive_color, (x, y, self.w, self.h))
        print_text(message=message, x=x + 10, y=y + 10, font_size=font_size)


def main_menu():
    global show_main_menu
    start_btn = Button(290, 70)
    settings_btn = Button(255, 70)
    quit_btn = Button(160, 70)
    show_main_menu = True
    main_menu_background = pygame.image.load("data/main_menu_background.png")
    while show_main_menu:
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
    pygame.mixer.music.fadeout(2000)

    #pass
def check_sounds():
    global show_optoins_menu
    global master_volume
    global sounds_volume
    global music_volume
    f = open('data/config.txt')
    master_volume = float(f.readline().split('=')[1])
    sounds_volume = float(f.readline().split('=')[1])
    music_volume = float(f.readline().split('=')[1])
    f.close()

def options_menu():
    global show_optoins_menu
    global master_volume
    global sounds_volume
    global music_volume
    show_optoins_menu = True
    options_menu_background = pygame.image.load("data/options_menu_background.png")
    show = True
    back_btn = Button(170, 70)
    slider1 = 500 + (200 * master_volume)
    slider2 = 500 + (200 * sounds_volume)
    slider3 = 500 + (200 * music_volume)
    slider_rect1 = pygame.Rect(500, 115, 210, 20)
    slider_rect2 = pygame.Rect(500, 215, 210, 20)
    slider_rect3 = pygame.Rect(500, 315, 210, 20)
    while show_optoins_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.blit(options_menu_background, (0, 0))
        back_btn.draw(50, 600, 'В меню', main_menu)
        print_text('Общая громкость', 50, 100, (255, 255, 255), 'data/EE-Bellflower.ttf', 50)
        print_text('Громкость звуков', 50, 200, (255, 255, 255), 'data/EE-Bellflower.ttf', 50)
        print_text('Громкость музыки', 50, 300, (255, 255, 255), 'data/EE-Bellflower.ttf', 50)



        mouse_pos = pygame.mouse.get_pos()

        if slider_rect1.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0] != 0:
            # collision detection also needed here
            slider1 = pygame.mouse.get_pos()[0] - 10
            if slider1 < 500:
                slider1 = 500
            if slider1 > 700:
                slider1 = 700
            f = open('data/config.txt', 'w')
            value = (slider1 - 500) / 200
            master_volume = value
            f.write('master_volume=' + str(value) + '\n')
            f.write('sounds_volume=' + str(sounds_volume) + '\n')
            f.write('music_volume=' + str(music_volume) + '\n')
            f.close()
            pygame.mixer.music.set_volume(master_volume * music_volume)

        if slider_rect2.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0] != 0:
            # collision detection also needed here
            slider2 = pygame.mouse.get_pos()[0] - 10
            if slider2 < 500:
                slider2 = 500
            if slider2 > 700:
                slider2 = 700
            f = open('data/config.txt', 'w')
            value = (slider2 - 500) / 200
            sounds_volume = value
            f.write('master_volume=' + str(master_volume) + '\n')
            f.write('sounds_volume=' + str(value) + '\n')
            f.write('music_volume=' + str(music_volume) + '\n')
            f.close()

        if slider_rect3.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0] != 0:
            # collision detection also needed here
            slider3 = pygame.mouse.get_pos()[0] - 10
            if slider3 < 500:
                slider3 = 500
            if slider3 > 700:
                slider3 = 700
            f = open('data/config.txt', 'w')
            value = (slider3 - 500) / 200
            music_volume = value
            f.write('master_volume=' + str(master_volume) + '\n')
            f.write('sounds_volume=' + str(sounds_volume) + '\n')
            f.write('music_volume=' + str(value) + '\n')
            f.close()
            pygame.mixer.music.set_volume(master_volume * music_volume)

        pygame.draw.rect(screen, 'White', slider_rect1)
        pygame.draw.rect(screen, 'RED', pygame.Rect(slider1, 115, 20, 20))

        pygame.draw.rect(screen, 'WHITE', slider_rect2)
        pygame.draw.rect(screen, 'RED', pygame.Rect(slider2, 215, 20, 20))

        pygame.draw.rect(screen, 'WHITE', slider_rect3)
        pygame.draw.rect(screen, 'RED', pygame.Rect(slider3, 315, 20, 20))
        pygame.display.update()

check_sounds()
pygame.mixer.music.load('data/main_menu_music.wav')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(master_volume * music_volume)
print(master_volume, music_volume)

main_menu()
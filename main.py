import pygame
import sys
import os
import tkinter as tk
from tkinter import *
from tkinter import ttk

pygame.init()
size = width, height = 800, 800
screen = pygame.display.set_mode(size)
FPS = 60
clock = pygame.time.Clock()
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


# группы спрайтов
all_sprites = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
bullets_group = pygame.sprite.Group()

wall_images = load_image('texture/map/Tilemap/wall1.png')
tile_images = load_image('texture/map/Tilemap/sand1.png')
player_image = load_image('texture/tanks/player.png')
enemy_image = load_image('texture/tanks/Enemy.png')
#bullet_image = load_image()
tile_width = tile_height = 50


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

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.direction = direction
        if self.direction == 'right' or self.direction == 'left':
            self.rect.bottom += 30
            self.rect.centerx += 30
        self.speedy = -10

    def update(self):
        if self.direction == 'up':
            self.rect.y += self.speedy
        if self.direction == 'down':
            self.rect.y -= self.speedy
        if self.direction == 'right':
            self.rect.x -= self.speedy
        if self.direction == 'left':
            self.rect.x += self.speedy
        # убить, если он заходит за верхнюю часть экрана
        if self.rect.bottom < 0 or pygame.sprite.groupcollide(bullets_group, wall_group, True, False) or \
                pygame.sprite.groupcollide(bullets_group, enemy_group, True, True):
            self.kill()

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Wall(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(wall_group, all_sprites)
        self.image = wall_images
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, direction):
        super().__init__(player_group, all_sprites)
        self.x, self.y = pos_x * 50, pos_y * 50
        self.direction = direction
        self.image = player_image
        if self.direction == 'down':
            self.image = pygame.transform.rotate(player_image, 180)
        if self.direction == 'right':
            self.image = pygame.transform.rotate(player_image, 270)
        if self.direction == 'left':
            self.image = pygame.transform.rotate(player_image, 90)
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)

    def update(self, pos_x, pos_y):
        #print(self.x, self.y)
        x = (self.x + pos_x) // 50
        y = (self.y + pos_y) // 50
        self.x += pos_x
        self.y += pos_y
        self.image = player_image
        self.rect = self.image.get_rect().move(self.x, self.y)
        if pygame.sprite.groupcollide(player_group, wall_group, False, False) or self.x > 450 or self.y > 450 or \
                self.y < 0 or self.x < 0 or pygame.sprite.groupcollide(player_group, enemy_group, False, False):
            self.x -= pos_x
            self.y -= pos_y
        self.image = player_image
        self.direction = 'up'
        if pos_x == 0 and pos_y > 0:
            self.image = pygame.transform.rotate(player_image, 180)
            self.direction = 'down'
        if pos_x > 0 and pos_y == 0:
            self.image = pygame.transform.rotate(player_image, 270)
            self.direction = 'right'
        if pos_x < 0 and pos_y == 0:
            self.image = pygame.transform.rotate(player_image, 90)
            self.direction = 'left'
        self.rect = self.image.get_rect().move(self.x, self.y)

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top, self.direction)
        all_sprites.add(bullet)
        bullets_group.add(bullet)



class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(enemy_group, all_sprites)
        self.image = enemy_image
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)






def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile(x, y)
            elif level[y][x] == '#':
                Wall(x, y)
            elif level[y][x] == '@':
                Tile(x, y)
                new_player = Player(x, y, 'up')
                print(x, y)
            elif level[y][x] == '!':
                Tile(x, y)
                new_enemy = Enemy(x, y)

    # вернем игрока, а также размер поля в клетках
    return new_player, x, y
lev = load_level('map/1.txt')

def start_game():
    move_left = False
    move_right = False
    move_up = False
    move_down = False
    pygame.mixer.music.fadeout(2000)
    show_game = True
    #pygame.init()
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    player, level_x, level_y = generate_level(load_level('map/1.txt'))
    screen.fill((250, 250, 250))
    while show_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    move_up = True
                    move_down = False
                    move_right = False
                    move_left = False
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    move_up = False
                    move_down = True
                    move_right = False
                    move_left = False
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    move_up = False
                    move_down = False
                    move_right = True
                    move_left = False
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    move_up = False
                    move_down = False
                    move_right = False
                    move_left = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    move_up = False
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    move_down = False
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    move_right = False
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    move_left = False
        if move_right:
            player.update(2, 0)
        if move_left:
            player.update(-2, 0)
        if move_up:
            player.update(0, -2)
        if move_down:
            player.update(0, 2)
        bullets_group.update()
        screen.fill((0, 0, 0))
        tiles_group.draw(screen)
        wall_group.draw(screen)
        player_group.draw(screen)
        enemy_group.draw(screen)
        bullets_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
        #pygame.event.pump()
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

#game_start
check_sounds()
pygame.mixer.music.load('data/main_menu_music.wav')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(master_volume * music_volume)
#print(master_volume, music_volume)

main_menu()
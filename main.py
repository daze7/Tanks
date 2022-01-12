import sqlite3
import time
import random
import pygame
import sys
import os
import tkinter as tk
from tkinter import *
from tkinter import ttk

player_x = 0
player_y = 0
play = False
pygame.init()
size = width, height = 800, 700
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Танчики')
FPS = 60
clock = pygame.time.Clock()
current_volume = 1
show_main_menu = False
show_optoins_menu = False
show_game = False
show_authorization = False
autorization_complete = False
show_user_statistik = False
cheak_login = False
reg_complete = False
reg_error = False
cheak = False
blok_game = False
login_user = ''
COLOR_INACTIVE = pygame.Color('white')
COLOR_ACTIVE = pygame.Color('green')
FONT = pygame.font.Font('data/EE-Bellflower.ttf', 20)


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
exp_group = pygame.sprite.Group()

wall_images = load_image('texture/map/Tilemap/wall1.png')
tile_images = load_image('texture/map/Tilemap/sand1.png')
player_image = load_image('texture/tanks/player.png')
enemy_image = load_image('texture/tanks/Enemy.png')
exp1 = load_image('texture/tanks/Explosion_A.png')
exp2 = load_image('texture/tanks/Explosion_B.png')
exp3 = load_image('texture/tanks/Explosion_C.png')
exp4 = load_image('texture/tanks/Explosion_D.png')
exp5 = load_image('texture/tanks/Explosion_E.png')
exp6 = load_image('texture/tanks/Explosion_F.png')
exp7 = load_image('texture/tanks/Explosion_G.png')
exp8 = load_image('texture/tanks/Explosion_H.png')
exp_a = [exp1, exp2, exp3, exp4, exp5, exp6, exp7, exp8]
bullet_image = load_image('texture/tanks/bullet1.png')
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


def sign_in():
    global play, autorization_complete, cheak_login, cheak, show_authorization, show_user_statistik
    f = open('data/user_login.txt', 'r')
    a = f.readline()
    f.close()
    if a != '' and a != 'Введите логин':
        con = sqlite3.connect("data/database/users.db")
        cur = con.cursor()
        cur.execute(f'SELECT * FROM user WHERE login="{a}";')
        value = cur.fetchall()
        cur.close()
        con.close()
        if value != []:
            #print_text('Успешная авторизация!', 450, 200, font_size=25)
            cheak = True
            autorization_complete = True
            play = True
            show_authorization = False
            show_user_statistik = True

        else:
            #print_text('Проверте правильность ввода данных', 350, 200, font_size=25)
            cheak = True
            cheak_login = True


def sign_up():
    global reg_complete, reg_error, cheak
    f = open('data/user_login.txt', 'r')
    a = f.readline()
    f.close()
    if a != '' and a != 'Введите логин':
        con = sqlite3.connect("data/database/users.db")
        cur = con.cursor()
        cur.execute(f'SELECT * FROM user WHERE login="{a}";')
        value = cur.fetchall()
        if value != []:
            #print_text('Такой ник уже используется', 420, 200, font_size=25)
            cheak = True
            reg_error = True
        else:
            cur.execute(f"INSERT INTO user(login,bestscore) VALUES ('{a}', 0)")
            #print_text('Вы успешно зарегистрированны!', 420, 200, font_size=25)
            cheak = True
            reg_complete = True
            con.commit()
        cur.close()
        con.close()

def blok_start_game():
    global cheak, blok_game
    blok_game = True
    cheak = True

def restart_auth():
    global show_authorization, show_user_statistik, blok_game, play
    f = open('data/user_login.txt', 'w')
    f.write('')
    f.close()
    show_user_statistik = False
    blok_game = True
    play = False
    show_authorization = True


def main_menu():
    global show_main_menu, autorization_complete, cheak_login, reg_complete, reg_error, cheak, blok_game, \
        show_authorization, show_user_statistik
    start_btn = Button(290, 70)
    settings_btn = Button(255, 70)
    quit_btn = Button(160, 70)
    input_box_login = InputBox(480, 400, 120, 30, 'Введите логин')
    sign_in_btn = Button(75, 40)
    sign_up_btn = Button(215, 45)
    restart_authorization = Button(230, 45)
    value = None
    cheak_bd = True
    last = None
    show_main_menu = True
    show_authorization = True
    main_menu_background = pygame.image.load("data/main_menu_background.png")
    while show_main_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            input_box_login.handle_event(event)
        input_box_login.update()
        screen.blit(main_menu_background, (0, 0))
        if show_authorization:
            cheak_bd = True
            #pygame.draw.rect(screen, (255, 255, 255), (300, 400, 400, 300), 1)
            input_box_login.draw(screen)
            sign_in_btn.draw(445, 435, 'Войти', sign_in, font_size=20)
            sign_up_btn.draw(525, 435, 'Зарегистрироваться', sign_up, font_size=20)
            f = open('data/user_login.txt', 'w')
            f.write(input_box_login.text)
            f.close()
        if show_authorization is False and cheak_bd is True:
            cheak_bd = False
            con = sqlite3.connect("data/database/users.db")
            cur = con.cursor()
            f = open('data/user_login.txt', 'r')
            a = f.readline()
            cur.execute(f'SELECT * FROM user WHERE login="{a}";')
            value = cur.fetchall()
            f.close()
            cur.close()
            con.close()
        if show_user_statistik:
            f = open('data/user_login.txt', 'r')
            text = f'Добро пожаловать, {f.readline()}!'
            f.close()
            print_text(text, 450, 200, font_size=25)
            if value[0][2] > 0:
                print_text(f'Ваш лучший результат: {value[0][2]}', 460, 230, font_size=20)
            restart_authorization.draw(550, 600, 'Выход из аккаунта', restart_auth, font_size=25)
        if cheak:
            if not last:
                last = pygame.time.get_ticks()
            now = pygame.time.get_ticks()
            if autorization_complete is True and now - last <= 1500:
                print_text('Успешная авторизация!', 450, 100, font_size=25)
            elif cheak_login is True and now - last <= 1500:
                print_text('Проверте правильность ввода данных', 350, 200, font_size=25)
            elif reg_complete is True and now - last <= 1500:
                print_text('Вы успешно зарегистрированны!', 420, 200, font_size=25)
            elif reg_error is True and now - last <= 1500:
                print_text('Такой ник уже используется', 420, 200, font_size=25)
            elif blok_game is True and now - last <= 1500:
                print_text('Сначала авторизуйтесь!', 420, 200, font_size=25)
            else:
                cheak = False
                autorization_complete = False
                cheak_login = False
                reg_complete = False
                reg_error = False
                last = None
        print_text('Танчики', 50, 100, (255, 255, 255), 'data/EE-Bellflower.ttf', 100)
        if play:
            start_btn.draw(50, 300, 'Начать игру', start_game)
        else:
            start_btn.draw(50, 300, 'Начать игру', blok_start_game)
        settings_btn.draw(50, 400, 'Настройки', options_menu)
        quit_btn.draw(50, 500, 'Выход', terminate)
        pygame.display.update()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, type):
        pygame.sprite.Sprite.__init__(self, bullets_group)
        self.type = type
        self.image = bullet_image
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.crash_tank = pygame.mixer.Sound("data/crash_tank.wav")
        check_sounds()
        self.crash_tank.set_volume(master_volume * sounds_volume * 2)
        self.direction = direction
        if self.direction == 'right':
            self.image = pygame.transform.rotate(bullet_image, 270)
            self.rect.bottom += 40
            self.rect.centerx += 30
        if self.direction == 'left':
            self.image = pygame.transform.rotate(bullet_image, 90)
            self.rect.bottom += 40
            self.rect.centerx -= 30
        if self.direction == 'down':
            self.image = pygame.transform.rotate(bullet_image, 180)
            self.rect.bottom += 60
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
        if self.type == 'player':
            if pygame.sprite.spritecollide(self, wall_group, False, False):
                self.kill()
            else:
                roogi = pygame.sprite.spritecollide(self, enemy_group, False, False)
                if roogi:
                    expl = Explosion(roogi[0].rect.center)
                    self.crash_tank.play()
                    exp_group.add(expl)
                    self.kill()
                    roogi[0].kill()
                elif self.rect.bottom < 0 or self.rect.bottom > 500 or self.rect.x < 0 or self.rect.x > 500:
                    self.kill()
        else:
            if pygame.sprite.groupcollide(bullets_group, wall_group, False, False):
                self.kill()
            else:
                roogi = pygame.sprite.spritecollide(self, player_group, False, False)
                if roogi:
                    expl = Explosion(roogi[0].rect.center)
                    self.crash_tank.play()
                    exp_group.add(expl)
                    self.kill()
                    #roogi[0].kill()
                elif self.rect.bottom < 0 or self.rect.bottom > 500 or self.rect.x < 0 or self.rect.x > 500:
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
        global player_x
        global player_y
        super().__init__(player_group, all_sprites)
        self.last_shoot = 0
        self.x, self.y = pos_x * 50, pos_y * 50
        self.fair_player = pygame.mixer.Sound("data/fair-player.wav")
        check_sounds()
        self.fair_player.set_volume(master_volume * sounds_volume)
        player_x = pos_x
        player_y = pos_y
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
        global player_x
        global player_y
        # print(self.x, self.y)
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
        player_x = self.x // 50
        player_y = self.y // 50

    def shoot(self):
        now = pygame.time.get_ticks()
        if pygame.time.get_ticks() - self.last_shoot >= 400:
            self.fair_player.play()
            self.last_shoot = now
            bullet = Bullet(self.rect.centerx, self.rect.top, self.direction, 'player')
            all_sprites.add(bullet)
            bullets_group.add(bullet)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, direction):
        super().__init__(enemy_group, all_sprites)
        self.x, self.y = pos_x * 50, pos_y * 50
        self.last_shoot = 0
        self.tttime = 1
        self.direction = direction
        self.image = enemy_image
        self.last_update = 0
        self.fair_player = pygame.mixer.Sound("data/fair-player.wav")
        check_sounds()
        self.fair_player.set_volume(master_volume * sounds_volume)
        if self.direction == 'down':
            self.image = pygame.transform.rotate(enemy_image, 180)
        if self.direction == 'right':
            self.image = pygame.transform.rotate(enemy_image, 270)
        if self.direction == 'left':
            self.image = pygame.transform.rotate(enemy_image, 90)
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


    def possible_directions(self):
        where = []
        x = self.x
        y = self.y - 2
        self.rect = self.image.get_rect().move(x, y)
        g = pygame.sprite.spritecollide(self, enemy_group, False, False)
        if not(pygame.sprite.spritecollide(self, wall_group, False, False) or y > 450 or \
                y < 0 or pygame.sprite.spritecollide(self, player_group, False, False) or len(g) > 1):
            where.append('up')
        y = self.y + 2
        self.rect = self.image.get_rect().move(x, y)
        g = pygame.sprite.spritecollide(self, enemy_group, False, False)
        if not(pygame.sprite.spritecollide(self, wall_group, False, False) or y > 450 or \
                y < 0 or pygame.sprite.spritecollide(self, player_group, False, False) or len(g) > 1):
            where.append('down')
        y = self.y
        x = self.x + 2
        self.rect = self.image.get_rect().move(x, y)
        g = pygame.sprite.spritecollide(self, enemy_group, False, False)
        if not(pygame.sprite.spritecollide(self, wall_group, False, False) or x > 450 or \
                x < 0 or pygame.sprite.spritecollide(self, player_group, False, False) or len(g) > 1):
            where.append('right')
        x = self.x - 2
        self.rect = self.image.get_rect().move(x, y)
        g = pygame.sprite.spritecollide(self, enemy_group, False, False)
        if not(pygame.sprite.spritecollide(self, wall_group, False, False) or x > 450 or \
                x < 0 or pygame.sprite.spritecollide(self, player_group, False, False) or len(g) > 1):
            where.append('left')
        self.rect = self.image.get_rect().move(self.x, self.y)
        return where


    def can_shoot(self):
        x = self.x // 50
        y = self.y // 50
        print(x, y)
        if x == player_x or y == player_y:
            if y == player_y:
                if x > player_x:
                    self.direction = 'left'
                    self.image = pygame.transform.rotate(enemy_image, 90)
                else:
                    self.direction = 'right'
                    self.image = pygame.transform.rotate(enemy_image, 270)
                now = pygame.time.get_ticks()
                if pygame.time.get_ticks() - self.last_shoot >= 1000:
                    self.last_shoot = now
                    bullet = Bullet(self.rect.centerx, self.rect.top, self.direction, 'enemy')
                    fair_player = pygame.mixer.Sound("data/fair-player.wav")
                    check_sounds()
                    fair_player.set_volume(master_volume * sounds_volume)
                    self.fair_player.play()
                    all_sprites.add(bullet)
                    bullets_group.add(bullet)
            else:
                if y > player_y:
                    self.direction = 'up'
                else:
                    self.direction = 'down'
                    self.image = pygame.transform.rotate(enemy_image, 180)
                now = pygame.time.get_ticks()
                if pygame.time.get_ticks() - self.last_shoot >= 1000:
                    self.last_shoot = now
                    bullet = Bullet(self.rect.centerx, self.rect.top, self.direction, 'enemy')
                    all_sprites.add(bullet)
                    bullets_group.add(bullet)


    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 1000 * self.tttime:
            self.last_update = now
            self.tttime = random.randint(1, 5)
            direct = self.possible_directions()
            if len(direct) > 0:
                self.direction = random.choice(direct)
        self.can_shoot()
        self.image = enemy_image
        x = self.x
        y = self.y
        if self.direction == 'up':
            self.y -= 2
            self.rect = self.image.get_rect().move(self.x, self.y)
            g = pygame.sprite.spritecollide(self, enemy_group, False, False)
            if pygame.sprite.spritecollide(self, wall_group, False, False) or self.y > 450 or \
                    self.y < 0 or pygame.sprite.spritecollide(self, player_group, False, False) or len(g) > 1:
                self.last_update = 0
                self.y += 2
        elif self.direction == 'down':
            self.y += 2
            self.rect = self.image.get_rect().move(self.x, self.y)
            g = pygame.sprite.spritecollide(self, enemy_group, False, False)
            if pygame.sprite.spritecollide(self, wall_group, False, False) or self.y > 450 or \
                    self.y < 0 or pygame.sprite.spritecollide(self, player_group, False, False) or len(g) > 1:
                self.last_update = 0
                self.y -= 2
            self.image = pygame.transform.rotate(enemy_image, 180)
        elif self.direction == 'right':
            self.x += 2
            self.rect = self.image.get_rect().move(self.x, self.y)
            g = pygame.sprite.spritecollide(self, enemy_group, False, False)
            if pygame.sprite.spritecollide(self, wall_group, False, False) or self.x > 450 or \
                    self.x < 0 or pygame.sprite.spritecollide(self, player_group, False, False) or len(g) > 1:
                self.last_update = 0
                self.x -= 2
            self.image = pygame.transform.rotate(enemy_image, 270)
        elif self.direction == 'left':
            self.x -= 2
            self.rect = self.image.get_rect().move(self.x, self.y)
            g = pygame.sprite.spritecollide(self, enemy_group, False, False)
            if pygame.sprite.spritecollide(self, wall_group, False, False) or self.x > 450 or \
                    self.x < 0 or pygame.sprite.spritecollide(self, player_group, False, False) or len(g) > 1:
                self.last_update = 0
                self.x += 2
            self.image = pygame.transform.rotate(enemy_image, 90)
        self.rect = self.image.get_rect().move(self.x, self.y)


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = exp_a[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(exp_a):
                self.kill()
            else:
                center = self.rect.center
                self.image = exp_a[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.text == 'Введите логин':
                    self.text = ''
                self.active = not self.active
            else:
                self.active = False
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)


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
                # print(x, y)
            elif level[y][x] == '!':
                Tile(x, y)
                new_enemy = Enemy(x, y, 'down')

    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


lev = load_level('map/1.txt')


def start_game():
    pygame.mixer.music.fadeout(200)
    check_sounds()
    pygame.mixer.music.load('data/fon_game.mp3')
    pygame.mixer.music.play(-1)
    move_left = False
    move_right = False
    move_up = False
    move_down = False
    show_game = True
    # pygame.init()
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
                    #fair_player.play()
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
        enemy_group.update()
        exp_group.update()
        bullets_group.update()
        screen.fill((0, 0, 0))
        tiles_group.draw(screen)
        wall_group.draw(screen)
        player_group.draw(screen)
        enemy_group.draw(screen)
        exp_group.draw(screen)
        bullets_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
        #print(len(bullets_group))
        # pygame.event.pump()
    # pass


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


# game_start
check_sounds()
pygame.mixer.music.load('data/main_menu_music.wav')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(master_volume * music_volume)
# print(master_volume, music_volume)

main_menu()

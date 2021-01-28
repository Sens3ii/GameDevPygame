import pygame
from threading import Thread
import sys
import threading
import random
from enum import Enum
pygame.init()

JUMP_POWER = 6
GRAVITY = 0.2  # Сила, которая будет тянуть нас вниз


class Wall():
    def __init__(self, x, y, texture):
        self.x = x
        self.y = y
        self.width = 25
        self.height = 13
        self.texture = texture
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self):
        screen.blit(self.texture, (self.x, self.y))
        # pygame.draw.rect(screen, [0, 255, 0],
        #                  (self.x, self.y, self.width, self.height), 1)


class Gem():
    def __init__(self, x, y, texture):
        self.x = x
        self.y = y
        self.width = 25
        self.height = 25
        self.texture = texture
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self):
        screen.blit(self.texture, (self.x, self.y))
        pygame.draw.rect(screen, [0, 255, 0],
                         (self.x, self.y, self.width, self.height), 1)


class Buttons():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.choosed = (255, 255, 255)
        self.unchoosed = (56, 0, 209)

    def draw_rect(self, x, y, message, play=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if (x < mouse[0] < x + self.width) and (y < mouse[1] < y + self.height):
            # Рисую кнопки, чтобы видеть их область
            pygame.draw.rect(screen, self.choosed,
                             (x, y, self.width, self.height), 2)
            if click[0] == 1 and play is not None:
                play()

        else:
            pygame.draw.rect(screen, self.unchoosed,
                             (x, y, self.width, self.height), 2)

        print_text(message, x+10, y+10)

    def draw_circ(self, x, y, message, play, n):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if (x < mouse[0] < x + self.width) and (y < mouse[1] < y + self.height):
            # Рисую кнопки, чтобы видеть их область
            pygame.draw.circle(screen, self.choosed, (x+35, y+20), 30)
            if click[0] == 1 and play is not None:
                play(n)

        else:
            pygame.draw.circle(screen, self.unchoosed, (x+35, y+20), 30)

        print_text(message, x+10, y+10, font_color=(255, 0, 33))


def print_text(message, x, y, font_color=(204, 204, 0), font_type='BitDust One', font_size=25):
    font_type = pygame.font.SysFont(font_type, font_size)
    text = font_type.render(message, True, font_color)
    screen.blit(text, (x, y))


class Floor():
    def __init__(self, x, y, texture):
        self.x = x
        self.y = y
        self.width = 83
        self.height = 13
        self.texture = texture
        self.hitbox = pygame.Rect(self.x, self.y-1, self.width, self.height)

    def draw(self):
        screen.blit(self.texture, (self.x, self.y))
        pygame.draw.rect(screen, [0, 255, 0],
                         (self.x, self.y, self.width, self.height), 3)


# Персонажи
fire = pygame.image.load('img/fire.png')
fire_l = pygame.image.load('img/fire_left.png')
fire_r = pygame.image.load('img/fire_right.png')

water = pygame.image.load('img/water.png')
water_l = pygame.image.load('img/water_left.png')
water_r = pygame.image.load('img/water_right.png')


# Класс направлений
class Direction(Enum):
    UP = 'UP'
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'


MOVE_KEYS = {
    pygame.K_a: 'LEFT',
    pygame.K_d: 'RIGHT',
    pygame.K_w: 'UP'
}


class Type(Enum):
    FIRE = 'fire'
    WATER = "water"


person_images = {
    Type.FIRE: {
        Direction.UP: fire,
        Direction.LEFT: fire_l,
        Direction.RIGHT: fire_r
    },
    Type.WATER: {
        Direction.UP: water,
        Direction.LEFT: water_l,
        Direction.RIGHT: water_r
    },

}
# Меню игры
menu = pygame.image.load('img/menu.png')
map_view = pygame.image.load('img/map_view.png')
levels = pygame.image.load('img/Levels.jpg')


win = pygame.image.load('img/Win.png')
lose = pygame.image.load('img/Lose.png')

# Размер игры

screen = pygame.display.set_mode((800, 640))

background = pygame.Surface(screen.get_size())
background.fill((255, 255, 255))
pygame.display.set_caption('Fire and water')


screen_size = screen.get_size()

# Стены

wall_texture = pygame.image.load('img/wall_1.png')
wall2_texture = pygame.image.load('img/wall_2.png')
wall_wout = pygame.image.load('img/wall_wout.png')

# Углы

angle_l_1 = pygame.image.load('img/angle_l.png')
angle_r_1 = pygame.image.load('img/angle_r.png')

# Жидкости

liquid_fire = pygame.image.load('img/liquid_fire.png')
liquid_water = pygame.image.load('img/liquid_water.png')
liquid_both = pygame.image.load('img/liquid_both.png')

# Кнопки

button_1 = Buttons(165, 30)
button_2 = Buttons(85, 30)

button_3 = Buttons(30, 30)
button_4 = Buttons(30, 30)
button_5 = Buttons(30, 30)
button_6 = Buttons(30, 30)
button_7 = Buttons(30, 30)
button_8 = Buttons(180, 30)
button_9 = Buttons(180, 30)

# Стены

walls = []
gems = []
doors = []
door_woman = []
floors = []
characters = []

# Время
clock = pygame.time.Clock()  # create pygame clock object
mainloop = True
# desired max. framerate in frames per second.
FPS = 60
playtime = 0

# Двери
door_w = pygame.image.load('img/door_woman.png')
door_m = pygame.image.load('img/door_man.png')

gem_w = pygame.image.load('img/gem_blue.png')
gem_m = pygame.image.load('img/gem_red.png')


class Door():
    def __init__(self, x, y, texture):
        self.x = x
        self.y = y
        self.width = 56
        self.height = 63
        self.texture = texture
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, [0, 255, 0],
                         (self.x, self.y, self.width, self.height), 1)

    def draw(self):
        screen.blit(self.texture, (self.x, self.y))
        pygame.draw.rect(screen, [0, 255, 0],
                         (self.x, self.y, self.width, self.height), 3)


class Charachter():
    def __init__(self, x, y, type_, d_right=pygame.K_RIGHT, d_left=pygame.K_LEFT, d_up=pygame.K_UP):
        self.x = x
        self.score = 0
        self.y = y
        self.dy = 0
        self.dx = 0
        self.width = 34
        self.height = 50
        self.type = type_
        self.makeJump = False
        self.direction = Direction.UP
        self.KEY = {d_right: Direction.RIGHT,
                    d_left: Direction.LEFT, d_up: Direction.UP}
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.onGround = True

    def run(self, direction, time):
        if self.direction == Direction.RIGHT or self.direction == Direction.LEFT:
            self.dx = 4
        else:
            self.dx = 0

        self.change_direction(direction)
        if self.direction == Direction.LEFT:
            self.dx *= -1

        self.hitbox = pygame.Rect(
            round(self.x+2*self.dx), round(self.y), self.width, self.height)

        if self.onGround and self.direction == Direction.UP:
            self.dy = -JUMP_POWER

        self.x += self.dx
        for wall in walls:
            if self.hitbox.colliderect(wall.hitbox):
                self.x -= self.dx
                return

    def collider(self):
        for gem in gems:
            if gem.texture == gem_w and characters[0].hitbox.colliderect(gem.hitbox):
                gems.remove(gem)
                characters[0].score += 1
            if gem.texture == gem_m and characters[1].hitbox.colliderect(gem.hitbox):
                gems.remove(gem)
                characters[1].score += 1
        if not self.onGround:
            self.dy += GRAVITY
        self.hitbox = pygame.Rect(
            round(self.x), round(self.y+self.dy), self.width, self.height)
        pygame.draw.rect(screen, [0, 255, 0],
                         (round(self.x), round(self.y+self.dy), self.width, self.height), 1)
        self.y += self.dy
        self.onGround = False  # Мы не знаем, когда мы на земле((
        for wall in walls:
            if self.hitbox.colliderect(wall.hitbox):
                if self.dy > 0:
                    self.y -= self.dy
                    self.dy = 0
                    self.onGround = True
                if self.dy < 0:
                    self.y -= self.dy
                    self.dy = 0

    def draw(self):
        img = person_images[self.type][self.direction]
        screen.blit(img, (round(self.x-img.get_width()/5), round(self.y)))

    def change_direction(self, direction):
        self.direction = direction


def map(i):
    with open(f'maps/map_{i}/1.txt', mode='r') as file:
        j = 0
        for line in file:
            for i in range(len(line)):
                if line[i] == '@':
                    walls.append(Wall(i*25, j*25, wall2_texture))
                if line[i] == 'b':
                    gems.append(Gem(i*25, j*25, gem_w))
                if line[i] == 'r':
                    gems.append(Gem(i*25, j*25, gem_m))
                elif line[i] == '.':
                    walls.append(Wall(i*25, j*25, wall_wout))
                elif line[i] == '&':
                    walls.append(Wall(i*25, j*25, wall_texture))
                elif line[i] == '%':
                    doors.append(Door(i*25-10, j*25-38, door_m))
                elif line[i] == '*':
                    doors.append(Door(i*25-10, j*25-38, door_w))
                elif line[i] == '#':
                    floors.append(Floor(i*25, j*25, liquid_fire))
                elif line[i] == '!':
                    floors.append(Floor(i*25, j*25, liquid_water))
                elif line[i] == '-':
                    floors.append(Floor(i*25, j*25, liquid_both))
                elif line[i] == 'm':
                    characters.append(Charachter(i*25, j*25, Type.FIRE))
                elif line[i] == 'g':
                    characters.append(Charachter(
                        i*25, j*25, Type.WATER, pygame.K_d, pygame.K_a, pygame.K_w))
            j += 1


def start():

    is_ok = True
    while is_ok:
        screen.blit(menu, (0, 0))  # Заливаю картинку на экран
        button_1.draw_rect(350, 598, 'START THE GAME', choosing)
        pygame.display.flip()  # Обновляю картинку, чтобы черный экран превратился в меню
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_ok = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    is_ok = False
                    pygame.quit()


def you_win():
    is_ok = True
    while is_ok:
        screen.blit(win, (0, 0))
        button_8.draw_rect(350, 598, '<--Back to choosing', start)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_ok = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    is_ok = False
                    pygame.quit()


def you_lose():
    is_ok = True
    while is_ok:
        screen.blit(lose, (0, 0))
        button_9.draw_rect(350, 598, '<--Back to choosing', start)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_ok = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    is_ok = False
                    pygame.quit()


def choosing():
    is_ok = True
    while is_ok:
        screen.blit(levels, (0, 0))  # Заливаю картинку на экран
        button_2.draw_rect(15, 36, '<-BACK', start)
        button_3.draw_circ(345, 90, '1 level', game, 1)
        button_4.draw_circ(190, 305, '2 level', game, 2)
        button_5.draw_circ(483, 305, '3 level', game, 3)
        button_6.draw_circ(98, 520, '4 level', game, 4)
        button_7.draw_circ(593, 515, '5 level', game, 5)
        pygame.display.flip()  # Обновляю картинку, чтобы черный экран превратился в игру
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_ok = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    is_ok = False
                    pygame.quit()


def drawScore():
    font = pygame.font.SysFont('smaller.fon', 26)
    text1 = font.render(f'Fire:{characters[1].score}', 1, (255, 0, 0))
    text2 = font.render(f'Water:{characters[0].score}', 1, (50, 50, 255))
    screen.blit(text1, (680, 40))
    screen.blit(text2, (680, 60))


def game(n):
    is_ok = True
    characters.clear()
    floors.clear()
    doors.clear()
    walls.clear()
    gems.clear()
    map(n)
    print("ch[0]", characters[0].type)
    global playtime
    while is_ok:
        milliseconds = clock.tick(FPS)  # milliseconds passed since last frame
        # seconds passed since last frame (float)
        seconds = milliseconds / 1000.0
        playtime += seconds
        screen.blit(map_view, (0, 0))
        drawScore()
        for wall in walls:
            wall.draw()
        for gem in gems:
            gem.draw()
        for door in doors:
            door.draw()
        for fl in floors:
            fl.draw()
            if (fl.texture == liquid_both or fl.texture == liquid_water) and characters[1].hitbox.colliderect(fl.hitbox):
                you_lose()
            if (fl.texture == liquid_both or fl.texture == liquid_fire) and characters[0].hitbox.colliderect(fl.hitbox):
                you_lose()
        for i in characters:
            i.collider()
            i.draw()

        if characters[1].hitbox.colliderect(doors[0].hitbox) and characters[0].hitbox.colliderect(doors[1].hitbox):
            you_win()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_ok = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    is_ok = False
                    pygame.quit()
                    sys.exit()
                    return
        keys = pygame.key.get_pressed()
        for ch in characters:
            for k in ch.KEY:
                if keys[k]:
                    ch.run(ch.KEY[k], seconds)
                    break
            # else:
            #     ch.change_direction(Direction.UP)
        pygame.display.flip()


start()

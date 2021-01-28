import pygame
import random
pygame.init()

# ========================================================================================================================
# Settings
# ========================================================================================================================
winWidth = 800
winHeight = 640
win = pygame.display.set_mode((winWidth, winHeight))

# ========================================================================================================================
# Snake
# ========================================================================================================================


class Snake(object):
    def __init__(self):
        self.x = 56
        self.y = 56
        self.speed = [16, 0]  # dx,dy
        self.size = 1
        self.elements = [[self.x, self.y]]
        self.radius = 8
        self.up = False
        self.down = False
        self.right = True
        self.left = False
        for i in range(3):
            self.size += 1
            self.elements.append([self.x, self.y])

    def addSize(self):
        self.size += 1
        self.elements.append([self.x, self.y])

    def draw(self):
        for element in self.elements:
            pygame.draw.circle(win, (150, 0, 150), element, self.radius)

    def move(self):
        for i in range(1, self.size):
            self.elements[self.size-i][0] = self.elements[self.size-i-1][0]
            self.elements[self.size-i][1] = self.elements[self.size-i-1][1]
        self.elements[0][0] += self.speed[0]
        self.elements[0][1] += self.speed[1]

# ========================================================================================================================
# Walls
# ========================================================================================================================


def createWalls():
    for n in range(snake.radius, winWidth, snake.radius*2):
        pygame.draw.circle(win, (100, 100, 100), (n, 8), 8)
        walls.append([n, 8])
        pygame.draw.circle(win, (100, 100, 100), (n, winHeight - 8), 8)
        walls.append([n, winHeight - 8])

    for n in range(snake.radius, winHeight, snake.radius*2):
        pygame.draw.circle(win, (100, 100, 100), (8, n), 8)
        walls.append([8, n])
        pygame.draw.circle(win, (100, 100, 100), (winWidth - 8, n), 8)
        walls.append([winWidth - 8, n])

# ========================================================================================================================
# Monster
# ========================================================================================================================


class Monster():
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.radius = snake.radius
        self.color = color

    def draw(self):
        pygame.draw.circle(win, self.color, [self.x, self.y], self.radius)

# ========================================================================================================================
# Score
# ========================================================================================================================


def drawScore():
    global score
    font = pygame.font.SysFont('smaller.fon', 26)
    text = font.render(f'Score:{score}', 1, (255, 255, 255))
    win.blit(text, (716, 4))

# ========================================================================================================================
# Updating display
# ========================================================================================================================


def winUpdate():
    win.fill((0, 0, 0))
    createWalls()
    snake.move()
    snake.draw()
    for monster in monsters:
        monster.draw()
    drawScore()
    pygame.display.update()


# ========================================================================================================================
# Variables
# ========================================================================================================================
snake = Snake()
speed = snake.radius * 2
walls = []
monsters = []
gameOver = False
score = 0
lenX = 0
lenY = 0
fps = pygame.time.Clock()
randomDir = 1
# ========================================================================================================================
# Main game loop
# ========================================================================================================================
run = True
while run:
    fps.tick(12)
    winUpdate()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_d] and not snake.left:
        snake.right = True
        snake.up = snake.down = snake.left = False
        snake.speed = [speed, 0]
    elif keys[pygame.K_a] and not snake.right:
        snake.left = True
        snake.up = snake.down = snake.right = False
        snake.speed = [-speed, 0]
    elif keys[pygame.K_w] and not snake.down:
        snake.up = True
        snake.down = snake.right = snake.left = False
        snake.speed = [0, -speed]
    elif keys[pygame.K_s] and not snake.up:
        snake.down = True
        snake.up = snake.right = snake.left = False
        snake.speed = [0, speed]

    if monsters == []:
        monsterX = random.randrange(24, winWidth-24, 16)
        monsterY = random.randrange(24, winHeight-24, 16)
        if [monsterX,monsterY] not in snake.elements:
            monsters.append(Monster(monsterX, monsterY, (228, 130, 0)))

    for monster in monsters:
        if snake.elements[0] == [monster.x,monster.y]:
            monsters.clear()
            snake.addSize()
            score += 1

        if [monster.x,monster.y] in walls or monster.x >= 800 or monster.x <= 0 or monster.y >=600 or monster.y <=0:
            monsters.clear()

        lenX = snake.elements[0][0]-monster.x
        lenY = snake.elements[0][1]-monster.y
        r = random.randrange(0,1)
        if r == 0:
            randomDir = -1
        elif r == 1:
            randomDir = 1

        if lenX == 0:
            monster.x += speed * randomDir
            monster.x += speed * randomDir

        elif lenY == 0:
            monster.y +=speed * randomDir
            monster.y +=speed * randomDir

    if snake.elements[0] in snake.elements[1:] or snake.elements[0] in walls:
        gameOver = True
        run = False

# ========================================================================================================================
# Game menu(or i'm lazy)
# ========================================================================================================================
pygame.quit()

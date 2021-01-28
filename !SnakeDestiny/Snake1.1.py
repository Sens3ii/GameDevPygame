import pygame
import random
pygame.init()

# ========================================================================================================================
# Settings
# ========================================================================================================================
winWidth = 800
winHeight = 640
win = pygame.display.set_mode((winWidth, winHeight))
bg = pygame.image.load('bg.jpg')
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


def wallsDraw():
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
# Functions
# ========================================================================================================================
def spawnMonster():
    if monsters == []:
        monsterX = random.randrange(24, winWidth-24, 16)
        monsterY = random.randrange(24, winHeight-24, 16)
        if [monsterX, monsterY] not in snake.elements:
            monsters.append(Monster(monsterX, monsterY, (228, 130, 0)))


def drawScore():
    global score
    font = pygame.font.SysFont('ComicSans', 23)
    text = font.render(f'Score:{score}', 1, (255, 255, 255))
    win.blit(text, (20, 20))


def drawFails():
    global fails
    font = pygame.font.SysFont('ComicSans', 23)
    text = font.render(f'Fails:{fails}', 1, (255, 255, 255))
    win.blit(text, (20, 40))


def drawMaxScore():
    global maxScore, score
    if score > maxScore:
        maxScore = score
    font = pygame.font.SysFont('ComicSans', 23)
    text = font.render(f'MaxScore:{maxScore}', 1, (255, 255, 255))
    win.blit(text, (20, 60))


# ========================================================================================================================
# Updating display
# ========================================================================================================================


def winUpdate():
    win.blit(bg, (0, 0))
    wallsDraw()
    snake.move()
    snake.draw()
    for monster in monsters:
        monster.draw()

    drawScore()
    drawFails()
    drawMaxScore()

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
fails = 0
maxScore = 0
FPS = 15
clock = pygame.time.Clock()
run = True
# ========================================================================================================================
# MainCycles
# ========================================================================================================================

# main game cycle
def runGame():
    global run, speed, monsters, score, gameOver
    while run:
        ms = clock.tick(FPS) # FPS - fps, ms - millsec between frames
        winUpdate() # for updating objects on display
        spawnMonster() # spawn fruit(s)
        
        # for quit game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # movement
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

        for monster in monsters:  # Collision with monsters
            if snake.elements[0] == [monster.x, monster.y]:
                monsters.remove(monster)
                snake.addSize()
                score += 1

        # Collision with snake,walls
        if snake.elements[0] in snake.elements[1:] or snake.elements[0] in walls:
            gameOver = True
            run = False


runGame()

# cycle for restart game
run2 = True
while run2:
    if gameOver:
        monsters = []
        snake.right = True
        snake.up = snake.down = snake.left = False
        snake.speed = [speed, 0]
        snake.x = 56
        snake.y = 56
        snake.size = 1
        snake.elements = [[snake.x, snake.y]]
        for i in range(3):
            snake.size += 1
            snake.elements.append([snake.x, snake.y])

        fails += 1
        score = 0
        run = True
        gameOver = False
        runGame()


pygame.quit()

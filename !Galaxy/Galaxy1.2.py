import pygame
import random
import sys
pygame.init()
# ========================================================================================================================
# Settings
# ========================================================================================================================
winWidth = 800
winHeight = 600
win = pygame.display.set_mode((winWidth, winHeight))
pygame.display.set_caption("Galaxy")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)
# ========================================================================================================================
# Textures
# ========================================================================================================================
heroSpr = []
for i in range(11):
    heroSpr.append(pygame.image.load(f'anim/hero/heroSpr{i}.png'))
enemySpr = []
for i in range(8):
    enemySpr.append(pygame.image.load(f'anim/enemy1/enemy1Spr{i}.png'))
bulletSpr = []
for i in range(8):
    bulletSpr.append(pygame.image.load(f'anim/bullet/bulletSpr{i}.png'))
bg = pygame.image.load('bg.jpg')
explSpr = []
for i in range(10):
    explSpr.append(pygame.image.load(
        f'anim/explosion/exp{i}.png'))
# ========================================================================================================================
# Sounds
# ========================================================================================================================
# from NieR: Automata (Ending E)
pifpafSnd = pygame.mixer.Sound('audio/pifpaf.wav')
pygame.mixer.music.load('audio/soundtrack/NierAutomata.mp3')
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)
# ========================================================================================================================
# Hero
# ========================================================================================================================


class Hero(object):
    def __init__(self, x, y, width, height, sprite, speed, dir):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.up = True
        self.down = False
        self.left = False
        self.right = False
        self.sprite = sprite
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.limit = limit
        self.dir = dir
        self.count = 0

    def draw(self):
        win.blit(self.sprite[self.count], (self.x, self.y))

    def direction(self, right=False, left=False, down=False, up=False):
        self.right = right
        self.left = left
        self.up = up
        self.down = down

    def move(self):
        if self.right:
            self.x += self.speed
            self.count += 1
        elif self.left:
            self.x -= self.speed
            self.count += 1
        if self.count > 10:
            self.count = 0

    def explosion(self):
        for i in explSpr:
            win.blit(i, (self.x, self.y))
            pygame.display.update()
# ========================================================================================================================
# Enemy
# ========================================================================================================================


class Enemy(Hero):

    def move(self):
        self.x += self.speed * self.dir
        if self.x < 30 or self.x > 736:
            self.x -= self.speed * self.dir
            self.y += self.speed
            self.limit += self.speed
            if self.limit >= 12*self.speed:
                self.limit = 0
                self.dir = self.dir * -1
        self.count += 1
        if self.count > 7:
            self.count = 0

# ========================================================================================================================
# Bullet
# ========================================================================================================================


class Bullet(object):
    def __init__(self, x, y, width, height, up=False, down=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 40
        self.color = (200, 30, 30)
        self.down = down
        self.up = up
        self.count = 0
        self.sprite = bulletSpr

    def draw(self):
        win.blit(self.sprite[self.count], (self.x, self.y))

    def move(self):
        if self.up:
            self.y -= self.speed
            self.count += 1
        elif self.down:
            self.y += self.speed
            self.count += 1
        if self.count > 7:
            self.count = 0
# ========================================================================================================================
# Updating frames on display
# ========================================================================================================================


def redrawWin():
    #win.fill((0, 0, 0))
    win.blit(bg, (0, 0))
    drawScore()
    myHero.draw()
    for enemy in enemyList:
        enemy.draw()
        enemy.move()
    for bullet in bulletList:
        bullet.move()
        bullet.draw()
    pygame.display.update()


# ========================================================================================================================
# Any functions
# ========================================================================================================================
def drawScore():
    global score
    font = pygame.font.SysFont('smaller.fon', 26)
    text = font.render(f'Score:{score}', 1, (255, 255, 255))
    win.blit(text, (716, 4))


def winGame():
    while True:
        win.fill((0, 0, 0))
        font = pygame.font.SysFont('smaller.fon', 50)
        if score < 50:
            winText = font.render(f'Play more', 1, (255, 0, 0))
        elif score >= 50 and score < 100:
            winText = font.render(f'Try again', 1, (255, 255, 255))
        elif score >= 100 and score < 180:
            winText = font.render(f'Well done!', 1, (255, 255, 255))
        elif score >= 180 and score < 250:
            winText = font.render(f'Good job!', 1, (255, 255, 255))
        elif score >= 250 and score < 300:
            winText = font.render(f'You definitely PRO', 1, (255, 255, 255))
        elif score >= 300:
            # Even I didn't take this
            winText = font.render(
                f'Oh God! Cybersport!!!!', 1, (255, 255, 255))

        scoreText = font.render(f'Score: {score}/300', 1, (255, 255, 255))
        win.blit(winText, (winWidth//2 - winText.get_width()//2, 200))
        win.blit(scoreText, (winWidth//2 - winText.get_width()//2, 250))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


def loseGame():
    while True:
        win.fill((0, 0, 0))
        font = pygame.font.SysFont('smaller.fon', 60)
        winText = font.render(f'Game over', 1, (255, 255, 255))
        scoreText = font.render(f'Score: {score}/300', 1, (255, 255, 255))
        win.blit(winText, (winWidth//2 - winText.get_width()//2, 200))
        win.blit(scoreText, (winWidth//2 - winText.get_width()//2, 250))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


def spawnEnemy(enemyList):
    global spawnDelay, score, enemyLimit, scoreLimit
    if len(enemyList) < enemyLimit and spawnDelay + 1000 < pygame.time.get_ticks() and score != scoreLimit:
        enemyX = random.randint(64, 736)
        enemyY = random.randint(8, 64)
        dirChange = random.randrange(0, 2)
        if dirChange == 0:
            dir = 1
        elif dirChange == 1:
            dir = -1
        enemyList.append(Enemy(enemyX, enemyY, 32, 32, enemySpr, 6, dir))
        spawnDelay = pygame.time.get_ticks()
# ========================================================================================================================
# Any variables
# ========================================================================================================================


limit = 0
fps = pygame.time.Clock()
myHero = Hero(416, 512, 32, 32, heroSpr, 8, dir)
score = 0
bulletList = []
timeDelay = pygame.time.get_ticks()
gunReload = 250
gameOver = False
enemyList = []
spawnDelay = pygame.time.get_ticks()
enemyLimit = 8
scoreLimit = 300
# ========================================================================================================================
# Game loop
# ========================================================================================================================
game = True
while game:
    fps.tick(30)
    redrawWin()
    spawnEnemy(enemyList)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

    if keys[pygame.K_d] and myHero.x < winWidth - myHero.width - myHero.speed:
        myHero.direction(right=True)
        myHero.move()
    elif keys[pygame.K_a] and myHero.x > 0:
        myHero.direction(left=True)
        myHero.move()
    if keys[pygame.K_SPACE] and bulletList == [] and timeDelay + gunReload < pygame.time.get_ticks():
        pifpafSnd.play()
        timeDelay = pygame.time.get_ticks()
        bulletList.append(Bullet(myHero.x + myHero.width //
                                 2 - 5, myHero.y+16, 9, 16, up=True))
    for bullet in bulletList:
        if bullet.y < 8:
            bulletList.clear()
        for enemy in enemyList:
            if bullet.y >= enemy.y and bullet.y <= enemy.y + enemy.height and bullet.x+bullet.width >= enemy.x and bullet.x <= enemy.x+enemy.width:
                bulletList.clear()
                enemyList.remove(enemy)
                enemy.explosion()
                score += 1
            if enemy.y >= 480:
                game = False
                gameOver = True
    if score >= 300:
        game = False

if gameOver == False:
    winGame()
elif gameOver == True:
    loseGame()

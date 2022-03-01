import time

import pygame
import random
import math

# Game Start
pygame.init()

# Screen
screen = pygame.display.set_mode((400, 650))

# Title and window
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('spaceshippixel.png')
pygame.display.set_icon(icon)
bg = pygame.image.load('pond.jpg')

# player
playerImg = pygame.image.load('duck_64.png')
playerX = 170
playerY = 550
X_changes = 0

# enemy
EnemyImg = []
EnemyX = []
EnemyY = []
X_enemy_changes = []
Y_enemy_changes = []
num_of_enemy = 5
for i in range(num_of_enemy):
    EnemyImg.append(pygame.image.load('clown-fish.png'))
    EnemyX.append(random.randint(0, 400))
    EnemyY.append(random.randint(50, 150))
    X_enemy_changes.append(0.3)
    Y_enemy_changes.append(0)

# Bullet
BulletImg = pygame.image.load('drop.png')
BulletX = 0
BulletY = playerY
Y_Bullet_changes = 0.75
Bullet_state = "ready"


# Score
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
text_x = 10
text_y = 10


def showscore(x, y):
    scoreon = font.render("Score:"+ str(score),True, (255, 255, 255))
    screen.blit(scoreon, (x, y))


# Collision
ExplosionImg = pygame.image.load('explosion.png')


def enemy(x, y, i):
    screen.blit(EnemyImg[i], (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def fire_bullet(x, y):
    global Bullet_state
    Bullet_state = "Fire"
    screen.blit(BulletImg, (x + 16, y - 10))


def collision(EnemyX, EnemyY, BulletX, BulletY):
    distance = math.sqrt((math.pow(EnemyX - BulletX, 2)) + (math.pow(EnemyY - BulletY, 2)))
    if distance < 30:
        return True
    else:
        return False


# Loop


running = True
clock = pygame.time.Clock()
while running:

    screen.fill((0, 16, 24))
    screen.blit(bg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # input
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                X_changes = -0.35
            if event.key == pygame.K_RIGHT:
                X_changes = 0.35
            if event.key == pygame.K_SPACE:
                if Bullet_state == "ready":
                    BulletX = playerX
                    fire_bullet(BulletX, BulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                X_changes = 0

    # player movement
    playerX += X_changes

    # boundaries
    if playerX > 345:
        playerX = 345
    if playerX < 0:
        playerX = 0

    # enemy movement zic-zac

    '''EnemyX[i] += X_enemy_changes[i]
    EnemyY[i] += Y_enemy_changes[i]
    if EnemyX[i] >= 345:
        X_enemy_changes[i] = -0.3
        Y_enemy_changes[i] = +0.1
    if EnemyX[i] <= 0:
        X_enemy_changes[i] = 0.3
        Y_enemy_changes[i] = +0.1'''
    # Enemy movement line
    for i in range(num_of_enemy):
        EnemyX[i] += X_enemy_changes[i]
        EnemyY[i] += Y_enemy_changes[i]
        if EnemyX[i] >= 345:
            X_enemy_changes[i] = -0.2
            EnemyY[i] += 30
        if EnemyX[i] <= 0:
            X_enemy_changes[i] = 0.2
            EnemyY[i] += 30

        # Collision
        if collision(EnemyX[i], EnemyY[i], BulletX, BulletY):
            screen.blit(ExplosionImg, (EnemyX[i], EnemyY[i]))
            time.sleep(0.1)
            Bullet_state = "ready"
            BulletY = playerY
            score += 1
            'print(score)'
            EnemyX[i] = random.randint(0, 344)
            EnemyY[i] = random.randint(50, 150)

        enemy(EnemyX[i], EnemyY[i], i)

    # Bullet Movement
    if Bullet_state == "Fire":
        fire_bullet(BulletX, BulletY)
        BulletY -= Y_Bullet_changes
    if BulletY <= 0:
        Bullet_state = "ready"
        BulletY = playerY

    player(playerX, playerY)
    showscore(text_x, text_y)
    pygame.display.update()
    clock.tick(900)

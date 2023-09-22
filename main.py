# Ctrl+Alt+l to format your code and make it better view
# Resource: flaticon.com , freepik.com


import pygame
import math
import random  # To appear enemy at random places
from pygame import mixer

# Intialize the pygame
pygame.init()  # must use in every game code

# creating screen
screen = pygame.display.set_mode((800, 600))  # (weidth,height)

# Background image
background = pygame.image.load("background.png")

# Music
mixer.music.load('backMusic.mp3')
mixer.music.play(-1)

# Title of the game
pygame.display.set_caption("SpaceWar")
icon = pygame.image.load("a01.png")
pygame.display.set_icon(icon)

# player
playerImage = pygame.image.load("ufo.png")
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImage = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemy = 4

for i in range(num_of_enemy):
    enemyImage.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 50))
    enemyX_change.append(0.8)
    enemyY_change.append(40)

# bullet
# Ready = You can't see the bullet
# Fire = The bullet will be moving
bulletImage = pygame.image.load("bullet.png")
bulletX = 370
bulletY = 480
bulletX_change = 0
bulletY_change = 2.5
bullet_state = "ready"

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game Over text
over_text = pygame.font.Font('freesansbold.ttf', 42)


def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (225, 225, 225))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = font.render(" GAME OVER " + str(score_value), True, (225, 225, 225))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImage, (x, y))  # blit means draw


def enemy(x, y, i):  # For enemy
    screen.blit(enemyImage[i], (x, y))  # blit means draw


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImage, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# gameloop
running = True
while running:
    # Changing Background
    screen.fill((0, 255, 255))

    # Background image load. blit draws the background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():  # every thing we do using our mouse & keyboard is an event.
        if event.type == pygame.QUIT:
            running = False

        # If keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -1.2
            if event.key == pygame.K_RIGHT:
                playerX_change = +1.2
            # Bullet calls
            if event.key == pygame.K_SPACE:
                bullet_sound = mixer.Sound("BulletMusic.mp3")
                bullet_sound.play()
                bulletX = playerX
                fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Movement of the ship
    # playerX+=.08

    # updating the display continuously
    playerX += playerX_change
    if playerX <= 0:  # checking for boundaries
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy movement
    for i in range(num_of_enemy):

        # Game Over
        if enemyY[i] > 300:
            for j in range(num_of_enemy):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:  # checking for boundaries
            enemyX_change[i] = 0.8
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.8
            enemyY[i] += enemyY_change[i]

        # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound("crash.mp3")
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 10
            print(score_value)
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 50)

        enemy(enemyX[i], enemyY[i], i)  # Calling for enemy movement changes

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)  # we have to call it after the screen printing
    show_score(textX, textY)
    pygame.display.update()  # must use in every game code

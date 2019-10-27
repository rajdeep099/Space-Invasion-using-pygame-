import pygame
import random
import math
from pygame import mixer

# Initialising the pygame module and starting it
pygame.init()

# Initialising the display screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('bg.png')

# Background music
mixer.music.load('bg.wav')
mixer.music.play(-1)  # -1 for looping of the background music

# Icons and Title
pygame.display.set_caption('firstGame')
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Declaring player that is to be used in the game
playerImg = pygame.image.load('space-invaders.png')
playerX = 370
playerY = 480
playerX_change = 0

# Declaring enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 10  # number of enemies

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(0, 100))
    enemyX_change.append(2)
    enemyY_change.append(40)

# Declaring bullet
# Ready - you cant see the bullet
# fire - when bullet is moving
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletY_change = 10
bulletState = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10  # coordinates of score text
textY = 10

# game over
overFont = pygame.font.Font('freesansbold.ttf', 64)


def game_over_text():
    overText = overFont.render("GAME OVER", True, (255, 255, 255))
    screen.blit(overText, (200, 250))


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


# Player function
def player(x, y):
    screen.blit(playerImg, (x, y))  # blit = draw


# Enemy function
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))  # blit = draw


# Bullet dynamics
def fire_bullet(x, y):
    global bulletState
    bulletState = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


# Collision detection
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Main loop / Game loop
running = True
while running:
    # Changing the screen color
    screen.fill((0, 0, 20))
    # background persist
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # checking a key is being pressed to control the movement of spaceship
        if event.type == pygame.KEYDOWN:  # it means a key has been pressed on keyboard
            if event.key == pygame.K_LEFT:
                playerX_change = -3

            if event.key == pygame.K_RIGHT:
                playerX_change = 3

            if event.key == pygame.K_SPACE:
                if bulletState == "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
                    bulletSound = mixer.Sound('gunshot.wav')
                    bulletSound.play()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:  # releasing of keys
                playerX_change = 0

    # Calling the player image
    playerX += playerX_change

    # Boundaries for spaceship
    if playerX < 0:
        playerX = 0
    elif playerX > 736:  # (80 - 64) because size of image is 64 pixels
        playerX = 736
    playerX += playerX_change

    # Boundaries for enemy and movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] < 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] > 736:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]

        # is collision happening ?
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)  # collision returns true and false
        if collision:
            collisionSound = mixer.Sound('explosion.wav')
            collisionSound.play()
            # reset bullets position and bulletState
            bulletY = 480
            bulletState = "ready"
            score_value += 1

            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(0, 100)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bulletState = "ready"

    if bulletState == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # function call
    player(playerX, playerY)
    show_score(textX, textY)
    # Need to update the display screen every time
    pygame.display.update()

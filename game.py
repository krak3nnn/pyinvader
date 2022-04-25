import pygame
import random
import math

pygame.init()

# setting up screen space
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# game title
pygame.display.set_caption("M6 - Space Invaders Replica")

# score tracker
score_val = 0
scoreX = 5
scoreY = 5
font = pygame.font.Font('freesansbold.ttf', 20)

# level tracker
current_lvl = 1
levelX = 5
levelY = 25

# end screen
game_over_font = pygame.font.Font('freesansbold.ttf', 64)


# show current score
def show_display(x, y):
    score = font.render("Points: " + str(score_val), True, (255, 255, 255))
    level = font.render("Level: " + str(current_lvl), True, (255, 255, 255))
    screen.blit(score, (x, y))
    screen.blit(level, (levelX, levelY))


# game over splash screen
def game_over():
    game_over_text = game_over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_over_text, (190, 250))


# player
playerImage = pygame.image.load('data/ship.png')
# player position when game starts
player_X = 370
player_Y = 525
player_Xchange = 0

# Invader
# list of invades that we will popular.
invaderImage = []
invader_X = []
invader_Y = []
invader_Xchange = []
invader_Ychange = []
no_of_invaders = 3

for num in range(no_of_invaders):
    # load three different variations of invaders
    alien = 'data/alien-' + str(num + 1) + '.png'
    invaderImage.append(pygame.image.load(alien))
    invader_X.append(random.randint(64, 737))
    invader_Y.append(random.randint(30, 180))
    invader_Xchange.append(1.2)
    invader_Ychange.append(50)

# Bullet
# rest - bullet is not moving
# fire - bullet is moving
bulletImage = pygame.image.load('data/bullet.png')
bullet_X = 0
bullet_Y = 500
bullet_Xchange = 0
bullet_Ychange = 3
bullet_state = "rest"


# Collision Concept
def isCollision(x1, x2, y1, y2):
    distance = math.sqrt((math.pow(x1 - x2, 2)) + (math.pow(y1 - y2, 2)))
    if distance <= 50:
        return True
    else:
        return False


def player(x, y):
    screen.blit(playerImage, (x - 16, y + 10))


def invader(x, y, i):
    screen.blit(invaderImage[i], (x, y))


def bullet(x, y):
    global bullet_state
    screen.blit(bulletImage, (x, y))
    bullet_state = "fire"


running = True
while running:

    # setting level 1 to black
    screen.fill((0, 0, 0))
    # when the score is greater than 3, move to level 2
    if score_val > 3:
        screen.fill((210, 180, 140))
        current_lvl = 2

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_Xchange = -1.7
            if event.key == pygame.K_RIGHT:
                player_Xchange = 1.7
            if event.key == pygame.K_SPACE:
                if bullet_state is "rest":
                    bullet_X = player_X
                    bullet(bullet_X, bullet_Y)
        if event.type == pygame.KEYUP:
            player_Xchange = 0

    player_X += player_Xchange
    for i in range(no_of_invaders):
        invader_X[i] += invader_Xchange[i]

    # bullet movement
    if bullet_Y <= 0:
        bullet_Y = 600
        bullet_state = "rest"
    if bullet_state is "fire":
        bullet(bullet_X, bullet_Y)
        bullet_Y -= bullet_Ychange

    # enemy movement
    for i in range(no_of_invaders):
        if invader_Y[i] >= 450:
            if abs(player_X - invader_X[i]) < 80:
                for j in range(no_of_invaders):
                    invader_Y[j] = 2000
                game_over()
                break

        if invader_X[i] >= 735 or invader_X[i] <= 0:
            invader_Xchange[i] *= -1
            invader_Y[i] += invader_Ychange[i]

        # collision logic
        collision = isCollision(bullet_X, invader_X[i], bullet_Y, invader_Y[i])
        if collision:
            score_val += 1
            bullet_Y = 600
            bullet_state = "rest"
            invader_X[i] = random.randint(64, 736)
            invader_Y[i] = random.randint(30, 200)
            invader_Xchange[i] *= -1

        invader(invader_X[i], invader_Y[i], i)

    # setting screen borders
    if player_X <= 16:
        player_X = 16;
    elif player_X >= 750:
        player_X = 750


    player(player_X, player_Y)
    show_display(scoreX, scoreY)
    pygame.display.update()

import pygame
import os
from time import sleep
import sys
import random

pygame.init()
pygame.mixer.init()
pygame.font.init()

# Pygame Screen
WIDTH, HEIGHT = 900, 500  # Pygame Screen Dimensions
WIN = pygame.display.set_mode((WIDTH, HEIGHT))


def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(__file__)

    return os.path.join(base_path, relative_path)


# Icon and Caption
pygame.display.set_caption("Space Shot !")
Icon = pygame.image.load(resource_path('assets/Ship1.png'))
pygame.display.set_icon(Icon)

# RGB COLORS AS VARIABLES
WHITE = (255, 255, 255)
RED = (255, 0, 0)
DARK_RED = (103, 0, 0)
BLUE = (0, 0, 255)
NAVY_BLUE = (0, 27, 60)
GREY = (116, 111, 104)
GREEN = (150, 255, 100)
YELLOW = (236, 255, 0)
CYAN = (70, 255, 248)
BLACK = (0, 0, 0)
LIGHT_GREEN = (133, 255, 164)
ORANGE = (255, 140, 0)

# The frames per second as a variable
FPS = 60

# The velocity of the character
VEL = 5

# Some variables for our character's bullets
BULLET_WIDTH, BULLET_HEIGHT = 5, 10
BULLET_VEL = 7
MAX_BULLETS = 3

# Creating events as variables for when we check if yellow,grey, or red are hit
YELLOW_HIT = pygame.USEREVENT + 1
GREY_HIT = pygame.USEREVENT + 2
RED_HIT = pygame.USEREVENT + 3

# All font usages
myfont = pygame.font.Font(resource_path('assets/OriginTech personal use.ttf'), 100)
Score = pygame.font.Font(resource_path('assets/freesansbold.ttf'), 20)
win = pygame.font.Font(resource_path('assets/freesansbold.ttf'), 90)
ENEMY_WAVE = pygame.font.Font(resource_path('assets/freesansbold.ttf'), 90)
wave_text = pygame.font.Font(resource_path('assets/freesansbold.ttf'), 20)
start = pygame.font.Font(resource_path('assets/freesansbold.ttf'), 70)
keys = pygame.font.Font(resource_path('assets/freesansbold.ttf'), 36)
health = pygame.font.Font(resource_path('assets/freesansbold.ttf'), 20)
ENEMYBOSSHEALTH = pygame.font.Font(resource_path('assets/freesansbold.ttf'), 20)

# Variables for what I shrunk images too
IMAGE_SCALE_WIDTH, IMAGE_SCALE_HEIGHT = 55, 40
E_I_W, E_I_H = 35, 35

# Background loading
Backgroundload = resource_path('assets/Background.png')
Background = pygame.image.load(Backgroundload).convert_alpha()
Background.convert()

# Main Character Loading and Shrinking
ShipLoad = resource_path('assets/Ship1.png')
GALAGA_SPACESHIP_IMAGE = pygame.image.load(ShipLoad).convert_alpha()
GALAGA_SPACESHIP = pygame.transform.scale(GALAGA_SPACESHIP_IMAGE, (IMAGE_SCALE_WIDTH, IMAGE_SCALE_HEIGHT))
GALAGA_SPACESHIP.convert()

# Level 5 Boss Loading and Shrinking
BossLoad = resource_path('assets/Boss.png')
Bosspng = pygame.image.load(BossLoad).convert_alpha()
Boss = pygame.transform.scale(Bosspng, (100, 100))
Boss.convert()

# Yellow/Green Insect Loading and Shrinking
ENEMYLOAD = resource_path('assets/Enemy.png')
ENEMY_INSECT_IMAGE = pygame.image.load(ENEMYLOAD).convert_alpha()
ENEMY_IMAGE = pygame.transform.scale(ENEMY_INSECT_IMAGE, (E_I_W, E_I_H)).convert_alpha()
ENEMY_IMAGE.convert()

# Butterfly Image Loading and Shrinking
ENEMY1LOAD = resource_path('assets/Enemy1.png')
ENEMY_INSECT_IMAGE_1 = pygame.image.load(ENEMY1LOAD)
ENEMY_IMAGE_1 = pygame.transform.scale(ENEMY_INSECT_IMAGE_1, (30, 30)).convert_alpha()
ENEMY_IMAGE_1.convert()

# Sound Effects Loading
bulletSoundload = resource_path('assets/GUN_FIRE-GoodSoundForYou-820112263 - Copy (2).mp3')
bulletSound = pygame.mixer.Sound(bulletSoundload)
deathSoundload = resource_path('assets/roblox-death-sound_1 - Copy.mp3')
deathSound = pygame.mixer.Sound(deathSoundload)
backgroundMusicload = resource_path('assets/epic-orchestra-the-commander-2608.mp3')
backgroundMusic = pygame.mixer.Sound(backgroundMusicload)
startMusicload = resource_path('assets/background-music-new-852.mp3')
startMusic = pygame.mixer.Sound(startMusicload)


def draw_window(grey, yellow, galaga_bullets, isCollided, bullet_hit, ENEMIES_SHOT_COUNT, red, RED_SHOT, bug_bullet,
                BIGENEMY,
                wave_count, GREY_HEALTH, BOSSHEALTH, boss_bullet, boss_bullet_1, boss_bullet_2):
    WIN.blit(Background, (0, 0))

    if wave_count == 5:
        BossHealth = ENEMYBOSSHEALTH.render('MONSTER HEALTH: ' + str(BOSSHEALTH), False, ORANGE)
        WIN.blit(Boss, (BIGENEMY.x, BIGENEMY.y))
        WIN.blit(BossHealth, (BIGENEMY.x - 50, BIGENEMY.y - 20))
    if not RED_SHOT:
        WIN.blit(ENEMY_IMAGE_1, (red.x, red.y))
    if isCollided:
        handle_collisions()
    if bullet_hit:
        WIN.blit(ENEMY_IMAGE, (yellow.x, yellow.y))
    if not bullet_hit:
        WIN.blit(ENEMY_IMAGE, (yellow.x, yellow.y))
    if not isCollided:
        WIN.blit(GALAGA_SPACESHIP, (grey.x, grey.y))
    for BOSSBULLET in boss_bullet:
        pygame.draw.rect(WIN, BLUE, BOSSBULLET)
    for BOSSBULLET1 in boss_bullet_1:
        pygame.draw.rect(WIN, BLUE, BOSSBULLET1)
    for BOSSBULLET2 in boss_bullet_2:
        pygame.draw.rect(WIN, BLUE, BOSSBULLET2)
    for enemy_bullet in bug_bullet:
        pygame.draw.rect(WIN, RED, enemy_bullet)
    for bullet in galaga_bullets:
        pygame.draw.rect(WIN, GREEN, bullet)
    HEALTH = health.render('Health: ' + str(GREY_HEALTH), False, CYAN)
    Wave_number = wave_text.render('Wave: ' + str(wave_count), False, BLUE)
    HIT_ENEMY_TEXT = Score.render('Score: ' + str(ENEMIES_SHOT_COUNT), False, GREEN)
    WIN.blit(HIT_ENEMY_TEXT, (800, 10))
    WIN.blit(HEALTH, (440, 10))
    WIN.blit(Wave_number, (10, 10))
    if isCollided:
        handle_collisions()

    pygame.display.update()


def player_controls(keys_pressed, grey):
    if keys_pressed[pygame.K_a] and grey.x - VEL > - 6:  # LEFT
        grey.x -= VEL
    if keys_pressed[pygame.K_d] and grey.x + VEL < 850:  # RIGHT
        grey.x += VEL
    if keys_pressed[pygame.K_w] and grey.y - VEL > 300:  # UP
        grey.y -= VEL
    if keys_pressed[pygame.K_s] and grey.y + VEL < HEIGHT - 40:  # DOWN
        grey.y += VEL


def handle_collisions():
    textsurface = myfont.render('YOU DIED !', False, DARK_RED)
    WIN.blit(textsurface, (200, 100))
    deathSound.play()

    pygame.display.update()
    sleep(3)
    run = False
    sys.exit()


def handle_bullets(galaga_bullets, yellow, bug_bullet, ENEMY_BULLET_VEL, boss_bullet, boss_bullet_1, boss_bullet_2,
                   grey, GREY_HEALTH, BOSSBULLETVEL):
    # Enemy Bullet
    for enemy_bullet in bug_bullet:
        enemy_bullet.y += ENEMY_BULLET_VEL
        if enemy_bullet.y > 500:
            bug_bullet.remove(enemy_bullet)

    # Boss bullet
    for BOSSBULLET in boss_bullet:
        BOSSBULLET.y += BOSSBULLETVEL
        BOSSBULLET.x -= BOSSBULLETVEL

        if BOSSBULLET.y > 500:
            boss_bullet.remove(BOSSBULLET)

    for BOSSBULLET1 in boss_bullet_1:
        BOSSBULLET1.y += BOSSBULLETVEL
        if BOSSBULLET1.colliderect(grey):
            GREY_HEALTH -= 2
        if BOSSBULLET1.y > 500:
            boss_bullet_1.remove(BOSSBULLET1)

    for BOSSBULLET2 in boss_bullet_2:
        BOSSBULLET2.y += BOSSBULLETVEL
        BOSSBULLET2.x += BOSSBULLETVEL

        if BOSSBULLET2.colliderect(grey):
            GREY_HEALTH -= 2

        if BOSSBULLET2.y > 500:
            boss_bullet_2.remove(BOSSBULLET2)

    # Player Bullet
    for bullet in galaga_bullets:
        bullet.y -= BULLET_VEL
        # if a bullet collides with
        if bullet.colliderect(yellow):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            galaga_bullets.remove(bullet)

        if bullet.y < 0 and len(galaga_bullets) > 0:
            galaga_bullets.remove(bullet)


def Winning():
    WIN.fill(BLACK)
    Win_Text = win.render('YOU WIN !', False, WHITE)
    WIN.blit(Win_Text, (200, 200))
    pygame.display.update()
    sleep(5)
    pygame.quit()
    sys.exit()


def main():
    global enemy_bullet
    global bullet



    RED_HEALTH = 3

    wave_count = 1
    WAVE = 20
    grey = GALAGA_SPACESHIP.get_rect()  # pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    grey.center = (440, 400)
    yellow = ENEMY_IMAGE.get_rect()
    yellow.center = (440, 0)  # pygame.Rect(100, 100, 40, 40)
    red = ENEMY_IMAGE_1.get_rect()
    bug_bullet = []
    galaga_bullets = []
    bullet_hit = False
    isCollided = False

    GREY_HEALTH = 5
    YELLOW_HEALTH = 1

    ENEMY_1_VEL = 1
    enemies = []
    ENEMY_VEL = 1
    ENEMIES_SHOT_COUNT = 0
    MAX_ENEMY_BULLET = 1
    ENEMY_BULLET_VEL = 4
    BIGENEMY = Boss.get_rect()

    BOSSHEALTH = 100
    boss_bullet = []
    boss_bullet_1 = []
    boss_bullet_2 = []
    BOSSVEL = 2
    BOSSBULLETVEL = 5

    RIGHTBOUNDARY = pygame.Rect(780, 0, 20, 500)
    LEFTBOUNDARY = pygame.Rect(0, 0, 20, 500)

    clock = pygame.time.Clock()
    run = True
    playing = True
    yellow.x = random.randint(0, 400)
    red.x = random.randint(401, 800)
    startMusic.play(loops=-1)

    # Start Screen
    while playing:
        WIN.fill(LIGHT_GREEN)
        WIN.blit(GALAGA_SPACESHIP, (440, 30))
        start_text = start.render('CLICK HERE TO START', False, WHITE)
        key_text = keys.render(' Keys are W A S D to move and space bar to shoot', False, WHITE)
        WIN.blit(start_text, (50, 200))
        WIN.blit(key_text, (10, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                playing = False
                startMusic.stop()
            if event.type == pygame.MOUSEBUTTONUP:
                playing = False
                startMusic.stop()

    backgroundMusic.play(loops=-1)
    BIGENEMY.y = 70
    # Main Game Loop
    while run:
        clock.tick(FPS)


        keys_pressed = pygame.key.get_pressed()
        player_controls(keys_pressed, grey)

        Insect_bullet = random.randint(1, 5)

        Bossbullet = random.randint(1, 2)
        Bossbullet1 = random.randint(1, 2)
        Bossbullet2 = random.randint(1, 2)

        # Setting 60 frames per second
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(galaga_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(grey.x + 23, grey.y + grey.height // 2 - 2, BULLET_WIDTH, BULLET_HEIGHT)
                    galaga_bullets.append(bullet)
                    bulletSound.play()
                if wave_count == 5:
                    if Bossbullet == 1 and Bossbullet1 == 1 and Bossbullet2 == 1:
                        BOSSBULLET = pygame.Rect(BIGENEMY.x + 23, BIGENEMY.y + BIGENEMY.height // 2 - 2, 10, 25)
                        BOSSBULLET1 = pygame.Rect(BIGENEMY.x + 45, BIGENEMY.y + BIGENEMY.height // 2 - 2, 10, 25)
                        BOSSBULLET2 = pygame.Rect(BIGENEMY.x + 70, BIGENEMY.y + BIGENEMY.height // 2 - 2, 10, 25)
                        boss_bullet.append(BOSSBULLET)
                        boss_bullet_1.append(BOSSBULLET1)
                        boss_bullet_2.append(BOSSBULLET2)

            if event.type == pygame.QUIT:
                run = False

            if not wave_count == 5:
                if Insect_bullet == 3 and len(bug_bullet) < MAX_ENEMY_BULLET:
                    enemy_bullet = pygame.Rect(red.x + 10, red.y + red.height // 2 - 2, BULLET_WIDTH, 15)
                    bug_bullet.append(enemy_bullet)

            if event.type == YELLOW_HIT:
                yellow.x = - 200
                YELLOW_HEALTH -= 1
                bullet_hit = True
                ENEMIES_SHOT_COUNT += 1
                yellow.y = 10
                yellow.x = random.randint(0, 450)

            if event.type == GREY_HIT:
                isCollided = True

            if event.type == RED_HIT:
                ENEMIES_SHOT_COUNT += 5
                red.x = -200
                red.y = 10
                red.x = random.randint(0, 900)

        if grey.colliderect(yellow):
            GREY_HEALTH -= 1
            yellow.y = 0

        if grey.colliderect(red):
            GREY_HEALTH -= 1
            red.y = 0
        if GREY_HEALTH == 0:
            pygame.event.post(pygame.event.Event(GREY_HIT))
            backgroundMusic.stop()
            deathSound.play()

        RED_SHOT = False
        WIN.blit(ENEMY_IMAGE_1, (red.x, red.y))
        WIN.blit(ENEMY_IMAGE, (yellow.x, yellow.y))
        enemies.append(yellow)
        enemies.append(red)

        if not wave_count == 5:
            BIGENEMY.x = 10000
            yellow.y += ENEMY_VEL
            yellow.x += ENEMY_VEL
            red.y += ENEMY_1_VEL
            red.x -= ENEMY_VEL
            if yellow.y < 0:
                yellow.y = 0
            if yellow.x >= 900 or yellow.x <= 0:
                yellow.y = 0
                yellow.x = random.randint(0, 900)
            if red.y >= 500:
                red.y = 0
            if red.x < 0 or red.x > 900:
                red.y = 0
                red.x = random.randint(0, 900)

        for enemy_bullet in bug_bullet:
            if grey.colliderect(enemy_bullet):
                GREY_HEALTH -= 1
                yellow.y = 0
                red.y = 0
                bug_bullet.remove(enemy_bullet)

        for BOSSBULLET in boss_bullet:
            if BOSSBULLET.colliderect(grey):
                GREY_HEALTH -= 2
        for BOSSBULLET1 in boss_bullet_1:
            if BOSSBULLET1.colliderect(grey):
                GREY_HEALTH -= 2
        for BOSSBULLET2 in boss_bullet_2:
            if BOSSBULLET2.colliderect(grey):
                GREY_HEALTH -= 2

        if GREY_HEALTH <= 0:
            pygame.event.post(pygame.event.Event(GREY_HIT))
            backgroundMusic.stop()
            deathSound.play()

        if RED_HEALTH == 0:
            RED_HEALTH += 3

        for bullet in galaga_bullets:
            if bullet.colliderect(BIGENEMY):
                BOSSHEALTH -= 1
                galaga_bullets.remove(bullet)
            if bullet.colliderect(red):
                RED_HEALTH = RED_HEALTH - 1
                galaga_bullets.remove(bullet)
                if RED_HEALTH == 0:
                    pygame.event.post(pygame.event.Event(RED_HIT))

        handle_bullets(galaga_bullets, yellow, bug_bullet, ENEMY_BULLET_VEL, boss_bullet, boss_bullet_1, boss_bullet_2,
                       grey, GREY_HEALTH, BOSSBULLETVEL)

        # Wave 2
        if ENEMIES_SHOT_COUNT >= WAVE:
            wave_count += 1
            WAVE += 50
            if wave_count == 3:
                ENEMY_1_VEL = 2
            if wave_count == 4:
                ENEMY_VEL = 2
            Levels = ENEMY_WAVE.render('Next Level !', False, WHITE)
            WIN.blit(Levels, (240, 240))
            pygame.display.flip()
            sleep(2)
            yellow.y = 0
            red.y = 0
        if wave_count == 5 and BIGENEMY.x == 10000:
            BIGENEMY.x = 70

        if wave_count == 5:
            yellow.y = - 2000
            red.y = - 2000
            BIGENEMY.x += BOSSVEL
            if BIGENEMY.colliderect(RIGHTBOUNDARY):
                BOSSVEL = -2
            if BIGENEMY.colliderect(LEFTBOUNDARY):
                BOSSVEL = 2

        if BOSSHEALTH <= 25:
            BOSSBULLETVEL = 6

        if BOSSHEALTH <= 0:
            ENEMIES_SHOT_COUNT += 200
            wave_count += 1

        if wave_count == 6:
            WIN.fill(GREEN)
            Win_Text = win.render('YOU WIN !', False, WHITE)
            WIN.blit(Win_Text, (200, 200))
            pygame.display.update()
            sleep(5)
            pygame.quit()
            sys.exit()

        draw_window(grey, yellow, galaga_bullets, isCollided, bullet_hit, ENEMIES_SHOT_COUNT, red, RED_SHOT,
                    bug_bullet, BIGENEMY, wave_count, GREY_HEALTH, BOSSHEALTH, boss_bullet, boss_bullet_1,
                    boss_bullet_2)

    pygame.quit()


if __name__ == "__main__":
    main()

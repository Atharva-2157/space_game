import pygame
import random

pygame.init()

SCREENWIDTH = 900
SCREENHEIGHT = 720

WINDOW = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption("Space Game")

EXIT_GAME = False
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (135, 206, 235)
GOLD = (255, 215, 0)
GREEN = (0, 255, 0)
FPS = 110
FPS_CLOCK = pygame.time.Clock()


def movePlaneBullet(bullet_list):
    for bullet in bullet_list:
        bullet[2] -= 1


def plotPlaneBullet(bullet_list, bullet_w, bullet_h):
    for bullet in bullet_list:
        pygame.draw.rect(WINDOW, YELLOW, [bullet[0], bullet[2], bullet_w, bullet_h])
        pygame.draw.rect(WINDOW, YELLOW, [bullet[1], bullet[2], bullet_w, bullet_h])


def checkPlaneBullet(bullet_list):
    for bullet in bullet_list:
        if bullet[2] <= 0:
            bullet_list.pop(0)


def PlotEnemy(multiple_enemy_list, enemy_size):
    for enemy in multiple_enemy_list:
        pygame.draw.rect(WINDOW, BLACK, [enemy[0], enemy[1], enemy_size, enemy_size])


def moveEnemy(multiple_enemy_list):
    for enemy in multiple_enemy_list:
        if enemy[2] > 0:
            enemy[0] += 1
        else:
            enemy[0] -= 1

        if enemy[3] > 0:
            enemy[1] += 1
        else:
            enemy[1] -= 1


def checkEnemy(multiple_enemy_list, enemy_size):
    for enemy in multiple_enemy_list:
        if enemy[0] <= 0:
            enemy[2] = 1
        if enemy[0] >= SCREENWIDTH - enemy_size:
            enemy[2] = -1

        if enemy[1] <= 0:
            enemy[3] = 1
        if enemy[1] >= 300:
            enemy[3] = -1


def moveEnemyBullet(bullet_list_enemy):
    for bullet in bullet_list_enemy:
        bullet[1] += 1


def PlotEnemyBullet(bullet_list_enemy, bullet_w, bullet_h):
    for bullet in bullet_list_enemy:
        pygame.draw.rect(WINDOW, WHITE, [bullet[0], bullet[1], bullet_w, bullet_h])


def checkEnemyBullet(bullet_list_enemy, bullet_h):
    for bullet in bullet_list_enemy:
        if bullet[1] + bullet_h >= SCREENHEIGHT + 150:
            bullet_list_enemy.pop(0)


def isEnemyDie(bullet_list_plane, multiple_enemy_list, bullet_w, enemy_size, hit):
    i = 0
    if len(bullet_list_plane) <= 6:
        b_list = bullet_list_plane
    else:
        b_list = bullet_list_plane[:7]

    for bullet in b_list:
        left = bullet[0] + (bullet_w // 2)
        right = bullet[1] + (bullet_w // 2)
        height = bullet[2]

        if multiple_enemy_list[0][1] <= height <= multiple_enemy_list[0][1] + enemy_size:
            if multiple_enemy_list[0][0] <= left <= multiple_enemy_list[0][0] + enemy_size:
                bullet_list_plane[i][0] = -20
                hit += 1

            if multiple_enemy_list[0][0] <= right <= multiple_enemy_list[0][0] + enemy_size:
                bullet_list_plane[i][1] = -20
                hit += 1

        i += 1

    if hit >= 10:
        return True, hit
    else:
        return False, hit


def game():
    global EXIT_GAME
    plane_x = 290
    plane_y = 630
    plane_w = 40
    plane_h = 30
    change_x = 0
    bullet_w = 7
    bullet_h = 14
    enemy_size = 30
    bullet_list_plane = []
    bullet_list_enemy = []
    multiple_enemy_list = []
    enemy_dir_x = 1
    enemy_dir_y = 1
    enemy_x = random.randint(0, SCREENWIDTH - enemy_size)
    enemy_y = random.randint(0, 250)
    enemy_hit_count = 0
    score = 0

    bullet_list_plane.append([plane_x, plane_x + plane_w - bullet_w, plane_y])
    multiple_enemy_list.append([enemy_x, enemy_y, enemy_dir_x, enemy_dir_y])
    bullet_list_enemy.append(
        [multiple_enemy_list[0][0] + (enemy_size // 2) - (bullet_w // 2),
         multiple_enemy_list[0][1] + enemy_size - bullet_h]
    )

    while not EXIT_GAME:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                EXIT_GAME = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    change_x = 1
                if event.key == pygame.K_LEFT:
                    change_x = -1

        plane_x += change_x
        if plane_x <= 0:
            plane_x = 2
        if plane_x >= SCREENWIDTH - plane_w:
            plane_x = SCREENWIDTH - plane_w - 2

        WINDOW.fill(BLUE)

        if len(bullet_list_plane) > 0:
            movePlaneBullet(bullet_list_plane)
            plotPlaneBullet(bullet_list_plane, bullet_w, bullet_h)
            checkPlaneBullet(bullet_list_plane)
            if abs(plane_y - bullet_list_plane[-1][2]) >= 60:
                bullet_list_plane.append([plane_x, plane_x + plane_w - bullet_w, plane_y])

        if len(multiple_enemy_list) > 0:
            moveEnemy(multiple_enemy_list)
            PlotEnemy(multiple_enemy_list, enemy_size)
            checkEnemy(multiple_enemy_list, enemy_size)

        if len(bullet_list_enemy) == 0:
            bullet_list_enemy.append(
                [multiple_enemy_list[0][0] + (enemy_size // 2) - (bullet_w // 2),
                 multiple_enemy_list[0][1] + enemy_size - bullet_h]
            )

        if len(bullet_list_enemy) <= 5:
            if abs(bullet_list_enemy[-1][0] - multiple_enemy_list[0][0]) > 55:
                bullet_list_enemy.append(
                    [multiple_enemy_list[0][0] + (enemy_size // 2) - (bullet_w // 2),
                     multiple_enemy_list[0][1] + enemy_size - bullet_h]
                )

        if len(bullet_list_enemy) > 0:
            moveEnemyBullet(bullet_list_enemy)
            PlotEnemyBullet(bullet_list_enemy, bullet_w, bullet_h)
            checkEnemyBullet(bullet_list_enemy, bullet_h)

        enemy_die, enemy_hit_count = isEnemyDie(bullet_list_plane, multiple_enemy_list, bullet_w, enemy_size,
                                                enemy_hit_count)

        if enemy_die:
            enemy_x = random.randint(0, SCREENWIDTH - enemy_size)
            enemy_y = random.randint(0, 250)
            multiple_enemy_list.pop()
            multiple_enemy_list.append([enemy_x, enemy_y, enemy_dir_x, enemy_dir_y])
            score += 1
            enemy_hit_count = 0

        pygame.draw.rect(WINDOW, GREEN, [plane_x, plane_y, plane_w, plane_h])
        pygame.display.update()
        # FPS_CLOCK.tick(FPS)


if __name__ == '__main__':
    while not EXIT_GAME:
        game()

    pygame.quit()

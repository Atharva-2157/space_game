import random
import pygame

pygame.init()

SCREENWIDTH = 900
SCREENHEIGHT = 715

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

BG_IMG = pygame.image.load('Images\\space.jpeg')
MAIN_PLANE = pygame.image.load('Images\\player_ship.png')
PLANE_BULLET = pygame.image.load('Images\\bullet.png')
ENEMY_PLANE = pygame.image.load('Images\\enemy_ship.png')

BG_IMG = pygame.transform.scale(BG_IMG, (SCREENWIDTH, SCREENHEIGHT)).convert_alpha()
ENEMY_PLANE = pygame.transform.rotate(ENEMY_PLANE, 180)
ENEMY_PLANE = pygame.transform.scale(ENEMY_PLANE, (50, 40)).convert_alpha()


class Bullet:
    bullet_w = PLANE_BULLET.get_width()
    bullet_h = PLANE_BULLET.get_height()


class Plane:
    def __init__(self):
        self.plane_w = MAIN_PLANE.get_width()
        self.plane_h = MAIN_PLANE.get_height()
        self.plane_x = (SCREENWIDTH // 2) - (self.plane_w // 2)
        self.plane_y = 630
        self.change_x = 0
        self.life = 10
        self.bullets = [[self.plane_x - 7, self.plane_x + self.plane_w - 15, self.plane_y]]

    def drawPlane(self):
        WINDOW.blit(MAIN_PLANE, (self.plane_x, self.plane_y))

    def drawBullet(self):
        for bullet in self.bullets:
            WINDOW.blit(PLANE_BULLET, (bullet[0], bullet[2]))
            WINDOW.blit(PLANE_BULLET, (bullet[1], bullet[2]))

    def newBullet(self):
        if abs(self.plane_y - self.bullets[-1][2]) > 40:
            self.bullets.append([self.plane_x - 7, self.plane_x + self.plane_w - 15, self.plane_y])

    def moveBullet(self):
        for bullet in self.bullets:
            bullet[2] -= 1

    def deleteExtraBullet(self):
        for bullet in self.bullets:
            if bullet[2] <= 0:
                self.bullets.pop(0)

    def isPlaneHit(self, enemy):
        for bullet in enemy.bullets:
            if self.plane_x < bullet[0] < self.plane_x + self.plane_w and \
                    self.plane_y < bullet[1] + 14 < self.plane_y + self.plane_h:
                self.life -= 1
                bullet[1] = -20

        if enemy.enemy_x + enemy.enemy_w >= self.plane_x and enemy.enemy_x <= self.plane_x + self.plane_w:
            if enemy.enemy_y + enemy.enemy_w >= self.plane_y:
                self.life -= 1
                enemy.enemy_x = -100

        if self.life == 0:
            return True
        else:
            return False

    def showBullets(self):
        for bullet in self.bullets:
            print(f"{bullet[0]} , {bullet[1]}")


class Enemy:
    def __init__(self):
        self.enemy_w = ENEMY_PLANE.get_width()
        self.enemy_h = ENEMY_PLANE.get_height()
        self.enemy_x = random.randint(0, SCREENWIDTH - self.enemy_w)
        self.enemy_y = -self.enemy_h - 20
        self.dir_x = "right"
        self.dir_y = "down"
        self.damage = 0
        self.bullets = [[self.enemy_x + (self.enemy_w // 2) - 3,
                         self.enemy_y + self.enemy_h - 17]]

    def drawEnemy(self):
        WINDOW.blit(ENEMY_PLANE, (self.enemy_x, self.enemy_y))

    def moveEnemy(self):
        self.enemy_y += 1

    def newBullet(self):
        if self.bullets[-1][1] - self.enemy_y > random.randint(300, 400):
            self.bullets.append([self.enemy_x + (self.enemy_w // 2) - 3,
                                 self.enemy_y + self.enemy_h - 17])

    def drawBullet(self):
        for bullet in self.bullets:
            pygame.draw.rect(WINDOW, RED, [bullet[0], bullet[1], 7, 17])

    def checkEnemy(self):
        if self.enemy_y >= SCREENHEIGHT + 10:
            return True

    def isEnemyDie(self, bullet_list):
        i = 0
        for bullet in bullet_list:
            left = bullet[0] + (Bullet.bullet_w // 2)
            right = bullet[1] + (Bullet.bullet_w // 2)

            if self.enemy_y <= bullet[2] <= self.enemy_y + self.enemy_h:
                if self.enemy_x <= left <= self.enemy_x + self.enemy_w:
                    bullet_list[i][0] = -20
                    self.damage += 1
                if self.enemy_x <= right <= self.enemy_x + self.enemy_w:
                    bullet_list[i][1] = -20
                    self.damage += 1

            i += 1

        if self.damage >= 2:
            return True
        else:
            return False

    def moveBullet(self):
        for bullet in self.bullets:
            bullet[1] += 2

    def deleteExtraBullet(self):
        for bullet in self.bullets:
            if len(self.bullets) >= 2:
                if bullet[1] > SCREENHEIGHT + 5:
                    self.bullets.pop(0)


def gameLoop():
    global EXIT_GAME
    plane = Plane()
    opponent = Enemy()
    enemy_list = [opponent]
    score = 0
    game_over = False
    while not EXIT_GAME:
        if game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    EXIT_GAME = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return

            WINDOW.fill(WHITE)
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    EXIT_GAME = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        plane.change_x = -2

                    if event.key == pygame.K_RIGHT:
                        plane.change_x = 2

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        if plane.change_x < 0:
                            plane.change_x = 0

                    if event.key == pygame.K_RIGHT:
                        if plane.change_x > 0:
                            plane.change_x = 0

            plane.plane_x += plane.change_x
            if plane.plane_x <= 0:
                plane.plane_x = 1
            if plane.plane_x >= SCREENWIDTH - plane.plane_w:
                plane.plane_x = SCREENWIDTH - plane.plane_w - 1

            # WINDOW.blit(BG_IMG, (0, 0))
            WINDOW.fill(WHITE)

            plane.newBullet()
            plane.moveBullet()
            plane.drawBullet()
            plane.drawPlane()
            plane.deleteExtraBullet()

            if len(enemy_list) == 0:
                opponent = Enemy()
                enemy_list.append(opponent)

            if enemy_list[-1].enemy_y >= random.randint(270, 370):
                opponent = Enemy()
                enemy_list.append(opponent)

            i = 0
            for enemy in enemy_list:
                pop_status = 0
                enemy.newBullet()
                enemy.moveEnemy()
                enemy.drawEnemy()
                enemy.drawBullet()
                enemy.moveBullet()
                enemy.deleteExtraBullet()

                if plane.isPlaneHit(enemy):
                    game_over = True

                if enemy.checkEnemy():
                    pop_status = 1

                if enemy.isEnemyDie(plane.bullets):
                    score += 1
                    pop_status = 1

                if pop_status == 1:
                    enemy_list.pop(i)

                i += 1

        pygame.display.update()


if __name__ == '__main__':
    while not EXIT_GAME:
        gameLoop()

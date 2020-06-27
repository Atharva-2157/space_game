# Basic Modules needed for game
import random
import pygame

pygame.init()  # It is used to initialise all methods in Pygame
pygame.mixer.init()  # We can add sounds in the game using this method

# Screen resolution
SCREENWIDTH = 900
SCREENHEIGHT = 715

WINDOW = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))  # This method creates a basic window of game
pygame.display.set_caption("Space Game")  # Sets the title of the Game Window

EXIT_GAME = False  # When False game is running. When True game gets Quit

# RGB values of colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (135, 206, 235)
GOLD = (255, 215, 0)
GREEN = (0, 255, 0)

FPS = 110  # Frame per Seconds
FPS_CLOCK = pygame.time.Clock()  # clock variable which control FPS in game window

# Loading all necessary images in the game
# Using load function Image gets stored in variable in array form
WELCOME_IMG = pygame.image.load('Images\\welcomeSpace.jpeg')
BG_IMG = pygame.image.load('Images\\space.jpeg')
MAIN_PLANE = pygame.image.load('Images\\player_ship.png')
PLANE_BULLET = pygame.image.load('Images\\bullet.png')
ENEMY_PLANE = pygame.image.load('Images\\enemy_ship.png')
DIGITS = {
    '0': pygame.image.load('Images\\0.png'),
    '1': pygame.image.load('Images\\1.png'),
    '2': pygame.image.load('Images\\2.png'),
    '3': pygame.image.load('Images\\3.png'),
    '4': pygame.image.load('Images\\4.png'),
    '5': pygame.image.load('Images\\5.png'),
    '6': pygame.image.load('Images\\6.png'),
    '7': pygame.image.load('Images\\7.png'),
    '8': pygame.image.load('Images\\8.png'),
    '9': pygame.image.load('Images\\9.png'),
}

LABELS = {
    'PLAY': pygame.image.load('Images\\play.png'),
    'QUIT': pygame.image.load('Images\\quit.png'),
}

# Transform.scale converts the original image into specified resolution
BG_IMG = pygame.transform.scale(BG_IMG, (SCREENWIDTH, SCREENHEIGHT)).convert_alpha()
WELCOME_IMG = pygame.transform.scale(WELCOME_IMG, (SCREENWIDTH, SCREENHEIGHT)).convert_alpha()
ENEMY_PLANE = pygame.transform.rotate(ENEMY_PLANE, 180)
ENEMY_PLANE = pygame.transform.scale(ENEMY_PLANE, (50, 40)).convert_alpha()


# This is button class to control Buttons in game
class Button:
    # This is a constructor which initialises some variables
    def __init__(self, text, color, x, y, width, height):
        self.text = text
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    # This function draws Button on Screen
    def draw(self):
        pygame.draw.rect(WINDOW, self.color, [self.x, self.y, self.width, self.height])  # this method draws
        # rectangle on screen
        WINDOW.blit(self.text, (self.x, self.y))  # blit method draws the specified image or text on screen

    # It checks whether the mouse is on the button or not
    def isHover(self, pos):
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True

        return False


class Bullet:
    bullet_w = PLANE_BULLET.get_width()
    bullet_h = PLANE_BULLET.get_height()


# It is a class of players plane
class Plane:
    # Constructor which initialises some values
    def __init__(self):
        self.plane_w = MAIN_PLANE.get_width()  # plane width
        self.plane_h = MAIN_PLANE.get_height()  # plane height
        self.plane_x = (SCREENWIDTH // 2) - (self.plane_w // 2)  # plane position on x co-ordinate
        self.plane_y = 630  # plane position on y co-ordinate
        self.change_x = 0  # horizontal change
        self.life = 10  # It is Health of a plane
        self.bullets = [[self.plane_x - 7, self.plane_x + self.plane_w - 15, self.plane_y]]  # Bullets
        # fired by plane

    # Draws the Image of plane on window
    def drawPlane(self):
        WINDOW.blit(MAIN_PLANE, (self.plane_x, self.plane_y))

    # Draws plane bullet on screen
    def drawBullet(self):
        for bullet in self.bullets:
            WINDOW.blit(PLANE_BULLET, (bullet[0], bullet[2]))
            WINDOW.blit(PLANE_BULLET, (bullet[1], bullet[2]))

    # New bullet is loaded in plane
    def newBullet(self):
        if abs(self.plane_y - self.bullets[-1][2]) > 40:
            self.bullets.append([self.plane_x - 7, self.plane_x + self.plane_w - 15, self.plane_y])

    # Moves bullet in upward direction
    def moveBullet(self):
        for bullet in self.bullets:
            bullet[2] -= 2

    # This will delete bullet if it goes out of the screen
    def deleteExtraBullet(self):
        for bullet in self.bullets:
            if bullet[2] <= 0:
                self.bullets.pop(0)

    # It checks whether plane gets damage or not
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

    # This function draws health bar on the screen
    def healthBar(self):
        k = (self.plane_w + 1) // 10
        pygame.draw.rect(WINDOW, RED, [self.plane_x, self.plane_y + self.plane_h + 10, self.plane_w, 7])
        pygame.draw.rect(WINDOW, GREEN, [self.plane_x + (k * (10 - self.life)), self.plane_y + self.plane_h + 10,
                                         self.plane_w - (k * (10 - self.life)), 7])


# This class if for enemy plane
class Enemy:
    # constructor with initial values :-)
    def __init__(self):
        self.enemy_w = ENEMY_PLANE.get_width()  # enemy width
        self.enemy_h = ENEMY_PLANE.get_height()  # enemy height
        self.enemy_x = random.randint(0, SCREENWIDTH - self.enemy_w)  # enemy position of x co-ordinate
        self.enemy_y = -self.enemy_h - 20  # enemy position of y co-ordinate
        self.damage = 0  # plane damage managing variable
        self.bullets = [[self.enemy_x + (self.enemy_w // 2) - 3,
                         self.enemy_y + self.enemy_h - 17]]  # bullets of enemy plane

    # Draws enemy plane on screen
    def drawEnemy(self):
        WINDOW.blit(ENEMY_PLANE, (self.enemy_x, self.enemy_y))

    # It moves enemy downwards
    def moveEnemy(self):
        self.enemy_y += 1

    # Load new bullet for enemy
    def newBullet(self):
        if self.bullets[-1][1] - self.enemy_y > random.randint(220, 250):
            self.bullets.append([self.enemy_x + (self.enemy_w // 2) - 3,
                                 self.enemy_y + self.enemy_h - 17])

    # Draws enemy Bullet on screen
    def drawBullet(self):
        for bullet in self.bullets:
            pygame.draw.rect(WINDOW, RED, [bullet[0], bullet[1], 7, 17])

    # If enemy is in screen returns True. False if out of screen
    def checkEnemy(self):
        if self.enemy_y >= SCREENHEIGHT + 10:
            return True

    # if enemy get damage by player plane 2 times then enemy die
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

    # move Enemy bullet downward direction
    def moveBullet(self):
        for bullet in self.bullets:
            bullet[1] += 2

    # If bullet is out of screen then it is deleted
    def deleteExtraBullet(self):
        for bullet in self.bullets:
            if len(self.bullets) >= 2:
                if bullet[1] > SCREENHEIGHT + 5:
                    self.bullets.pop(0)


# This is the UI of Welcome Window which have play and quit button
def welcomeWindow():
    global EXIT_GAME
    # objects for play and quit button
    play_button = Button(LABELS['PLAY'], GREEN, SCREENWIDTH // 2 - 10, 250, 65, 35)
    quit_button = Button(LABELS['QUIT'], GREEN, SCREENWIDTH // 2 - 10, 300, 65, 35)

    # This infinite loop is for showing game window on screen
    # If we not apply this loop then window came stays 1 second and gone :-(
    while not EXIT_GAME:
        # for loop to handle all events like button press, mouse motion, mouse click etc
        for event in pygame.event.get():  # It gives all events
            position = pygame.mouse.get_pos()  # It gives co-ordinates of mouse position at that instance
            if event.type == pygame.QUIT:  # It checks whether user click on close button or not
                EXIT_GAME = True  # If we click close then Exit_game is True and game gets Quit

            if event.type == pygame.MOUSEMOTION:  # this event checks if mouse move or not
                if play_button.isHover(position):  # is mouse hovering on play button
                    play_button.color = YELLOW  # button color change to Yellow
                else:
                    play_button.color = GREEN  # else button color is green

                if quit_button.isHover(position):  # is mouse hovering on Quit button
                    quit_button.color = RED  # button color change to Yellow
                else:
                    quit_button.color = GREEN  # else button color is green

            if event.type == pygame.MOUSEBUTTONDOWN:  # It checks whether user single click on mouse button
                if play_button.isHover(position):  # if user click play button
                    return  # Then just return
                if quit_button.isHover(position):  # if user click quit button
                    EXIT_GAME = True  # then game gets quit

            if event.type == pygame.KEYDOWN:  # KEYDOWN checks whether a keyboard key is get pressed or not
                if event.key == pygame.K_RETURN:  # If user press enter
                    return  # Then just return

        # WINDOW.fill(WHITE)   # fill method is used to color the window with specified color
        WINDOW.blit(WELCOME_IMG, (0, 0))  # Blit draws Welcome_img in screen from (x, y) = (0, 0)
        play_button.draw()  # play button get drawn on screen
        quit_button.draw()  # Quit button get drawn on screen

        # This is very important function
        # The changes you done on black screen are not get reflected till you apply this method
        pygame.display.update()
        FPS_CLOCK.tick(FPS)  # It shows FPS no of frames in 1 second


# This is the main game
def gameLoop():
    global EXIT_GAME
    plane = Plane()  # Object of player plane
    opponent = Enemy()  # Object of enemy plane
    enemy_list = [opponent]  # List of enemy planes
    score = 0  # player score
    game_over = False  # when False then game is running. When True Game is over

    while not EXIT_GAME:
        # If game is over then show this screen
        if game_over:
            # Handling all events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    EXIT_GAME = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return

            WINDOW.fill(WHITE)

        # If game is running then show this screen
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    EXIT_GAME = True

                if event.type == pygame.KEYDOWN:     # If any Key is pressed
                    if event.key == pygame.K_LEFT:   # If left arrow key is pressed
                        plane.change_x = -5          # Plane goes in left direction

                    if event.key == pygame.K_RIGHT:  # If right arrow key is pressed
                        plane.change_x = 5           # Plane goes in right direction

                if event.type == pygame.KEYUP:       # If a key is release
                    if event.key == pygame.K_LEFT:   # Plane Stop moving
                        if plane.change_x < 0:
                            plane.change_x = 0

                    if event.key == pygame.K_RIGHT:
                        if plane.change_x > 0:
                            plane.change_x = 0

            plane.plane_x += plane.change_x     # Move the plane

            # It will not allow our plane to go outside game window
            if plane.plane_x <= 0:
                plane.plane_x = 1
            if plane.plane_x >= SCREENWIDTH - plane.plane_w:
                plane.plane_x = SCREENWIDTH - plane.plane_w - 1

            WINDOW.blit(BG_IMG, (0, 0))
            # WINDOW.fill(WHITE)

            # drawing score in game window
            score_list = [x for x in str(score)]
            k = 0
            for i in score_list:
                k += 1
                WINDOW.blit(DIGITS[i], (k * 25, 10))

            plane.newBullet()
            plane.moveBullet()
            plane.drawBullet()
            plane.drawPlane()
            plane.deleteExtraBullet()

            # for keeping at least 1 enemy in screen
            if len(enemy_list) == 0:
                opponent = Enemy()
                enemy_list.append(opponent)

            # Random enemy entry
            if enemy_list[-1].enemy_y >= random.randint(50, 100):
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

                if plane.isPlaneHit(enemy):   # Game will over if life of plane is become 0
                    game_over = True

                if enemy.checkEnemy():
                    pop_status = 1

                if enemy.isEnemyDie(plane.bullets):
                    score += 1
                    pop_status = 1

                if pop_status == 1:
                    enemy_list.pop(i)

                i += 1

                plane.healthBar()

        pygame.display.update()
        FPS_CLOCK.tick(FPS)


if __name__ == '__main__':
    while not EXIT_GAME:
        welcomeWindow()
        gameLoop()

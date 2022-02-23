from operator import truediv
import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900,500   # sets borders of windows
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  #how to create the display window in pygame
pygame.display.set_caption("cfugs game")  #sets name of game
WHITE = (255, 255, 255)      #sets the color white, used in background
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255 ,0)
spaceshipWidth, spaceshipHeight = 55, 40  #starting point for psaceships
FPS = 60                                    #implements an fps max variable
VEL = 5
bulletVel = 7
maxBullets = 5

healthFont = pygame.font.SysFont('comicsans', 40)
winnerFont = pygame.font.SysFont('comicsans', 100)

yellowHit = pygame.USEREVENT + 1
redHit = pygame.USEREVENT + 2

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)     #creates rectangle in the middle of the screen

yellowSpaceshipImage = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))       #adding images for spaceships from assets folder
redSpaceshipImage = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))

yellowSpaceship = pygame.transform.rotate(pygame.transform.scale(yellowSpaceshipImage, (spaceshipWidth, spaceshipHeight)), 90)             #scaling the image down and rotating 90 deg
redSpaceship = pygame.transform.rotate(pygame.transform.scale(redSpaceshipImage, (spaceshipWidth, spaceshipHeight)), 270)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))



def draw_window(red, yellow, redBullets, yellowBullets, redHealth, yellowHealth):
    WIN.blit(SPACE, (0, 0))                               #setting background color
    pygame.draw.rect(WIN, BLACK, BORDER)
    WIN.blit(yellowSpaceship, (yellow.x, yellow.y))    #blit used to draw text or image on screen, coordinates start from top left and right/down
    WIN.blit(redSpaceship, (red.x, red.y))             #yel.x and yel.y used to make images follow cords of rectanges that are moving
    redHealthText = healthFont.render("health: " + str(redHealth), 1, WHITE)
    yellowHealthText = healthFont.render("health: " + str(yellowHealth), 1, WHITE)
    WIN.blit(redHealthText, (WIDTH - redHealthText.get_width() - 10, 10))
    WIN.blit(yellowHealthText, (10, 10))
    for bullet in redBullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in yellowBullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    pygame.display.update()                       #updatees diplay to show changes

def yellowMovement(keysPressed, yellow):
    if keysPressed[pygame.K_a] and yellow.x - VEL > 0:           #if a is pressed move the spaceship to the left (subtract on x axis, etc.) by velocity
            yellow.x -= VEL                                      # and checks to make sure the movement input doesnt put the spaceship off the screen (or move position to a negative)
    if keysPressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:
            yellow.x += VEL
    if keysPressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15:
            yellow.y += VEL
    if keysPressed[pygame.K_w] and yellow.y - VEL > 0:
            yellow.y -= VEL

def redMovement(keysPressed, red):
    if keysPressed[pygame.K_j] and red.x - VEL > BORDER.x + BORDER.width:              
            red.x -= VEL 
    if keysPressed[pygame.K_l] and red.x + VEL + red.width < WIDTH:
            red.x += VEL
    if keysPressed[pygame.K_k] and red.y + VEL + red.height < HEIGHT - 15:
            red.y += VEL
    if keysPressed[pygame.K_i] and red.y - VEL > 0:
            red.y -= VEL

def handleBullets(yellowBullets, redBullets, yellow, red):
    for bullet in yellowBullets:
        bullet.x += bulletVel
        if red.colliderect(bullet):                                #coliderect used to check if 2 rect collide, true or false
            pygame.event.post(pygame.event.Event(redHit))
            yellowBullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellowBullets.remove(bullet)


    for bullet in redBullets:
        bullet.x -= bulletVel
        if yellow.colliderect(bullet):                                #coliderect used to check if 2 rect collide, true or false
            pygame.event.post(pygame.event.Event(yellowHit))
            redBullets.remove(bullet)
        elif bullet.x <0:
            redBullets.remove(bullet)

def draw_winner(text):
    draw_text = winnerFont.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():                                 #function or loop to keep game running
    red = pygame.Rect(700, 300, spaceshipWidth, spaceshipHeight)         #creating a rectange to act as spaceship so it can move
    yellow = pygame.Rect(100, 300, spaceshipWidth, spaceshipHeight)
    redBullets = []
    yellowBullets = []
    redHealth = 100
    yellowHealth = 100
    clock = pygame.time.Clock()             # setting a clock to control speed of while loop
    run = True                              #sets run to true
    while run:                              #starrting while loop (while user is playing)
        clock.tick(FPS)                     #setting the tick to 60 fps
        for event in pygame.event.get():    #checking events to make sure they are playing game
            if event.type == pygame.QUIT:   #if the event type or click is a quit
                run = False                 #run is set to false, breaking the loop
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellowBullets) < maxBullets:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellowBullets.append(bullet)
                if event.key == pygame.K_RCTRL and len(redBullets) < maxBullets:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    redBullets.append(bullet)
            if event.type == redHit:
                redHealth -= 10
            if event.type == yellowHit:
                yellowHealth -= 10
        winnerText = ""
        if redHealth <= 0:
            winnerText = "yellow won"
        if yellowHealth <= 0:
            winnerText = "red won"
        if winnerText != "":
            draw_winner(winnerText)
            break

        keysPressed = pygame.key.get_pressed()   #tells what keys are being pressed down, if key stays down it will still be registered
        yellowMovement(keysPressed, yellow)      #cleans code up, yellow movement in a function, passes keys and color
        redMovement(keysPressed, red)
        handleBullets(yellowBullets, redBullets, yellow, red)
        draw_window(red, yellow, redBullets, yellowBullets, redHealth, yellowHealth)                       #calls window function
    




if __name__ == "__main__":                 #making sure if the code is being used by other code
    main()                                 #the main function or game isnt opened when not wanted



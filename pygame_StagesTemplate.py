
import pygame, pygame.mixer   # accesses pygame files
import sys      # to communicate with windows
import random, math


def textDraw(msgText, XYPosition, color):
    font = pygame.font.Font(fontName, 28)  # <<<<<<<< try changing the size
    text_surface = font.render(msgText, True, color)  # <<<<< try changing the color
    screen.blit(text_surface, XYPosition)  # <<<< try changing the position


def pythag(pX, pY, tX, tY):
    a = pX - tX
    b = pY - tY
    c = math.sqrt(a ** 2 + b ** 2)
    return c

# game setup ################ only runs once

pygame.init()   # starts the game engine
clock = pygame.time.Clock()     # creates clock to limit frames per second
FPS = 60  # sets max speed of min loop
SCREENSIZE = SCREENWIDTH, SCREENHEIGHT = 1000, 800  # sets size of screen/window
screen = pygame.display.set_mode(SCREENSIZE)  # creates window and game screen
# set variables for colors RGB (0-255)
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)
green = (0, 255, 0)
fontName = pygame.font.match_font('arial')
gameState = "splash"  # controls which state the games is in
# loads font, images and sounds
BGImage = pygame.image.load("background.jpg")
player1Image = pygame.image.load("crossHair.png")
targetImage = pygame.image.load("sprites.png")
gunSound = pygame.mixer.Sound("Laser_Cannon.ogg")
sploosh = pygame.image.load("sploosh.jpg")

# resize images
player1ImageWidthHeight = [100, 97]  # set size for player sprite
player1Image = pygame.transform.scale(player1Image, player1ImageWidthHeight)  # modifies size of image
targetImageWidthHeight = [41, 50]
targetImage = pygame.transform.scale(targetImage, targetImageWidthHeight)

targetXY = [500, 500]  # sets target start position

# game loop #################### runs 60 times a second!
while gameState != "exit":  # game loop - note: everything in the mainloop is indented

    for event in pygame.event.get():  # get user interaction
        if event.type == pygame.QUIT:  # tests if window X has been clicked
            gameState = "exit"  # causes exit of game loop
        if event.type == pygame.MOUSEBUTTONUP:
            fireLock = 0

    if gameState == "splash":
        screen.fill(white)
        textDraw("Click to begin", (SCREENWIDTH / 2 - 100, SCREENHEIGHT / 2), red)
        screen.blit(sploosh, (0, 0))
        if pygame.mouse.get_pressed()[0]:
            gameState = "playing"
            startTime = pygame.time.get_ticks()  # stores current time
            # set start game variables
            startTime = pygame.time.get_ticks()
            fireLock = 0
            score = 0
            hitList = []
            distanceList = []

    elif gameState == "playing":
        screen.fill(black)
        pygame.mouse.set_visible(False)  # hide mouse cursor
        screen.blit(BGImage, (0, 0))  # draw background image
        mousePosition = pygame.mouse.get_pos()
        target = screen.blit(targetImage, targetXY)
        player1XY = mousePosition[0] - player1ImageWidthHeight[0] / 2, mousePosition[1] - player1ImageWidthHeight[1] / 2
        player1 = screen.blit(player1Image, player1XY)
        distance = pythag(player1XY[0], player1XY[1], targetXY[0], targetXY[1])

        if pygame.mouse.get_pressed()[0] == 1 and fireLock == 0:  # player fires
            gunSound.play()
            fireLock = 1
            if player1.colliderect(target):  # when the target is hit
                targetXY[0] = random.randint(0, SCREENWIDTH - 50)  # new target X
                targetXY[1] = random.randint(0, SCREENHEIGHT - 50)  # new target Y
                score += 1  # add to score
                hitList.append([int(player1XY[0]), int(player1XY[1])])
                distanceList.append(distance)

        # draw text to screen
        textDraw("distance: " + str(int(distance)), (SCREENWIDTH / 2 - 100, 10), black)
        textDraw("Score: " + str(score), (SCREENWIDTH / 2 - 100, 40), black)
        textDraw("Time: " + str( pygame.time.get_ticks() - startTime), (SCREENWIDTH / 2 - 100, 70), black)

        if pygame.time.get_ticks() - startTime > 10000:  # end game after 10 seconds
            gameState = "gameOver"

        textDraw("Time: " + str(pygame.time.get_ticks() - startTime), (SCREENWIDTH / 2 - 100, 70), green)
        if pygame.time.get_ticks() - startTime > 10000:  # change state after 10 seconds
            gameState = "gameOver"

    elif gameState == "gameOver":
        screen.fill(black)
        pygame.mouse.set_visible(True)
        for h in range(0, len(hitList) - 1):  # for each hit....
            pygame.draw.circle(screen, red, hitList[h], 30)
            textDraw(str(int(distanceList[h])), (hitList[h][0] + 20, hitList[h][1] + 20), red)
            textDraw("Score: " + str(score), (10, 40), green)
            avDistance = sum(distanceList) / len(distanceList)
            textDraw("Average distance: " + str(int(avDistance)), (10, 100), green)
            textDraw("Right click to play again", (400, 400), green)
        if pygame.mouse.get_pressed()[2]:
            gameState = "splash"
        textDraw("Right click to play again", (400, 400), green)
        if pygame.mouse.get_pressed()[2]:
            gameState = "splash"

    pygame.display.flip()  # transfers virtual screen to human viable screen
    clock.tick(FPS)
    # your code ends here ###############################
    pygame.display.flip()  # transfers virtual screen to human viable screen
    clock.tick(FPS)  # limits loop cycles per second

# out of game loop ###############
print("The game has closed")
pygame.quit()   # stops the game engine
sys.exit()  # close windows window





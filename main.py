"""
Final Project : Snake
Coded By : Brandon Irving
Programming IDE Used : JetBrains PyCharm Community Edition
Programming Language Used : Python 3.7.0
Modules Used : Pygame, Time and Random
Modules Created : SnakeColours
Day Finished : January 11th, 2019
"""

# Built-In Module(s)
import random
import pygame
import time

# My Module(s)
from SnakeColours import *

# Initialize Pygame
pygame.init()

# Setting Variables For Display Size
display_width = 800
display_height = 600

# Setting Variable For High Scores
with open("highScore.txt", "r") as highScore:
	high_score = highScore.read()

# Setting Initial Variables For FPS Counter
deltatime = 0
cSec = 0
cFrame = 0
FPS = 0

# Initialize Window
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Final Project : Snake')
pygame.display.update()
clock = pygame.time.Clock()

# Texture Size
block_size = 10

# Font Sizes
smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("comicsansms", 80)


def choose_difficulty():
    global speed
    select = True
    while select:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    speed = 1
                    select = False
                    gameLoop()
                elif event.key == pygame.K_2:
                    speed = 5
                    select = False
                    gameLoop()
                elif event.key == pygame.K_3:
                    speed = 10
                    select = False
                    gameLoop()
                elif event.key == pygame.K_4:
                    speed = 30
                    select = False
                    gameLoop()
                elif event.key == pygame.K_5:
                    speed = 60
                    select = False
                    gameLoop()
                elif event.key == pygame.K_6:
                    speed = 100
                    select = False
                    gameLoop()

        gameDisplay.fill(Colour.SaddleBrown)
        message_to_screen("Select Difficulty/Speed", Colour.Green, -100, "medium")
        message_to_screen("1. Almost Standing Still...", Colour.LawnGreen, 25)
        message_to_screen("2. Slow", Colour.LawnGreen, 65)
        message_to_screen("3. Medium", Colour.LawnGreen, 105)
        message_to_screen("4. Fast", Colour.LawnGreen, 145)
        message_to_screen("5. Insane", Colour.LawnGreen, 185)
        message_to_screen("6. You're A Fly!", Colour.LawnGreen, 225)
        pygame.display.update()
        clock.tick(30)


def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        gameDisplay.fill(Colour.SaddleBrown)
        message_to_screen("Paused", Colour.Green, -100, "large")
        message_to_screen("Press C to continue or Q to quit.", Colour.LawnGreen, 25)
        pygame.display.update()
        clock.tick(30)


def randAppleGen():
    randAppleX = round(random.randrange(0, display_width - block_size) / 10.0) * 10.0
    randAppleY = round(random.randrange(0, display_height - block_size) / 10.0) * 10.0
    return randAppleX, randAppleY


def game_intro():
    intro = True

    while intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    choose_difficulty()
                    intro = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        gameDisplay.fill(Colour.SaddleBrown)
        message_to_screen("Final Project : Snake", Colour.Green, -100, "medium")
        message_to_screen("The objective of the game is to eat red apples", Colour.LawnGreen, -30)
        message_to_screen("The more apples you eat, the longer you get", Colour.LawnGreen, 10)
        message_to_screen("If you run into yourself, or the edges, you die!", Colour.LawnGreen, 50)
        message_to_screen("Press C to play or Q to quit.", Colour.LawnGreen, 180)
        message_to_screen("The current High Score is: " + high_score, Colour.LawnGreen, 220)

        pygame.display.update()
        clock.tick(30)


def snake(block_size, snakelist):
    for XnY in snakelist:
        pygame.draw.rect(gameDisplay, Colour.Lime, [XnY[0], XnY[1], block_size, block_size])


def show_score(score):
    score_overlay = smallfont.render("Score: " + str(score), True, Colour.Aquamarine)
    gameDisplay.blit(score_overlay, (0, 0))


def text_objects(text, colour, size):
    if size == "small":
        textSurface = smallfont.render(text, True, colour)
    elif size == "medium":
        textSurface = medfont.render(text, True, colour)
    elif size == "large":
        textSurface = largefont.render(text, True, colour)
    return textSurface, textSurface.get_rect()


def message_to_screen(msg, colour, y_displace=0, size="small"):
    textSurf, textRect = text_objects(msg, colour, size)
    textRect.center = (display_width / 2), (display_height / 2) + y_displace
    gameDisplay.blit(textSurf, textRect)


def gameLoop():
    global speed
    gameExit = False
    gameOver = False

    lead_x = display_width / 2
    lead_y = display_height / 2

    lead_x_change = 0
    lead_y_change = 0

    snakeList = []
    snakeLength = 1

    randAppleX, randAppleY = randAppleGen()

    while not gameExit:

        # Game Over Screen
        while gameOver:
            gameDisplay.fill(Colour.Black)
            message_to_screen("Game Over", Colour.Red, -50, "large")
            message_to_screen("Press C to play again or Q to quit", Colour.White, 50, "medium")
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    elif event.key == pygame.K_c:
                        choose_difficulty()
        # Key Presses
        for event in pygame.event.get():

            # Exit
            if event.type == pygame.QUIT:
                gameExit = True

            # Movement
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a or event.key == pygame.K_LEFT or event.key == pygame.K_KP4:
                    lead_x_change = -block_size
                    lead_y_change = 0
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT or event.key == pygame.K_KP6:
                    lead_x_change = block_size
                    lead_y_change = 0
                elif event.key == pygame.K_w or event.key == pygame.K_UP or event.key == pygame.K_KP8:
                    lead_y_change = -block_size
                    lead_x_change = 0
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN or event.key == pygame.K_KP2:
                    lead_y_change = block_size
                    lead_x_change = 0
                elif event.key == pygame.K_p:
                    pause()

        # Border Collision Logic
        if lead_x >= display_width or lead_x < 0 or lead_y >= display_height or lead_y < 0:
            gameOver = True

        lead_x += lead_x_change
        lead_y += lead_y_change

        # Render Display, Apple, Snake, Score and FPS
        gameDisplay.fill(Colour.SaddleBrown)
        pygame.draw.rect(gameDisplay, Colour.AppleRed, [randAppleX, randAppleY, block_size, block_size])

        snakeHead = [lead_x, lead_y]
        snakeList.append(snakeHead)

        if len(snakeList) > snakeLength:
            del snakeList[0]

        # Snake Collision Logic
        for eachSegment in snakeList[:-1]:
            if eachSegment == snakeHead:
                gameOver = True

        # Call "Snake" Function
        snake(block_size, snakeList)

        # Call "Show Score" Function
        show_score(snakeLength - 1)

        # Apple Logic
        if lead_x == randAppleX and lead_y == randAppleY:
            randAppleX, randAppleY = randAppleGen()
            speed += 1
            snakeLength += 1

        # Call Update Display Function
        pygame.display.update()
        clock.tick(speed)

    finalScore = snakeLength - 1
    if finalScore > int(high_score):
        finalScore = str(finalScore)
        with open("highScore.txt", "w") as highScore:
            highScore.write(finalScore)

    # Call Built-In Quit Functions
    pygame.quit()
    time.sleep(0.1)
    quit()


# Call Main Function
game_intro()


from typing import Any
import pygame
from sys import exit
import random
from pygame.sprite import AbstractGroup

# TODO
# Få cup-klassen til å si ifra til dice klassen at den er ferdig med å rise 

pygame.init()

bredde = 500
hoyde = 800
cupXSpeed = 10
cupYSpeed = 2.1
showDice = False

screen = pygame.display.set_mode((bredde, hoyde))
pygame.display.set_caption("Meyer")
clock = pygame.time.Clock()

kopp = pygame.image.load("grafikk/kopper.png").convert_alpha()
kopp = pygame.transform.rotozoom(kopp, 0, 0.3)
cupX = 200
cupY = 90

class Cup(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, size: int):
        super().__init__()
        self.image = pygame.image.load("grafikk/kopper.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, size)
        self.rect = self.image.get_rect(midbottom = (x, y))
        self.xMiddle = x
        self.yMiddle = y
        self.size = size
        self.isPressed = False

    def followCursor(self):
        cursor = pygame.mouse.get_pos()
        movementSpeed = 20
        smoothenes = 80

        xDiff = cursor[0] - self.rect.center[0]
        yDiff = cursor[1] - self.rect.center[1]

        if(not self.isPressed):
            xDiff = self.xMiddle - self.rect.center[0]
            yDiff = self.yMiddle - self.rect.midbottom[1]

            if(xDiff != 0):
                self.rect.x += movementSpeed * (xDiff/smoothenes)

            if(yDiff != 0):
                self.rect.y += movementSpeed * (yDiff/smoothenes)
            
            return
        
        if(xDiff < -50 or xDiff > 50):
            self.rect.x += movementSpeed * (xDiff/smoothenes)

        if(yDiff < -50 or yDiff > 50):
            self.rect.y += movementSpeed * (yDiff/smoothenes)

    def detectPress(self):
        global showDice
        x = pygame.mouse.get_pos()[0]
        y = pygame.mouse.get_pos()[1]

        if(event.type == pygame.MOUSEBUTTONDOWN):
            showDice = False
            self.isPressed = True

        elif(event.type == pygame.MOUSEBUTTONUP):
            showDice = True
            self.isPressed = False

    def update(self):
        self.followCursor()
        self.detectPress()

class Dice(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, size, xEnd: int):
        super().__init__()
        self.image = pygame.image.load("grafikk/dice_"+str(random.randrange(1,6))+".png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, size)
        self.rect = self.image.get_rect(midbottom = (x, y))
        self.xMiddle = x
        self.size = size
        self.xEnd = xEnd

    def animateDiceIn(self):
        movementSpeed = 10

        if(self.rect.x < self.xEnd - 10):
            self.rect.x += movementSpeed

        elif(self.rect.x > self.xEnd + 10):
            self.rect.x -= movementSpeed

    def animateDiceOut(self):
        self.rect.x = self.xMiddle
        self.image = pygame.image.load("grafikk/dice_"+str(random.randrange(1,6))+".png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, self.size)

    def update(self):
        if(showDice):
            self.animateDiceIn()
        else:
            self.animateDiceOut()
        
cup = pygame.sprite.GroupSingle()
cup.add(Cup(bredde/2, hoyde*0.9, 0.2))

dice = pygame.sprite.Group()
dice.add(Dice(-100, hoyde*0.4, 0.1, 100))
dice.add(Dice(800, hoyde*0.4, 0.1, 300))

bakgrunn = pygame.image.load("grafikk/bakgrunn.png").convert_alpha()
bakgrunn = pygame.transform.rotozoom(bakgrunn, 0, 0.5)

tekst = pygame.font.Font("font/banger.ttf", 50)
tekst = tekst.render("MEYER", False, "White")

while True: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(bakgrunn,(-30,0))
    screen.blit(tekst, (150, 50))

    cup.draw(screen)
    cup.update()
    dice.draw(screen)
    dice.update()

    pygame.display.update()
    clock.tick(60)



import random
import numpy
import pygame
import cv2 as cv
from cvzone.HandTrackingModule import HandDetector
import time
import winsound
import os
from email.message import EmailMessage
import smtplib
import imghdr
from pygame.locals import *

pygame.init()

width, height = 1280,720
window = pygame.display.set_mode((width,height))
pygame.display.set_caption('Fruits Game')
icon = pygame.image.load('fruit.png')
pygame.display.set_icon(icon)
fps = 5
clock = pygame.time.Clock()
if not os.path.exists('images'):
    os.makedirs('images')

cap = cv.VideoCapture(0,cv.CAP_DSHOW)
cap.set(3,1280)
cap.set(4,720)

imgWatermelon = pygame.image.load('watermelon.png').convert_alpha()
imgAvocado = pygame.image.load('avocado.png').convert_alpha()
imgHamburger = pygame.image.load('hamburger.png').convert_alpha()
imgHot_pepper = pygame.image.load('hot_pepper.png').convert_alpha()
imgKivi = pygame.image.load('kivi.png').convert_alpha()

rectWatermelon = imgWatermelon.get_rect()
rectAvocado = imgAvocado.get_rect()
rectHamburger = imgHamburger.get_rect()
rectHot_paper = imgHot_pepper.get_rect()
rectKivi = imgKivi.get_rect()

RectFruit = [rectHamburger,
            rectHot_paper,
            rectKivi,
            rectWatermelon,
            rectAvocado]

# Variables
speed = 10
score = 0
stastTime= time.time()
totalTime = 90
count = 0
font = pygame.font.Font('grawust.regular.ttf', 50)
font1 = pygame.font.Font('Black.ttf', 20)
user_mail = "Enter an email address"

detector = HandDetector(detectionCon=0.8, maxHands=2)

def send_email():

    EMAIL_PASSWORD = os.environ.get('pass')

    msg = EmailMessage()
    msg["Subject"] = "Your pictures from Fruit Game"
    msg["From"] = "python_code@gmail.com"
    msg["To"] = user_mail
    msg.set_content(
        f"Hello! Thank you for playing my game. In the attachment you will find the pictures during the game. Have fun!")

    files = ['images/game0.png','images/game3.png','images/game4.png']

    for file in files:
        with open(file, "rb") as f:
            file_data = f.read()
            file_type = imghdr.what(f.name)
            file_name = f.name

        msg.add_attachment(file_data, maintype="image", subtype=file_type, filename=file_name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login("python_code@gmail.com", PASS)
        smtp.send_message(msg)

def pictures(window,time):
    global count
    if timeRemain == time:
        save_file = './images/game' + str(count) + '.png'
        pygame.image.save(window,save_file)
        count += 1

def final_image():

    img1 = pygame.image.load("images/game1.png").convert()
    frm = pygame.image.load("frame.png").convert_alpha()
    img1 = pygame.transform.scale(img1, (448, 252))
    window.blit(img1, (60, 400))
    window.blit(frm, (60, 400))

    img2 = pygame.image.load("images/game3.png").convert()
    frm = pygame.image.load("frame.png").convert_alpha()
    img2 = pygame.transform.scale(img2, (448, 252))
    window.blit(img2, (750, 400))
    window.blit(frm, (750, 400))

    img3 = pygame.image.load("images/game5.png").convert()
    frm = pygame.image.load("frame.png").convert_alpha()
    img3 = pygame.transform.scale(img3, (448, 252))
    window.blit(img3, (375, 100))
    window.blit(frm, (375, 100))

def resetFruits():
    for i in RectFruit:
        if i.y < 0:
            i.y = img.shape[0] + 50
            i.x = random.randrange(150,1150,100)

def collide(rect,scor,speed1=0):
    global score
    global speed
    if rect.collidepoint(x, y) or rect.collidepoint(z, k):
        rect.x = random.randrange(150, img.shape[1] - 150, 100)
        rect.y = img.shape[0] + 50
        score +=scor
        speed +=speed1

bg = (204, 102, 0)
red = (255, 0, 0)
black = (0, 0, 0)
white = (255, 255, 255)

# define global variable
clicked = False

class button():
    # colours for button and text
    button_col = (255, 0, 0)
    hover_col = (75, 225, 255)
    click_col = (50, 150, 255)
    text_col = black
    width = 250
    height = 30

    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.text = text

    def draw_button(self):

        global clicked
        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()

        # create pygame Rect object for the button
        button_rect = Rect(self.x, self.y, self.width, self.height)

        # check mouseover and clicked conditions
        if button_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                clicked = True
                pygame.draw.rect(window, self.click_col, button_rect)
            elif pygame.mouse.get_pressed()[0] == 0 and clicked == True:
                clicked = False
                action = True
            else:
                pygame.draw.rect(window, self.hover_col, button_rect)
        else:
            pygame.draw.rect(window, self.button_col, button_rect)

        # add shading to button
        pygame.draw.line(window, white, (self.x, self.y), (self.x + self.width, self.y), 2)
        pygame.draw.line(window, white, (self.x, self.y), (self.x, self.y + self.height), 2)
        pygame.draw.line(window, black, (self.x, self.y + self.height), (self.x + self.width, self.y + self.height), 2)
        pygame.draw.line(window, black, (self.x + self.width, self.y), (self.x + self.width, self.y + self.height), 2)

        # add text to button
        text_img = font1.render(self.text, True, self.text_col)
        text_len = text_img.get_width()
        window.blit(text_img, (self.x + int(self.width / 2) - int(text_len / 2), self.y + 7))
        return action

sendButton = button(910, 170, 'Send photo to Email')

# input email box
input_rect = pygame.Rect(850,230,140,32)
color_active = pygame.Color('black')
color_pasive = pygame.Color('red')
color = color_pasive
active = False

start = True
while start:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False
            pygame.quit()
        #mail
        if event.type == pygame.MOUSEBUTTONDOWN:  # text mail
            if input_rect.collidepoint(event.pos):
                active = True

            else:
                active = False
        if event.type == pygame.KEYDOWN:
            if active == True:
                if event.key == pygame.K_BACKSPACE:
                        user_mail = user_mail[:-1]
                else:
                    user_mail += event.unicode

    # Apply Logic

    timeRemain = int(totalTime - (time.time()-stastTime))

    if timeRemain == 0:
        winsound.PlaySound('over.wav', winsound.SND_NOWAIT)
    if timeRemain < 0:
        window.fill((97,236,227))

        textGameOver = font.render(f'Game Over! Your score is: {score}', True, (255, 0, 0))
        window.blit(textGameOver, (300, 40))
        final_image()
        if sendButton.draw_button():
            send_email()

        # input mail
        if active:
            color = color_active
        else:
            color = color_pasive

        pygame.draw.rect(window,color,input_rect,3)
        text_surface = font1.render(user_mail,True,(0,0,0))
        window.blit(text_surface,(input_rect.x +10,input_rect.y +5))

        input_rect.w = max(400,text_surface.get_width() + 10)

    else:
        # Open Cv
        succes, img = cap.read()
        img =  cv.flip(img,1)

        hands,img = detector.findHands(img,flipType=False)

        rectWatermelon.y -= speed +1
        rectAvocado.y -= speed +2
        rectHamburger.y -= speed+10
        rectHot_paper.y -= speed +10
        rectKivi.y -= speed +1

        resetFruits()

        if len(hands) == 2:
            hand = hands[0]
            hand2 = hands[1]
            x,y = hand['lmList'][9]
            z,k = hand2['lmList'][9]
            collide(rectKivi,1)
            collide(rectHamburger,-3)
            collide(rectHot_paper,0,3)
            collide(rectAvocado,3)
            collide(rectWatermelon,1)

        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        imgRGB = numpy.rot90(imgRGB)
        frame = pygame.surfarray.make_surface(imgRGB).convert()
        frame = pygame.transform.flip(frame, True, False)
        window.blit(frame, (0, 0))

        window.blit(imgWatermelon,rectWatermelon)
        window.blit(imgAvocado,rectAvocado)
        window.blit(imgHamburger,rectHamburger)
        window.blit(imgHot_pepper,rectHot_paper)
        window.blit(imgKivi, rectKivi)

        textScore = font.render(f'Score: {score}',True,(255,0,0))
        textTime = font.render(f'Time: {timeRemain}',True,(255,0,0))
        textSpeed = font.render(f'Speed: {speed}',True,(255,0,0))
        window.blit(textScore,(35,35))
        window.blit(textTime,(1000,35))
        window.blit(textSpeed,(600,35))

        pictures(window,10)
        pictures(window,20)
        pictures(window,25)

    # Update display
    pygame.display.update()

    # Set FPS
    clock.tick(fps)
    cv.destroyAllWindows()

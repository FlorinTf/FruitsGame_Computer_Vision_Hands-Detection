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
imgLemon = pygame.image.load('lemon.png').convert_alpha()
imgPepper = pygame.image.load('pepper.png').convert_alpha()
imgPizza = pygame.image.load('pizza.png').convert_alpha()
imgTomato = pygame.image.load('tomato.png').convert_alpha()

rectWatermelon = imgWatermelon.get_rect()
rectAvocado = imgAvocado.get_rect()
rectHamburger = imgHamburger.get_rect()
rectHot_paper = imgHot_pepper.get_rect()
rectKivi = imgKivi.get_rect()
rectLemon = imgLemon.get_rect()
rectPepper = imgPepper.get_rect()
rectPizza = imgPizza.get_rect()
rectTomato = imgTomato.get_rect()

RectFruit = [rectHamburger,
            rectHot_paper,
            rectKivi,
            rectWatermelon,
            rectAvocado,
            rectPizza ]

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


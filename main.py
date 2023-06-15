import pygame
import random
import math
from pygame import mixer
#initialising pygame module
pygame.init()
#creating window
screen=pygame.display.set_mode((700,500))
#background
background=pygame.image.load('bg.jpg')
mixer.music.load('bgd.mp3')
mixer.music.play(-1)
mixer.music.set_volume(0.1)
#title and icon
pygame.display.set_caption("space invaders")
icon=pygame.image.load('gamepng.png')
pygame.display.set_icon(icon)
#player
playerImg=pygame.image.load('ufo.png')
playerX=300
playerY=420
playerX_change=0
#enemy
enemyImg=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
no_of_enemies=6
for i in range(no_of_enemies):
  enemyImg.append(pygame.image.load('opp.png'))
  enemyX.append(random.randint(0,630))
  enemyY.append(random.randint(0,350))
  enemyX_change.append(1)
  enemyY_change.append(40)
#bullet
#ready state- not visible, fire- moving bullet
bulletImg=pygame.image.load('bullet.png')
bulletX=0
bulletY=420
bulletX_change=0
bulletY_change=3
bullet_state="ready"

#score
score_value=0
font=pygame.font.Font('freesansbold.ttf',30)
textX=10
textY=10

won_font=pygame.font.Font('freesansbold.ttf',64)

def show_score(x,y):
  score=font.render("SCORE: "+str(score_value),True,(0,255,0))
  screen.blit(score,(x,y))

def game_won():
  won=font.render("YOU WON!!!",True,(0,255,0))
  screen.blit(won,(300,200))
  
  

def player(x,y):
  screen.blit(playerImg,(x,y))

def enemy(x,y,i):
  screen.blit(enemyImg[i],(x,y))

def fire_bullet(x,y):
  global bullet_state
  bullet_state="fire"
  screen.blit(bulletImg,(x+16,y+10))

def isCollision(enemyX,enemyY,bulletX,bulletY):
  distance=math.sqrt((math.pow(enemyX-bulletY,2))+(math.pow(bulletX-enemyY,2)))
  if(distance<30):
    return True
  else:
    return False
  

#window will close when the program is executed
#game loop
running=True
while running:
  screen.fill((32,24,55))
  screen.blit(background,(0,0))
  for event in pygame.event.get():
    if event.type==pygame.QUIT:
      running=False

    if event.type==pygame.KEYDOWN:
      if event.key==pygame.K_LEFT:
        playerX_change=-2
      if event.key==pygame.K_RIGHT:
        playerX_change=2
      if event.key==pygame.K_SPACE:
        if bullet_state=='ready':
          bullet_sound=mixer.Sound('laser.wav')
          bullet_sound.play()
          bulletX=playerX
          fire_bullet(bulletX,bulletY)
    if event.type==pygame.KEYUP:
      if (event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT):
        playerX_change=0
  

  playerX+=playerX_change
  if(playerX<=0):
    playerX=0
  if(playerX>=630):
    playerX=630
  for i in range(no_of_enemies):
    if(score_value==5):
      for j in range(no_of_enemies):
        enemyY[j]=3000
      game_won()
      break
  
    enemyX[i]+=enemyX_change[i]
    if(enemyX[i]<=0):
      enemyX_change[i]=1
      enemyY[i]+=enemyY_change[i]
    if(enemyX[i]>=630):
      enemyX_change[i]=-1
      enemyY[i]+=enemyY_change[i]
    collision=isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
    if collision:
      explosion_sound=mixer.Sound('explosion.wav')
      explosion_sound.play()
      bulletY=420
      bullet_state='ready'
      score_value+=1
      enemyX[i]=random.randint(0,630)
      enemyY[i]=random.randint(0,350)
    enemy(enemyX[i],enemyY[i],i)
  if bulletY<=0:
    bulletY=420
    bullet_state='ready'
  if bullet_state=='fire':
    fire_bullet(bulletX,bulletY)
    bulletY-=bulletY_change
  
  
    
  player(playerX,playerY)
  show_score(textX,textY)
  pygame.display.update()
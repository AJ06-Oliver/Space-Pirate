import pygame
import random
from pygame import mixer

#initiator
pygame.init()

#screen setting
screen = pygame.display.set_mode((800,600))

#bg image
background = pygame.image.load("bg_spacepirate.jpg")  

#bgm
mixer.music.load("bg_game.wav")
mixer.music.play(-1)

#screen features
pygame.display.set_caption("Space pirates")
icon = pygame.image.load("pikaicon.png")
pygame.display.set_icon(icon)

#player details
playerImage = pygame.image.load("space-ship.png")
playerX = 370
playerY = 500
playerX_change = 0

#enemy details
enemyImage = pygame.image.load("alien.png")
enemyX = random.randint(0,736)
enemyY = random.randint(-50,-10)
enemyX_change = 0
enemyY_change = 0.5

#bullet
bulletImage = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 500
bulletY_change = 1
bullet_state = "ready"

#score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 24)
textX = 10
textY = 20

font_64 = pygame.font.Font('freesansbold.ttf', 64)
# FUNCTIONS
def show_score(x,y):
    score = font.render("Score: " + str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))
    
def game_over():
    over_text = font_64.render("GAME OVER",True,(255,255,255))
    screen.blit(over_text,(200,250))

def bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImage,(x+16,y+10))
    
def player(x,y):
    screen.blit(playerImage,(x,y))  

def enemy(x,y):
    screen.blit(enemyImage,(x,y))

def is_Collision(enemyX, enemyY, bulletX, bulletY):
    if enemyX-20 <= bulletX <= enemyX+50 and enemyY <= bulletY <= enemyY+64:
        return True
    return False

#loop for running game
running = True
while running:
    screen.fill((0,0,0))
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False           
        #key press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.6
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.6     
            if event.key == pygame.K_SPACE: 
                if bullet_state == "ready":
                    bullet_sound=mixer.Sound('gun_shot.wav')
                    bullet_sound.play()             
                    bulletX = playerX
                    bullet(bulletX,bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    playerX += playerX_change
    
    #boundaries
    if playerX<=0:
        playerX=0
    elif playerX>=736:
        playerX=736
    player(playerX,playerY)
    
    #bullet
    if bulletY <= 0:
        bulletY = 500
        bullet_state = "ready"
        
    if bullet_state == "fire":
        bullet(bulletX,bulletY) 
        bulletY -= bulletY_change
    
    #ENEMY TACTICS
    if enemyY >= -50:
        enemyY += enemyY_change
        if enemyY >= 540:
            game_over()
    enemy(enemyX,enemyY)
    
    collision = is_Collision(enemyX, enemyY, bulletX, bulletY)
    if collision:
        hit_sound=mixer.Sound('hit_sound.wav')
        hit_sound.play()
        bulletY = playerY
        bullet_state = "ready"
        score_value += 100
        enemyX = random.randint(0,736)
        enemyY = random.randint(-50,-10)
        
    show_score(textX,textY)
    pygame.display.update()
    
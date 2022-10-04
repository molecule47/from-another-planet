import pygame, sys
from pygame.locals import *
import buttons 
import random

clock = pygame.time.Clock()

pygame.init()

windowSize = (1200, 800)
window = pygame.display.set_mode(windowSize, 0, 32)

#pause
gamePause = False 

icon = pygame.image.load('assets/icon.png')
pygame.display.set_icon(icon)
pygame.display.set_caption("From Another Planet")

#fonts C&C Red Alert [INET]
menuFont = pygame.font.Font("fonts/font.ttf", 100)
font = pygame.font.Font("fonts/font.ttf", 60) 
font2 = pygame.font.Font("fonts/font.ttf", 30)
font3 = pygame.font.Font("fonts/font.ttf", 25)

mColor = (110, 69, 206)
lvl = 1
aliensKilled = 0
nA = 4 #number of aliens every level; level 1: 4
alienList = []

#buttons
playButton = pygame.image.load('assets/resume_button.png')

resumeb = pygame.image.load('assets/resume_button.png').convert_alpha()
resumeButton = buttons.Button(580, 380, resumeb, 1)

quitb = pygame.image.load('assets/quit_button.png').convert_alpha()
quitButton = buttons.Button(580, 490, quitb, 1)

def menu(text, font, mColor, x, y):
    m = font.render(text, True, mColor)
    window.blit(m, (x,y))

#backgrounds
bg = pygame.image.load('assets/bg.png')
menu_bg = pygame.image.load('assets/menu_bg.png')
over_bg = pygame.image.load('assets/over_bg.png')

#player and enemy
p = pygame.image.load('assets/p.png')
a = pygame.image.load('assets/aliens/a1.png')
a2 = pygame.image.load('assets/aliens/a2.png')

#bullet
b = pygame.image.load('assets/bullet.png')

#laser/log
l1 = pygame.image.load('assets/log1.png')
l2 = pygame.image.load('assets/log2.png')

rockRandom = []
for i in range(1,6):
    rockChoose = pygame.image.load(f'assets/rocks/r{i}.png')
    rockRandom.append(rockChoose)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(p, (int(p.get_width()*scale), p.get_height() * scale))
        self.lives = 3
        self.flip = False
        self.directionx = 0
        self.directiony = 0
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.location = location
        self.rate = 0
        self.velocity = 0

    def update(self):
        if self.rate > 0:
            self.rate -= 1

        collisionsAlien = pygame.sprite.spritecollide(self, alienList, False)
        for i in collisionsAlien:      
            if self.lives != 0:  
                self.lives -= 1

        collisionsRock = pygame.sprite.spritecollide(self, rockGroup, False)
        for j in collisionsRock:      
            if self.lives != 0:  
                self.lives -= 3
                self.kill()

        collisionsLog = pygame.Rect.colliderect(self.rect, log.rect)
        if collisionsLog:
            #print(log.pos, self.rect.y) 
            if self.rect.y < log.pos - 48 or self.rect.y > log.pos + 48:
                if self.lives != 0:  
                    self.lives -= 1
                    self.kill()
            else:
                pass

    def move(self, moveR, moveL, moveU, moveD):
        x = 0
        y = 0

        if moveR: 
            x = self.location
            self.directionx = 1
            self.flip = True
            y = 0
        if moveL:
            x = -self.location
            self.directionx = -1
            self.flip = False 
            y = 0
        if moveU: 
            y = -self.location
            self.directiony = 1
            self.flip = True
            x = 0
        if moveD:
            y = self.location
            self.directiony = -1
            self.flip = False
            x = 0
            
        if self.rect.bottom + y > 740:
            y = 740 - self.rect.bottom
        
        if self.rect.top + y < 65:
            y = 5

        if self.rect.left + x > 1080:
            x = 1080 - self.rect.left

        if self.rect.right + x <= 120:
            x = 120 - self.rect.right
        
        self.rect.x += x
        self.rect.y += y      

    def shoot(self):
        if self.rate == 0:
            self.rate = 30
            bullet = Bullet(self.rect.centerx+(40*self.directionx), self.rect.centery+(5*self.directiony),self.directionx)
            bulletGroup.add(bullet)

    def show(self):
        window.blit(pygame.transform.flip(self.image, self.flip, self.flip), self.rect)

player = Player(600, 400, 1, 4)

class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = a
        self.image2 = a2
        self.rect = self.image.get_rect()
        self.rect2 = self.image.get_rect()
        self.rect.center = (x,y)
        self.rect2.center = (x,y)
        self.location = location
        self.speed = 2
        self.speed2 = 3
        self.chance = random.randint(1,5)

    def move(self):
        self.rect.x -= self.speed
        if self.chance == 2:
            self.rect2.x -= self.speed2

    def update(self): 
        global aliensKilled 

        collisionsBullet = pygame.sprite.spritecollide(self, bulletGroup, False)

        for k in collisionsBullet:   
            self.kill()
            alienList.remove(alien) 
            aliensKilled += 1

    def show(self):
        window.blit(a, (self.rect.x, self.rect.y))
        if self.chance == 2:
            window.blit(a2, (self.rect2.x, self.rect2.y))

for j in range(nA):
    alien = Alien(random.randint(1200, 1400), (random.randint(70, 680)), 3)
    alienList.append(alien)

class Log(pygame.sprite.Sprite):
    def __init__(self, x, y, location):
        pygame.sprite.Sprite.__init__(self)
        #self.sprites = [] #disabling animation for now
        #self.sprites.append(l1)
        #self.sprites.append(l2)
        #self.current_sprite = 0
        #self.image = self.sprites[self.current_sprite]
        self.image = l1
        self.image2 = pygame.image.load('assets/opening.png')
        self.rect = self.image.get_rect()
        self.rect2 = self.image2.get_rect()
        self.rect.center = (x,y)
        self.rect2.center = (x,y)
        self.location = location
        self.speed = 3
        self.pos = random.randint(70, 580) 

    def update(self):
        self.speed += lvl/4

    def moveLR(self):
        self.rect.x += self.speed
        self.rect2.x += self.speed

    def moveRL(self): 
        self.rect.x = (self.rect.x *-1) + self.speed
        self.rect2.x = (self.rect2.x *-1) + self.speed
        self.pos = random.randint(70, 580)
        
    def show(self):
        #disabling animation for now
        #self.current_sprite += 0 
        #if self.current_sprite > 1:
            #self.current_sprite = 0
        #self.image = self.sprites[int(self.current_sprite)]
        window.blit(self.image, (self.rect.x, self.rect.y))
        window.blit(self.image2, (self.rect2.x, self.pos))

log = Log(100, 396, 3)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, directionx):
        pygame.sprite.Sprite.__init__(self)
        self.image = b
        self.directionx = directionx
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.speed = 10

    def update(self):
        self.rect.x += (self.directionx * self.speed)

        if self.rect.right < 95 or self.rect.left > 1105:
            #print(self.rect.right)
            #print(self.rect.left)
            self.kill()

bulletGroup = pygame.sprite.Group()

class Rock(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = random.choice(rockRandom)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

rockGroup = pygame.sprite.Group()

rockList = []
for i in range(3):
    x = random.randint(60, 1080)
    y = random.randint(70, 680)
    rock = Rock(x, y)
    rockList.append(rock)
    rockGroup.add(rock)
    if x <= 600+70 and x >= 600-70 and y <= 400+70 and y >= 400-70:
        x += random.randint(80, 100)
        y += random.randint(80, 100)
        rock = Rock(x, y)
        rockList.append(rock)
        rockGroup.add(rock)


gameOver = False

moveR = False
moveL = False
moveU = False
moveD = False
shoot = False

jump = False
playerTurn = False

click = False 

#game loop
while True: 
    if gameOver == True: 
        window.blit(over_bg, (0, 0))
        menu("YOU DIED", font, mColor, 500, 320)
        menu("GAME OVER", font, mColor, 480, 400)

    elif gamePause == True:
        window.blit(menu_bg, (0, 0))
        menu("GAME MENU", font, mColor, 470, 240)

        if resumeButton.draw(window):
            gamePause = False

        if quitButton.draw(window):
            pygame.quit()
            sys.exit()

    else:
        gameOver = False
        window.blit(bg, (0, 0))
        
        menu(f"Direction: {player.directionx, player.directiony}", font3, mColor, 975, 20)

        menu(f"Location: {player.rect.x, player.rect.y}", font3, mColor, 75, 20)
        menu(f"tap SPACE to shoot", font3, mColor, 520, 20)

        hearts = player.lives * ' X '
        if player.lives == 0:
            menu(f"LIVES: *DEAD*", font3, mColor, 75, 745)
        else:
            menu(f"LIVES:{hearts}", font3, mColor, 75, 745)
    
        menu(f"ALIENS KILLED: {aliensKilled}", font3, mColor, 390, 745)
        menu(f"LEVEL: {lvl}", font3, mColor, 720, 745)

        if player.rate == 0:
            menu(f"Fire Rate: ready", font3, mColor, 945, 745)
        else:
            menu(f"Fire Rate: {player.rate}", font3, mColor, 945, 745)

        if len(alienList) == 0:
            lvl += 1
            nA += 2
            for j in range(nA):
                alien = Alien(random.randint(1200, 1400), (random.randint(70, 680)), 2)
                alienList.append(alien)
            log.update()

        rockGroup.draw(window)

        bulletGroup.draw(window)
        bulletGroup.update()

        log.show()
        log.moveLR()
        if log.rect2.x >= 1080 and log.rect.x >= 1080:
            log.moveRL()
            #print(log.rect.x, log.rect2.x)

        for alien in alienList:
            alien.show()
            alien.update()
            alien.move()
            if alien.rect.x + alien.image.get_height() < 64: 
                player.lives -= 1
                alienList.remove(alien)

        player.update()
        player.show()
        player.move(moveR, moveL, moveU, moveD)

        if player.lives <= 3 and player.lives > 0:
            if shoot: 
                comb = []
                comb.append(player.directionx)
                comb.append(player.directiony)
                #print(comb) 
                player.shoot()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        
        if player.lives == 0:
            gameOver = True

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                gamePause = True
            if event.key == K_e:
                jump = True
            if event.key == K_SPACE:
                shoot = True
            if event.key == K_RIGHT or event.key == K_d:
                moveR = True
            if event.key == K_LEFT or event.key == K_a:
                moveL = True
            if event.key == K_UP or event.key == K_w:
                moveU = True
            if event.key == K_DOWN or event.key == K_s:
                moveD = True

        if event.type == KEYUP:
            if event.key == K_e:
                jump = False
            if event.key == K_SPACE:
                shoot = False
            if event.key == K_RIGHT or event.key == K_d:
                moveR = False
            if event.key == K_LEFT or event.key == K_a:
                moveL = False
            if event.key == K_UP or event.key == K_w:
                moveU = False
            if event.key == K_DOWN or event.key == K_s:
                moveD = False
    
    pygame.display.update()
    clock.tick(60)

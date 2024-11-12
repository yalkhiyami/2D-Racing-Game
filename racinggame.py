import pygame
import time
import math
from helpers import imgscale
from helpers import rotatecenter
from helpers import centertext, titletext, subtitletext, subsubtitletext
import random
#from helpers import pause


pygame.font.init()
TRACK = imgscale(pygame.image.load("imgs/track.png"),0.6)
TRACK2 = imgscale(pygame.image.load("imgs/track2.png"),1.7)
TRACK2M = imgscale(pygame.image.load("imgs/track2mask.png"),1.7)
TRACK2M2 = pygame.mask.from_surface(TRACK2M)

BLUE = imgscale(pygame.image.load("imgs/blueline.png"), 0.6)
FINISH = imgscale(pygame.image.load("imgs/finish.png"), 0.8)
FINISHP = (905, 327)
KONI =  imgscale(pygame.image.load("imgs/koni.png"), 0.8)
MUSTANG = imgscale(pygame.image.load("imgs/mustanggt.png"), 0.4)
BG1 = imgscale(pygame.image.load("imgs/bg1.jpg"), 2)
BG2 = imgscale(pygame.image.load("imgs/bg2.jpg"), 0.5)
bgL = [BG1,BG2]
f = 30
finc = True    
CARS = [MUSTANG,KONI]
BLUE2 = pygame.mask.from_surface(BLUE)
FINISHMASK = pygame.mask.from_surface(FINISH)
randbg = random.choice(bgL)
MAINF = pygame.font.SysFont("comicsans",20)

TITLEF = pygame.font.SysFont("adorn",40)

SUBTITLEF = pygame.font.SysFont("arial",f)

RED_CAR = imgscale(pygame.image.load("imgs/red-car.png"),0.07)
YELLOW_CAR = imgscale(pygame.image.load("imgs/yellow-car.png"),0.07)

quotes = ["If you're in control, you're not going fast enough.","What's behind you doesn't matter.", "Faster, Faster, until the thrill of speed overcomes the fear of death." ]

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing game")

FPS = 60

TRAIL = [(937, 128), (633, 110), (486, 38),
         (338, 109), (153, 124), (120, 218), (603, 240), (652, 365), (116, 400), (147, 518), (958, 513), (954, 338)]
TRAIL2 = [(805, 145), (290, 163), (203, 333), (361, 499), (851, 481), (949, 347)]




class Info:
    
    L = 10
    
    def __init__(self, level = 1):
        self.level = level
        self.start = False
        self.leveltime = 0
        
    def nextL(self):
        
        self.level += 1
        self.start = False
        
    def reset(self):
        self.level = 1
        self.start = False
        self.leveltime = 0
    
    def gameOver(self):
        
        return self.level > self.L
    
    def startL(self):
        self.start = True
        self.leveltime = time.time()
        
    def getLtime(self):
        if not self.start:
            return 0
        return round(time.time() - self.leveltime)

gameInfo = Info()

class Car:
    
    def __init__(self,maxspeed,rotationspeed):
        self.img = self.IMG
        self.maxspeed = maxspeed
        
        self.v = 0
        self.rotationspeed = rotationspeed
        self.angle = 0
        self.x, self.y = self.STARTPOS
        #acceleration: https://www.geeksforgeeks.org/python-program-to-calculate-acceleration-final-velocity-initial-velocity-and-time/#:~:text=Python%20program%20to%20calculate%20acceleration%2C%20final%20velocity%2C%20initial%20velocity%20and%20time,-View%20Discussion&text=Here%20we%20can%20find%20the,a%20%3D%20(v%2Du)%2Ft.
        self.acc = 0.2
    def rotate(self,left=False,right=False):
        if left:
            self.angle += self.rotationspeed
        elif right:
            self.angle -= self.rotationspeed
            
    def draw(self,win):
        rotatecenter(win, self.img, (self.x,self.y), self.angle)
    def forward(self):
        self.v = min(self.v + self.acc, self.maxspeed)
        self.move()
    def backward(self):
        self.v = max(self.v - self.acc, -self.maxspeed/2)
        self.move()
        
    def deceleration(self):
        self.v = max(self.v - self.acc,0)
        self.move()
    def move(self):
        r = math.radians(self.angle)
        ver = math.cos(r) * self.v
        hor = math.sin(r) * self.v
        
        self.x -= hor
        self.y -= ver
    #https://stackoverflow.com/questions/29640685/how-do-i-detect-collision-in-pygame
    #i did this mostly myself, i used this website as it helped me to understand
    #collision in pygame
    def collision(self,mask,x=0,y=0):
        carmask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        intersec = mask.overlap(carmask,offset)
        return intersec
    
    def reset(self):
        self.x, self.y = self.STARTPOS
        self.angle = 0
        self.v = 0
    
        
class PlayCar(Car):
    IMG = RED_CAR
    STARTPOS = (924, 280)
    
    def deceleration(self):
        self.v = max(self.v - self.acc,0)
        self.move()
        
    def bounce(self):
        self.v = -self.v
        self.move()

class BotCar(PlayCar):
    IMG = YELLOW_CAR
    STARTPOS = (960, 280)
    
    def __init__(self,maxspeed,rotationspeed,trail=[]):
        super().__init__(maxspeed,rotationspeed)
        self.trail = trail
        self.place = 0
        self.v = maxspeed
        
    def dpoints(self,win):
        for p in self.trail:
            #pygame.draw.circle(win,(0,0,0), p, 5)
            pass
        
    def draw(self,win):
        super().draw(win)
        self.dpoints(win)
    
    def calangle(self):
        tx, ty = self.trail[self.place]
        deltax = tx - self.x
        deltay = ty - self.y
        #https://stackoverflow.com/questions/61966933/how-to-calculate-the-angle-of-a-line-form-by-two-points-from-the-north-direction
        #didnt copy this but it helped a lot 
        if deltay == 0:
           ang = math.pi/2
        else:
           if ty > self.y:
              ang = math.pi + math.atan(deltax/deltay)
           else:
              ang = math.atan(deltax/deltay)
            
        if deltay > self.y:
            ang += math.pi

            
        
        deltaangle = self.angle - math.degrees(ang)
        
        if deltaangle >= 180:
            deltaangle -= 0
    
        if deltaangle > 0:
            self.angle -= min(self.rotationspeed, abs(deltaangle))
        else:
            self.angle += min(self.rotationspeed, abs(deltaangle))
        
    def newtrailp(self):
            
        objective = self.trail[self.place]
        rec = pygame.Rect(self.x,self.y,self.img.get_width(),self.img.get_height())
        if rec.collidepoint(*objective):
            self.place += 1
            
    def move(self):
        if self.place >= len(self.trail):
            return
        
        self.calangle()
        self.newtrailp()
        super().move()
        
    def nextL(self,level):
        self.reset()
        self.v = self.maxspeed + (level - 1) * 0.2
        self.place = 0


    
def draw (win, images, playercar,botcar,gameInfo):
    for img, pos in images:
        win.blit(img,pos)
        
    levelT = MAINF.render(f"Level {gameInfo.level}",1,(0,0,0))
    win.blit(levelT,(10,HEIGHT - levelT.get_height()-70))
    
    timeT = MAINF.render(f"Time {gameInfo.getLtime()}",1,(0,0,0))
    win.blit(timeT,(10,HEIGHT - timeT.get_height()-40))
    
    velocityT = MAINF.render(f"Velocity {round(playercar.v,1)}",1,(0,0,0))
    win.blit(velocityT,(10,HEIGHT - velocityT.get_height()-10))
        
    playercar.draw(win)
    botcar.draw(win)
    pygame.display.update()
    
def pause():
    
    paused = True
    

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                
        pygame.display.get_surface().fill((10,30, 25))
        titletext(WIN,TITLEF,"Paused")
        subtitletext(WIN,SUBTITLEF,"Press C to continue")
        pygame.display.update()
        clock.tick(10)    
def movePlayer(playercar):
    keys = pygame.key.get_pressed()
    moved = False
    if keys[pygame.K_a]:
        playercar.rotate(left = True)
    if keys[pygame.K_d]:
        playercar.rotate(right = True)
    if keys[pygame.K_w]:
        moved = True
        playercar.forward()
    if keys[pygame.K_b]:
        moved = True
        playercar.forward()
        playercar.v +=5
        
    if keys[pygame.K_s]:
        moved = True
        playercar.backward()
    
    elif keys[pygame.K_p]:
        pause()


        
    if not moved:
        playercar.deceleration()
        
def coll(playercar,botcar,gameInfo):    
    if playercar.collision(BLUE2) != None:
        playercar.bounce()
        

        
    botfinishline = botcar.collision(FINISHMASK,*FINISHP)
    if botfinishline != None:
        centertext(WIN,MAINF,"Loss!")
        pygame.display.update()
        pygame.time.wait(2000)
        gameInfo.reset()
        playercar.reset()
        botcar.reset()
    
    
    playerfinishline = playercar.collision(FINISHMASK,*FINISHP)
    if playerfinishline != None:
        if playerfinishline[1] == 0:
            playercar.bounce()
        else:
            gameInfo.nextL()
            playercar.reset()
            botcar.nextL(gameInfo.level)

run = True
clock = pygame.time.Clock()
images = [(randbg,(0,0)),(TRACK, (0,0)),(FINISH,FINISHP),(BLUE,(0,0))]
playercar = PlayCar(7,6)
botcar = BotCar(3,8,TRAIL)





        

while run:

        
 
    WIN.blit(FINISH,(110,110))
    WIN.blit(TRACK,(0,0))
    WIN.blit(BLUE,(0,0))
    rand = random.choice(quotes)
    randd = random.choice(CARS)
    WIN.blit(RED_CAR,(50,60))
    draw(WIN, images,playercar,botcar, gameInfo)
    
    while not gameInfo.start:
        
        
        pygame.display.get_surface().fill((100, 23, 255))
        titletext(WIN,TITLEF,"2D RACING GAME!")
        WIN.blit(randd,(0,0))
        
        subtitletext(WIN,TITLEF,rand)
        centertext(WIN,MAINF,f"press space to play level {gameInfo.level}")
        subsubtitletext(WIN,MAINF,f"press 2 for the cowards way out in level {gameInfo.level}, easy map")
        pygame.display.update()
        keys = pygame.key.get_pressed()
        L = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() 
                break
 
                

            if keys[pygame.K_SPACE]:
                gameInfo.startL()
            elif keys[pygame.K_2]:
           
                
                TRACK = TRACK2
                BLUE = TRACK2M
                BLUE2 = TRACK2M2
                FINISH = imgscale(pygame.image.load("imgs/finish.png"), 1.5)
                FINISHMASK = pygame.mask.from_surface(FINISH)
                botcar.trail = TRAIL2
                images = [(randbg,(0,0)),(FINISH,(842,330)),(TRACK2M,(0,0))]
                
                FINISHMASK = pygame.mask.from_surface(FINISH)
                gameInfo.startL()
            
                

            
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break


        
    movePlayer(playercar)
    botcar.move()
    
    if playercar.collision(pygame.mask.from_surface(YELLOW_CAR), botcar.x,botcar.y) is not None:
        playercar.bounce()
    
    coll(playercar,botcar,gameInfo)
    
    if gameInfo.gameOver():
        centertext(WIN,MAINF,"Win!")
        pygame.display.update()
        pygame.time.wait(2000)
        gameInfo.reset()
        playercar.reset()
        botcar.reset()
            
        
    
print(botcar.trail)   
pygame.quit()

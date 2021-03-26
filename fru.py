from tkinter import *
import os
import random
import pygame
pygame.init()
random.seed()

try:
    d = open("frustat.txt")
    d.close()
except:
    d = open("frustat.txt", "w")
    d.write("0")
    d.close()

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class runner:
    def __init__(self):
        self.x=screenSize/2
        self.y=screenSize/2
        self.size=30
        self.speed=5
        self.color=runnerColor
        self.way="up"
        self.right, self.left, self.up, self.down = False, False, False, False
        self.shots=[]
        self.knifes=[]

    def move(self):
        if self.x<0:
            self.x=1
        if self.y<0:
            self.y=1
        if self.x>=screenSize-self.size:
            self.x=screenSize-self.size-1
        if self.y>=screenSize-self.size:
            self.y=screenSize-self.size-1
        else:
            if self.right:
                self.x+=self.speed
            if self.left:
                self.x-=self.speed
            if self.up:
                self.y-=self.speed
            if self.down:
                self.y+=self.speed

    def image(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size), 0)

    def attack(self, lastX, lastY):
        newShot=shot(self.x+self.size/2, self.y+self.size/2, lastX, lastY)
        self.shots.append(newShot)

    def attackKnife(self):
        global allowedKnifes
        if allowedKnifes<=0:
            return
        allowedKnifes-=1
        newKnife=knife()
        self.knifes.append(newKnife)


class shot:
    def __init__(self, x, y, lastX, lastY):
        self.x, self.y, self.lastX, self.lastY = x, y, lastX, lastY
        self.size=5
        self.color=weaponColor
        self.speed=10
        while (self.lastX-self.x)%self.speed != 0:
            self.lastX+=1
        while (self.lastY-self.y)%self.speed != 0:
            self.lastY+=1

    def move(self):
        if self.x>self.lastX:
            self.x-=self.speed
        if self.x<self.lastX:
            self.x+=self.speed
        if self.y>self.lastY:
            self.y-=self.speed
        if self.y<self.lastY:
            self.y+=self.speed
        if self.x  == self.lastX and self.y == self.lastY:
            player.shots.remove(self)

    def kill(self):
        for enemyNr in enemyList:
            if self.x>=enemyNr.x and self.y>=enemyNr.y and self.x<=enemyNr.x+enemyNr.size and self.y<=enemyNr.y+enemyNr.size:
                try:
                    player.shots.remove(self)
                except:
                    pass
                try:    
                    enemyNr.minus()
                except:
                    pass
                continue
    def image(self):
        pygame.draw.ellipse(screen, self.color, (self.x, self.y, self.size, self.size), 0)


class knife:
    def __init__(self):
        self.size=100
        self.x, self.y = player.x-(self.size-player.size)/2, player.y-(self.size-player.size)/2
        self.color=weaponColor
        self.timeLeft=5

    def kill(self):
        for enemyNr in enemyList:
            if self.x-self.size<=enemyNr.x and self.y-self.size<=enemyNr.y and enemyNr.x<=self.x+self.size and enemyNr.y<=self.y+self.size:
                try:
                    enemyList.remove(enemyNr)
                except:
                    pass

    def image(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size), 0)

class bonus:
    def __init__(self):
        self.size = 25
        self.x, self.y = random.randint(0, screenSize-self.size), random.randint(0, screenSize-self.size)
        self.color = weaponColor
    
    def delete(self):
        global lives, bonusList
        for enemyNr in enemyList:
            if enemyNr.x>=self.x-self.size and enemyNr.x<=self.x+self.size and enemyNr.y>=self.y-self.size and enemyNr.y<=self.y+self.size:
                bonusList.remove(self)
                break
        if player.x>=self.x-self.size and player.x<=self.x+self.size and  player.y>=self.y-self.size and player.y<=self.y+self.size:
            lives+=1
            bonusList.remove(self)

    def image(self):
        pygame.draw.ellipse(screen, self.color, (self.x, self.y, self.size, self.size), 0)

class enemy:
    def __init__(self):
        self.size=30
        if random.randint(0,1) == 0:
            self.x=random.randint(0, screenSize-self.size)
            self.y=random.randint(0,1)*screenSize-self.size
        else:
            self.x=random.randint(0,1)*screenSize-self.size
            self.y=random.randint(0, screenSize-self.size)
        if random.randint(1, 50) == 1:
            self.general = True
        else:
            self.general = False
        self.color=enemyColor
        if self.general:
            self.speed = 4
            self.lives = 2
        else:
            self.speed = 3.6
            self.lives = 1

    def move(self):
        global aktiv
        if self.x>player.x:
            self.x-=self.speed
        if self.x<player.x:
            self.x+=self.speed
        if self.y>player.y:
            self.y-=self.speed
        if self.y<player.y:
            self.y+=self.speed

        if self.x>player.x-self.size and self.x<player.x+self.size and self.y>player.y-self.size and self.y<player.y+self.size:
            aktiv=False

    def minus(self):
        self.lives-=1
        if self.lives <= 0:
            enemyList.remove(self)
        
    def image(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size), 0)
        if self.general:
            pygame.draw.line(screen, runnerColor, (self.x, self.y), (self.x+self.size, self.y+self.size), 3)
            pygame.draw.line(screen, runnerColor, (self.x+self.size, self.y), (self.x, self.y+self.size), 3)


def draw():
    global lives, lvl, hs
    screen.fill(screenColor)
    for shotNr in player.shots:
        shotNr.image()
    for knifeNr in player.knifes:
        knifeNr.image()
    for enemyNr in enemyList:
        enemyNr.image()
    for bonusNr in bonusList:
        bonusNr.image()
    lvlText=font.render(str(lvl), True, runnerColor)
    for i in range(lives):
        pygame.draw.ellipse(screen, runnerColor, (i*20+5, 10, 15, 15), 0)
    screen.blit(lvlText, (950,10))
    player.image()

def win():
    global lvl, aktiv, lives
    if len(enemyList) == 0:
        lvl+=1
        lives+=1
        aktiv=False
    

def main(lvl):
    global screenSize, enemyList, bonusList, kinfesCounter, attackCounter, gameAktiv, player, screen, aktiv, lives
    
    clock=pygame.time.Clock()

    player=runner()

    enemyList=[]
    for i in range(lvl):
        newEnemy=enemy()
        enemyList.append(newEnemy)

    bonusList=[]
    if random.randint(1, 20) == 1:
        newBonus = bonus()
        bonusList.append(newBonus)

    kinfesCounter=3
    attackCounter=0

    aktiv=True
    while aktiv:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                aktiv, gameAktiv= False, False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player.up=True
                if event.key == pygame.K_s:
                    player.down=True
                if event.key == pygame.K_a:
                    player.left=True
                if event.key == pygame.K_d:
                    player.right=True
                if event.key == pygame.K_SPACE and kinfesCounter>0:
                    player.attackKnife()
                    attackCounter+=1
                    kinfesCounter-=1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    player.up=False
                if event.key == pygame.K_s:
                    player.down=False
                if event.key == pygame.K_a:
                    player.left=False
                if event.key == pygame.K_d:
                    player.right=False
            if event.type == pygame.MOUSEBUTTONDOWN:
                attackCounter+=1
                x, y = pygame.mouse.get_pos()
                player.attack(x, y)

        for enemyNr in enemyList:
            enemyNr.move()
        for shotNr in player.shots:
            shotNr.move()
            shotNr.kill()
        for knifeNr in player.knifes:
            knifeNr.kill()
            knifeNr.timeLeft-=1
        for bonusNr in bonusList:
            bonusNr.delete()
        player.move()
        draw()
        for knifeNr in player.knifes:
            if knifeNr.timeLeft==0:
                player.knifes.remove(knifeNr)
        win()
        pygame.display.flip()
        fps = 60
        clock.tick(fps)
    for enemyNr in enemyList:
        enemyList.remove(enemyNr)
    for shotNr in player.shots:
        player.shots.remove(shotNr)
    lives-=1

    
def gameSession():
    global gameAktiv, lvl, lives, hs, green, red, black, white, yellow, font, screen, enemyColor, runnerColor, weaponColor, screenColor, screenSize, allowedKnifes
    green, red, black, white, yellow, blue = (0,100,0), (255,0,0), (0,0,0), (255,255,255), (255,255,0), (0,0,255)
    font=pygame.font.SysFont("comicsansms",20)
    screenSize=1000
    screen=pygame.display.set_mode((screenSize, screenSize))
    pygame.display.set_caption("Frunker")
    with open("frustat.txt","r") as f:
        hs=f.read()
    allowedKnifes = 5
    lives=5
    lvl=1
    gameAktiv=True
    while gameAktiv:
        if lives<=0:
            gameAktiv=False
            break
        main(lvl)
    try:
        if lvl>int(hs):
            with open("frustat.txt","w") as f:
                try:   
                    f.write(str(lvl))
                except: pass
    except:
        with open("frustat.txt","w") as f:
            f.write(str(lvl))
    frunkerScreen()
    
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------ 

def frunkerScreen():
    screen.fill(black)
    mainTextFont=pygame.font.SysFont("comicsansms", 100)
    mainText=mainTextFont.render("FRUNKER", True, white)
    screen.blit(mainText, (250, 450))
    nameText=font.render("Name: "+str(name), True, white)
    screen.blit(nameText, (50, 950))
    if lvl>int(hs):
        lvltext = str(lvl)
        gratulationtext = font.render("New Highscore!", True, yellow)
    else:
        lvltext = str(hs)
        gratulationtext = font.render("", True, black)
    screen.blit(gratulationtext, (250, 600))
    scoreText=font.render("Highscore: "+lvltext, True, white)
    screen.blit(scoreText, (300,950))
    colorThemeText=font.render("Colortheme: "+str(colorThemesNames[colorIndex]), True, white)
    screen.blit(colorThemeText, (500,950))
    pygame.display.flip()

menu = Tk()
menu.title("Frunkermenu")

e = Entry(menu)
e.pack()

#color themes: (bg, enemy, runner, weapon)
green, red, black, white, yellow, blue = (0,100,0), (255,0,0), (0,0,0), (255,255,255), (255,255,0), (0,0,255)
classic=(green, yellow, red, black)
cowb=((255,117,20),(54,36,10),(30,110,27),(54,36,10))
green=((220,255,220),(0,42,9),(2,140,106),(0,42,9))
blue=((133,184,203),(40,59,66),(29,106,150),(40,59,66))
sand=((237,201,175),(164,104,67),(55,13,0),(0,100,0))
smgreen=((155,207,184),(104,156,151),(7,42,36),(0,150,0))
red=((254,119,115),(14,3,1),(232,30,37),(14,3,1))
lila=((211,183,216),(161,62,151),(40,14,59),(99,42,126))
colorThemes=(classic, cowb, green, blue, sand, smgreen, red, lila)
colorThemesNames=("classic","cowboy","green","blue","sand","smgreen","red","lila")


def game():
    global name
    name=e.get()
    try:
        if not name[0].isalpha():
            pass
    except:
        return False
    gameSession()
colorIndex=0
screenColor, enemyColor, runnerColor, weaponColor = colorThemes[colorIndex] 

def change_color():
    global colorIndex, screenColor, enemyColor, runnerColor, weaponColor
    colorIndex+=1
    if colorIndex>=len(colorThemes):    colorIndex=0
    screenColor, enemyColor, runnerColor, weaponColor = colorThemes[colorIndex]
    try:
        frunkerScreen()
    except: pass

gameB=Button(menu, text="New Game", command=game)
colorB=Button(menu, text="change color", command=change_color)
gameB.pack()
colorB.pack()


menu.mainloop()

pygame.quit()

import pygame as pg
from pygame.math import Vector2
from Subroutines import *
from operator import * 


class Button():

    # initiatte sprite
    def __init__(self, image, pos, name):
        # load atributes
        self.image_active = pg.image.load(f'Images/Buttons/{image}_active.png').convert_alpha()
        self.image_inactive = pg.image.load(f'Images/Buttons/{image}_inactive.png').convert_alpha()
        self.image = self.image_inactive
        self.rect = self.image.get_rect()
        self.pressed = False
        self.active = False
        self.pos = Vector2(pos)
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        self.nameText = name
        self.name = ''

    def update(self, screen, surface, mouseDown):
        self.handleEvent(mouseDown)
        self.draw(screen, surface)

    def handleEvent(self, mouseDown):
        # check if button pressed
        mousePos = pg.mouse.get_pos()
        if self.rect.collidepoint(mousePos):
            self.active = True
            if mouseDown:
                self.pressed = True
            else:
                self.pressed = False
        else:
            self.active = False
        self.image = self.image_active if self.active else self.image_inactive
        self.name = self.nameText if self.active else ''
        
    def draw(self, screen, surface):
        # draw button
        screen.blit(self.image, self.pos)
        surface.blit(self.image, self.pos)
        mousePos = Vector2(pg.mouse.get_pos())
        font = pg.font.SysFont("Consolas", 10)
        screen.blit((font.render(self.name, 1, (0,0,0))), (mousePos.x + 15, mousePos.y))
        surface.blit((font.render(self.name, 1, (0,0,0))), (mousePos.x + 15, mousePos.y))
        


class MovingButton(Button):

    # initiatte sprite
    def __init__(self, image, pos, offset, proximityFeildName, name):
        # load superior atributes
        super().__init__(image, pos, name)
        # load atributes
        self.pos = Vector2(self.pos.x + offset[0], self.pos.y + offset[1])
        self.proximityFeildName = proximityFeildName

    def update(self, screen, surface, mouseDown, map1):
        self.move(map1)
        self.handleEvent(mouseDown, map1)
        self.draw(screen, surface)

    def move(self, map1):
        # move button 
        self.pos = Vector2(self.pos.x + map1.moveXY.x, self.pos.y + map1.moveXY.y)
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

    def handleEvent(self, mouseDown, map1):
        # check if button pressed
        mousePos = pg.mouse.get_pos()
        if self.rect.collidepoint(mousePos) and self.proximityFeildName in map1.movementResult[1] or self.rect.collidepoint(mousePos) and self.proximityFeildName == 'alwaysAvalable':
            self.active = True
            if mouseDown:
                self.pressed = True
            else:
                self.pressed = False
        else:
            self.active = False
        self.image = self.image_active if self.active else self.image_inactive
        self.name = self.nameText if self.active else ''


class ScrollingButton(Button):

    # initiatte sprite
    def __init__(self, image, pos, offset, direction, deactivationFeild, name):
        # load superior atributes
        super().__init__(image, pos, name)
        # load atributes
        self.pos = Vector2(self.pos.x + offset[0], self.pos.y + offset[1])
        self.xScroll = True if direction == 'x' else False
        if len(deactivationFeild) == 2:
            self.twoDeactivationFeilds = True
            self.deactivationFeild1 = deactivationFeild[0]
            self.deactivationFeild2 = deactivationFeild[1]
        else:
            self.twoDeactivationFeilds = False
            self.deactivationFeild = deactivationFeild[0]
        self.deactivated = False

    def update(self, screen, surface, mouseDown, mouseScroll):
        self.move(mouseScroll)
        self.handleEvent(mouseDown)
        if not self.deactivated:
            self.draw(screen, surface)

    def move(self, mouseScroll):
        # move button
        self.pos = Vector2(self.pos.x + (mouseScroll*30), self.pos.y) if self.xScroll else Vector2(self.pos.x, self.pos.y + (mouseScroll*30))
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

    def handleEvent(self, mouseDown):
        if self.twoDeactivationFeilds:
            if self.rect.colliderect(self.deactivationFeild1):
                self.deactivated = True
            elif self.rect.colliderect(self.deactivationFeild2):
                self.deactivated = True
            else: 
                self.deactivated = False
        else:
            self.deactivated = True if self.rect.colliderect(self.deactivationFeild) else False

        # check if button pressed
        mousePos = pg.mouse.get_pos()
        if self.rect.collidepoint(mousePos) and not self.deactivated:
            self.active = True
            if mouseDown:
                self.pressed = True
            else:
                self.pressed = False
        else:
            self.active = False
        self.image = self.image_active if self.active else self.image_inactive
        self.name = self.nameText if self.active else ''
    


class Clock12Hr():
    def __init__(self):
        self.clockBackground = pg.image.load(f'Images/Objects/ClockBackground.png').convert_alpha()
        self.clockHand = pg.image.load(f'Images/Objects/ClockHand.png').convert_alpha()
        self.pos = Vector2((1390,760))
        self.angle = 0
        self.totTicks = 0
        self.timeOfDay = [0,0]
        self.offset = Vector2(0,7)
        self.active = False

    def retTick(self):
        return self.totTicks

    def setTick(self, data):
        self.totTicks = data
        
    def update(self, screen, surface):
        self.itrTick()
        self.calcTime()
        self.draw(screen, surface)
        self.dispayTime(screen, surface)

    def itrTick(self):
        self.totTicks += 1

    def calcTime(self):
        timeOfDayInSecconds = self.totTicks % 21600  // 30
        days = self.totTicks // 21600
        hours = timeOfDayInSecconds // 60
        secconds = (timeOfDayInSecconds % 60)
        self.timeOfDay = [str(days),str(hours),str(secconds)]
        
    def draw(self, screen, surface):
        self.angle = (self.totTicks % 21600) // 60
        screen.blit(self.clockBackground,(self.pos.x - 25, self.pos.y - 25))
        surface.blit(self.clockBackground,(self.pos.x - 25, self.pos.y - 25))
        clockHandRotate = pg.transform.rotate(self.clockHand, -(self.angle - 180))
        offsetRotated = self.offset.rotate(self.angle)
        clockHandRotateRect = clockHandRotate.get_rect(center = self.pos+offsetRotated)
        screen.blit(clockHandRotate,clockHandRotateRect)
        surface.blit(clockHandRotate,clockHandRotateRect)

    def dispayTime(self, screen, surface):
        mousePos = pg.mouse.get_pos()
        if mousePos[0] >= (self.pos.x-25) and mousePos[0] <= ((self.pos.x-25)+50) and mousePos[1] >= (self.pos.y-25) and mousePos[1] <= ((self.pos.y-25)+50):
            font = pg.font.SysFont("Consolas", 18)
            text(screen, surface, [f'{self.timeOfDay[1]:2}:{self.timeOfDay[2]:2}', (self.pos.x-85,self.pos.y-20), 18, (0,0,0)])
            text(screen, surface, [f'{self.timeOfDay[0]:2} day(s)', (self.pos.x-125,self.pos.y), 18, (0,0,0)])

            

class Light():
    def __init__(self, lightType, pos):

        # load atributes
        self.pos = Vector2(pos)
        self.background = pg.image.load(f'Images/Objects/Light1_background.png').convert_alpha()
        self.foreground = pg.image.load(f'Images/Objects/Light1_foreground.png').convert_alpha()
        self.lightBulb = pg.image.load(f'Images/Objects/{lightType}.png').convert_alpha()
        self.lightOrb = pg.image.load(f'Images/Objects/{lightType}Light.png').convert_alpha()
        
        
    def draw(self, screen, surface):

        screen.blit(self.background, self.pos)
        surface.blit(self.background, self.pos)
        screen.blit(self.lightBulb, ((self.pos.x + 61),(self.pos.y + 103)))
        surface.blit(self.lightBulb, ((self.pos.x + 61),(self.pos.y + 103)))
        surface.blit(self.lightOrb, ((self.pos.x - 220),(self.pos.y + 103)))
        surface.blit(self.foreground, self.pos)



class Object():

    # initiate sprite
    def __init__(self, image, pos):
        self.image = pg.image.load(f'Images/Objects/{image}.png').convert_alpha()
        self.pos = Vector2(pos)

    def draw(self, screen, surface):
        # draw object
        screen.blit(self.image, self.pos)
        surface.blit(self.image, self.pos)
        

class Menu(Object):
    
    def __init__(self, image):
        super().__init__(f'Menus/{image}', (0,0))
        


class InventoryItem(pg.sprite.Sprite):

    def __init__(self, image, pos, quantity):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(f'Images/Buttons/itemPacketButtons/{image}_inactive.png').convert_alpha()
        self.pos = Vector2(pos)
        self.quantity = quantity

    def update(self, screen, surface, mouseScroll):
        self.pos.y += mouseScroll*30
        text(screen, surface, (f'x{self.quantity}', (self.pos.x + 150,self.pos.y + 90), 72))
        screen.blit(self.image, self.pos)

        

class Map():

    # initiate sprite
    def __init__(self, imageForeground, imageBackground, pos, obsticalList):
        
        # initiate map
        self.mapImageForeground =  pg.image.load(f'Images/Maps/{imageForeground}.png').convert_alpha()
        self.foreground = True
        self.mapImageBackground =  pg.image.load(f'Images/Maps/{imageBackground}.png').convert_alpha()
        self.pos = Vector2(pos)

        # initiate playerRect ghost
        self.playerRectImage = pg.Surface((50,10))
        self.playerRect = self.playerRectImage.get_rect()
        self.playerRect.center = (720, 455)

        # initiate player images
        self.ticks = 0
        self.playerUp1 = pg.image.load(f'Images/Character/joeup1.png').convert_alpha()
        self.playerUp2 = pg.image.load(f'Images/Character/joeup2.png').convert_alpha()
        self.playerDown1 = pg.image.load(f'Images/Character/joedown1.png').convert_alpha()
        self.playerDown2 = pg.image.load(f'Images/Character/joedown2.png').convert_alpha()
        self.playerLeft1 = pg.image.load(f'Images/Character/joeleft1.png').convert_alpha()
        self.playerLeft2 = pg.image.load(f'Images/Character/joeleft2.png').convert_alpha()
        self.playerRight1 = pg.image.load(f'Images/Character/joeright1.png').convert_alpha()
        self.playerRight2 = pg.image.load(f'Images/Character/joeright2.png').convert_alpha()
        self.playerImage = self.playerDown1

        # initiate colision map
        self.obsticals = []
        for line in obsticalList:
            if line[2] == 'w':
                obstical = ((lineObstical(line[0],line[1])),'w')
            if line[2] == 'a':
                obstical = ((areaObstical(line[0],line[1])),'a', line[3])
            obstical[0].x += self.pos.x
            obstical[0].y += self.pos.y
            self.obsticals.append(obstical)
        self.showColisionMap = False

    # update sprite
    def update(self, screen):
        self.move()
        self.draw(screen)

    def move(self):
        self.foreground = True

        # misc key presses
        keys = pg.key.get_pressed()
        if keys[pg.K_c]:
            self.showColisionMap = True
        else:
            self.showColisionMap = False

        # call movement engine subroutine
        self.movementResult = wasd(self)
        self.moveXY = Vector2(self.movementResult[0])
        if 'Remove_Foreground' in self.movementResult[1]:
            self.foreground = False
        
        # update pos
        self.pos.x += self.moveXY.x
        self.pos.y += self.moveXY.y

        # update colision map pos
        for obstical in self.obsticals:
            obstical[0].x += self.moveXY.x
            obstical[0].y += self.moveXY.y
        
    def draw(self, screen):

        # draw map background
        screen.blit(self.mapImageBackground, self.pos)

    def drawForeground(self, screen):
        
        # draw player
        pattern = 0
        if self.movementResult[3]:
            if self.ticks < 10:
                pattern = 1
            elif self.ticks < 20:
                pattern = 2
            else:
                self.ticks -= 21
            self.ticks += 1
    
        if self.movementResult[2] == 'up':
            self.playerImage = self.playerUp1 if pattern == 1 else self.playerUp2
        if self.movementResult[2] == 'down':
            self.playerImage = self.playerDown1 if pattern == 1 else self.playerDown2
        if self.movementResult[2] == 'left':
            self.playerImage = self.playerLeft1 if pattern == 1 else self.playerLeft2
        if self.movementResult[2] == 'right':
            self.playerImage = self.playerRight1 if pattern == 1 else self.playerRight2

        screen.blit(self.playerImage, (695, 360))
            
        
        # draw map foreground
        if self.foreground: # if "foregreound" = True
            screen.blit(self.mapImageForeground, self.pos)

        if self.showColisionMap:
            
            # draw colision map
            for obstical in self.obsticals:
                if obstical[1] == 'w':
                    pg.draw.rect(screen, (0,255,0), obstical[0])
                if obstical[1] == 'a':
                    pg.draw.rect(screen, (255,0,255), obstical[0])

            # draw playerRect ghost
            pg.draw.rect(screen, (255,0,0), self.playerRect, 2)

            # display stats
            font = pg.font.SysFont("Consolas", 18)
            screen.blit((font.render(f'pos = {self.pos}', 1, (0,255,0))), (10,30))



class Plant(pg.sprite.Sprite):

    # initiate sprite and atributes
    def __init__(self, plantID, pos):
        pg.sprite.Sprite.__init__(self)
        self.pos = Vector2(pos)
        self.plantID = plantID
        self.image = pg.image.load(f'Images/Plants/Blank.png').convert_alpha()
        if self.plantID != -1:
            self.plantName = Qs('Crop.Name', 'Crop, Plant', f'Plant.CropID = Crop.CropID AND Plant.PlantID == {self.plantID}')
            self.startTick = Qi('GrowthStartTick', 'Plant', f'PlantID = {self.plantID}')
            multiplier = Qf('Light.SpeedBonus', 'Light, Planter, PlantPot, Plant', f'Plant.PlantPotID = PlantPot.PlantPotID AND PlantPot.PlanterID = Planter.PlanterID AND Planter.LightID = Light.LightID AND Plant.PlantID = {self.plantID}')
            self.growTicks = int(Qi('Crop.GrowTime', 'Crop, Plant', f'Plant.CropID = Crop.CropID AND Plant.PlantID = {self.plantID}') / multiplier)
            print(self.growTicks)
            self.stageChange = self.growTicks / 5
            self.progTick = (self.stageChange) + self.startTick
            self.dieCheck = plantID
            self.checkedGS1 = False
            self.checkedGS2 = False
            self.checkedGS3 = False
            self.checkedGS4 = False
            self.checkedGS5 = False
        else:
            self.image = pg.image.load(f'Images/Plants/Blank.png').convert_alpha()
        
    def update(self, screen, surface, curTick, dieValue):
        if self.plantID != -1:
            self.die(dieValue)
            self.growthStage(curTick)
        self.draw(screen, surface)

    def die(self, dieValue):
        if dieValue == self.dieCheck:
            print('bruh')
            self.kill()

    def growthStage(self, curTick):
        #print(self.progTick)
        #print(self.stageChange)
        if curTick < self.progTick and self.checkedGS1 == False:
            self.image = pg.image.load(f'Images/Plants/{self.plantName}GS1.png').convert_alpha()
            self.checkedGS1 = True
        elif curTick < self.progTick + self.stageChange and curTick > self.progTick and self.checkedGS2 == False:
            self.image = pg.image.load(f'Images/Plants/{self.plantName}GS2.png').convert_alpha()
            self.checkedGS2 = True
        elif curTick < self.progTick + self.stageChange*2 and curTick > self.progTick + self.stageChange and self.checkedGS3 == False:
            self.image = pg.image.load(f'Images/Plants/{self.plantName}GS3.png').convert_alpha()
            self.checkedGS3 = True
        elif curTick < self.progTick + self.stageChange*3 and curTick > self.progTick + self.stageChange*2 and self.checkedGS4 == False:
            self.image = pg.image.load(f'Images/Plants/{self.plantName}GS4.png').convert_alpha()
            self.checkedGS4 = True
        elif curTick > self.progTick + self.stageChange*4 and self.checkedGS5 == False:
            self.image = pg.image.load(f'Images/Plants/{self.plantName}GS5.png').convert_alpha()
            self.checkedGS5 = True
        else:
            pass

    def draw(self, screen, surface):
        screen.blit(self.image, self.pos)
        surface.blit(self.image, self.pos)



class Queue():
    
    def __init__(self, maxSize):
        self.maxSize = maxSize
        self.size = 0
        self.front, self.rear = 0, -1
        self.queue = []
        for i in range(maxSize):
            self.queue.append('')

    def isFull(self):
        return True if self.maxSize == self.size else False

    def isEmpty(self):
        return True if self.size == 0 else False

    def load(self):
        file = open('GameData/QueueData.txt','r')
        rawData = file.read()
        data = rawData.split(",")
        file.close()
        for item in data:
           self.enqueue(item)

    def save(self):
        queue = ",".join(self.queue)
        file = open('GameData/QueueData.txt','w')
        file.write(queue)
        file.close()
        
    def enqueue(self, item):
        if self.isFull():
            self.dequeue()
            self.enqueue(item)
        else:
            self.size += 1
            self.rear += 1 if self.rear != self.maxSize - 1 else -(self.maxSize - 1)
            self.queue[self.rear] = item

    def dequeue(self):
        if self.isEmpty():
            return 'The queue is empty'
        else:
            self.size -= 1
            item = self.queue[self.front]
            self.front += 1 if self.front != self.maxSize-1 else -(self.maxSize - 1)
            return item

    def showQueue(self):
        print(f'{self.queue}, Front: {self.front}, Rear: {self.rear}')

    def suspicionPercentage(self):
        queueItems = []
        for i in range(len(self.queue)):
            if self.queue[i] not in queueItems and self.queue[i] != '':
                queueItems.append(self.queue[i])
                
        maX = ('',0)
        for i in range(len(queueItems)):
            numItem = countOf(self.queue, queueItems[i])
            if numItem > maX[1]:
                maX = (queueItems[i], numItem)

        sussyness = int((maX[1] / self.maxSize) * 100)

        return sussyness



class suspicionOMatik():

    def __init__(self, RPC):
        self.pos = Vector2(0,0)
        self.backgroundImage = pg.image.load('Images/Objects/susMeterBackground.png').convert_alpha()
        self.suspentage = RPC.suspicionPercentage()
        self.loadingBar = (5, 805-self.suspentage, 10, self.suspentage)
        self.nonLoaded = (5, 705, 10, 100)
        self.color = (0,0,0)
        
    def update(self, screen, surface):
        self.calcLoadingBarColor()
        self.draw(screen, surface)

    def calcLoadingBarColor(self):
        self.color = (255,0,0)
        if self.suspentage < 80:
            self.color = (255,165,0)
            if self.suspentage < 60:
                self.color = (255, 255, 0)
                if self.suspentage < 40:
                    self.color = (0,255,0)

    def draw(self, screen, surface):
        screen.blit(self.backgroundImage, (0, 690))
        pg.draw.rect(screen, (255,255,255), self.nonLoaded)
        pg.draw.rect(screen, self.color, self.loadingBar)
        

class Helicopter():

    def __init__(self):
        self.h1 = pg.image.load('Images/Objects/Helicopter 1.png').convert_alpha()
        self.h2 = pg.image.load('Images/Objects/Helicopter 2.png').convert_alpha()
        self.h3 = pg.image.load('Images/Objects/Helicopter 3.png').convert_alpha()
        self.h4 = pg.image.load('Images/Objects/Helicopter 4.png').convert_alpha()
        self.pos = Vector2(1180,120)
        self.tick = 0

    def update(self,screen,surface):
        self.draw(screen, surface, self.calcRot())

    def calcRot(self):
        self.tick += 1
        if self.tick == 1:
            return self.h1
        elif self.tick == 2:
            return self.h2
        elif self.tick == 3:
            return self.h3
        elif self.tick == 4:
            return self.h4
        else:
            self.tick = 1
            return self.h1

    def draw(self, screen, surface, choice):
        screen.blit(choice, self.pos)
        surface.blit(choice, self.pos)
        
        
        
            
        




        

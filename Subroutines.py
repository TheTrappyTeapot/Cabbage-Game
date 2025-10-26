import pygame as pg
from pygame.math import Vector2
import sqlite3

con = sqlite3.connect('DB/CGDB.db')
cur = con.cursor()



def areaObstical(pos1, pos2):
    image = pg.Surface(((pos2[0]-pos1[0]),(pos2[1]-pos1[1])))
    image = image.get_rect()
    image.x = pos1[0]
    image.y = pos1[1]
    return image


def lineObstical(pos1, pos2):
    # form a rectangle from pos1 & pos2
    if pos1[0] == pos2[0]:
        image = pg.Surface((1,int(pos2[1] - pos1[1])))
    else: # here lies rangBeetValus, gone but not forgotten
        image = pg.Surface((int(pos2[0] - pos1[0]),1))

    image = image.get_rect()
    image.x = pos1[0]
    image.y = pos1[1]

    return image

    
def wasd(map1):
    areaColisionResult = []
    dx = 0 # delta x
    dy = 0 # delta y

    # movement engine
    keys = pg.key.get_pressed()
    moving = True
    if keys[pg.K_w]:
        direction = 'up'
        dy += 5
    if keys[pg.K_s]:
        direction = 'down'
        dy += -5
    if keys[pg.K_a]:
        direction = 'right'
        dx += 5
    if keys[pg.K_d]:
        direction = 'left'
        dx += -5
    if keys[pg.K_LSHIFT]:
        moving = True
        if keys[pg.K_w]:
            dy += 4
        if keys[pg.K_s]:
            dy += -4
        if keys[pg.K_a]:
            dx += 4
        if keys[pg.K_d]:
            dx += -4

    if not keys[pg.K_d] and not keys[pg.K_a] and not keys[pg.K_w] and not keys[pg.K_s]:
        moving = False
        direction = 'down'

    ddx = dx # delta delta x
    ddy = dy # delta delta y     

    # coolisioon detectioon
    for obstical in map1.obsticals:

        # check colision type
        if obstical[1] == 'w':
            # check for y colision
            if map1.playerRect.colliderect(obstical[0].x, obstical[0].y + dy, obstical[0][2], obstical[0][3]):
                if dy == 5 or dy == 9:
                    # change dy to permitable amount
                    ddy = map1.playerRect.top - obstical[0].bottom
            if map1.playerRect.colliderect(obstical[0].x, obstical[0].y + dy, obstical[0][2], obstical[0][3]):
                if dy == -5 or dy == -9:
                    # change dy to permitable amount
                    ddy = map1.playerRect.bottom - obstical[0].top

            # check for x colision
            if map1.playerRect.colliderect(obstical[0].x + dx, obstical[0].y, obstical[0][2], obstical[0][3]):
                if dx == 5 or dx == 9:
                    # change dx to permitable amount
                    ddx = map1.playerRect.left - obstical[0].right
            if map1.playerRect.colliderect(obstical[0].x + dx, obstical[0].y, obstical[0][2], obstical[0][3]):
                if dx == -5 or dx == -9:
                    ddx = map1.playerRect.right - obstical[0] .left

        if obstical[1] == 'a':
             # check for y colision
            if map1.playerRect.colliderect(obstical[0].x + dx, obstical[0].y + dy, obstical[0][2], obstical[0][3]):
                areaColisionResult.append(obstical[2])

    # return pos
    return (ddx, ddy), areaColisionResult, direction, moving


def getPrevLocation(zone):
    # open text file
    LocationLogx = open(f'GameData/{zone}/LocationLogx.txt','r')
    LocationLogy = open(f'GameData/{zone}/LocationLogy.txt','r')
    # retrieve position
    prevLocationx = int(float(LocationLogx.read()))
    prevLocationy = int(float(LocationLogy.read()))
    prevLocation = (prevLocationx, prevLocationy)
    # close text file
    LocationLogx.close()
    LocationLogy.close()
    return prevLocation


def setPrevLocation(pos, zone):
    # open text file
    LocationLogx = open(f'GameData/{zone}/LocationLogx.txt','w')
    LocationLogy = open(f'GameData/{zone}/LocationLogy.txt','w')
    # write new position
    LocationLogx.write(str(pos.x))
    LocationLogy.write(str(pos.y))
    # close text file
    LocationLogx.close()
    LocationLogy.close()

def getMoney():
    # open text file
    file = open(f'GameData/money.txt','r')
    # retrieve money
    money = int(float(file.read()))
    # close text file
    file.close()
    return money

def addMoney(amount):
    curMoney = getMoney()
    # open text file
    file = open(f'GameData/money.txt','w')
    # write new money
    file.write(str(curMoney + amount))
    # close text file
    file.close()

def subMoney(amount):
    curMoney = getMoney()
    # open text file
    file = open(f'GameData/money.txt','w')
    # write new money
    file.write(str(curMoney - amount))
    # close text file
    file.close()

def displayStats(screen,map1):
    # simply write stats on screen corner
    font = pg.font.SysFont("Consolas", 18)
    screen.blit((font.render(f'pos = {map1.pos}', 1, (0,255,0))), (10,10))


def getList(fileName):
    # open text file
    listFile = open(f'GameData/{fileName}.txt','r')
    # retrieve data
    listData = listFile.read()
    # close text file
    listFile.close()

    # format string into list using .split()
    data = []
    temp = []
    temptemp = []
    listData = listData.split(',,,,')
    for i in listData:
        i = i.split(',,,')
        for j in i:
            j = j.split(',,')
            for k in j:
                k = k.split(',')
                temptemp.append(k)
            temp.append(temptemp)
            temptemp = []
        data.append(temp)
        temp = []
    return data


def setList(fileName, data):
    data = str(data)
    data = data.replace("]], [[",",,,")
    data = data.replace("], [",",,")
    data = data.replace("[[[[","")
    data = data.replace("]]]]","")
    data = data.replace("'","")
    data = data.replace(" ","")
    listFile = open(f'GameData/{fileName}.txt','w')
    listFile.write(data)
    listFile.close()


def displaySeedData(screen, surface, uniqueID):
    font = pg.font.SysFont("Consolas", 24)

    if uniqueID == 0:
        name,cost,growthTime,dirt,water = 0,0,0,0,0
    else:
        name = Qs('Name','Crop',f'CropID = {uniqueID}')
        cost = Qi('Price','Crop',f'CropID = {uniqueID}')
        growthTime = Qi('GrowTime','Crop',f'CropID = {uniqueID}')
        dirt = 'Yes'
        if Qi('HydroComp','Crop',f'CropID = {uniqueID}') == 1:
            water = 'Yes'
        else:
            water = 'No'

    displayData = [[(font.render((f'Name: {name}'),1,(0,0,0))), (970,570)] ,
                   [(font.render((f'Cost: {cost}'),1,(0,0,0))), (970,600)] ,
                   [(font.render((f'Growth Time: {growthTime} ticks'),1,(0,0,0))), (970,630)] , 
                   [(font.render((f'Suitible to grow in:'),1,(0,0,0))), (970,660)] ,
                   [(font.render((f'Dirt: {dirt}'),1,(0,0,0))), (1000,685)] ,
                   [(font.render((f'Water: {water}'),1,(0,0,0))), (1000,710)]]

    for i in range(len(displayData)):
        screen.blit(displayData[i][0],displayData[i][1])
        surface.blit(displayData[i][0],displayData[i][1])


def displayProductData(screen, surface, uniqueID):
    font = pg.font.SysFont("Consolas", 24)

    if uniqueID == 0:
        name,sellingValue = 0,0
    else:
        name = Qs('Name','Crop',f'CropID = {uniqueID}')
        sellingValue = Qi('SellingPrice','Crop',f'CropID = {uniqueID}')
    
    displayData = [[(font.render((f'Name: {name}'),1,(0,0,0))), (100,570)] ,
                   [(font.render((f'Value: {sellingValue}'),1,(0,0,0))), (100,600)]]

    for i in range(len(displayData)):
        screen.blit(displayData[i][0],displayData[i][1])
        surface.blit(displayData[i][0],displayData[i][1])


def displayLightData(screen, surface, uniqueID):
    font = pg.font.SysFont("Consolas", 24)

    if uniqueID == 0:
        name,cost,speedBonus = 0,0,0
    else:
        name = Qs('Name','Light',f'LightID = {uniqueID}')
        cost = Qi('Price','Light',f'LightID = {uniqueID}')
        speedBonus = (Qf('SpeedBonus','Light',f'LightID = {uniqueID}') - 1 ) * 100
    
    displayData = [[font.render((f'Name: {name}'),1,(0,0,0)), (770,570)] ,
                   [(font.render((f'Cost: {cost}'),1,(0,0,0))), (770,600)] ,
                   [(font.render((f'Speed Bonus: {speedBonus}% '),1,(0,0,0))), (770,630)]]


    for i in range(len(displayData)):
        screen.blit(displayData[i][0],displayData[i][1])
        surface.blit(displayData[i][0],displayData[i][1])


def displayPlanterData(screen, surface, uniqueID):
    font = pg.font.SysFont("Consolas", 24)

    if uniqueID == 0:
        name,cost,yeildBonus = 0,0,0
    else:
        name = Qs('Name','GrowthMedia',f'GrowthMediaID = {uniqueID}')
        cost = Qi('Price','GrowthMedia',f'GrowthMediaID = {uniqueID}')
        yeildBonus = (Qf('YeildBonus','GrowthMedia',f'GrowthMediaID = {uniqueID}') - 1 ) * 100
    
    displayData = [[font.render((f'Name: {name}'),1,(0,0,0)), (770,570)] ,
                   [font.render((f'Cost: {cost}'),1,(0,0,0)), (770,600)] ,
                   [font.render((f'Yeild Bonus: {yeildBonus}%'),1,(0,0,0)), (770,630)]]


    for i in range(len(displayData)):
        screen.blit(displayData[i][0],displayData[i][1])
        surface.blit(displayData[i][0],displayData[i][1])


def planterEquiptmentSwap(itemID, tableName, uniqueID):
    # check if player has item in inventory
    curQuant = Qi(f'Quantity', 'Inventory', f'itemID = {itemID} AND TableName = "{tableName}"')
    if curQuant > 0:
        # update inventory
        # decrese quantity of new planter type in inventory
        newQuant = (curQuant) - 1
        U('Inventory', f'Quantity = {newQuant}', f'itemID = {itemID} AND TableName = "{tableName}"')
        # increase quantity of old planter type in inventory
        curThingID = Qi(f'{tableName}ID', 'Planter', f'PlanterID = {uniqueID}')
        newQuantCurThingID = (Qi('Quantity', 'Inventory', f'itemID = {curThingID} AND TableName = "{tableName}"')) + 1
        U('Inventory', f'Quantity = {newQuantCurThingID}', f'itemID = {curThingID} AND TableName = "{tableName}"')
        # change planter
        U('Planter',f'{tableName}ID = {itemID}', f'PlanterID = {uniqueID}')
        # exit planter menu
        return 'exit'
    # return error message to player
    else:
        return 'error_message_quantity'


def seedImage(uniqueID):
    imageName = Qs('Name','Crop',f'CropID = {uniqueID}')
    image = f'itemPacketButtons/{imageName}Seeds'
    return image


def productImage(uniqueID):
    imageName = Qs('Name','Crop',f'CropID = {uniqueID}')
    image = f'itemPacketButtons/{imageName}Product'
    return image

def lQ(what, fromWhere, where):
    res = (cur.execute(f'SELECT {what} FROM {fromWhere} WHERE {where}')).fetchall()
    for i in range(len(res)):
        res[i] = int(str(res[i]).replace("(","").replace(",)",""))
    return res

def rQ(what, fromWhere, where):
    return (cur.execute(f'SELECT {what} FROM {fromWhere} WHERE {where}')).fetchall()

def Qs(what, fromWhere, where):
    return (((str((cur.execute(f'SELECT {what} FROM {fromWhere} WHERE {where}')).fetchall())).replace("[('","")).replace("',)]",""))

def Qi(what, fromWhere, where):
    return int((((str((cur.execute(f'SELECT {what} FROM {fromWhere} WHERE {where}')).fetchall())).replace("[(","")).replace(",)]","")))

def Qf(what, fromWhere, where):
    return float((((str((cur.execute(f'SELECT {what} FROM {fromWhere} WHERE {where}')).fetchall())).replace("[(","")).replace(",)]","")))

def U(table, st, where):
    cur.execute(f'UPDATE {table} SET {st} WHERE {where}')
    con.commit()

def I(table, data):
    cur.execute(f'INSERT INTO {table} VALUES({data[0]},{data[1]},{data[2]},{data[3]})')
    con.commit()

def D(table, where):
    cur.execute(f'DELETE FROM {table} WHERE {where}')
    con.commit()

def Tt(table):
    cur.execute(f'DELETE FROM   {table}')
    con.commit()


def plantNewPlant(screen, surface, cropID, buttonPressed, plants, plantPos, plantPotID, newPlantID):
    # display quantity of chosen seed
    quantitySeed = Qi('Quantity', 'Inventory', f'ItemID = {cropID} AND Type = "Seed"')
    if quantitySeed >= 1:
        newQUant = quantitySeed - 1
        U('Inventory', f'Quantity = {newQUant}', f'ItemID = {cropID} AND Type = "Seed"')
        name = Qs('Name', 'Crop', f'CropID = {cropID}')
        hydroComp = True if Qi('HydroComp', 'Crop', f'CropID = {cropID}') == 1 else False
        if Qs('GrowthMedia.Name', 'GrowthMedia, PlantPot, Planter', f'Planter.PlanterID = PlantPot.PlanterID AND Planter.GrowthMediaID = GrowthMedia.GrowthMediaID AND PlantPot.PlantPotID = {plantPotID}') == 'Hydroponic' and hydroComp == False:
            return 'error_message_incompatible'
        else:
            I('Plant', [newPlantID, plantPotID, cropID, newPlantID])
            return 'planter'
    else:
        return 'error_message_quantity'


def text(screen, surface, data): # text, pos, fontSize, color, font
    text = str(data[0])
    pos = data[1]
    fontSize = 18
    color = (0,0,0)
    font = 'Consolas'

    lD = len(data)
    if lD >= 3:
        fontSize = data[2]
        if lD >= 4:
            color = data[3]
            if lD == 5:
                font = data[4]

    font = pg.font.SysFont(font, fontSize)
    screen.blit((font.render(text, 1, color)), pos)
    surface.blit((font.render(text, 1, color)), pos)


def fps(screen, surface, clock):
    fps = clock.get_fps()
    text(screen, surface, (f'FPS : {fps}', (10,10), 18, (0,255,0)))


def setCurTick(newCurTick):
    curTickFile = open('GameData/currentTick.txt','w')
    curTickFile.write(str(newCurTick-1))
    curTickFile.close()


def getCurTick():
    curTickFile = open('GameData/currentTick.txt','r')
    curTick = int((curTickFile).read())
    curTickFile.close()
    return curTick


def plantEndTick(plantID):
    return int((Qi('Crop.GrowTime', 'Crop, Plant', f'Plant.CropID = Crop.CropID AND Plant.PlantID = {plantID}') / Qf('Light.SpeedBonus', 'Light, Planter, PlantPot, Plant', f'Plant.PlantPotID = PlantPot.PlantPotID AND PlantPot.PlanterID = Planter.PlanterID AND Planter.LightID = Light.LightID AND Plant.PlantID = {plantID}') ) + Qi('GrowthStartTick', 'Plant', f'PlantID = {plantID}'))

def t(num):
    print(f'test: {num}')
















    


    
    


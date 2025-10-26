import pygame as pg
from Levels import *

def alfonzesGarageFrame():
    result = alfonzesGarage()
    if result == None:
        return
    if result == 'exit':
        villageFrame()
    if result == 'tempMenu':
        tempMenuFrame(['alfonzesGarage'])
        
def davesShopFrame():
    result = davesShop()
    if result == None:
        return
    if result == 'exit':
        villageFrame()
    if result == 'tempMenu':
        tempMenuFrame(['davesShop'])

def churchFrame():
    result = church()
    if result == None:
        return
    if result == 'exit':
        villageFrame()
    if result == 'tempMenu':
        tempMenuFrame(['church'])
    
def planterFrame(source, uniqueID):
    result = planterMenu(uniqueID)
    if result == None:
        return
    if result == 'exit':
        if source == 'bobsHouse':
            bobsHouseFrame()
        if source == 'alfredsHouse':
            alfredsHouseFrame()
    if result == 'tempMenu':
        tempMenuFrame(['planter', source, uniqueID])

def tempMenuFrame(source):
    result = tempMenu()
    if result == None:
        return
    if result == 'resume':
        if source[0] == 'davesShop':
            davesShopFrame()
        if source[0] == 'church':
            churchFrame()
        if source[0] == 'bobsHouse':
            bobsHouseFrame()
        if source[0] == 'alfredsHouse':
            alfredsHouseFrame()
        if source[0] == 'village':
            villageFrame()
        if source[0] == 'planter':
            planterFrame(source[1], source[2])
        if source[0] == 'alfonzesGarage':
            alfonzesGarageFrame()
        if source[0] == 'finnishMenu':
            finnishMenuFrame()
    if result == 'quit':
        return
    if result == 'mainMenu':
        mainMenuFrame()

def inventoryFrame(source):
    result = inventory()
    if result == None:
        return
    if result == 'exit':
        if source[0] == 'bobsHouse':
            bobsHouseFrame()
        if source[0] == 'alfredsHouse':
            alfredsHouseFrame()
        if source[0] == 'village':
            villageFrame()
    if result == 'quit':
        return
    if result == 'mainMenu':
        mainMenuFrame()

def mainMenuFrame():
    result = mainMenu()
    if result == None:
        return
    if result == 'load':
        bobsHouseFrame()
    if result == 'new':
        newGameMenuFrame()
    if result == 'quit':
        return

def newGameMenuFrame():
    result = newGameMenu()
    if result == None:
        return
    if result == 'play game':
        bobsHouseFrame()

def finnishMenuFrame():
    result = finnishMenu()
    if result == None:
        return
    if result == 'tempMenu':
        tempMenuFrame(['finishMenu'])
    if result == 'alfredsHouse':
        alfredsHouseFrame()
    
def villageFrame():
    result = village()
    if result == None:
        return
    if result == 'bobsHouse':
        bobsHouseFrame()
    if result == 'alfredsHouse':
        alfredsHouseFrame()
    if result == 'davesShop':
        davesShopFrame()
    if result == 'church':
        churchFrame()
    if result == 'alfonzesGarage':
        alfonzesGarageFrame()
    if result == 'tempMenu':
        tempMenuFrame(['village'])
    if result == 'inventory':
        inventoryFrame(['village'])
        
def bustedFrame():
    result = busted()
    if result == None:
        return
    if result == 'ok':
        bobsHouseFrame()
    
def bobsHouseFrame():
    result = bobsHouse()
    if result == None:
        return
    if result[0] == 'village':
        villageFrame()
    if result[0] == 'planter':
        planterFrame('bobsHouse', result[1])
    if result[0] == 'tempMenu':
        tempMenuFrame(['bobsHouse'])
    if result[0] == 'inventory':
        inventoryFrame(['bobsHouse'])
    if result == 'busted':
        bustedFrame()

def alfredsHouseFrame():
    result = alfredsHouse()
    if result == None:
        return
    if result == 'village':
        villageFrame()
    if result == 'planter':
        planterFrame('alfredsHouse', [])
    if result == 'tempMenu':
        tempMenuFrame(['alfredsHouse'])
    if result == 'grandma':
        finnishMenuFrame()

def main():
    mainMenuFrame()


# initiator
if True:
    pg.init()
    main()
    pg.quit()

import pygame as pg
from pygame.math import Vector2
from Classes import *
from Subroutines import *
from GameData.ColisionMaps import *



# game setup
screen = pg.display.set_mode((1440,810)) #(960,540) (720, 405)
surface = pg.Surface((1440,810), pg.SRCALPHA)
pg.display.set_caption('CABBAGE GAME ALPHA')
clock = pg.time.Clock()
setPrevLocation(Vector2(-45,-350), 'VillageLL')
setPrevLocation(Vector2(-270,-685), 'BobsHouseLL')
setPrevLocation(Vector2(-270,-685), 'AlfredsHouseLL')
RPC = Queue(20) # Recently Purchased Crops
RPC.load()




# levels
def alfonzesGarage():

    # initiate values
    veiwing = 'packets'
    purchaseBoxOrigImage = pg.image.load('Images/Objects/blank.png')
    playerMonies = getMoney()
    print(playerMonies)
    
    # initiate sprites
    alfonzesGarageMenu = Menu("alfonzesGarageMenu")
    exitButton = Button("MenuButtons/Exit", (1340, 0), 'Exit')
    Dplanter = Button("itemPacketButtons/DirtPlanterPacket", (880, 300), 'Purchase Planter')
    SDplanter = Button("itemPacketButtons/SuperDirtPlanterPacket", (1050, 300), 'Purchase Planter')
    Hplanter = Button("itemPacketButtons/HydroponicPlanterPacket", (1220, 300), 'Purchase Planter')
    YhalBulb = Button("itemPacketButtons/YellowHalogenBulbPacket", (710, 300), 'Purchase Lights')
    YLEDBulb = Button("itemPacketButtons/YellowLEDBulbPacket", (540, 300), 'Purchase Lights')
    BLEDBulb = Button("itemPacketButtons/BlueLEDBulbPacket", (370, 300), 'Purchase Lights')
    confirmPurchaseBox = Object('ConfirmPurchaseBox',(750, 530))
    purchaseBoxContents = Object('blank',(1067,612))
    yesButton = Button("MenuButtons/Yes", (775, 653), 'Yes')
    noButton = Button("MenuButtons/No", (910, 653), 'No')
    errorMessageLowMoney = Object('ErrorMesageLowMoney', (420,50))
    okButton = Button("MenuButtons/OKsmall", (680, 290), 'Ok')

    # get time from curTick file
    clock1 = Clock12Hr()
    clock1.setTick(getCurTick())

    # main loop
    while True:
        clock.tick(30)

        # event handling
        mouseDown = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                setCurTick(clock1.retTick())
                return
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouseDown = True

        # screen setup
        screen.fill((199,140,93))

        # sprite updating
        alfonzesGarageMenu.draw(screen, surface)
        exitButton.update(screen, surface, mouseDown)
        Dplanter.update(screen, surface, mouseDown)
        SDplanter.update(screen, surface, mouseDown)
        Hplanter.update(screen, surface, mouseDown)
        YhalBulb.update(screen, surface, mouseDown)
        YLEDBulb.update(screen, surface, mouseDown)
        BLEDBulb.update(screen, surface, mouseDown)
        clock1.update(screen, surface)

        # button handling
        keys = pg.key.get_pressed() 
        if keys[pg.K_ESCAPE]:
            setCurTick(clock1.retTick())
            return 'exit'
        if keys[pg.K_c]:
            fps(screen, surface, clock)
        if exitButton.pressed:
            setCurTick(clock1.retTick())
            return 'exit'
        # this if statement displays the buttons if 'veiwing' is on the 'packet' stage
        if veiwing == 'packets':
            # choice is for the purchase box later
            choice = 'none'
            # if button is hovered over
            if Dplanter.active:
                # display data about the item
                displayPlanterData(screen, surface, 3)
                # if button is pressed
                if Dplanter.pressed:
                    if Qi('Price','GrowthMedia',f'GrowthMediaID = 3') > playerMonies:
                        veiwing = 'error_message_low_money'
                    else:
                        # save data for the purchase box
                        purchaseBoxContents.image = Dplanter.image_active
                        choice = 'Dirt', 'GrowthMedia'
                        # activate purchase box menu
                        veiwing = 'purchase box'
                    
            # same for all buttons
            elif SDplanter.active:
                displayPlanterData(screen, surface, 2)
                if SDplanter.pressed:
                    if Qi('Price','GrowthMedia',f'GrowthMediaID = 2') > playerMonies:
                        veiwing = 'error_message_low_money'
                    else:
                        purchaseBoxContents.image = SDplanter.image_active
                        choice = 'SuperDirt', 'GrowthMedia'   
                        veiwing = 'purchase box'

            elif Hplanter.active:
                displayPlanterData(screen, surface, 1)
                if Hplanter.pressed:
                    if Qi('Price','GrowthMedia',f'GrowthMediaID = 1') > playerMonies:
                        veiwing = 'error_message_low_money'
                    else:
                        purchaseBoxContents.image = Hplanter.image_active
                        choice = 'Hydroponic', 'GrowthMedia' 
                        veiwing = 'purchase box'

            elif YhalBulb.active:
                displayLightData(screen, surface, 3)
                if YhalBulb.pressed:
                    if Qi('Price','Light',f'LightID = 3') > playerMonies:
                        veiwing = 'error_message_low_money'
                    else:
                        purchaseBoxContents.image = YhalBulb.image_active
                        choice = 'YellowHalogenBulb', 'Light' 
                        veiwing = 'purchase box'
                        
            elif YLEDBulb.active:
                displayLightData(screen, surface, 2)
                if YLEDBulb.pressed:
                    if Qi('Price','Light',f'LightID = 2') > playerMonies:
                        veiwing = 'error_message_low_money'
                    else:
                        purchaseBoxContents.image = YLEDBulb.image_active
                        choice = 'YellowLEDBulb', 'Light'
                        veiwing = 'purchase box'

            elif BLEDBulb.active:
                displayLightData(screen, surface, 1)
                if BLEDBulb.pressed:
                    if Qi('Price','Light',f'LightID = 1') > playerMonies:
                        veiwing = 'error_message_low_money'
                    else:
                        purchaseBoxContents.image = BLEDBulb.image_active
                        choice = 'BlueLEDBulb', 'Light'
                        veiwing = 'purchase box'
            else:
                # display null data
                font = pg.font.SysFont("Consolas", 24)
                displayData = [[(font.render((f'Name: '),1,(0,0,0))),(770,570)],
                               [(font.render((f'Cost: '),1,(0,0,0))),(770,600)],
                               [(font.render((f'..... Bonus: '),1,(0,0,0))),(770,630)]]
                for i in range(len(displayData)):
                    screen.blit(displayData[i][0],displayData[i][1])
                    surface.blit(displayData[i][0],displayData[i][1])
                        
        if veiwing == 'purchase box':
            # draw purchase box and 'yes','no' buttons
            confirmPurchaseBox.draw(screen, surface)
            purchaseBoxContents.draw(screen, surface)
            yesButton.update(screen, surface, mouseDown)
            noButton.update(screen, surface, mouseDown)

            if yesButton.pressed:
                # find itemID
                itemID = Qi(f'{choice[1]}ID', f'{choice[1]}', f'Name = "{choice[0]}"')
                # update inventory
                newQuant = (Qi(f'Quantity', f'Inventory', f'itemID = {itemID} AND TableName = "{choice[1]}"')) + 1
                U('Inventory', f'Quantity = {newQuant}', f'itemID = {itemID} AND TableName = "{choice[1]}"')
                # update money
                amount = Qi('Price', 'Light', f'LightID = {itemID}')
                subMoney(amount)
                purchaseBoxContents.image = purchaseBoxOrigImage
                veiwing = 'packets'
                yesButton.pressed = False

            if noButton.pressed:
                purchaseBoxContents.image = purchaseBoxOrigImage
                veiwing = 'packets'
                noButton.pressed = False

        if veiwing == 'error_message_low_money':
            errorMessageLowMoney.draw(screen, surface)
            okButton.update(screen, surface, mouseDown)

            if okButton.pressed:
                veiwing = 'packets'
                okButton.pressed = False
                
        # screen update
        pg.display.flip()


def davesShop():

    # initiate values
    veiwing = 'packets'
    pos = (0,0)
    disapearRect = (0, 244, 402, 208)
    hoverValue = 'Purchase Seeds'
    purchaseBoxOrigImage = pg.image.load('Images/Objects/blank.png')

    # initiate sprites
    davesShopScreen = Menu(f"davesShopMenu")
    exitButton = Button("MenuButtons/Exit", (1340, 0), 'Exit')
    cabbageSeeds = ScrollingButton(seedImage(1), pos, (700, 275), 'x', [disapearRect], hoverValue)
    cocoaSeeds = ScrollingButton(seedImage(2), pos, (870, 275), 'x', [disapearRect], hoverValue)
    celeriacSeeds = ScrollingButton(seedImage(3), pos, (1040, 275), 'x', [disapearRect], hoverValue)
    carrotSeeds = ScrollingButton(seedImage(4), pos, (1210, 275), 'x', [disapearRect], hoverValue)
    cornSeeds = ScrollingButton(seedImage(5), pos, (1380, 275), 'x', [disapearRect], hoverValue)
    potatoSeeds = ScrollingButton(seedImage(6), pos, (1550, 275), 'x', [disapearRect], hoverValue)
    pumpkinSeeds = ScrollingButton(seedImage(7), pos, (1720, 275), 'x', [disapearRect], hoverValue)
    tomatoSeeds = ScrollingButton(seedImage(8), pos, (1890, 275), 'x', [disapearRect], hoverValue)
    seedTunnel = Object('SeedTunnel',(0, 244))
    confirmPurchaseBox = Object('ConfirmPurchaseBox',(950, 550))
    purchaseBoxContents = Object('blank',(1267,632))
    yesButton = Button("MenuButtons/Yes", (975, 673), 'Yes')
    noButton = Button("MenuButtons/No", (1110, 673), 'No')
    errorMessageLowMoney = Object('ErrorMesageLowMoney', (420,50))
    okButton = Button("MenuButtons/OKsmall", (680, 290), 'Ok')

    # get time from curTick file
    clock1 = Clock12Hr()
    clock1.setTick(getCurTick())

    # initiate lights
    light1 = Light('YellowLEDBulb', (605,0))
    light2 = Light('YellowLEDBulb', (1161,0))

    # main loop
    while True:
        clock.tick(30)

        # event handling
        mouseDown = False
        mouseScroll = 0
        for event in pg.event.get():
            if event.type == pg.QUIT:
                setCurTick(clock1.retTick())
                return
            if event.type == pg.MOUSEWHEEL:
                mouseScroll += event.y
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouseDown = True

        # screen setup
        screen.fill((20,20,20))
        surface.fill((20,20,20))

        # sprite updating
        davesShopScreen.draw(screen, surface)
        exitButton.update(screen, surface, mouseDown)
        cabbageSeeds.update(screen, surface, mouseDown, mouseScroll)
        cocoaSeeds.update(screen, surface, mouseDown, mouseScroll)
        celeriacSeeds.update(screen, surface, mouseDown, mouseScroll)
        carrotSeeds.update(screen, surface, mouseDown, mouseScroll)
        cornSeeds.update(screen, surface, mouseDown, mouseScroll)
        potatoSeeds.update(screen, surface, mouseDown, mouseScroll)
        pumpkinSeeds.update(screen, surface, mouseDown, mouseScroll)
        tomatoSeeds.update(screen, surface, mouseDown, mouseScroll)
        seedTunnel.draw(screen, surface)
        clock1.update(screen, surface)

        # button handling
        keys = pg.key.get_pressed() 
        if keys[pg.K_ESCAPE]:
            setCurTick(clock1.retTick())
            return 'exit'
        if keys[pg.K_c]:
            fps(screen, surface, clock)
        if exitButton.pressed:
            setCurTick(clock1.retTick())
            return 'exit'
        if veiwing == 'packets':
            # if mouse hovering over button
            if cabbageSeeds.active:
                # display data about that item
                displaySeedData(screen, surface, 1)
                # if mouse pressed on button
                if cabbageSeeds.pressed:
                    playerMonies = getMoney()
                    if Qi('Price','Crop',f'CropID = 1') > playerMonies:
                        veiwing = 'error_message_low_money'
                    else:
                        # open purchase menu
                        purchaseBoxContents.image = cabbageSeeds.image_active
                        veiwing = 'purchase box'
                        choice = 'Cabbage', 'Crop'
            # same for all buttons
            elif cocoaSeeds.active:
                displaySeedData(screen, surface, 2)
                if cocoaSeeds.pressed:
                    playerMonies = getMoney()
                    if Qi('Price','Crop',f'CropID = 2') > playerMonies:
                        veiwing = 'error_message_low_money'
                    else:
                        purchaseBoxContents.image = cocoaSeeds.image_active
                        veiwing = 'purchase box'
                        choice = 'Cocoa', 'Crop'
            elif celeriacSeeds.active:
                displaySeedData(screen, surface, 3)
                if celeriacSeeds.pressed:
                    playerMonies = getMoney()
                    if Qi('Price','Crop',f'CropID = 3') > playerMonies:
                        veiwing = 'error_message_low_money'
                    else:
                        purchaseBoxContents.image = celeriacSeeds.image_active
                        veiwing = 'purchase box'
                        choice = 'Celeriac', 'Crop'
            elif carrotSeeds.active:
                displaySeedData(screen, surface, 4)
                if carrotSeeds.pressed:
                    playerMonies = getMoney()
                    if Qi('Price','Crop',f'CropID = 4') > playerMonies:
                        veiwing = 'error_message_low_money'
                    else:
                        purchaseBoxContents.image = carrotSeeds.image_active
                        veiwing = 'purchase box'
                        choice = 'Carrot', 'Crop'
            elif cornSeeds.active:
                displaySeedData(screen, surface, 5)
                if cornSeeds.pressed:
                    playerMonies = getMoney()
                    if Qi('Price','Crop',f'CropID = 5') > playerMonies:
                        veiwing = 'error_message_low_money'
                    else:
                        purchaseBoxContents.image = cornSeeds.image_active
                        veiwing = 'purchase box'
                        choice = 'Corn', 'Crop'
            elif potatoSeeds.active:
                displaySeedData(screen, surface, 6)
                if potatoSeeds.pressed:
                    playerMonies = getMoney()
                    if Qi('Price','Crop',f'CropID = 6') > playerMonies:
                        veiwing = 'error_message_low_money'
                    else:
                        purchaseBoxContents.image = potatoSeeds.image_active
                        veiwing = 'purchase box'
                        choice = 'Potato', 'Crop'
            elif pumpkinSeeds.active:
                displaySeedData(screen, surface, 7)
                if pumpkinSeeds.pressed:
                    playerMonies = getMoney()
                    if Qi('Price','Crop',f'CropID = 7') > playerMonies:
                        veiwing = 'error_message_low_money'
                    else:
                        purchaseBoxContents.image = pumpkinSeeds.image_active
                        veiwing = 'purchase box'
                        choice = 'Pumpkin', 'Crop'
            elif tomatoSeeds.active:
                displaySeedData(screen, surface, 8)
                if tomatoSeeds.pressed:
                    playerMonies = getMoney()
                    if Qi('Price','Crop',f'CropID = 8') > playerMonies:
                        veiwing = 'error_message_low_money'
                    else:
                        purchaseBoxContents.image = tomatoSeeds.image_active
                        veiwing = 'purchase box'
                        choice = 'Tomato', 'Crop'
            # this displays the feilds with no data in them
            else:
                displaySeedData(screen, surface, 0)
     
        if veiwing == 'purchase box':
            # draw purchase box and 'yes','no' buttons
            confirmPurchaseBox.draw(screen, surface)
            purchaseBoxContents.draw(screen, surface)
            yesButton.update(screen, surface, mouseDown)
            noButton.update(screen, surface, mouseDown)

            if yesButton.pressed:
                # find itemID
                itemID = Qi(f'{choice[1]}ID', f'{choice[1]}', f'Name = "{choice[0]}"')
                # update inventory
                newQuant = (Qi(f'Quantity', f'Inventory', f'itemID = {itemID} AND TableName = "{choice[1]}" AND Type = "Seed"')) + 1
                U('Inventory', f'Quantity = {newQuant}', f'itemID = {itemID} AND TableName = "{choice[1]}" AND Type = "Seed"')
                # update money
                amount = Qi('Price', 'Crop', f'CropID = {itemID}')
                subMoney(amount)
                purchaseBoxContents.image = purchaseBoxOrigImage
                veiwing = 'packets'
                yesButton.pressed = False

            if noButton.pressed:
                purchaseBoxContents.image = purchaseBoxOrigImage
                veiwing = 'packets'
                noButton.pressed = False

        # light updating
        light1.draw(screen, surface)
        light2.draw(screen, surface)

        if veiwing == 'error_message_low_money':
            errorMessageLowMoney.draw(screen, surface)
            okButton.update(screen, surface, mouseDown)

            if okButton.pressed:
                veiwing = 'packets'
                okButton.pressed = False
                
        # screen update
        screen.blit(surface, (0,0))
        pg.display.flip()


def church():

    # initiate values
    veiwing = 'products'
    pos = (0,0)
    disapearRect = (1200, 250, 1002, 208)
    hoverValue = 'Sell Produce'
    sellingBoxOrigImage = pg.image.load('Images/Objects/blank.png')

    # initiate sprites
    churchScreen = Menu(f"robertsChurchMenu")
    exitButton = Button("MenuButtons/Exit", (1340, 0), 'Exit')
    cabbageProduct = ScrollingButton(productImage(1), pos, (100, 275), 'x', [disapearRect], hoverValue)
    cocoaProduct = ScrollingButton(productImage(2), pos, (270, 275), 'x', [disapearRect], hoverValue)
    celeriacProduct = ScrollingButton(productImage(3), pos, (440, 275), 'x', [disapearRect], hoverValue)
    carrotProduct = ScrollingButton(productImage(4), pos, (610, 275), 'x', [disapearRect], hoverValue)
    cornProduct = ScrollingButton(productImage(5), pos, (780, 275), 'x', [disapearRect], hoverValue)
    potatoProduct = ScrollingButton(productImage(6), pos, (950, 275), 'x', [disapearRect], hoverValue)
    pumpkinProduct = ScrollingButton(productImage(7), pos, (1120, 275), 'x', [disapearRect], hoverValue)
    tomatoProduct = ScrollingButton(productImage(8), pos, (1290, 275), 'x', [disapearRect], hoverValue)
    sellingBox = Object('sellingBox',(50, 550))
    sellingBoxContents = Object('blank',(367,632))
    sellAll = Button("MenuButtons/SellAll", (75, 673), 'Sell All')
    sellOne = Button("MenuButtons/SellOne", (210, 673), 'Sell One')
    errorMesageQuantity = Object('ErrorMesageQuantity', (420,50))
    okButton = Button("MenuButtons/OKsmall", (680, 290), 'Ok')
    miniExitButton = Button('PlanterButtons/TinyExitButton', (541, 550), 'Exit Interface')

    # get time from curTick file
    clock1 = Clock12Hr()
    clock1.setTick(getCurTick())

    # main loop
    while True:
        clock.tick(30)

        # event handling
        mouseDown = False
        mouseScroll = 0
        for event in pg.event.get():
            if event.type == pg.QUIT:
                RPC.save()
                setCurTick(clock1.retTick())
                return
            if event.type == pg.MOUSEWHEEL:
                mouseScroll += event.y
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouseDown = True


        # screen setup
        screen.fill((20,20,20))
        surface.fill((20,20,20))

        # sprite updating
        churchScreen.draw(screen, surface)
        exitButton.update(screen, surface, mouseDown)
        cabbageProduct.update(screen, surface, mouseDown, mouseScroll)
        cocoaProduct.update(screen, surface, mouseDown, mouseScroll)
        celeriacProduct.update(screen, surface, mouseDown, mouseScroll)
        carrotProduct.update(screen, surface, mouseDown, mouseScroll)
        cornProduct.update(screen, surface, mouseDown, mouseScroll)
        potatoProduct.update(screen, surface, mouseDown, mouseScroll)
        pumpkinProduct.update(screen, surface, mouseDown, mouseScroll)
        tomatoProduct.update(screen, surface, mouseDown, mouseScroll)
        clock1.update(screen, surface)

        # button handling
        keys = pg.key.get_pressed() 
        if keys[pg.K_ESCAPE]:
            setCurTick(clock1.retTick())
            RPC.save()
            return 'exit'
        if keys[pg.K_c]:
            fps(screen, surface, clock)
        if exitButton.pressed:
            setCurTick(clock1.retTick())
            RPC.save()
            return 'exit'
        if veiwing == 'products':
            # if mouse hovering over button
            if cabbageProduct.active:
                # display data about that item
                displayProductData(screen, surface, 1)
                # if mouse pressed on button
                if cabbageProduct.pressed:
                    if Qi('Quantity', 'Inventory', 'ItemID = 1 AND Type = "Product"') < 1:
                        veiwing = 'error_message_quantity'
                    else:
                        # change image for selling box display
                        sellingBoxContents.image = cabbageProduct.image_inactive
                        # change menu to the selling box menu
                        veiwing = 'selling_box'
                        # save data for later use by selling box
                        choice = 'Cabbage', 'Crop'
            # same for all buttons
            elif cocoaProduct.active:
                displayProductData(screen, surface, 2)
                if cocoaProduct.pressed:
                    if Qi('Quantity', 'Inventory', 'ItemID = 2 AND Type = "Product"') < 1:
                        veiwing = 'error_message_quantity'
                    else:
                        sellingBoxContents.image = cocoaProduct.image_inactive
                        RPC.enqueue('Cocoa')
                        veiwing = 'selling_box'
                        choice = 'Cocoa', 'Crop'
            elif celeriacProduct.active:
                displayProductData(screen, surface, 3)
                if celeriacProduct.pressed:
                    if Qi('Quantity', 'Inventory', 'ItemID = 3 AND Type = "Product"') < 1:
                        veiwing = 'error_message_quantity'
                    else:
                        sellingBoxContents.image = celeriacProduct.image_inactive
                        RPC.enqueue('Celeriac')
                        veiwing = 'selling_box'
                        choice = 'Celeriac', 'Crop'
            elif carrotProduct.active:
                displayProductData(screen, surface, 4)
                if carrotProduct.pressed:
                    if Qi('Quantity', 'Inventory', 'ItemID = 4 AND Type = "Product"') < 1:
                        veiwing = 'error_message_quantity'
                    else:
                        sellingBoxContents.image = carrotProduct.image_inactive
                        veiwing = 'selling_box'
                        choice = 'Carrot', 'Crop'
            elif cornProduct.active:
                displayProductData(screen, surface, 5)
                if cornProduct.pressed:
                    if Qi('Quantity', 'Inventory', 'ItemID = 5 AND Type = "Product"') < 1:
                        veiwing = 'error_message_quantity'
                    else:
                        sellingBoxContents.image = cornProduct.image_inactive
                        veiwing = 'selling_box'
                        choice = 'Corn', 'Crop'
            elif potatoProduct.active:
                displayProductData(screen, surface, 6)
                if potatoProduct.pressed:
                    if Qi('Quantity', 'Inventory', 'ItemID = 6 AND Type = "Product"') < 1:
                        veiwing = 'error_message_quantity'
                    else:
                        sellingBoxContents.image = potatoProduct.image_inactive
                        veiwing = 'selling_box'
                        choice = 'Potato', 'Crop'
            elif pumpkinProduct.active:
                displayProductData(screen, surface, 7)
                if pumpkinProduct.pressed:
                    if Qi('Quantity', 'Inventory', 'ItemID = 7 AND Type = "Product"') < 1:
                        veiwing = 'error_message_quantity'
                    else:
                        sellingBoxContents.image = pumpkinProduct.image_inactive
                        veiwing = 'selling_box'
                        choice = 'Pumpkin', 'Crop'
            elif tomatoProduct.active:
                displayProductData(screen, surface, 8)
                if tomatoProduct.pressed:
                    if Qi('Quantity', 'Inventory', 'ItemID = 8 AND Type = "Product"') < 1:
                        veiwing = 'error_message_quantity'
                    else:
                        sellingBoxContents.image = tomatoProduct.image_inactive
                        veiwing = 'selling_box'
                        choice = 'Tomato', 'Crop'
            # this displays the feilds with no data in them
            else:
                displayProductData(screen, surface, 0)
     
        if veiwing == 'selling_box':
            # draw purchase box and 'yes','no' buttons
            sellingBox.draw(screen, surface)
            sellingBoxContents.draw(screen, surface)
            sellAll.update(screen, surface, mouseDown)
            sellOne.update(screen, surface, mouseDown)
            miniExitButton.update(screen, surface, mouseDown)

            if sellOne.pressed:
                # find itemID
                itemID = Qi(f'{choice[1]}ID', f'{choice[1]}', f'Name = "{choice[0]}"')
                # update inventory
                newQuant = (Qi(f'Quantity', f'Inventory', f'itemID = {itemID} AND TableName = "{choice[1]}" AND Type = "Product"')) - 1
                U('Inventory', f'Quantity = {newQuant}', f'itemID = {itemID} AND TableName = "{choice[1]}" AND Type = "Product"')
                # update money
                amount = Qi('SellingPrice', 'Crop', f'CropID = {itemID}')
                addMoney(amount)
                # add item to 'recently purchased crops'(RPC) circular queue
                RPC.enqueue(choice[0])
                RPC.showQueue()
                sellingBoxContents.image = sellingBoxOrigImage
                veiwing = 'products'
                sellOne.pressed = False

            if sellAll.pressed:
                # find itemID
                itemID = Qi(f'{choice[1]}ID', f'{choice[1]}', f'Name = "{choice[0]}"')
                # update inventory
                quantity = Qi('Quantity', 'Inventory', f'itemID = {itemID} AND Type = "Product"')
                U('Inventory', f'Quantity = 0', f'itemID = {itemID} AND Type = "Product"')
                # update money
                addMoney(Qi('Price', 'Crop', f'CropID = {itemID}') * quantity)
                # add item to 'recently purchased crops'(RPC) circular queue
                for i in range(quantity):
                    RPC.enqueue(choice[0])
                RPC.showQueue()
                sellingBoxContents.image = sellingBoxOrigImage
                veiwing = 'products'
                sellAll.pressed = False

            if miniExitButton.pressed:
                sellingBoxContents.image = sellingBoxOrigImage
                veiwing = 'products'
                miniExitButton.pressed = False

        if veiwing == 'error_message_quantity':
            errorMesageQuantity.draw(screen, surface)
            okButton.update(screen, surface, mouseDown)

            if okButton.pressed:
                veiwing = 'products'
                okButton.pressed = False
        
        # screen update
        screen.blit(surface, (0,0))
        pg.display.flip()

    
    
def planterMenu(uniqueID):

    # initiate imediet sprites
    pPloc = [(145, 384),(561, 389),(968, 394)]
    pos = (0,0)
    veiwing = 'planter'
    planterType = Qs('Name', 'Planter, GrowthMedia', f'Planter.GrowthMediaID = GrowthMedia.GrowthMediaID AND PlanterID = {uniqueID}')
    lightType = Qs('Name', 'Planter, Light', f'Planter.LightID = Light.LightID AND PlanterID = {uniqueID}')
    planterScreen = Menu(f"planterTable{planterType}")
    plantPot1 = Button(f'PlanterButtons/{planterType}PlantPot1', pPloc[0], 'Veiw Options')
    plantPot2 = Button(f'PlanterButtons/{planterType}PlantPot2', pPloc[1], 'Veiw Options')
    plantPot3 = Button(f'PlanterButtons/{planterType}PlantPot3', pPloc[2], 'Veiw Options')
    tableTop = Button(f'PlanterButtons/{planterType}TableTop',(21, 493), 'Change Planter Type')
    changeLight = Button('PlanterButtons/ChangeLightBulb',(10, 10), 'Change Light Type')
    exitButton = Button("MenuButtons/Exit", (1340, 0), 'Exit')
    vMenu = Object('VersitileMenu', (100,100))
    # initiate menu sprites
    errorMesageQuantity = Object('ErrorMesageQuantity', (420,50))
    okButton = Button("MenuButtons/OKsmall", (680, 290), 'Ok')
    Dplanter = Button("itemPacketButtons/DirtPlanterPacket", (130, 200), 'Equip Planter')
    SDplanter = Button("itemPacketButtons/SuperDirtPlanterPacket", (300, 200), 'Equip Planter')
    Hplanter = Button("itemPacketButtons/HydroponicPlanterPacket", (470, 200), 'Equip Planter')
    YhalBulb = Button("itemPacketButtons/YellowHalogenBulbPacket", (130, 200), 'Equip Lights')
    YLEDBulb = Button("itemPacketButtons/YellowLEDBulbPacket", (300, 200), 'Equip Lights')
    BLEDBulb = Button("itemPacketButtons/BlueLEDBulbPacket", (470, 200), 'Equip Lights')
    newPlantButton = Button('PlanterButtons/NewPlant', (pPloc[0][0]-10, pPloc[0][1]+100), 'Plant A New Plant')
    removePlantButton = Button('PlanterButtons/RemovePlant', (pPloc[0][0]-10, pPloc[0][1]+145), 'Remove Plant')
    harvestPlantButton = Button('PlanterButtons/HarvestPlant', (pPloc[0][0]-10, pPloc[0][1]+190), 'Harvest Plant')
    miniExitButton = Button('PlanterButtons/TinyExitButton', (pPloc[0][0]+200, pPloc[0][1]+200), 'Exit Interface')
    plantOptionsMenu = Object('PlantPotOptionsMenu', (pPloc[0][0], pPloc[0][1]+90))
    errorMesageOcupied = Object('ErrorMesageOcupied', (420,50))
    errorMesageNotOcupied = Object('ErrorMesageNotOcupied', (420,50))
    errorMesagePlanterFull = Object('ErrorMesagePlanterFull', (420,50))
    errorMesageIncompatible = Object('errorMesageIncompatible', (420,50))
    hoverValue = 'Use Seeds'
    disapearRect = [(0, 186, 116, 383), (1084, 186, 456, 383)]
    cabbageSeeds = ScrollingButton(seedImage(1), pos, (300, 200), 'x', disapearRect, hoverValue)
    cocoaSeeds = ScrollingButton(seedImage(2), pos, (470, 200), 'x', disapearRect, hoverValue)
    celeriacSeeds = ScrollingButton(seedImage(3), pos, (640, 200), 'x', disapearRect, hoverValue)
    carrotSeeds = ScrollingButton(seedImage(4), pos, (810, 200), 'x', disapearRect, hoverValue)
    cornSeeds = ScrollingButton(seedImage(5), pos, (980, 200), 'x', disapearRect, hoverValue)
    potatoSeeds = ScrollingButton(seedImage(6), pos, (1150, 200), 'x', disapearRect, hoverValue)
    pumpkinSeeds = ScrollingButton(seedImage(7), pos, (1320, 200), 'x', disapearRect, hoverValue)
    tomatoSeeds = ScrollingButton(seedImage(8), pos, (1490, 200), 'x', disapearRect, hoverValue)
    VTMarrowLeft = Object('ArrowForVTM_Left', (920,186))
    VTMarrowRight = Object('ArrowForVTM_Right', (116,186))
    
    
    # setup plants (102, 329) : hydro 1(265, 429) 2(704, 429) 3(1106, 429)
    plantPotIDlist = lQ('PlantPotID','PlantPot',f'PlanterID = {uniqueID}')
    plants = pg.sprite.Group()

    if str(rQ('Plant.PlantID','Plant, PlantPot, Planter',f'Plant.PlantPotID = PlantPot.PlantPotID AND PlantPot.PlanterID = Planter.PlanterID AND PlantPot.PlantPotID = {plantPotIDlist[0]} AND Planter.PlanterID = {uniqueID}')) != '[]':
        plant1 = Plant(Qi('Plant.PlantID','Plant, PlantPot, Planter',f'Plant.PlantPotID = PlantPot.PlantPotID AND PlantPot.PlanterID = Planter.PlanterID AND PlantPot.PlantPotID = {plantPotIDlist[0]} AND Planter.PlanterID = {uniqueID}'), (163,100))
    else:
        plant1 = Plant(-1, (163,100))
    plants.add(plant1)
    if str(rQ('Plant.PlantID','Plant, PlantPot, Planter',f'Plant.PlantPotID = PlantPot.PlantPotID AND PlantPot.PlanterID = Planter.PlanterID AND PlantPot.PlantPotID = {plantPotIDlist[1]} AND Planter.PlanterID = {uniqueID}')) != '[]':
        plant2 = Plant(Qi('Plant.PlantID','Plant, PlantPot, Planter',f'Plant.PlantPotID = PlantPot.PlantPotID AND PlantPot.PlanterID = Planter.PlanterID AND PlantPot.PlantPotID = {plantPotIDlist[1]} AND Planter.PlanterID = {uniqueID}'), (602,100))
    else:
        plant2 = Plant(-1, (602,100))
    plants.add(plant2)
    if str(rQ('Plant.PlantID','Plant, PlantPot, Planter',f'Plant.PlantPotID = PlantPot.PlantPotID AND PlantPot.PlanterID = Planter.PlanterID AND PlantPot.PlantPotID = {plantPotIDlist[2]} AND Planter.PlanterID = {uniqueID}')) != '[]':
        plant3 = Plant(Qi('Plant.PlantID','Plant, PlantPot, Planter',f'Plant.PlantPotID = PlantPot.PlantPotID AND PlantPot.PlanterID = Planter.PlanterID AND PlantPot.PlantPotID = {plantPotIDlist[2]} AND Planter.PlanterID = {uniqueID}'), (1004,98))
    else:
        plant3 = Plant(-1, (1004,98))
    plants.add(plant3)
    
    # setup clock
    clock1 = Clock12Hr()
    clock1.setTick(getCurTick())

    # initiate lights
    light1 = Light(lightType, (120,0))
    light2 = Light(lightType, (605,0))
    light3 = Light(lightType, (1060,0))

    # main loop
    while True:
        clock.tick(30)

        # event handling
        mouseDown = False
        mouseScroll = 0
        for event in pg.event.get():
            if event.type == pg.QUIT:
                setCurTick(clock1.retTick())
                return
            if event.type == pg.MOUSEWHEEL:
                mouseScroll += event.y
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouseDown = True

        # screen setup
        screen.fill((20,20,20))
        surface.fill((20,20,20))

        # sprite updating
        planterScreen.draw(screen, surface)
        exitButton.update(screen, surface, mouseDown)

        if veiwing == 'planter':
            plantPot1.update(screen, surface, mouseDown)
            plantPot2.update(screen, surface, mouseDown)
            plantPot3.update(screen, surface, mouseDown)
            tableTop.update(screen, surface, mouseDown)
            changeLight.update(screen, surface, mouseDown)
        
            if tableTop.pressed: # change planter type
                veiwing = 'change_table_top'
                tableTop.pressed = False
            if changeLight.pressed: # change light type 
                veiwing = 'change_light_type'
                changeLight.pressed = False
            if plantPot1.pressed: # open plant pot interface
                veiwing = 'plant_pot_1'
                plantPot1.pressed = False
            if plantPot2.pressed: 
                veiwing = 'plant_pot_2'
                plantPot2.pressed = False
            if plantPot3.pressed: 
                veiwing = 'plant_pot_3'
                plantPot3.pressed = False

        # plant update
        plants.update(screen, surface, clock1.retTick(), -1)

        # clock update
        clock1.update(screen, surface)
                      
        # light updating
        light1.draw(screen, surface)
        light2.draw(screen, surface)
        light3.draw(screen, surface)

        # button handling
        keys = pg.key.get_pressed() 
        if keys[pg.K_ESCAPE]: # exit planter interface
            setCurTick(clock1.retTick())
            return 'exit'
        if keys[pg.K_c]: # display FPS and current tick on scren
            fps(screen, surface, clock)
            text(screen, surface, [f'Current Tick: {clock1.retTick()}', (10, 30), 18, (0,255,0)])
        if exitButton.pressed: # exit planter interface
            setCurTick(clock1.retTick())
            return 'exit'
        if veiwing == 'exit': # exit planter interface
            setCurTick(clock1.retTick())
            return 'exit'

        if veiwing == 'change_table_top': # change planter type interface
            if str(rQ('Plant.PlantID', 'Plant, PlantPot, Planter', f'Plant.PlantPotID = PlantPot.PlantPotID AND PlantPot.PlanterID = Planter.PlanterID AND Planter.PlanterID = {uniqueID}')) != '[]':
                veiwing = 'error_message_planter_full'
            else:
                vMenu.draw(screen, surface)
                text(screen, surface, ('Change Planter Type', (113,113), 32))
                miniExitButton.pos.x = vMenu.pos.x + 990
                miniExitButton.rect.x = vMenu.pos.x + 990
                miniExitButton.pos.y = vMenu.pos.y
                miniExitButton.rect.y = vMenu.pos.y
                miniExitButton.update(screen, surface, mouseDown)
                Dplanter.update(screen, surface, mouseDown)
                SDplanter.update(screen, surface, mouseDown)
                Hplanter.update(screen, surface, mouseDown)

            if miniExitButton.pressed:
                veiwing = 'planter'
                miniExitButton.pressed = False
                
            if Dplanter.pressed:
                veiwing = planterEquiptmentSwap(3, 'GrowthMedia', uniqueID)
                Dplanter.pressed = False
            if SDplanter.pressed:
                veiwing = planterEquiptmentSwap(2, 'GrowthMedia', uniqueID)
                SDplanter.pressed = False
            if Hplanter.pressed:
                veiwing = planterEquiptmentSwap(1, 'GrowthMedia', uniqueID)
                Hplanter.pressed = False
            
        if veiwing == 'change_light_type': # change light type interface
            if str(rQ('Plant.PlantID', 'Plant, PlantPot, Planter', f'Plant.PlantPotID = PlantPot.PlantPotID AND PlantPot.PlanterID = Planter.PlanterID AND Planter.PlanterID = {uniqueID}')) != '[]':
                veiwing = 'error_message_planter_full'
            else:
                vMenu.draw(screen, surface)
                text(screen, surface, ('Change Light Type', (113,113), 32))
                miniExitButton.pos.x = vMenu.pos.x + 990
                miniExitButton.rect.x = vMenu.pos.x + 990
                miniExitButton.pos.y = vMenu.pos.y
                miniExitButton.rect.y = vMenu.pos.y
                miniExitButton.update(screen, surface, mouseDown)
                YhalBulb.update(screen, surface, mouseDown)
                YLEDBulb.update(screen, surface, mouseDown)
                BLEDBulb.update(screen, surface, mouseDown)
                
            if miniExitButton.pressed:
                veiwing = 'planter'
                miniExitButton.pressed = False
            if YhalBulb.pressed:
                veiwing = planterEquiptmentSwap(3, 'Light', uniqueID)
                YhalBulb.pressed = False
            if YLEDBulb.pressed:
                veiwing = planterEquiptmentSwap(2, 'Light', uniqueID)
                YLEDBulb.pressed = False
            if BLEDBulb.pressed:
                veiwing = planterEquiptmentSwap(1, 'Light', uniqueID)
                BLEDBulb.pressed = False
        
        if veiwing == 'error_message_planter_full':
            errorMesagePlanterFull.draw(screen, surface)
            okButton.update(screen, surface, mouseDown)

            if okButton.pressed:
                veiwing = 'planter'
                okButton.pressed = False
                
        if veiwing == 'error_message_quantity':
            errorMesageQuantity.draw(screen, surface)
            okButton.update(screen, surface, mouseDown)

            if okButton.pressed:
                veiwing = 'planter'
                okButton.pressed = False

        if veiwing == 'error_message_incompatible':
            errorMesageIncompatible.draw(screen, surface)
            okButton.update(screen, surface, mouseDown)

            if okButton.pressed:
                veiwing = 'planter'
                okButton.pressed = False

        if veiwing.startswith('plant_pot'):
            # there are three diffrent plant pots per planter and this stage handles all three of them
            potNum = int(veiwing[-1])
            plantPos = (0,0) # first we find the pos of the plant pot we are working with, for future usage
            harvestReady = False
            potOcup = False 
            if potNum == 1:
                plantPos = (163,100)
            elif potNum == 2:
                plantPos = (602,100)
            else:
                plantPos = (1004,100)

            if str(rQ('PlantID','Plant',f'PlantPotID = {plantPotIDlist[potNum-1]}')) != '[]':
                potOcup = True
                potPltID = Qi('PlantID','Plant',f'PlantPotID = {plantPotIDlist[potNum-1]}')
                harvestReady = True if clock1.retTick() >= plantEndTick(potPltID) else False

            # update the location of the mini menu
            newXpos = plantPos[0] + 10
            plantOptionsMenu.pos.x = newXpos - 10
            
            newPlantButton.pos.x = newXpos
            newPlantButton.rect.x = newXpos
            
            removePlantButton.pos.x = newXpos
            removePlantButton.rect.x = newXpos
            
            harvestPlantButton.pos.x = newXpos
            harvestPlantButton.rect.x = newXpos
            
            miniExitButton.pos.x = newXpos + 180
            miniExitButton.rect.x = newXpos + 180
            miniExitButton.pos.y = plantPos[1] + 374
            miniExitButton.rect.y = plantPos[1] + 374

            # draw and update relevant sprites
            plantOptionsMenu.draw(screen, surface)
            miniExitButton.update(screen, surface, mouseDown)
            newPlantButton.update(screen, surface, mouseDown)
            removePlantButton.update(screen, surface, mouseDown)
            if harvestReady:
                harvestPlantButton.update(screen, surface, mouseDown)

            if miniExitButton.pressed:
                veiwing = 'planter'
                miniExitButton.pressed = False
                
            if newPlantButton.pressed:
                if not potOcup:
                    veiwing = f'new_plant_{potNum}'
                else:
                    veiwing = 'error_message_occupied'
                newPlantButton.pressed = False
                
            if removePlantButton.pressed:
                if not potOcup:
                    veiwing = 'error_message_not_occupied'
                else:
                    plants.update(screen, surface, clock1.retTick(), potPltID)
                    D('Plant', f'PlantID = {potPltID}')
                    veiwing = 'planter'
                removePlantButton.pressed = False
                
            if harvestPlantButton.pressed:
                cropID = Qi('CropID','Plant',f'PlantID = {potPltID}')
                yeildBonus = Qf('GrowthMedia.YeildBonus', 'GrowthMedia, Planter, PlantPot, Plant', f'Plant.PlantPotID = PlantPot.PlantPotID AND PlantPot.PlanterID = Planter.PlanterID AND Planter.GrowthMediaID = GrowthMedia.GrowthMediaID AND Plant.PlantID = {potPltID}')
                newQuantity = Qi('Quantity', 'Inventory', f'ItemID = {cropID} AND Type = "Product"') + (2 * yeildBonus)
                plants.update(screen, surface, clock1.retTick(), potPltID) # remove from 'plants' sprite group
                D('Plant', f'PlantID = {potPltID}') # remove from database
                U('Inventory', f'Quantity = {newQuantity}', f'ItemID = {cropID} AND Type = "Product"')
                veiwing = 'planter'
                harvestPlantButton.pressed = False
                

        if veiwing == 'error_message_occupied':
            errorMesageOcupied.draw(screen, surface)
            okButton.update(screen, surface, mouseDown)

            if okButton.pressed:
                veiwing = 'planter'
                okButton.pressed = False

        if veiwing == 'error_message_not_occupied':
            errorMesageNotOcupied.draw(screen, surface)
            okButton.update(screen, surface, mouseDown)

            if okButton.pressed:
                veiwing = 'planter'
                okButton.pressed = False

        if veiwing.startswith('new_plant'):
            potNum = int(veiwing[-1])
            miniExitButton.pos.x = vMenu.pos.x + 990
            miniExitButton.rect.x = vMenu.pos.x + 990
            miniExitButton.pos.y = vMenu.pos.y
            miniExitButton.rect.y = vMenu.pos.y
            
            vMenu.draw(screen, surface)
            miniExitButton.update(screen, surface, mouseDown)
            cabbageSeeds.update(screen, surface, mouseDown, mouseScroll)
            cocoaSeeds.update(screen, surface, mouseDown, mouseScroll)
            celeriacSeeds.update(screen, surface, mouseDown, mouseScroll)
            carrotSeeds.update(screen, surface, mouseDown, mouseScroll)
            cornSeeds.update(screen, surface, mouseDown, mouseScroll)
            potatoSeeds.update(screen, surface, mouseDown, mouseScroll)
            pumpkinSeeds.update(screen, surface, mouseDown, mouseScroll)
            tomatoSeeds.update(screen, surface, mouseDown, mouseScroll)
            VTMarrowLeft.draw(screen, surface)
            VTMarrowRight.draw(screen, surface)

            newPlantID = clock1.retTick()
            plantPos = (0,0)
            if potNum == 1:
                plantPos = (163,100)
            elif potNum == 2:
                plantPos = (602,100)
            else:
                plantPos = (1004,100)
            

            if miniExitButton.pressed:
                veiwing = 'planter'
                miniExitButton.pressed = False

            if cabbageSeeds.active:
                quantitySeed = Qi('Quantity', 'Inventory', f'ItemID = 1 AND Type = "Seed"')
                text(screen, surface, (f'Cabbage Seeds - You own: {quantitySeed}', (113,113), 32))
                if cabbageSeeds.pressed:
                    veiwing = plantNewPlant(screen, surface, 1, True, plants, plantPos, plantPotIDlist[potNum-1], newPlantID)
                    if veiwing == 'planter':
                        plants.add(Plant(newPlantID, plantPos))
                cabbageSeeds.pressed = False
            elif cocoaSeeds.active:
                if cocoaSeeds.pressed:
                    veiwing = plantNewPlant(screen, surface, 2, True, plants, plantPos, plantPotIDlist[potNum-1], newPlantID)
                    if veiwing == 'planter':
                        plants.add(Plant(newPlantID, plantPos))
                cocoaSeeds.pressed = False
            elif celeriacSeeds.active:
                if celeriacSeeds.pressed:
                    veiwing = plantNewPlant(screen, surface, 3, True, plants, plantPos, plantPotIDlist[potNum-1], newPlantID)
                    if veiwing == 'planter':
                        plants.add(Plant(newPlantID, plantPos))
                celeriacSeeds.pressed = False
            elif carrotSeeds.active:
                if carrotSeeds.pressed:
                    veiwing = plantNewPlant(screen, surface, 4, True, plants, plantPos, plantPotIDlist[potNum-1], newPlantID)
                    if veiwing == 'planter':
                        plants.add(Plant(newPlantID, plantPos))
                carrotSeeds.pressed = False
            elif cornSeeds.active:
                if cornSeeds.pressed:
                    veiwing = plantNewPlant(screen, surface, 5, True, plants, plantPos, plantPotIDlist[potNum-1], newPlantID)
                    if veiwing == 'planter':
                        plants.add(Plant(newPlantID, plantPos))
                cornSeeds.pressed = False
            elif potatoSeeds.active:
                if potatoSeeds.pressed:
                    veiwing = plantNewPlant(screen, surface, 6, True, plants, plantPos, plantPotIDlist[potNum-1], newPlantID)
                    if veiwing == 'planter':
                        plants.add(Plant(newPlantID, plantPos))
                potatoSeeds.pressed = False
            elif pumpkinSeeds.active:
                if pumpkinSeeds.pressed:
                    veiwing = plantNewPlant(screen, surface, 7, True, plants, plantPos, plantPotIDlist[potNum-1], newPlantID)
                    if veiwing == 'planter':
                        plants.add(Plant(newPlantID, plantPos))
                pumpkinSeeds.pressed = False
            elif tomatoSeeds.active:
                if tomatoSeeds.pressed:
                    veiwing = plantNewPlant(screen, surface, 8, True, plants, plantPos, plantPotIDlist[potNum-1], newPlantID)
                    if veiwing == 'planter':
                        plants.add(Plant(newPlantID, plantPos))
                tomatoSeeds.pressed = False
            else:
                text(screen, surface, ('Choose New Plant\'s seed', (113,113), 32))
            
            
        # screen update
        screen.blit(surface, (0,0))
        pg.display.flip()

def inventory():

    # initiate sprites
    inventoryScreen = Menu('InventoryMenu')
    inventoryScreenForeground = Menu('InventoryMenuForeground')
    exitButton = Button("MenuButtons/Exit", (1340, 0), 'Exit')
    ammountMoney = getMoney()
    money = ((f'Money = {ammountMoney}'),(10,10))

    count = -1
    locations = [(250,230),(550,230),(850,230),
                 (250,410),(550,410),(850,410),
                 (250,590),(550,590),(850,590),
                 (250,770),(550,770),(850,770),
                 (250,950),(550,950),(850,950),
                 (250,1130),(550,1130),(850,1130),
                 (250,1310),(550,1310)]
    itemsList = []
    resLight = rQ('Light.Name, Inventory.Quantity, Inventory.TableName','Light, Inventory','Inventory.ItemID = Light.LightID AND Inventory.TableName = "Light" AND Inventory.Quantity >= 1')
    resPlanters = rQ('GrowthMedia.Name, Inventory.Quantity, Inventory.TableName','GrowthMedia, Inventory','Inventory.ItemID = GrowthMedia.GrowthMediaID AND Inventory.TableName = "GrowthMedia" AND Inventory.Quantity >= 1')
    resCrops = rQ('Crop.Name, Inventory.Quantity, Inventory.TableName, Inventory.Type','Crop, Inventory','Inventory.ItemID = Crop.CropID AND Inventory.TableName = "Crop" AND Inventory.Quantity >= 1')
    res = resLight + resPlanters + resCrops
    for result in res:
        count += 1
        if result[2] == 'Light':
            itemsList.append((f'{result[0]}Packet', locations[count], result[1]))
        elif result[2] == 'GrowthMedia':
            itemsList.append((f'{result[0]}PlanterPacket', locations[count], result[1]))
        else:
            if result[3] == 'Seed':
                itemsList.append((f'{result[0]}Seeds', locations[count], result[1]))
            else:
                itemsList.append((f'{result[0]}Product', locations[count], result[1]))
    items = pg.sprite.Group()
    for item in itemsList:
        newItem = InventoryItem(item[0],item[1],item[2])
        items.add(newItem)

    # main loop
    while True:
        clock.tick(30)
        
        # event handling
        mouseDown = False
        mouseScroll = 0
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pg.MOUSEBUTTONDOWN:
                mouseDown = True
            if event.type == pg.MOUSEWHEEL:
                mouseScroll -= event.y

        # screen setup
        screen.fill((20,20,20))

        # sprite updating
        inventoryScreen.draw(screen, surface)
        exitButton.update(screen, surface, mouseDown)
        items.update(screen, surface, mouseScroll)
        inventoryScreenForeground.draw(screen, surface)
        text(screen, surface, money)
        
        # button handling
        keys = pg.key.get_pressed() 
        if exitButton.pressed:
            return 'exit'
        if keys[pg.K_c]:
            fps(screen, surface, clock)

        # screen update
        pg.display.flip()

    
def tempMenu():
    
    # initiate sprites
    resumeButton = Button("MenuButtons/ResumeGame", (100, 300), 'Resume Game')
    mainMenuButton = Button("MenuButtons/MainMenu", (600, 300), 'Back to Main Menu')
    quitButton = Button("MenuButtons/QuitGame", (520, 520), 'Quit Game')
    tempMenuScreen = Menu("tempMenu")

    # main loop
    while True:
        clock.tick(30)

        # event handling
        mouseDown = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pg.MOUSEBUTTONDOWN:
                mouseDown = True

        # screen setup
        screen.fill((20,20,20))

        # sprite updating
        tempMenuScreen.draw(screen, surface)
        resumeButton.update(screen, surface, mouseDown)
        mainMenuButton.update(screen, surface, mouseDown)
        quitButton.update(screen, surface, mouseDown)

        # button handling
        keys = pg.key.get_pressed() 
        if keys[pg.K_c]:
            fps(screen, surface, clock)
        if resumeButton.pressed:
            return 'resume'
        if mainMenuButton.pressed:
            return 'mainMenu'
        if quitButton.pressed:
            return 'quit'

        # screen update
        pg.display.flip()

    
def mainMenu():

    # initiate sprites
    ticks = 0
    slide = 'up'
    veiwing = 'menu'
    newButton = Button("MenuButtons/NewGame", (50, 500), 'New Game')
    loadButton = Button("MenuButtons/LoadGame", (500, 500), 'Load Game')
    quitButton = Button("MenuButtons/QuitGame", (950, 500), 'Quit Game')
    confrimationBox = Object("ConfirmNewGameBox",(450,50))
    yesButton = Button("MenuButtons/Yes", (475, 173), 'Load Game')
    noButton = Button("MenuButtons/No", (610, 173), 'Load Game')
    cabbage = Object('Cabbage',(65,-40))
    helicopter = Helicopter()
    mainMenuScreen = Menu("mainMenu")

    # main loop
    while True:
        clock.tick(30)
        
        # event handling
        mouseDown = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pg.MOUSEBUTTONDOWN:
                mouseDown = True

        # screen setup
        screen.fill((20,20,20))

        # cabbage movement
        if slide == 'up':
            ticks += 1
            cabbage.pos.y -= 1
        else:
            ticks -= 1
            cabbage.pos.y += 1

        if ticks == 30:
            slide = 'down'
        if ticks == 0:
            slide = 'up'
            

        # constant sprite updating
        mainMenuScreen.draw(screen, surface)
        helicopter.update(screen, surface)
        cabbage.draw(screen, surface)
        
        if veiwing == 'menu': # condition is that veiwing is 'menu'
            # conditional sprite updating
            quitButton.update(screen, surface, mouseDown)
            loadButton.update(screen, surface, mouseDown)
            newButton.update(screen, surface, mouseDown)
            # button handling
            if newButton.pressed:
                veiwing = 'confirmationBox'
                newButton.pressed = False
            if loadButton.pressed:
                return 'load'
            if quitButton.pressed:
                return 'quit'
        if veiwing == 'confirmationBox':
            confrimationBox.draw(screen, surface)
            yesButton.update(screen, surface, mouseDown)
            noButton.update(screen, surface, mouseDown)
            if yesButton.pressed:
                return 'new'
            if noButton.pressed:
                veiwing = 'menu'
            


        # screen update
        pg.display.flip()



def finnishMenu():

    # initiation
    veiwing = 'grandma'
    veiwing2 = 'notLiar'
    if getMoney() >= 5000:
        cash = 'gc'
    else:
        cash = 'ngc'
    ticks = getCurTick()
    grandmaMenu = Menu('payGrandmasBills')
    endMenu = Menu('finalMenu')
    confrimationBox = Object('NotEnoughCash',(360,202))
    okButton = Button('MenuButtons/OKsmall',(860,535),'Ok')
    finishButton = Button('MenuButtons/FinnishGame', (570,650), 'Finnish Game!')
    gtc = Button('MenuButtons/IGotTheCash',(770,560),'I Got The Cash!')
    dgtc = Button('MenuButtons/IDontGotTheCash',(270,560),'I Dont Got The Cash :(')
    exitButton = Button('MenuButtons/Exit',(1340,0),'Exit Interface')

    while True:
        clock.tick(30)

        # event handling
        mouseDown = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pg.MOUSEBUTTONDOWN:
                mouseDown = True

        # screen setup
        screen.fill((20,20,20))

        keys = pg.key.get_pressed() 
        if keys[pg.K_c]:
            fps(screen, surface, clock)
        if keys[pg.K_ESCAPE]:
            return 'tempMenu'

        if veiwing == 'grandma':

            grandmaMenu.draw(screen,surface)
            if veiwing2 == 'notLiar':
                # sprite update
                gtc.update(screen,surface,mouseDown)
                dgtc.update(screen,surface,mouseDown)
                exitButton.update(screen,surface,mouseDown)
                
                # button handling
                if exitButton.pressed:
                    return 'alfredsHouse'
                if gtc.pressed and cash == 'gc':
                    veiwing = 'finish'
                if gtc.pressed and cash == 'ngc':
                    veiwing2 = 'liar'
                if dgtc.pressed:
                    return 'alfredsHouse'

            if veiwing2 == 'liar':
                # sprite update
                confrimationBox.draw(screen,surface)
                okButton.update(screen,surface,mouseDown)

                # button handling
                if okButton.pressed:
                    gtc.pressed = False
                    veiwing2 = 'notLiar'

        if veiwing == 'finish':
            # sprite update
            endMenu.draw(screen,surface)
            finishButton.update(screen,surface,mouseDown)
            text(screen, surface, (f'Score = {ticks}',(500,250),36))

            # button handling
            if finishButton.pressed:
                print('yay')
                return

        pg.display.flip()
    
    
def newGameMenu():

    # reset player data
    # delete all crops growing & clear queue
    Tt('Plant')
    for i in range(20):
        RPC.enqueue('')
        RPC.save()
    # reset money
    subMoney(getMoney())
    addMoney(500)
    # reset inventory
    U('Inventory','Quantity = 0','EntryID >= 0')
    # reset planer types
    U('Planter', 'LightID = 3', 'PlanterID >= 0')
    U('Planter', 'GrowthMediaID = 3', 'PlanterID >= 0')
    
    
    # initiate sprites
    okButton = Button("MenuButtons/OKsmall", (780, 700), 'Play Game')
    newGameMenuScreen = Menu("NewGameMenu")

    # main loop
    while True:
        clock.tick(30)

        # event handling
        mouseDown = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pg.MOUSEBUTTONDOWN:
                mouseDown = True

        # screen setup
        screen.fill((20,20,20))

        # sprite updating
        newGameMenuScreen.draw(screen, surface)
        okButton.update(screen, surface, mouseDown)

        # button handling
        keys = pg.key.get_pressed() 
        if keys[pg.K_c]:
            fps(screen, surface, clock)
        if okButton.pressed:
            return 'play game'
        
        # screen update
        pg.display.flip()


        
def village():
    
    # initiate sprites
    pos = getPrevLocation('VillageLL')
    map1 = Map("village _ foreground", "village _ background", pos, CMvillage)
    bobsHouseDoor = MovingButton("Doors/bobsHouseEXT", pos, (724, 595), 'bobsHouseDoorVillage', 'Open Door')
    alfredsHouseDoor = MovingButton("Doors/alfredsHouseEXT", pos, (1331, 847), 'alfredsHouseDoorVillage', 'Open Door')
    davesShopDoor = MovingButton("Doors/davesShopEXT", pos, (849, 1835), 'davesShopDoorVillage', 'Enter Shop')
    alfonzesGarageDoor = MovingButton("Doors/alfonzesGarageDoorEXT", pos, (2991, 311), 'alfonzesGarageDoorVillage', 'Enter Garage')
    churchDoor = MovingButton("Doors/churchEXT", pos, (2228, 1616), 'churchDoorVillage', 'Enter Church')
    inventoryButton = Button('MenuButtons/InventoryIcon', (1340, 0), 'Open Inventory')
    susMeter = suspicionOMatik(RPC)

    # get time from curTick file
    clock1 = Clock12Hr()
    clock1.setTick(getCurTick())

    # main loop
    while True:
        clock.tick(30)
        
        # event handling
        mouseDown = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                setCurTick(clock1.retTick())
                return
            if event.type == pg.MOUSEBUTTONDOWN:
                mouseDown = True

        # screen setup
        screen.fill((199,140,93))

        # sprite update
        map1.update(screen)
        bobsHouseDoor.update(screen, surface, mouseDown, map1)
        alfredsHouseDoor.update(screen, surface, mouseDown, map1)
        davesShopDoor.update(screen, surface, mouseDown, map1)
        alfonzesGarageDoor.update(screen, surface, mouseDown, map1)
        churchDoor.update(screen, surface, mouseDown, map1)
        map1.drawForeground(screen)
        inventoryButton.update(screen, surface, mouseDown)
        clock1.update(screen, surface)
        susMeter.update(screen, surface)

        #button handling
        keys = pg.key.get_pressed() 
        if keys[pg.K_ESCAPE]:
            setPrevLocation(map1.pos, 'VillageLL')
            setCurTick(clock1.retTick())
            return 'tempMenu'
        if keys[pg.K_c]:
            fps(screen, surface, clock)
        if bobsHouseDoor.pressed:
            setPrevLocation(map1.pos, 'VillageLL')
            setCurTick(clock1.retTick())
            return 'bobsHouse'
        if alfredsHouseDoor.pressed:
            setPrevLocation(map1.pos, 'VillageLL')
            setCurTick(clock1.retTick())
            return 'alfredsHouse'
        if davesShopDoor.pressed:
            setPrevLocation(map1.pos, 'VillageLL')
            setCurTick(clock1.retTick())
            return 'davesShop'
        if alfonzesGarageDoor.pressed:
            setPrevLocation(map1.pos, 'VillageLL')
            setCurTick(clock1.retTick())
            return 'alfonzesGarage'
        if churchDoor.pressed:
            setPrevLocation(map1.pos, 'VillageLL')
            setCurTick(clock1.retTick())
            return 'church'
        if inventoryButton.pressed or keys[pg.K_TAB] or keys[pg.K_i]:
            setPrevLocation(map1.pos, 'VillageLL')
            setCurTick(clock1.retTick())
            return 'inventory'

        # scren update
        pg.display.flip()


def busted():

    # initiate sprites
    bustedMenu = Menu('Busted')
    okButton = Button("MenuButtons/OKsmall", (920, 705), 'Ok')
    
    # delete all crops growing & clear queue
    Tt('Plant')
    for i in range(20):
        RPC.enqueue('')
        RPC.save()
    # deduct money
    lossMoney = int(getMoney()/4)
    subMoney(lossMoney)
    
    while True:
        clock.tick(30)

        # event handling
        mouseDown = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pg.MOUSEBUTTONDOWN:
                mouseDown = True

        # screen setup
        screen.fill((20,20,20))

        # sprite update
        bustedMenu.draw(screen, surface)
        okButton.update(screen, surface, mouseDown)
        text(screen, surface, [lossMoney, (222,320), 38, (255,0,0)])

        # button handling
        keys = pg.key.get_pressed()
        if keys[pg.K_ESCAPE]:
            return'ok'
        if keys[pg.K_c]:
            fps(screen, surface, clock)
        if okButton.pressed:
            return 'ok'
   
        # screen update
        pg.display.flip()

def bobsHouse():

    # consider CEA raid
    if RPC.suspicionPercentage() == 100:
        return 'busted'
    
    # initiate sprites
    data = getList('PlanterData')
    pos = getPrevLocation('BobsHouseLL')
    inventoryButton = Button('MenuButtons/InventoryIcon', (1340, 0), 'Open Inventory')
    map1 = Map("bobsHouse _ foreground", "bobsHouse _ background", pos, CMbobsHouse)
    exitDoor = MovingButton("Doors/interiorDoor", pos, (891, 1176), 'intExitDoor', 'Open Door')
    res = Qs('GrowthMedia.Name', 'Planter, GrowthMedia', 'Planter.GrowthMediaID = GrowthMedia.GrowthMediaID AND PlanterID = 1')
    planter1 = MovingButton(f"PlanterButtons/planterTable{res}Small", pos, (850, 50), "alwaysAvalable", "Open Interface")
    res = Qs('GrowthMedia.Name', 'Planter, GrowthMedia', 'Planter.GrowthMediaID = GrowthMedia.GrowthMediaID AND PlanterID = 2')
    planter2 = MovingButton(f"PlanterButtons/planterTable{res}Small", pos, (500, 50), "alwaysAvalable", "Open Interface")
    res = Qs('GrowthMedia.Name', 'Planter, GrowthMedia', 'Planter.GrowthMediaID = GrowthMedia.GrowthMediaID AND PlanterID = 3')
    planter3 = MovingButton(f"PlanterButtons/planterTable{res}Small", pos, (150, 50), "alwaysAvalable", "Open Interface")

    # get time from curTick file
    clock1 = Clock12Hr()
    clock1.setTick(getCurTick())
    
    # main loop
    while True:
        clock.tick(30)
        
        # event handling
        mouseDown = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                setCurTick(clock1.retTick())
                return
            if event.type == pg.MOUSEBUTTONDOWN:
                mouseDown = True

        # screen setup
        screen.fill((20,20,20))

        # sprite update
        map1.update(screen)
        exitDoor.update(screen, surface, mouseDown, map1)
        planter1.update(screen, surface, mouseDown, map1)
        planter2.update(screen, surface, mouseDown, map1)
        planter3.update(screen, surface, mouseDown, map1)
        map1.drawForeground(screen)
        inventoryButton.update(screen, surface, mouseDown)
        clock1.update(screen, surface)

        #button handling
        keys = pg.key.get_pressed() 
        if keys[pg.K_ESCAPE]:
            setPrevLocation(map1.pos, 'BobsHouseLL')
            setCurTick(clock1.retTick())
            return ['tempMenu']
        if keys[pg.K_c]:
            fps(screen, surface, clock)
        if exitDoor.pressed:
            setPrevLocation(Vector2(-270,-685), 'BobsHouseLL')
            setCurTick(clock1.retTick())
            return ['village']
        if planter1.pressed:
            setPrevLocation(map1.pos, 'BobsHouseLL')
            setCurTick(clock1.retTick())
            return 'planter', 1
        if planter2.pressed:
            setPrevLocation(map1.pos, 'BobsHouseLL')
            setCurTick(clock1.retTick())
            return 'planter', 2
        if planter3.pressed:
            setPrevLocation(map1.pos, 'BobsHouseLL')
            setCurTick(clock1.retTick())
            return 'planter', 3
        if inventoryButton.pressed or keys[pg.K_TAB] or keys[pg.K_i]:
            setPrevLocation(map1.pos, 'BobsHouseLL')
            setCurTick(clock1.retTick())
            return ['inventory']
        
        # scren update
        pg.display.flip()

        
def alfredsHouse():
    
    # initiate sprites
    pos = getPrevLocation('AlfredsHouseLL')
    map1 = Map("bobsHouse _ foreground", "alfredsHouse _ background", pos, CMbobsHouse)
    exitDoor = MovingButton("Doors/interiorDoor", pos, (891, 1176), 'intExitDoor', 'Open Door')
    grandma = MovingButton('MenuButtons/Grandma',pos,(375,730),'alwaysAvalable','Pay Grandmas Medical Bills?')

    # get time from curTick file
    clock1 = Clock12Hr()
    clock1.setTick(getCurTick())
    
    # main loop
    while True:
        clock.tick(30)
        
        # event handling
        mouseDown = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pg.MOUSEBUTTONDOWN:
                mouseDown = True

        # screen setup
        screen.fill((20,20,20))

        # sprite update
        map1.update(screen)
        exitDoor.update(screen, surface, mouseDown, map1)
        grandma.update(screen, surface, mouseDown, map1)
        map1.drawForeground(screen)

        #button handling
        keys = pg.key.get_pressed() 
        if keys[pg.K_ESCAPE]:
            setPrevLocation(map1.pos, 'AlfredsHouseLL')
            return 'tempMenu'
        if keys[pg.K_c]:
            fps(screen, surface, clock)
        if exitDoor.pressed:
            setPrevLocation(Vector2(-270,-685), 'AlfredsHouseLL')
            return 'village'
        if grandma.pressed:
            setPrevLocation(map1.pos, 'AlfredsHouseLL')
            return 'grandma'
        
        # scren update
        pg.display.flip()


# list
CMvillage = ReturnCMvillage()
CMbobsHouse = ReturnCMbobsHouse()

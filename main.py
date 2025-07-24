import time
from random import randint, choice

try:
    import pygame
except:
    print("Pygame must be installed to play top trumps!")
    quit()

# colour palette - https://www.color-hex.com/color-palette/1294

# constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 500
FRAMERATE = 60

class MENU:
    def __init__(self, screen, font, offsety = 55, offsetx = 0, startx = 400, starty = 250, width = 300, height = 50, **buttonData):
        self.screen = screen
        self.font = font
        self.offsety = offsety
        self.offsetx = offsetx
        self.starty = starty
        self.startx = startx
        self.buttons = [] # [title, rectObject, destinationMethod]
        
        for i, buttonName in enumerate(buttonData.keys()):
            self.buttons.append(    
                [buttonName, 
                    pygame.Rect(startx + (i * offsetx) - (width/2),
                    (starty + (i * offsety) - (height/2)),
                    width, 
                    height), 
                    buttonData[buttonName]
                ] 
            )
            
    def update(self, mouseUp = False):
        for i, button in enumerate(self.buttons):
            textColour = (179,205,224)
            btnColour = (0,91,150)
            
            # check for mouse collisions
            mousePos = pygame.mouse.get_pos()
            if button[1].collidepoint(mousePos) and mouseUp: # check for LMB up
                #print(button[0], "clicked")
                
                if button[2] != 0:
                    button[2]() # call the destination methohd     
                    
            elif button[1].collidepoint(mousePos):
                textColour = (250,250,250)
                btnColour = (10,101,160)
                
                if pygame.mouse.get_pressed()[0]:
                    textColour = (169,195,214)
                    btnColour = (0,81,150)
                
            # draw all the buttons
            pygame.draw.rect(self.screen, btnColour, button[1], border_radius=7)
            text = self.font.render(button[0].replace("_", " "), True, textColour)
            textRect = text.get_rect(center = (self.startx + (i*self.offsetx), self.starty + (i*self.offsety)))
            self.screen.blit(text, textRect)

class CARD:
    def __init__(self, screen, font, name, exercise, intelligence, friendliness, drool):
        self.name = name
        self.exercise = exercise
        self.intelligence = intelligence
        self.friendliness = friendliness
        self.drool = drool
        self.screen = screen
        self.font = font
    
    def display(self, flipX = False, hideDetails = False):
        if flipX:
            backing = pygame.Rect(SCREEN_WIDTH*3/4 - (215/2), 265 - (120/2), 215, 120)
            pygame.draw.rect(self.screen, (0,91,150), backing, border_radius=10)
            
            
            if not hideDetails:
                infotext = self.font.render(("Exercise - %s\nIntelligence - %s\nFriendliness - %s\nDrool - %s" %(self.exercise, self.intelligence, self.friendliness, self.drool)), True, (179,205,224))
                infotextRect = infotext.get_rect(center = (SCREEN_WIDTH*3/4, 265))
                self.screen.blit(infotext, infotextRect)
                nameText = self.font.render(self.name, True, (179,205,224))
                nameTextRect = nameText.get_rect(center = (SCREEN_WIDTH*3/4, 180))
                self.screen.blit(nameText, nameTextRect)
                return
            
            infotext = self.font.render(("Exercise - ?\nIntelligence - ?\nFriendliness - ?\nDrool - ?"), True, (179,205,224))
            infotextRect = infotext.get_rect(center = (SCREEN_WIDTH*3/4, 265))
            self.screen.blit(infotext, infotextRect)
            nameText = self.font.render("?????", True, (179,205,224))
            nameTextRect = nameText.get_rect(center = (SCREEN_WIDTH*3/4, 180))
            self.screen.blit(nameText, nameTextRect)
            return
            
        backing = pygame.Rect(SCREEN_WIDTH/4 - (215/2), 265 - (120/2), 215, 120)
        pygame.draw.rect(self.screen, (0,91,150), backing, border_radius=10)
        nameText = self.font.render(self.name, True, (179,205,224))
        nameTextRect = nameText.get_rect(center = (SCREEN_WIDTH/4, 180))
        self.screen.blit(nameText, nameTextRect)
        infotext = self.font.render(("Exercise - %s\nIntelligence - %s\nFriendliness - %s\nDrool - %s" %(self.exercise, self.intelligence, self.friendliness, self.drool)), True, (179,205,224))
        infotextRect = infotext.get_rect(center = (SCREEN_WIDTH/4, 265))
        self.screen.blit(infotext, infotextRect)

class MAIN:
    def __init__(self):
        self.setupGame()
        self.running = True
        self.mainLoop()
        
    def setupGame(self):
        pygame.init()
        pygame.display.set_caption("Top Trumps")
        pygame.display.set_icon(pygame.image.load("cardicon.png"))
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("Poppins-Bold.ttf", size=20)
        self.largefont = pygame.font.Font("Poppins-Bold.ttf", size=40)
        self.mouseButtonUp = False
        self.state = "MAINMENU"
        self.turn = 0
        self.cardNum = ""
        self.playerCards = []
        self.computerCards = []
        self.awaitingInput = False
        self.backgroundImage = pygame.image.load("gradient.png").convert()
        
        self.mainMenu = MENU(self.screen, self.font, Play = lambda: self.changeState("CARDINPUT"), Quit = self.closeGame)
        self.gameOverMenu = MENU(self.screen, self.font, Main_Menu = lambda: self.changeState("MAINMENU"), Play_Again = self.replayGame, Quit = self.closeGame)
    
    def replayGame(self):
        self.playerCards = []
        self.computerCards = []
        self.turn = 0
        self.state = "CARDINPUT"
    
    def changeState(self, newState):
        self.state = newState
    
    def drawActiveState(self): # draw UI to window
        match self.state:
            case "MAINMENU":
                titleText = self.largefont.render("Top Trumps", True, (255,255,255))
                self.screen.blit(titleText, titleText.get_rect(center = (SCREEN_WIDTH/2, 150)))
                subText = self.font.render("by Harry", True, (179,205,224))
                self.screen.blit(subText, subText.get_rect(center = (SCREEN_WIDTH/2, 180)))
                self.mainMenu.update(mouseUp=self.mouseButtonUp)
                
            case "CARDINPUT":
                titleText = self.largefont.render("Enter an even number of cards", True, (255,255,255))
                self.screen.blit(titleText, titleText.get_rect(center = (SCREEN_WIDTH/2, 150)))
                subText = self.font.render("between 4 and 30 inclusive", True, (179,205,224))
                self.screen.blit(subText, subText.get_rect(center = (SCREEN_WIDTH/2, 180)))
                subText = self.font.render("_____", True, (179,205,224))
                self.screen.blit(subText, subText.get_rect(center = (SCREEN_WIDTH/2, 270)))
                
                self.awaitingInput = True
                inputText = self.font.render(str(self.cardNum), True, (179,205,224))
                self.screen.blit(inputText, inputText.get_rect(center = (SCREEN_WIDTH/2, 260)))
                
            case "GAME":
                titleText = self.largefont.render("Choose a category", True, (255,255,255))
                self.screen.blit(titleText, titleText.get_rect(center = (SCREEN_WIDTH/2, 75)))
                subText = self.largefont.render("Your card:", True, (179,205,224))
                self.screen.blit(subText, subText.get_rect(center = (SCREEN_WIDTH/4, 135)))
                subText = self.largefont.render("AI's card:", True, (179,205,224))
                self.screen.blit(subText, subText.get_rect(center = (SCREEN_WIDTH*3/4, 135)))
                subText = self.font.render((f"{len(self.playerCards)} Cards"), True, (179,205,224))
                self.screen.blit(subText, subText.get_rect(center = (SCREEN_WIDTH/4, 350)))
                subText = self.font.render((f"{len(self.computerCards)} Cards"), True, (179,205,224))
                self.screen.blit(subText, subText.get_rect(center = (SCREEN_WIDTH*3/4, 350)))
                self.playerCard.display()
                
                if self.turn % 2 == 0:
                    self.computerCard.display(flipX = True, hideDetails = True)
                    self.cardOptionsMenu.update(self.mouseButtonUp)
                    self.mouseButtonUp = False
                else:
                    self.computerCard.display(flipX = True, hideDetails = False)
                    self.timer -= self.deltaTime
                    
                    
                    if self.timer <= 0:
                        if len(self.computerCards) < 1:
                            self.state = "PLAYERWIN"
                            return
                        
                        elif len(self.playerCards) < 1:
                            self.state = "COMPUTERWIN"
                            return
                        
                        self.turn += 1
                        self.playerCard = self.playerCards[0]
                        self.computerCard = self.computerCards[0]
            
            case "PLAYERWIN":
                titleText = self.largefont.render(f"Player wins after {self.turn} turns!", True, (255,255,255))
                self.screen.blit(titleText, titleText.get_rect(center = (SCREEN_WIDTH/2, 75)))
                self.gameOverMenu.update(self.mouseButtonUp)
                self.mouseButtonUp = False
            
            case "COMPUTERWIN":
                titleText = self.largefont.render(f"Computer wins after {self.turn} turns!", True, (255,255,255))
                self.screen.blit(titleText, titleText.get_rect(center = (SCREEN_WIDTH/2, 75)))
                self.gameOverMenu.update(self.mouseButtonUp)
                self.mouseButtonUp = False
                
    def generateCards(self): # generate random stats for each card and then distribute half to player and ai
        dogNames = []
        cards = []
        with open("dogs.txt", "r") as file:
            dogNames = file.readlines()
        
        for dog in dogNames:
            cards.append(CARD(self.screen, self.font, dog, randint(1,5), randint(1,100), randint(1,10), randint(1,10)))
        
        # assing a deck using half of the cards for each
        for _ in range(int(self.cardNum)//2):
            card = choice(cards)
            self.playerCards.append(card)
            cards.remove(card)
            
            card = choice(cards)
            self.computerCards.append(card)
            cards.remove(card)
    
        # randomly pick a card for the player and the computer
        self.playerCard = self.playerCards[0]
        self.computerCard = self.computerCards[0]
        
        self.cardOptionsMenu = MENU(
            self.screen, self.font, 
            offsety=0, offsetx=175, startx=135, starty=400, width=150,
            Exercise = lambda: self.choose("Exercise"), 
            Intelligence = lambda: self.choose("Intelligence"), 
            Friendliness = lambda: self.choose("Friendliness"), 
            Drool = lambda: self.choose("Drool")
        )
    
    def playerWin(self): # add both cards to back of pile and then remove card on top of pile
        self.playerCards.append(self.computerCard)
        self.playerCards.append(self.playerCard)
        self.computerCards.remove(self.computerCard)
        self.playerCards.remove(self.playerCard)
        #print("playerwin")
        
    def computerWin(self):
        self.computerCards.append(self.playerCard)
        self.playerCards.remove(self.playerCard)
        self.computerCards.append(self.computerCard)
        self.computerCards.remove(self.computerCard)
        #print("computerwin")

    def choose(self, trait):
        if trait == "Exercise":
            if self.playerCard.exercise >= self.computerCard.exercise:
                self.playerWin()
            else:
                self.computerWin()
                
        elif trait == "Intelligence":
            if self.playerCard.intelligence >= self.computerCard.intelligence:
                self.playerWin()
            else:
                self.computerWin()
                
        elif trait == "Friendliness":
            if self.playerCard.friendliness >= self.computerCard.friendliness:
                self.playerWin()
            else:
                self.computerWin()
        
        elif trait == "Drool":
            if self.playerCard.drool <= self.computerCard.drool:
                self.playerWin()
            else:
                self.computerWin()
                    
        self.turn += 1
        self.timer = 1.5
        
    def eventLoop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: 
                    self.mouseButtonUp = True
            else: 
                self.mouseButtonUp = False
            
            # allow 600ms to show the error message and then send player to main menu
            if self.cardNum == "Invalid Input!":
                time.sleep(0.6)
                self.cardNum = ""
                self.state = "MAINMENU"
            
            # take input and test it
            if event.type == pygame.KEYDOWN and self.awaitingInput:
                if event.key == pygame.K_BACKSPACE:
                    self.cardNum = self.cardNum[:-1]
                    return
                
                if event.key != pygame.K_RETURN:
                    self.cardNum += event.unicode
                    return
                
                if self.cardNum.isdigit():
                    if int(self.cardNum) >= 4 and int(self.cardNum) <= 30:
                        if int(self.cardNum) % 2 == 0:
                            self.awaitingInput = False
                            self.state = "GAME"
                            self.generateCards()
                            return
                    
                self.cardNum = "Invalid Input!"
    
    def mainLoop(self):
        while self.running:
            self.screen.fill((3,57,108)) # clear the screen
            self.screen.blit(self.backgroundImage)
            self.drawActiveState()
            
            self.eventLoop()
            pygame.display.flip() # update screen

            self.deltaTime = self.clock.tick(FRAMERATE) / 1000 # use delta time for smoothness
            self.deltaTime = max(0.001, min(0.1, self.deltaTime))
            
        self.closeGame()
            
    def closeGame(self):
        print("Quitting..")
        pygame.quit()
        quit() # stop the program from running as pygame will throw an error if any calls are made to pygame after quit
   
if __name__ == "__main__":
    try:
        MAIN()
    except Exception as e:
        print(f"An unexpected error occured\n\nDetails:\n{e}")
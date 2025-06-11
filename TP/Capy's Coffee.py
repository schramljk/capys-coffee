from cmu_graphics import *
from PIL import Image
import random
import time

###### Functions ######

EPSILON = 10e-2
def almostEqual(x, y, epsilon=EPSILON): #from cmu graphics, changed 10e-7 to 10e-2
    return abs(x - y) <= epsilon

def distance(x0, y0, x1, y1):
    return ((x1 - x0)**2 + (y1 - y0)**2)**0.5

def dotsOverlap(x0, y0, r0, x1, y1, r1):
    return distance(x0, y0, x1, y1) <= r0+r1

#makes sure that two options can't be clicked at the same time
def noRepeats(mouseX, mouseY, optionList):
    optionSet = set(optionList)
    for option in optionList:
        for other in optionSet:
            if option != other and other.selected == False:
                option.selectOption(mouseX, mouseY)

###### Classes ######

class Pic:
    def __init__(self, url, centerX, centerY, scale, operator, name):
        self.url = url
        self.x = centerX
        self.y = centerY
        self.scale = scale
        self.op = operator
        self.name = name

    def drawPic(self):
        name = CMUImage(Image.open(self.url))
        imageWidth, imageHeight = getImageSize(name)
        if self.op == "/": #makes image smaller
            width = imageWidth/self.scale
            height = imageHeight/self.scale
        elif self.op == "*": #makes image larger
            width = imageWidth*self.scale
            height = imageHeight*self.scale
        return drawImage(name, self.x, self.y, align="center", width=width, 
                         height=height)
    
    def moveToCounter(self):
        self.x += 5 #moves to the right

class CoffeeMachine:
    def __init__(self, x, y, number):
        self.x = x
        self.y = y
        self.number = number

    def drawMachine(self):
        drawRect(self.x, self.y, 300, 500, fill="maroon")
        drawOval(self.x + 150, self.y + 450, 250, 50, fill="gray")
        drawRect(self.x, self.y, 300, 100, fill="dimGray")
        drawRect(self.x + 125, self.y + 100, 50, 30, fill="dimGray")
        drawLabel(f"{self.number}", self.x + 150, 250, size=30)

    def brew(self): #coffee comes out of machine
        drawLine(self.x + 150, 330, self.x + 150, 500, fill="saddleBrown",
                 lineWidth=3)
        return True

class Cup:
    def __init__(self, centerX, centerY, number, color, screen):
        self.x = centerX
        self.y = centerY
        self.number = number
        self.color = color
        self.screen = screen

    def drawCup(self):
        drawPolygon(self.x - 100, self.y - 100, self.x + 100, self.y - 100,
                    self.x + 50, self.y + 100, self.x - 50, self.y + 100,
                    fill=self.color)
        drawLabel(self.number, self.x, self.y, size=30)

    def moving(self, mouseX, mouseY): #center of cup follows mouse
        self.x = mouseX
        self.y = mouseY

    def isDone(self): #placed in correct position to continue
        if dotsOverlap(1000, 550, 20, self.x, self.y, 0):
            return True
        return False

class Button:
    def __init__(self, left, right, top, bottom, fill, text, color, size, 
                 action, params):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self.fill = fill
        self.text = text
        self.color = color
        self.size = size
        self.action = action
        self.params = params
        self.width = self.right - self.left
        self.height = self.bottom - self.top
        self.showOrder = False

    def isInside(self, mouseX, mouseY): #mouse is inside the button 
        if (self.left <= mouseX <= self.right and 
            self.top <= mouseY <= self.bottom):
            return True
        return False
    
    def doAction(self, mouseX, mouseY): #does the action the button is assigned to
        if self.isInside(mouseX, mouseY):
            self.action(self.params)
            return True
        
    def drawBackground(self):
        return drawRect(self.left, self.top, self.width, self.height, 
                        fill=self.fill)
    
    def drawText(self):
        centerX = self.left + (self.width / 2)
        centerY = self.top + (self.height / 2)
        return drawLabel(self.text, centerX, centerY, size=self.size, 
                         fill=self.color)
    
    def view(self, mouseX, mouseY): #can view the order from a different screen
        if self.isInside(mouseX, mouseY):
            self.showOrder = not self.showOrder
    
class Orders:
    def __init__(self, number):
        self.number = number
        #makes sure that every order is random
        milkFlavors = ["Skim", "Strawberry", "Chocolate", "Blueberry"]
        self.milk = milkFlavors[random.randrange(len(milkFlavors))]
        espressoFlavors = ["City", "Decaf", "French", "New England"]
        self.espresso = espressoFlavors[random.randrange(len(espressoFlavors))]
        syrupFlavors = ["Chocolate", "Salted Caramel", "Cinnamon Dulce", "Marshmallow"]
        self.syrup = syrupFlavors[random.randrange(len(syrupFlavors))]
        creamFlavors = ["Whipped", "Butterscotch", "Strawberry", "Chocolate", 
                        "Lemon", "Peach"]
        self.cream = creamFlavors[random.randrange(len(creamFlavors))]
        toppingFlavors = ["Cinnamon Sugar", "Crushed Pistachios", 
                          "Shaved Chocolate", "Toasted Coconut", "Mini Mallows", 
                          "Rainbow Sprinkles"]
        self.topping = toppingFlavors[random.randrange(len(toppingFlavors))]

    def display(self): #shows the order
        milk = f"{self.milk} Milk"
        espresso = f"{self.espresso} Roast"
        syrup = f"{self.syrup} Syrup"
        cream = f"{self.cream} Cream"
        topping = f"{self.topping} Topping"
        order = [milk, espresso, syrup, cream, topping]
        for i in range(len(order)):
            drawLabel(order[i], 225 + 375*(self.number-1), 300 + 50*i, size=25, 
                      fill="saddleBrown")
            
    def viewOrder(self): #shows order on different screen
        drawRect(600, 200, 300, 300, fill="blanchedAlmond", align="center")
        milk = f"{self.milk} Milk"
        espresso = f"{self.espresso} Roast"
        syrup = f"{self.syrup} Syrup"
        cream = f"{self.cream} Cream"
        topping = f"{self.topping} Topping"
        order = [milk, espresso, syrup, cream, topping]
        for i in range(len(order)):
            drawLabel(order[i], 600, 100+50*i, size=25, fill="saddleBrown")

class Option:
    def __init__(self, name, centerX, centerY, radius, color, row):
        self.name = name
        self.x = centerX
        self.y = centerY
        self.r = radius
        self.color = color
        self.row = row
        self.border = "black"
        self.selected = False

    def __eq__(self, other): #if the option is the same as another option
        if self.name == other.name:
            return True
        return False
    
    def __hash__(self):
        return hash(str(self))

    def drawOption(self): #draws option on screen and modifies border if selected
        if self.selected == True:
            self.border = "yellow"
        else:
            self.border = "black"
        drawCircle(self.x, self.y, self.r, fill=self.color, 
                   border=self.border, borderWidth=4)
        
    def selectOption(self, mouseX, mouseY): #changes border color if selected
        if dotsOverlap(self.x, self.y, self.r, mouseX, mouseY, 0):
            self.selected = not self.selected

###### Graphics ######

def onAppStart(app):
    restartApp(app)

def restartApp(app): #loads everything again
    app.counterStart = 0
    app.stepsPerSecond = 25

    #Timers for timing the orders
    app.startTime1 = 0
    app.startTime2 = 0
    app.startTime3 = 0
    app.endTime1 = 0
    app.endTime2 = 0
    app.endTime3 = 0

    #Images
    app.cuteCoffeeImage = Pic("other/cuteCoffee.PNG", 600, 400, 4, "/", "Cute Coffee") #https://cdn.pixabay.com/photo/2022/08/29/22/43/cartoon-7419928_1280.png
    app.capybaraImage = Pic("animals/capybara.png", 1050, 600, 1.8, "/", "Capybara") #https://thumb.ac-illust.com/d2/d25d2964a50cbc26d2c6948d520006c7_t.jpeg
    app.raccoonImage = Pic("animals/raccoon.png", 150, 600, 1.8, "/", "Raccoon") #https://e7.pngegg.com/pngimages/817/241/png-clipart-cute-raccoon-fly-net-gray-cartoon.png
    app.duckImage = Pic("animals/duck.png", 150, 600, 1.8, "/", "Duck") #https://www.pngkey.com/png/detail/183-1835678_free-tracks-clipartmansion-com-duckling-cartoon-farm-animal.png
    app.bunnyImage = Pic("animals/bunny.png", 150, 600, 1.7, "/", "Bunny") #https://png.pngtree.com/png-clipart/20190116/ourmid/pngtree-white-rabbit-cute-rabbit-anthropomorphic-rabbit-cartoon-illustration-png-image_410973.jpg
    app.catImage = Pic("animals/cat.png", 150, 600, 1.8, "/", "Cat") #https://media.istockphoto.com/id/1097490360/vector/vector-illustration-of-cute-black-cat.jpg?s=612x612&w=0&k=20&c=Ef0qYl79aZJ6NJXJVbJ0onjXVNnSyqrN_TKPjieAIGE=
    app.speechBubble = Pic("other/speechBubble.png", 1000, 350, 7, "/", "Speech") #https://static.vecteezy.com/system/resources/previews/001/195/588/original/speech-bubble-png.png
    app.cowImage = Pic("flavors/cow.png", 115, 280, 10, "/", "Cow") #https://media.istockphoto.com/id/1256233718/vector/cute-cow-vector-icon-illustration.jpg?s=612x612&w=0&k=20&c=i_MCfgGxR-6GvXYV5yZ4jNF_7VwGKxd0TMaEEyo0Mqk=
    app.strawberryMilk = Pic("flavors/strawberry.png", 190, 280, 13, "/", "Strawberry") #https://static.vecteezy.com/system/resources/previews/004/557/722/original/fruit-strawberry-cartoon-object-vector.jpg
    app.chocolateMilk = Pic("flavors/chocolate.png", 265, 280, 9, "/", "Chocolate") #https://t4.ftcdn.net/jpg/02/86/24/63/360_F_286246320_YdcHrujL8N1A0CVR5BNchcwXKj6YYtax.jpg
    app.blueberryImage = Pic("flavors/blueberry.png", 340, 280, 5.5, "/", "Blueberry") #https://t3.ftcdn.net/jpg/01/91/01/54/360_F_191015478_q9FaYV71294oCziklqfqWkhFfrlcmh3S.jpg
    app.cityImage = Pic("flavors/city.png", 115, 447, 12, "/", "City") #https://png.pngtree.com/element_origin_min_pic/16/06/30/21577520ee1252d.jpg
    app.decafImage = Pic("flavors/decaf.png", 190, 447, 6, "/", "Decaf") #https://www.google.com/url?sa=i&url=http%3A%2F%2Fclipart-library.com%2Ffree%2Fcartoon-coffee-cup-png.html&psig=AOvVaw2SgTrfDQeNVr5EGlhXIDVw&ust=1682229224546000&source=images&cd=vfe&ved=0CBAQjRxqFwoTCIDhpN_mvP4CFQAAAAAdAAAAABA3
    app.frenchImage = Pic("flavors/french.png", 265, 447, 14, "/", "French") #https://static.vecteezy.com/system/resources/previews/003/700/673/original/french-flag-illustration-free-vector.jpg
    app.newEnglandImage = Pic("flavors/newEngland.png", 340, 447, 10, "/", "New England") #https://png.pngtree.com/png-clipart/20210309/original/pngtree-green-cartoon-pine-tree-clipart-png-image_5875230.jpg
    app.chocolateSyrup = Pic("flavors/chocolate.png", 115, 614, 9, "/", "Chocolate")
    app.caramelImage = Pic("flavors/caramel.png", 190, 614, 8, "/", "Caramel") #https://us.123rf.com/450wm/mything/mything1707/mything170700044/82433078-piece-of-caramel-vector-illustration-flat-icon-isolated-on-white.jpg?ver=6
    app.cinnamonImage = Pic("flavors/cinnamon.png", 265, 614, 9, "/", "Cinnamon") #https://cdn3.vectorstock.com/i/1000x1000/69/92/cinnamon-sticks-icon-cartoon-style-vector-10306992.jpg
    app.marshmallowImage = Pic("flavors/marshmallow.png", 340, 614, 11, "/", "Marshmallow") #https://media.istockphoto.com/id/1442899473/pt/vetorial/marshmallow-cartoon-vector-marshmallow-logo-design-marshmallow-icon.jpg?s=612x612&w=0&k=20&c=vOrubp3eTZe1RM6cNhya0dES63osHwen4QkLkVGito4=
    app.whippedImage = Pic("flavors/whipped.png", 100, 300, 6, "/", "Whipped") #https://media.istockphoto.com/id/1215372643/vector/whipped-cream-isolated-on-white-background-vector-illustration-of-dessert-in-cartoon-flat.jpg?s=612x612&w=0&k=20&c=8hjv7xN7OZ5Z6Dlmv0wylAIBxLnBKXqFIXvOkuSUMl8=
    app.butterscotchImage = Pic("flavors/caramel.png", 100, 425, 5, "/", "Butterscotch")
    app.strawberryCream = Pic("flavors/strawberry.png", 100, 550, 7, "/", "Strawberry")
    app.chocolateCream = Pic("flavors/chocolate.png", 250, 300, 5, "/", "Chocolate")
    app.lemonImage = Pic("flavors/lemon.png", 250, 425, 6, "/", "Lemon") #https://img.lovepik.com/free-png/20210922/lovepik-cartoon-hand-painted-lemon-png-image_401098937_wh1200.png
    app.peachImage = Pic("flavors/peach.png", 250, 550, 5.5, "/", "Peach") #https://img.freepik.com/premium-vector/set-fresh-whole-half-cut-slice-piece-peach-isolated-white-background-vegan-food-icons-trendy-cartoon-style-healthy-concept_168129-689.jpg?w=2000
    app.cinnamonSugar = Pic("flavors/cinnamon.png", 950, 300, 4.5, "/", "Cinnamon Sugar")
    app.pistachioImage = Pic("flavors/pistachio.png", 950, 425, 5.5, "/", "Crushed Pistachios") #https://cdn3.vectorstock.com/i/1000x1000/79/77/pistachios-icon-cartoon-style-vector-21187977.jpg
    app.shavedChocolate = Pic("flavors/chocolate.png", 950, 550, 5, "/", "Shaved Chocolate")
    app.coconutImage = Pic("flavors/coconut.png", 1100, 300, 7.5, "/", "Toasted Coconut") #https://upload.wikimedia.org/wikipedia/commons/8/8d/Coconut_Clipart_Cartoon.png
    app.miniMallows = Pic("flavors/marshmallow.png", 1100, 425, 6, "/", "Mini Mallows")
    app.rainbowSprinkles = Pic("flavors/sprinkles.png", 1100, 550, 6, "/", "Rainbow Sprinkles") #https://www.vhv.rs/dpng/d/545-5453439_small-pile-of-rainbow-sprinkle-confetti-on-a.png

    #Animals
    app.animalList = [app.raccoonImage, app.duckImage, app.bunnyImage,
                      app.catImage]
    animalIndex = random.randrange(len(app.animalList))
    app.animal = app.animalList[animalIndex]

    #Buttons
    app.instrucBut = Button(450, 750, 575, 625, 'saddleBrown', "Instructions", 
                            "burlyWood", 30, setActiveScreen, "instructions")
    app.startBut = Button(450, 750, 675, 725, 'saddleBrown', "Start Game", 
                          "burlyWood", 30, setActiveScreen, "startGame")
    app.backBut = Button(500, 700, 675, 725, "sienna", "Back", "bisque", 30,
                         setActiveScreen, "home")
    app.orderBut = Button(905, 1105, 270, 370, "sienna", "Take Order", "wheat", 
                          35, setActiveScreen, "order")
    app.makeBut1 = Button(175, 275, 600, 650, "peru", "Make", "blanchedAlmond",
                          30, setActiveScreen, "build")
    app.makeBut2 = Button(550, 650, 600, 650, "peru", "Make", "blanchedAlmond",
                          30, setActiveScreen, "build")
    app.makeBut3 = Button(925, 1025, 600, 650, "peru", "Make", "blanchedAlmond",
                          30, setActiveScreen, "build")
    app.brewBut1 = Button(175, 275, 225, 275, "white", "Brew", "black", 20,
                          setActiveScreen, "toppings")
    app.brewBut2 = Button(550, 650, 225, 275, "white", "Brew", "black", 20, 
                          setActiveScreen, "toppings")
    app.brewBut3 = Button(925, 1025, 225, 275, "white", "Brew", "black", 20,
                          setActiveScreen, "toppings")
    app.nextBut = Button(950, 1050, 375, 425, "saddleBrown", "Next", 
                         "burlyWood", 30, setActiveScreen, "brew")
    app.order1But = Button(125, 175, 100, 150, "burlyWood", "1", "saddleBrown",
                           30, setActiveScreen, "none")
    app.order2But = Button(200, 250, 100, 150, "burlyWood", "2", "saddleBrown",
                           30, setActiveScreen, "none")
    app.order3But = Button(275, 325, 100, 150, "burlyWood", "3", "saddleBrown",
                           30, setActiveScreen, "none")
    app.finishedBut = Button(950, 1100, 50, 100, "saddleBrown", "Finished",
                             "burlyWood", 30, setActiveScreen, "scores")
    app.playAgainBut = Button(450, 750, 575, 625, "saddleBrown", "Play Again",
                              "burlyWood", 30, setActiveScreen, "home")
    app.cup1But = Button(500, 550, 50, 100, "burlyWood", "1", "saddleBrown",
                         30, setActiveScreen, "none")
    app.cup2But = Button(575, 625, 50, 100, "burlyWood", "2", "saddleBrown",
                         30, setActiveScreen, "none")
    app.cup3But = Button(650, 700, 50, 100, "burlyWood", "3", "saddleBrown", 
                         30, setActiveScreen, "none")
    
    #Options
    app.milkList = [Option("Skim", 115, 280, 28, "floralWhite", 1),
                    Option("Strawberry", 190, 280, 28, "pink", 1),
                    Option("Chocolate", 265, 280, 28, "saddleBrown", 1),
                    Option("Blueberry", 340, 280, 28, "lightSkyBlue", 1)]
    app.espressoList = [Option("City", 115, 447, 28, "darkGray", 2),
                        Option("Decaf", 190, 447, 28, "darkOrange", 2),
                        Option("French", 265, 447, 28, "mediumBlue", 2),
                        Option("New England", 340, 447, 28, "darkGreen", 2)]
    app.syrupList = [Option("Chocolate", 115, 614, 28, "saddleBrown", 3),
                     Option("Salted Caramel", 190, 614, 28, "chocolate", 3),
                     Option("Cinnamon Dulce", 265, 614, 28, "burlyWood", 3),
                     Option("Marshmallow", 340, 614, 28, "cornSilk", 3)]

    #Flavors
    app.creamList = [Option("Whipped", 100, 300, 50, "floralWhite", 1),
                     Option("Butterscotch", 100, 425, 50, "peru", 1),
                     Option("Strawberry", 100, 550, 50, "lightPink", 1),
                     Option("Chocolate", 250, 300, 50, "saddleBrown", 2),
                     Option("Lemon", 250, 425, 50, "lemonChiffon", 2),
                     Option("Peach", 250, 550, 50, "peachPuff", 2)]
    app.toppingList = [Option("Cinnamon Sugar", 950, 300, 50, "tan", 1),
                       Option("Crushed Pistachios", 950, 425, 50, "darkSeaGreen", 1),
                       Option("Shaved Chocolate", 950, 550, 50, "saddleBrown", 1),
                       Option("Toasted Coconut", 1100, 300, 50, "wheat", 2),
                       Option("Mini Mallows", 1100, 425, 50, "white", 2),
                       Option("Rainbow Sprinkles", 1100, 550, 50, "plum", 2)]

    #Cups
    app.cup1 = Cup(600, 550, 1, "white", "none")
    app.cup2 = Cup(600, 550, 2, "white", "none")
    app.cup3 = Cup(600, 550, 3, "white", "none")
    app.cup1CanMove = True
    app.cup2CanMove = True
    app.cup3CanMove = True

    #Orders
    app.order1 = None
    app.order2 = None
    app.order3 = None
    app.buildCounter = 0
    app.brewCounter = 0
    app.showOrder2 = False
    app.showOrder3 = False
    app.completed = 0

    #Coffee Machines
    app.machine1 = CoffeeMachine(75, 200, 1)
    app.machine2 = CoffeeMachine(450, 200, 2)
    app.machine3 = CoffeeMachine(825, 200, 3)
    app.brew1 = False
    app.brew2 = False
    app.brew3 = False
    app.counterBrew1 = 0
    app.counterBrew2 = 0
    app.counterBrew3 = 0
    app.brewDone1 = False
    app.brewDone2 = False
    app.brewDone3 = False

    #Whipped Cream
    app.creamLocations = [ ]
    app.creamX = None
    app.creamY = None
    app.dragging = False
    app.hit = 0

    #Toppings
    app.toppingLocations = [ ]
    app.toppingX = None
    app.toppingY = None

    #Accuracy of whipped cream
    app.slopeLeft = (200-450) / (575-475)
    app.slopeRight = (200-450) / (625-725)
    app.intersect = False

################################################################################

def home_redrawAll(app):
    #Background and title
    drawRect(0, 0, 1200, 800, fill="burlyWood")
    drawLabel("Capy's Coffee", app.width/2, 140, size=80, fill="saddleBrown")
    #Buttons
    app.instrucBut.drawBackground()
    app.instrucBut.drawText()
    app.startBut.drawBackground()
    app.startBut.drawText()
    #Coffee image
    app.cuteCoffeeImage.drawPic()

def home_onMousePress(app, mouseX, mouseY):
    #Buttons
    app.instrucBut.doAction(mouseX, mouseY)
    app.startBut.doAction(mouseX, mouseY)
        
################################################################################

def instructions_redrawAll(app):
    #Background and title
    drawRect(0, 0, 1200, 800, fill="bisque")
    drawLabel("Instructions", app.width/2, 140, size=80, fill="sienna")
    #Back button
    app.backBut.drawBackground()
    app.backBut.drawText()
    #Instructions
    first = "1. Accept the order from the customer"
    second = "2. Progress through different stations"
    third = "3. Select correct items based on their order"
    fourth = "4. Put the cup at the correct coffee station"
    fifth = "5. Draw the cream on top of the cup"
    sixth = "6. Sprinkle your toppings after by clicking around the cream"
    seventh = "7. Complete multiple orders at a time using arrow keys"
    eighth = "8. When all orders are completed, you're done!"
    instrucList = [first, second, third, fourth, fifth, sixth, seventh, eighth]
    for i in range(len(instrucList)):
        drawLabel(instrucList[i], 600, 250 + 50*i, size=30, align="center",
                  fill="sienna")

def instructions_onMousePress(app, mouseX, mouseY):
    #Button
    app.backBut.doAction(mouseX, mouseY)

################################################################################

def startGame_redrawAll(app):
    drawRect(0, 0, 1200, 800, fill="rosyBrown")
    #Capybara behind counter
    app.capybaraImage.drawPic()
    #Counter
    drawRect(875, 600, 200, 100, fill='wheat')
    drawLine(875, 600, 1075, 600, lineWidth=5, fill='saddleBrown')
    #Door
    drawRect(50, 300, 225, 400, fill='saddleBrown')
    drawCircle(225, 525, 10, fill='wheat')

    #Animal coming through door
    if app.counterStart > 15:
        app.animal.drawPic()
        #Animal stops at counter
        if app.animal.x == 750:
            #Take order in speech bubble
            app.speechBubble.drawPic()
            app.orderBut.drawBackground()
            app.orderBut.drawText()

def startGame_onMousePress(app, mouseX, mouseY):
    #When animal reaches counter
    if app.animal.x == 750: 
        if app.orderBut.doAction(mouseX, mouseY): #If button pressed
            app.order1 = Orders(1) #First order is made
       
def startGame_onStep(app):
    app.counterStart += 1
    if app.counterStart > 25:
        #Animal comes through the door and walks to counter
        app.animal.moveToCounter()
        if app.animal.x >= 750:
            app.animal.x = 750 #Animal stops at counter

################################################################################

def order_redrawAll(app):
    drawRect(0, 0, 1200, 800, fill="burlyWood")
    #Orders
    drawRect(75, 100, 300, 600, fill="blanchedAlmond")
    drawLabel("Order #1", 225, 150, size=40, fill="sienna")
    drawRect(450, 100, 300, 600, fill="blanchedAlmond")
    drawLabel("Order #2", 600, 150, size=40, fill="sienna")
    drawRect(825, 100, 300, 600, fill="blanchedAlmond")
    drawLabel("Order #3", 975, 150, size=40, fill="sienna")
    #Make buttons
    app.makeBut1.drawBackground()
    app.makeBut1.drawText()
    app.makeBut2.drawBackground()
    app.makeBut2.drawText()
    app.makeBut3.drawBackground()
    app.makeBut3.drawText()
    #Details of orders
    if app.order1 != None:
        app.order1.display()
    if app.order2 != None:
        app.order2.display()
    if app.order3 != None:
        app.order3.display()

def order_onMousePress(app, mouseX, mouseY):
    if app.order1 != None: #button works if there is an order
        if app.makeBut1.doAction(mouseX, mouseY):
            app.startTime1 = time.time() #timer starts
            app.cup1.screen = "build" #cup is created on next screen
    if app.order2 != None:
        if app.makeBut2.doAction(mouseX, mouseY):
            app.startTime2 = time.time()
            app.cup2.screen = "build"
            app.cup2.x = 600 #draws cup in correct location
            app.cup2.y = 550
    if app.order3 != None:
        if app.makeBut3.doAction(mouseX, mouseY):
            app.startTime3 = time.time()
            app.cup3.screen = "build"
            app.cup3.x = 600
            app.cup3.y = 550

def order_onKeyPress(app, key):
    if key == "right": #can switch to different station screen
        setActiveScreen("build")

################################################################################

def build_redrawAll(app):
    drawRect(0, 0, 1200, 800, fill="rosyBrown")
    drawRect(0, 700, 1200, 800, fill="brown")
    #Options display
    drawRect(75, 200, 300, 500, fill="maroon")
    for i in range(4):
        height = 200 + 167*i
        drawLine(75, height, 375, height, fill="black", lineWidth=4)
    drawLine(75, 200, 75, 700, fill="black", lineWidth=4)
    drawLine(375, 200, 375, 700, fill="black", lineWidth=4)
    #Labels
    titleList = ["Milks", "Espresso", "Syrups"]
    for i in range(len(titleList)):
        title = titleList[i]
        centerY = 220 + 167*i
        drawLabel(title, 225, centerY, fill="sandyBrown", size=25)
    #Options
    for option in app.milkList:
        option.drawOption()
        if option.selected:
            drawLabel(option.name, 225, 330+167*(option.row-1), size=20,
                      fill="white")
    for option in app.espressoList:
        option.drawOption()
        if option.selected:
            drawLabel(option.name, 225, 330+167*(option.row-1), size=20,
                      fill="white")
    for option in app.syrupList:
        option.drawOption()
        if option.selected:
            drawLabel(option.name, 225, 330+167*(option.row-1), size=20,
                      fill="white")
    #Images within the options
    app.cowImage.drawPic()
    app.strawberryMilk.drawPic()
    app.chocolateMilk.drawPic()
    app.blueberryImage.drawPic()
    app.cityImage.drawPic()
    app.decafImage.drawPic()
    app.frenchImage.drawPic()
    app.newEnglandImage.drawPic()
    app.chocolateSyrup.drawPic()
    app.caramelImage.drawPic()
    app.cinnamonImage.drawPic()
    app.marshmallowImage.drawPic()

    #Finished
    drawLabel("Drag here when done!", 1000, 275, size=30, fill="saddleBrown", bold=True)
    drawLine(1000, 300, 1000, 350, arrowEnd=True, fill="saddleBrown")
    drawRect(1000, 675, 250, 50, align="center")
    drawOval(1000, 650, 250, 50, fill="gray")
    #Cup
    drawRect(600, 675, 250, 50, align="center")
    drawOval(600, 650, 250, 50, fill="gray")
    #View the orders
    drawLabel("Click to view orders:", 225, 50, size=30, fill="saddlebrown", bold=True)
    app.order1But.drawBackground()
    app.order1But.drawText()
    if app.order1But.showOrder:
        if app.order1 != None:
            app.order1.viewOrder()
    app.order2But.drawBackground()
    app.order2But.drawText()
    if app.order2But.showOrder:
        if app.order2 != None:
            app.order2.viewOrder()
    app.order3But.drawBackground()
    app.order3But.drawText()
    if app.order3But.showOrder:
        if app.order3 != None:
            app.order3.viewOrder()
    
    #Makes sure that the order is accurate
    currentMilk = None
    for milk in app.milkList:
        if milk.selected:
            currentMilk = milk.name
    currentEspresso = None
    for espresso in app.espressoList:
        if espresso.selected:
            currentEspresso = espresso.name
    currentSyrup = None
    syrupColor = None
    for syrup in app.syrupList:
        if syrup.selected:
            currentSyrup = syrup.name
            syrupColor = syrup.color
    #Changes the color of the cup to the syrup color if all three options are the order
    if currentMilk != None and currentEspresso != None and currentSyrup != None:
        if app.order1 != None:
            if (currentMilk == app.order1.milk and currentEspresso == app.order1.espresso
                and currentSyrup == app.order1.syrup):
                app.cup1.color = syrupColor
        if app.order2 != None:
            if (currentMilk == app.order2.milk and currentEspresso == app.order2.espresso
                and currentSyrup == app.order2.syrup):
                app.cup2.color = syrupColor
        if app.order3 != None:
            if (currentMilk == app.order3.milk and currentEspresso == app.order3.espresso
                and currentSyrup == app.order3.syrup):
                app.cup3.color = syrupColor

    #Cups are on the build screen
    if app.cup1.screen == "build":
        app.cup1.drawCup()
    if app.cup2.screen == "build":
        app.cup2.drawCup()
    if app.cup3.screen == "build":
        app.cup3.drawCup()
    #Shows the next button if the order is completed and in the correct place
    if app.cup1.isDone():
        app.nextBut.drawBackground()
        app.nextBut.drawText()
    if app.cup2.isDone():
        app.nextBut.drawBackground()
        app.nextBut.drawText()
    if app.cup3.isDone():
        app.nextBut.drawBackground()
        app.nextBut.drawText()

    #New order notification
    if app.showOrder2:
        drawRect(850, 25, 300, 100, fill="maroon")
        drawLabel("New Order!", 1000, 75, fill="chocolate", size=30, bold=True)

def build_onMousePress(app, mouseX, mouseY):
    #No two options can be clicked at the same time
    noRepeats(mouseX, mouseY, app.milkList)
    noRepeats(mouseX, mouseY, app.espressoList)
    noRepeats(mouseX, mouseY, app.syrupList)

    #View order on current screen
    app.order1But.view(mouseX, mouseY)
    app.order2But.view(mouseX, mouseY)
    app.order3But.view(mouseX, mouseY)

    #Creates new orders when first step is complete
    if app.cup1.isDone():
        app.nextBut.doAction(mouseX, mouseY)
        app.order2 = Orders(2)
    if app.cup2.isDone():
        app.nextBut.doAction(mouseX, mouseY)
        app.order3 = Orders(3)
    if app.cup3.isDone():
        app.nextBut.doAction(mouseX, mouseY)

def build_onMouseDrag(app, mouseX, mouseY):
    #Can move cup to finished area
    if mouseX >= 450 and app.cup1CanMove:
        app.cup1.moving(mouseX, mouseY)
    if mouseX >= 450 and app.cup2CanMove:
        app.cup2.moving(mouseX, mouseY)
    if mouseX >= 450 and app.cup3CanMove:
        app.cup3.moving(mouseX, mouseY)

def build_onKeyPress(app, key):
    if key == "left":
        setActiveScreen("order")
    if key == "right":
        setActiveScreen("brew")

def build_onStep(app):
    #Timing of new order notification
    app.buildCounter += 1
    if app.buildCounter > 50:
        app.showOrder2 = True
    if app.buildCounter > 100:
        app.showOrder2 = False

################################################################################

def brew_redrawAll(app):
    drawRect(0, 0, 1200, 800, fill="rosyBrown")
    drawRect(0, 700, 1200, 800, fill="brown")
    #Coffee machines
    app.machine1.drawMachine()
    app.machine2.drawMachine()
    app.machine3.drawMachine()

    #Instructions
    first = "Click and hold to"
    second = "get cup to drag:"
    message = [first, second]
    for i in range(len(message)):
        drawLabel(message[i], 225, 60+50*i, size=30, fill="saddlebrown", bold=True)

    #Buttons
    app.cup1But.drawBackground()
    app.cup1But.drawText()
    app.cup2But.drawBackground()
    app.cup2But.drawText()
    app.cup3But.drawBackground()
    app.cup3But.drawText()

    #Coffee drip
    if app.brew1:
        app.machine1.brew()
    if app.brew2:
        app.machine2.brew()
    if app.brew3:
        app.machine3.brew()

    #Cups
    if app.cup1.screen == "brew":
        app.cup1.drawCup()
    if app.cup2.screen == "brew":
        app.cup2.drawCup()
    if app.cup3.screen == "brew":
        app.cup3.drawCup()

    #Brew button appears when done brewing
    if app.brewDone1:
        app.brewBut1.drawBackground()
        app.brewBut1.drawText()
    if app.brewDone2:
        app.brewBut2.drawBackground()
        app.brewBut2.drawText()
    if app.brewDone3:
        app.brewBut3.drawBackground()
        app.brewBut3.drawText()

    #New order notification
    if app.showOrder3:
        drawRect(850, 25, 300, 100, fill="maroon")
        drawLabel("New Order!", 1000, 75, fill="chocolate", size=30, bold=True)

def brew_onMousePress(app, mouseX, mouseY):
    #Goes to next station when completed
    if app.brewDone1:
        if app.brewBut1.doAction(mouseX, mouseY):
            app.cup1.screen = "toppings"
    if app.brewDone2:
        if app.brewBut2.doAction(mouseX, mouseY):
            app.cup2.screen = "toppings"
    if app.brewDone3:
        if app.brewBut3.doAction(mouseX, mouseY):
            app.cup3.screen = "toppings"

def brew_onMouseDrag(app, mouseX, mouseY):
    #Cup comes onto screen when inside top buttons
    if app.cup1But.isInside(mouseX, mouseY) and app.cup1 != None:
        app.cup1.screen = "brew"
    if app.cup1CanMove: #Cup follows mouse to coffee station
        app.cup1.x = mouseX
        app.cup1.y = mouseY
    if app.cup2But.isInside(mouseX, mouseY) and app.cup2 != None:
        app.cup2.screen = "brew"
    if app.cup2CanMove:
        app.cup2.x = mouseX
        app.cup2.y = mouseY
    if app.cup3But.isInside(mouseX, mouseY) and app.cup3 != None:
        app.cup3.screen = "brew"
    if app.cup3CanMove:
        app.cup3.x = mouseX
        app.cup3.y = mouseY

def brew_onMouseRelease(app, mouseX, mouseY):
    if 75 <= mouseX <= 375 and 330 <= mouseY <= 650:
        app.brew1 = True #Brewing starts when cup is at station
        app.cup1CanMove = False #Cup can no longer be moved when brewing
    if 450 <= mouseX <= 750 and 330 <= mouseY <= 650:
        app.brew2 = True
        app.cup2CanMove = False
    if 825 <= mouseX <= 1125 and 425 <= mouseY <= 650:
        app.brew3 = True
        app.cup3CanMove = False

def brew_onKeyPress(app, key):
    if key == "left":
        setActiveScreen("build")
    elif key == "right":
        setActiveScreen("toppings")

def brew_onStep(app):
    #Timing for coffee drips
    if app.brew1:
        app.counterBrew1 += 1
        if app.counterBrew1 % 200 == 0:
            app.brew1 = False
            app.brewDone1 = True
            app.counterBrew1 = 0
    if app.brew2:
        app.counterBrew2 += 1
        if app.counterBrew2 % 200 == 0:
            app.brew2 = False
            app.brewDone2 = True
            app.counterBrew2 = 0
    if app.brew3:
        app.counterBrew3 += 1
        if app.counterBrew3 % 200 == 0:
            app.brew3 = False
            app.brewDone3 = True
            app.counterBrew3 = 0

    #Timing for new order notification
    app.brewCounter += 1
    if app.brewCounter > 100:
        app.showOrder3 = True
    if app.brewCounter > 150:
        app.showOrder3 = False

################################################################################

def toppings_redrawAll(app):
    drawRect(0, 0, 1200, 800, fill="rosyBrown")
    drawRect(0, 700, 1200, 800, fill="brown")

    drawRect(600, 675, 250, 50, align="center")
    drawOval(600, 650, 250, 50, fill="gray")

    app.finishedBut.drawBackground()
    app.finishedBut.drawText()

    #Options
    for option in app.creamList:
        option.drawOption()
        if option.selected:
            drawLabel(option.name, 175, 650, size=30, fill="black")
    for option in app.toppingList:
        option.drawOption()
        if option.selected:
            drawLabel(option.name, 1025, 650, size=30, fill="black")

    #Images inside the options
    app.whippedImage.drawPic()
    app.butterscotchImage.drawPic()
    app.strawberryCream.drawPic()
    app.chocolateCream.drawPic()
    app.lemonImage.drawPic()
    app.peachImage.drawPic()
    app.cinnamonSugar.drawPic()
    app.pistachioImage.drawPic()
    app.shavedChocolate.drawPic()
    app.coconutImage.drawPic()
    app.miniMallows.drawPic()
    app.rainbowSprinkles.drawPic()

    #View orders from current screen
    drawLabel("Click to view orders:", 225, 50, size=30, fill="saddlebrown", bold=True)
    app.order1But.drawBackground()
    app.order1But.drawText()
    if app.order1But.showOrder:
        if app.order1 != None:
            app.order1.viewOrder()
    app.order2But.drawBackground()
    app.order2But.drawText()
    if app.order2But.showOrder:
        if app.order2 != None:
            app.order2.viewOrder()
    app.order3But.drawBackground()
    app.order3But.drawText()
    if app.order3But.showOrder:
        if app.order3 != None:
            app.order3.viewOrder()

    #Cups
    if app.cup1.screen == "toppings":
        app.cup1.x = 600
        app.cup1.y = 550
        app.cup1.drawCup()
    if app.cup2.screen == "toppings":
        app.cup2.x = 600
        app.cup2.y = 550
        app.cup2.drawCup()
    if app.cup3.screen == "toppings":
        app.cup3.x = 600
        app.cup3.y = 550
        app.cup3.drawCup()

    #Invisible line that checks for accuracy of the whipped cream
    drawLine(475, 450, 575, 200, fill=None)
    drawLine(725, 450, 625, 200, fill=None)

    #Draws the whipped cream
    currentCream = None
    for cream in app.creamList:
        if cream.selected:
            currentCream = cream.color
    for (x, y) in app.creamLocations:
        drawCircle(x, y, 20, fill=currentCream)

    #Draws the toppings
    currentTop = None
    for topping in app.toppingList:
        if topping.selected:
            currentTop = topping.color
    for (x, y) in app.toppingLocations:
        drawCircle(x, y, 15, fill=currentTop)

def toppings_onMousePress(app, mouseX, mouseY):
    #No two options can be selected at the same time
    noRepeats(mouseX, mouseY, app.creamList)
    noRepeats(mouseX, mouseY, app.toppingList)

    #View orders
    app.order1But.view(mouseX, mouseY)
    app.order2But.view(mouseX, mouseY)
    app.order3But.view(mouseX, mouseY)

    #Toppings placed at mouse location on screen
    for topping in app.toppingList:
        if topping.selected:
            if 475 <= mouseX <= 725 and 150 <= mouseY <= 450:
                app.toppingX = mouseX
                app.toppingY = mouseY
                app.toppingLocations.append((app.toppingX, app.toppingY))

    #Order disappears when completed
    if app.finishedBut.isInside(mouseX, mouseY):
        app.completed += 1
        if app.completed == 1:
            app.endTime1 = time.time() #Ends timer
            app.creamLocations = [ ] #Resets cream
            app.toppingLocations = [ ] #Resets toppings
            app.cup1.screen = "none"
            app.order1 = None
        elif app.completed == 2:
            app.endTime2 = time.time()
            app.creamLocations = [ ]
            app.toppingLocations = [ ]
            app.cup2.screen = "none"
            app.order2 = None
        elif app.completed == 3:
            app.endTime3 = time.time()
            app.creamLocations = [ ]
            app.toppingLocations = [ ]
            app.cup3.screen = "none"
            app.order3 = None
            #When all three orders are completed, go to scores screen
            app.finishedBut.doAction(mouseX, mouseY)

def toppings_onMouseDrag(app, mouseX, mouseY):
    if 475 <= mouseX <= 725 and 150 <= mouseY <= 450:
        app.creamX = mouseX
        app.creamY = mouseY
        #Cream can be drawn on screen
        app.creamLocations.append((app.creamX, app.creamY))

    try:
        #Checks if whipped cream is out of bounds, slope matches line
        if (almostEqual((mouseY-450)/(mouseX-475), app.slopeLeft) or
            almostEqual((mouseY-450)/(mouseX-725), app.slopeRight)):
            app.hit += 1
    except: #divide by 0 error
        pass

def toppings_onKeyPress(app, key):
    if key == "left":
        setActiveScreen("brew")

################################################################################

def scores_redrawAll(app):
    drawRect(0, 0, 1200, 800, fill="rosyBrown")

    #Calculates the score for timing
    elapsed1 = app.endTime1 - app.startTime1
    elapsed2 = app.endTime2 - app.startTime2
    elapsed3 = app.endTime3 - app.startTime3
    elapsedTotal = (elapsed1 + elapsed2 + elapsed3) / 3

    #Score to see if order was accurate with the selected options
    cupScore = 0
    if app.cup1.color == "white":
        cupScore += 5
    if app.cup2.color == "white":
        cupScore += 5
    if app.cup3.color == "white":
        cupScore += 5

    buildScore = 100 - elapsedTotal*0.1
    toppingScore = 100 - app.hit*5 #Accuracy of the whipped cream
    score = str((buildScore + toppingScore) / 2 - cupScore) #Total score
    newScore = score[:5] #Shortens float

    drawLabel(f"Score: {newScore}", 600, 200, size=50, fill="saddleBrown",
              bold=True)

    #User passed or failed depending on their score
    if int(newScore[:2]) >= 70:
        message = "You won!"
        color = "green"
    else:
        message = "You lost!"
        color = "fireBrick"
    drawLabel(message, 600, 400, size=40, fill=color)

    #Can choose to play again
    app.playAgainBut.drawBackground()
    app.playAgainBut.drawText()

def scores_onMousePress(app, mouseX, mouseY):
    if app.playAgainBut.isInside(mouseX, mouseY):
        restartApp(app) #Game is restarted
        app.playAgainBut.doAction(mouseX, mouseY)

################################################################################

def main():
    runAppWithScreens("home", 1200, 800)

main()
import os,game as main
class Colours:#static class to make code more readable, will not be used to make objects
    os.system("")#Required in order for ANSI escape codes to be used (allows for colours)
    red = "\033[91m"
    blue = "\033[96m"
    green = "\033[92m"
    white = "\033[97m"
    black = "\033[30m"
    special = ("\033[38;2;255;27;141m","\033[38;2;255;218;0m","\033[38;2;27;179;255m")


    
def display(game):#Display command for console
    if os.name == "nt":
        clearCommand = "cls"
    elif os.name == "posix":
        clearCommand = "clear"
    else:#if os.name is not nt (Windows), or posix (Linux), then this code does not support it
        print("Sorry, your os isn't supported, press enter to exit")
        input()
        exit()
    if game.settings["magnetic"] == False:#Each disk height will be twice as tall if magnetic
        screenHeight = game.settings["disks"]+2
    else:
        screenHeight = game.settings["disks"]*2+2
    pinWidth = game.settings["disks"]*2+3
    pinHeight = screenHeight
    screenWidth = 1+(pinWidth+2)*3
    
    screen = []#Sets up a screen to draw the pins and disks on
    for col in range(screenWidth):
        screen.append([])
        for row in range(screenHeight):
            screen[-1].append(Colours.black)

    for i in range(3):
        xLoc = 1+((pinWidth+2)*i)+(pinWidth-1)//2
        for j in range(pinHeight):#Draw centre bar
            yLoc = j
            screen[xLoc][yLoc] = Colours.white
        
        yLoc = -1
        for j in range(pinWidth):#Draw bottom of pin
            xLoc = 1+i*(pinWidth+2)+j
            screen[xLoc][yLoc] = Colours.white
        
            
    xLoc = 1+((pinWidth+2)*game.destination)+(pinWidth-1)//2
    yLoc = 0
    screen[xLoc][yLoc]=Colours.green
    
    if game.settings["magnetic"] == False:
        for i in range(3):
            pin = game.pins[i]
            for j in range(len(pin.disks)):
                disk = pin.disks[j]
                diskWidth = disk.size*2-1
                yPos = -2-j
                startX = game.settings["disks"]-disk.size+(i*(pinWidth+2))+2
                for k in range(diskWidth+2):
                    xPos = startX+k
                    screen[xPos][yPos] = Colours.special[(disk.size-1)%3]
        
    else:
        for i in range(3):
            pin = game.pins[i]
            for j in range(len(pin.disks)):
                disk = pin.disks[j]
                diskWidth = disk.size*2+1
                yPos = -2-(j*2)
                startX = game.settings["disks"]-disk.size+(i*(pinWidth+2))+2
                for k in range(diskWidth):
                    xPos = startX+k
                    if disk.polarity == True:
                        screen[xPos][yPos] = Colours.red
                        screen[xPos][yPos-1] = Colours.blue
                    else:
                        screen[xPos][yPos] = Colours.blue
                        screen[xPos][yPos-1] = Colours.red


    #Must now change the 2D list into a string to be displayed
    string="\n"
    for y in range(screenHeight):
        for x in range(screenWidth):
            string+=screen[x][y]+"█"
        string+="\n"
    string+=Colours.white#Sets the colour back to white for typing
    os.system(clearCommand)
    print(string)

def forceInput(question,validInputs=("Y","N"),integer=False):
    while True:
        inp = input(question)
        if integer == True:
            if inp.isdigit():
                return int(inp)
            continue
        if inp in validInputs:
            return inp
def getSettings():
    if forceInput("Magnetic? (Y/N)\n") == "Y":
        magnetic=True
    else:
        magnetic = False
    cyclical = False
    adjacent = False
    if magnetic == False:
        if forceInput("Cyclical? (Y/N)\n") == "Y":
            cyclical = True
        else:
            if forceInput("Adjacent? (Y/N)\n") == "Y":
                adjacent = True
            
    diskCount = forceInput("Disk count: ",integer=True)
    settings = dict()
    settings["disks"] = diskCount
    settings["magnetic"] = magnetic
    if cyclical:
        settings["valid"]=[[2],[3],[1]]
    elif adjacent:
        settings["valid"]=[[2],[1,3],[2]]
    else:
        settings["valid"]=[[2,3],[1,3],[2,3]]

    if not (magnetic or cyclical or adjacent):
        auto = forceInput("Automatic mode? (Y/N)\n")
        if auto == "Y":
            settings["auto"]=True
        else:
            settings["auto"]=False
    else:
        settings["auto"]=False
    unlimited = forceInput("Unlimited mode? (Y/N)\n")
    if unlimited == "Y":
        settings["unlimited"]=True
    else:
        settings["unlimited"]=False
    return settings



def getMove():
    pin,destination=0,0
    while pin==destination:
        pin = int(forceInput("Which pin do you want to move a disk from?\n",("1","2","3")))-1
        destination = int(forceInput("Where do you want to move it to?\n",("1","2","3")))-1
    return pin,destination

def win(game):
    print("You won in",game.count,"moves!\nPress enter to exit")
    input()

def play():
    #settings = {"valid":[[2,3],[1,3],[1,2]], "magnetic":False, "disks": 1, "auto": True, "unlimited":True}
    settings = getSettings()
    game = main.Game()
    game.settings = settings
    game.setup()
    game.display = display
    game.requestMove = getMove
    game.win=win
    game.play()

if __name__=="__main__":
    play()

import time
class Game:
    DEFAULT = {"Valid":[[2,3],[1,3],[1,2]],"disks":5,"magnetic":False,"unlimited":False,"auto":False}
    def __init__(self):
        self.settings = Game.DEFAULT
        self.display=Game.placeHolder
        self.requestMove = Game.placeHolder
        self.destination = 2
        self.count=0
        self.win=Game.placeHolder
    def setup(self):
        self.pins = [Pin(self,i) for i in range(3)]
        for i in range(self.settings["disks"]):
            if self.settings["magnetic"]!=True:
                self.pins[0].disks.append(Disk(self.settings["disks"]-i,self.pins[0]))
            else:
                self.pins[0].disks.append(MagneticDisk(self.settings["disks"]-i,self.pins[0],True))
    def tick(self):
        if self.settings["auto"]==False:
            move = self.requestMove()
            valid = self.validate(move)
        else:
            move = self.makeMove()
            valid=True
        if valid:
            self.pins[move[0]].disks[-1].move(move[1])
            self.count+=1
        
    def makeMove(self):
        start = 2-self.destination
        mid = 1
        modCount = self.count%3
        if modCount == 0:
            if self.settings["disks"]%2==0:
                move = (start,mid)
            else:
                move = (start,self.destination)
        if modCount == 1:
            if self.settings["disks"]%2==0:
                move = (start,self.destination)
            else:
                move = (start,mid)
        if modCount == 2:
                move = (self.destination,mid)
        if self.validate(move) == True:
            print(" ",move[0],">",move[1])
            time.sleep(0.1)
            return move
        else:
            print(" ",move[1],">",move[0])
            time.sleep(0.1)
            return (move[1],move[0])


    def validate(self,move):
        if len(self.pins[move[0]].disks)==0:
            return False
        if self.pins[move[0]].disks[-1].testMove(move[1]) == True:
            return True
        else:
            return False
    def play(self):
        swapped = False
        self.display(self)
        while True:
            self.tick()
            self.display(self)
            if self.done() == True:
                if self.settings["unlimited"]==False:
                    break
                else:
                    self.count=0
                    self.settings["disks"]+=1
                    if self.settings["magnetic"]==False:
                        self.pins[self.destination].disks.insert(0,Disk(self.settings["disks"],self.pins[self.destination]))
                    self.destination = 2-self.destination
                    self.display(self)
                    
                    
        self.win(self)
    def done(self):
        complete = True
        for i in range(3):
            if self.destination==i:
                continue
            if len(self.pins[i].disks) != 0:
                complete = False
                break
        return complete
    @staticmethod
    def placeHolder(): #Used as an empty function to prevent errors if game started without display
        pass
                    
class Pin:
    def __init__(self,game,num):
        self.disks = []
        self.game=game
        self.num=num
class Disk:
    def __init__(self,size,pin):
        self.size = size
        self.pin = pin
        if self.pin.game.settings["magnetic"] == True:
            self.polarity = True
    def testMove(self,pinNum):
        if len(self.pin.game.pins[pinNum].disks) == 0:
            return True
        if self.pin.game.pins[pinNum].disks[-1].size>self.size:
            return True
    def move(self,destination):
        self.pin.game.pins[destination].disks.append(self)
        del self.pin.disks[-1]
        self.pin = self.pin.game.pins[destination]
        if self.pin.game.settings["magnetic"]==True:
            self.polarity = not self.polarity
            
class MagneticDisk(Disk):#Polarity is positive, or negative.  Only two options so can be boolean
    def __init__(self,size,disk,polarity):
        self.polarity = polarity
        Disk.__init__(self,size,disk)
    def testMove(self,pinNum):
        if Disk.testMove(self,pinNum) == False:
            return False
        if len(self.pin.game.pins[pinNum].disks)==0:
            return True
        if self.pin.game.pins[pinNum].disks[-1].polarity != self.polarity:
            return True
        return False

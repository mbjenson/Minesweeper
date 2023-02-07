

# class which contains the tile object and some use functions pertaining to a tile which will
# appear on the minesweeper board.
class Tile:
    bomb = False
    flag = False
    Bombcount = 0
    x = 0
    y = 0
    flipped = False
    
    # constructor of Tile class
    def __init__(self, bomb, flag, x, y):
        self.bomb = bomb
        self.flag = flag
        self.x = x
        self.y = y
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def isBomb(self):
        return self.bomb
        
    def placeBomb(self):
        self.bomb = True
    
    def hasFlag(self):
        return self.flag
    
    def toggleFlag(self):
        self.flag = not self.flag
    
    def setCount(self, count):
        if self.bomb == False:
            self.Bombcount = count
            
    def getCount(self):
        return self.Bombcount
    
    def flipTile(self):
        self.flipped = True
    
    def isFlipped(self):
        return self.flipped

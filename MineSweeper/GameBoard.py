from tkinter import ttk
from tkinter import *
from Board import *

# Implement the Board class in an interactable interface.
class GameBoard:
    
    
    counter = 0
    win = False
    lose = False
    root = None
    buttons = []
    height = 0
    width = 0
    board = None
    flipCount = 0
    startingCords = None
    
    # creates a new board containing tiles and their asociated roles.
    def __init__(self, height, width, root, counter):
        self.counter = counter
        self.height = height
        self.width = width
        self.root = root
        self.board = Board(width, height)
        for y in range(height):
            self.buttons.append([])
            for x in range(width):
                if height <= 10:
                    b = ttk.Button(root, width=6)
                if height > 10 and height <= 18:
                    b = ttk.Button(root, width=4)
                if height > 18:
                    b = ttk.Button(root, width=4)
                self.buttons[y].append(b)
    
                
    # takes in an event and calculates which tile was interacted with and toggles the flag for that tile.
    def plantFlag(self, event):
        a = event.x_root - self.root.winfo_rootx()
        b = event.y_root - self.root.winfo_rooty()
        z = self.root.grid_location(a, b)
        x = z[0]
        y = z[1]
        if not self.board.board[y][x].isFlipped():
            if self.board.board[y][x].hasFlag():
                self.board.board[y][x].toggleFlag()
                self.buttons[y][x].config(text="")
                
            else:
                self.board.board[y][x].toggleFlag()
                self.buttons[y][x].config(text="F")
                
    # Takes a tile's coordinates and return the cords around that tile which are fair play.
    def getLegalCords(self, x, y):
        if y >= self.height or x >= self.width:
            pass
        else:
            indecies = [-1, 0, +1]
            legalCords = []
            for i in range(len(indecies)):
                for j in range(len(indecies)):
                    
                    tempY = y + indecies[i]
                    tempX = x + indecies[j]
                    if 0 <= tempY < self.height and 0 <= tempX < self.width:
                        if tempY != y or tempX != x:
                            legalCords.append([x+indecies[j],y+indecies[i]])
            
            return legalCords
    
    # takes a tile's coordinates and returns the number of bombs surrounding it.
    def display(self, x, y):
        return self.board.board[y][x].getCount()
    
    # checks the state of a tile, if the tile is flipped, it is disabled thus removing it from play.
    def check(self, x, y):
        if not self.board.board[y][x].isFlipped():
            
            if not self.board.board[y][x].isBomb():
                
                if not self.board.board[y][x].hasFlag():
                    
                    if self.board.board[y][x].getCount() < 1:
                    
                        self.board.board[y][x].flipTile()
                        self.buttons[y][x].config(state = DISABLED)
                        self.flipCount += 1 
                        
                        cords = self.getLegalCords(x, y)
                        for i in range(len(cords)):
                            self.check(cords[i][0], cords[i][1])
                        
                        
                    else:
                    
                        self.buttons[y][x].config(text=str(self.display(x, y)), state = DISABLED)
                        
                        self.board.board[y][x].flipTile()
                        self.flipCount += 1
                pass
            pass
        pass
    
    # recursively flips surrounding tiles that have a bomb count of zero
    def buildPath(self, curX, curY, forbadeCords, counter):
        
        trueLegal = []
        
        legal = self.getLegalCords(curX, curY)
        for i in range(len(legal)):
            if legal[i] in forbadeCords:
                continue
            else:
                trueLegal.append(legal[i])
        
        if len(trueLegal) != 0 and counter != 0:
            
            rand = random.choice(trueLegal)
            forbadeCords.append(rand)
            
            return self.buildPath(rand[0], rand[1], forbadeCords, counter-1)
        return forbadeCords
        
    # main algorithm used for building the starting area around the first click of the mouse.
    #       Implements a custom algorithm which steps randomly in each direction.
    #       Creates a very convincing minesweeper starting area.
    def createStartingArea(self):
        
        legal = self.getLegalCords(self.startingCords[0], self.startingCords[1])
        
        forbiddenCords = legal.copy()
        #add origin to forbidden cords
        forbiddenCords.append([self.startingCords[0],self.startingCords[1]])
        
        if len(legal) > 4:
            numExtraTiles = random.randint(2, 4)
        else:
            numExtraTiles = random.randint(2, len(legal))

        for i in range(numExtraTiles):
            counter = self.counter
            curTile = random.choice(legal)
            
            self.buildPath(curTile[0], curTile[1], forbiddenCords, counter)
        
        return forbiddenCords
        
    # function that flips all bombs once game ends
    def flipBombs(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.board.board[i][j].isBomb():
                    self.buttons[i][j].config(text = "(!)")
    
    # calculates mouse position from event param and 'flips' the tile being interacted with
    def flip(self, event):
        
        #get widget location
        a = event.x_root - self.root.winfo_rootx()
        b = event.y_root - self.root.winfo_rooty()
        z = self.root.grid_location(a, b)
        x = z[0]
        y = z[1]
        
        if self.flipCount == 0:
            self.startingCords = [z[0], z[1]]
            #then call createStartingArea that creates forbidden coordinates
            start = self.createStartingArea()
            #then call function that distributes bombs around the board and pass in the forbidden coordinates
            self.board.distributeBombs(start)
            #hopefully this should happen before the rest of the flip function takes place so that the starting area will be honored
            self.board.generateBombBoard()
            self.board.getBombCounts()
            # call the generate bomb board function to create the bomb board

        if not self.board.board[y][x].hasFlag():
            if self.board.board[y][x].isBomb():
                #display the bomb image
                #self.lose = True
                self.buttons[y][x].config(text = "{=}")
                self.lose = True
                self.checkState()
            else:
                self.check(x, y)
                
        if self.flipCount == self.board.numSafeTiles:
            self.win = True
            self.checkState()
            
    # main game loop update function
    def updateTkBoard(self):
        
        for y in range(self.height):
            for x in range(self.width):
                if self.height <= 10:
                    self.buttons[y][x].grid(column = x, row = y, ipady=10)
                if self.height > 10 and self.height <= 18:
                    self.buttons[y][x].grid(column = x, row = y, ipady=4.3)
                if 18 < self.height:
                    self.buttons[y][x].grid(column = x, row = y, ipady=4.3)
    
    # function that runs at game end to disable further play
    def disableAll(self):
        for i in range(self.height):
            for j in range(self.width):
                self.buttons[i][j].config(state = DISABLED)
    
    # Win condition check function
    def checkState(self):
        if self.win == True:
            
            self.disableAll()
        if self.lose == True:
            
            self.flipBombs()
            self.disableAll()
    
# main minesweeper game function that runs the code
def main():
    
    w = Tk()
    w.resizable(False, False)
    w.title("minesweeper")
    
    game = ttk.Frame(w)
    game.grid()
    
    gameBoard1 = GameBoard(15, 15, game, 5)
    
    w.bind("<Button-3>", gameBoard1.plantFlag)
    w.bind("<1>", gameBoard1.flip)
    
    gameBoard1.updateTkBoard()
    
    w.mainloop()
    
if __name__ == "__main__":
    main()
    
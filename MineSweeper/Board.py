from Tile import *
import random


# This class allows the creation of an array of tiles aswell as assigning different roles to those tiles like: bomb, flag, etc.
class Board:
    
    bombCount = 0
    height = 0
    width = 0
    board = []
    bombBoard = []
    xIndecies = []
    yIndecies = []
    bombCounts = []
    flagBoard = []
    numTiles = 0
    numSafeTiles = 0
    flagCounts = 0
    
    # constructor for a minesweeper board
    #       arguments: width, height {ints} - determine board dimensions
    def __init__(self, width, height):
        self.height = height
        self.width = width
        for y in range(self.height):
            self.board.append([])
            for x in range(self.width):
                self.board[y].append(Tile(False, False, x, y))
        self.numTiles = self.height * self.width
        
    # generates the board that holds specifically the bombs in it.
    def generateBombBoard(self):
        for y in range(self.height):
            self.bombBoard.append([])
            for x in range(self.width):
                if self.board[y][x].isBomb():
                    self.bombBoard[y].append(1)
                else:
                    self.bombBoard[y].append(0)
    
    # calculates the number of surrounding bombs for each non-bomb tile
    def getBombCounts(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x].isBomb:
                    count = 0
                    cords = self.getSurroundingCords(x, y)
                    for i in range(len(cords)):
                        count += self.bombBoard[cords[i][1]][cords[i][0]]
                    self.board[y][x].setCount(count)
                    
    #gets the coordinates surrounding a given tile that are within the bounds of the current board.
    def getSurroundingCords(self, x, y):
        if y >= self.height or x >= self.width:
            print("Index out of range")
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

    # function used for debugging the board
    def printBoard(self):
        for i in range(self.height):
            print(str(self.board[i]))

    # function used for debugging the bomb distribution
    def printBombBoard(self):
        for i in range(self.height):
            print(str(self.bombBoard[i]))
    
    # generates a list of all possible coordinate pairs for the board
    def makeIndexList(self):
        for i in range(self.height):
            self.yIndecies.append(i)
        for i in range(self.width):
            self.xIndecies.append(i)
    
    
    # Distributes the appropriote number of bombs around the board in a classic minesweeper fasion
    #       Arguments: forbiddenCoordindates {list} - the list of coordinates allocated after generating 
    #                                                 the starting region after first click
    
    
    def distributeBombs(self, forbiddenCoordinates):
        
        self.makeIndexList()
        
        usedCords = []
        
        for j in range(len(forbiddenCoordinates)):
            usedCords.append(forbiddenCoordinates[j])
        
        # original = 0.208, was too few trying 0.25
        self.bombCount = round((self.height * self.width)*0.25)
        self.numSafeTiles = self.numTiles - self.bombCount
        i = 0
        while i < self.bombCount:
            yCord = random.choice(self.yIndecies)
            xCord = random.choice(self.xIndecies)
            if [xCord, yCord] in usedCords:
                continue
            else:
                self.board[yCord][xCord].placeBomb()
                usedCords.append([xCord, yCord])
                i+=1
                
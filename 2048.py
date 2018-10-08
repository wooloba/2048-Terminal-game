import random as rnd
import os
import sys
import getch

class Grid():
    def __init__(self, row=4, col=4, initial=2):
        self.row = row                              # number of rows in grid
        self.col = col                              # number of columns in grid
        self.initial = initial                      # number of initial cells filled
        self.score = 0

        self._grid = self.createGrid(row, col)    # creates the grid specified above

        self.emptiesSet = list(range(row * col))    # list of empty cells

        for _ in range(self.initial):               # assignation to two random cells
            self.assignRandCell(init=True)


    def createGrid(self, row, col):
        self._grid = []
        for i in range(0,row):
            self._grid.append([])
            for j in range(0,col):
                self._grid[i].append(0)
                
        return self._grid



    def setCell(self, cell, val):

        row = cell // 4
        col = cell%4
        self._grid[row][col] = val
        pass


    def getCell(self, cell):

        row = cell // 4
        col = cell % 4
        return self._grid[row][col]


    def assignRandCell(self, init=False):

        if len(self.emptiesSet):
            cell = rnd.sample(self.emptiesSet, 1)[0]
            if init:
                self.setCell(cell, 2)
            else:
                cdf = rnd.random()
                if cdf > 0.75:
                    self.setCell(cell, 4)
                else:
                    self.setCell(cell, 2)
            self.emptiesSet.remove(cell)


    def drawGrid(self):

        for i in range(self.row):
            line = '\t|'
            for j in range(self.col):
                if not self.getCell((i * self.row) + j):
                    line += ' '.center(5) + '|'
                else:
                    line += str(self.getCell((i * self.row) + j)).center(5) + '|'
            print(line)



    def updateEmptiesSet(self):

        index = 0
        empty = []
        for i in range(0,4):
            for j in range(0,4):
                if self._grid[i][j] == 0:
                    empty.append(index)
                index+=1

        self.emptiesSet = empty
        pass


    def collapsible(self):

        tempBoard = self._grid
        tempScore = self.score
        for i in range(0,4):
            for j in range(0,4):
                if self._grid[i][j] == 0:
                    return True
                if self.collapseLeft() or self.collapseDown():
                    self._grid = tempBoard
                    self.score = tempScore
                    return True
                else:
                    return False


    def collapseRow(self, lst):

        temp = []
        for i in range(0,4):
            if lst[i] != 0:
                temp.append(lst[i])

        for i in range(0,len(temp)-1):
            if temp[i] == temp[i+1]:
                temp[i]+=temp[i+1]
                self.score+=temp[i]
                temp.pop(i+1)
                temp.append(0)

        while len(temp)<4:
            temp.append(0)

        if temp == lst:
            return temp,False
        else:
            return temp,True



    def collapseLeft(self):

        change = False
        board = []
        for lst in self._grid:
            [temp,collapsed] = self.collapseRow(lst)
            if collapsed == True:
                change = True
            board.append(temp)

        self._grid = board
        return change


    def collapseRight(self):

        change = False
        board = []
        for lst in self._grid:
            lst = list(reversed(lst))
            [temp, collapsed] = self.collapseRow(lst)
            if collapsed == True:
                change = True
            board.append(list(reversed(temp)))

        self._grid = board
        return change


    def collapseUp(self):

        self._grid = [list(i) for i in zip(*self._grid)]
        change = False
        board = []
        for lst in self._grid:
            [temp, collapsed] = self.collapseRow(lst)
            if collapsed == True:
                change = True
            board.append(temp)

        self._grid = [list(i) for i in zip(*board)]
        return change


    def collapseDown(self):

        self._grid = [list(i) for i in zip(*self._grid)]
        change = False
        board = []
        for lst in self._grid:
            lst = list(reversed(lst))
            [temp, collapsed] = self.collapseRow(lst)
            if collapsed == True:
                change = True
            board.append(list(reversed(temp)))

        self._grid = [list(i) for i in zip(*board)]
        return change


class Game():
    def __init__(self, row=4, col=4, initial=2):

        self.game = Grid(row, col, initial)
        self.play()


    def printPrompt(self):

        if sys.platform == 'win32':
            os.system("cls")
        else:
            os.system("clear")

        print('Press "w", "a", "s", or "d" to move Up, Left, Down or Right respectively.')
        print('Enter "p" to quit.\n')
        self.game.drawGrid()
        print('\nScore: ' + str(self.game.score))


    def play(self):

        moves = {'w' : 'Up',
                 'a' : 'Left',
                 's' : 'Down',
                 'd' : 'Right'}

        stop = False
        collapsible = True

        while not stop and collapsible:
            self.printPrompt()
            print('\nEnter a move: ')
            key = getch.getch()

            while not key in list(moves.keys()) + ['p']:
                self.printPrompt()
                print('\nEnter a move: ')
                key = getch.getch()
                

            if key == 'p':
                stop = True
            else:
                move = getattr(self.game, 'collapse' + moves[key])
                collapsed = move()

                if collapsed:
                    self.game.updateEmptiesSet()
                    self.game.assignRandCell()

                collapsible = self.game.collapsible()

        if not collapsible:
            if sys.platform == 'win32':
                os.system("cls")
            else:
                os.system("clear")
            self.game.drawGrid()
            print('\nScore: ' + str(self.game.score))
            print('No more legal moves.')


def main():
    game = Game()
    
main()

import sys
import random

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

#defining values for each direction in the maze
N,S,E,W = 1,2,4,8

#defining macro to reverse directions
REVERSE = {E: W, W: E, N: S, S: N}

#GUI object for the app
class MazeMakerGUI(QWidget):

    def __init__(self):
        super(MazeMakerGUI, self).__init__()

        #initializing variables and setting recursion limit
        self.mazeHeight = 0
        self.mazeWidth = 0
        
        sys.setrecursionlimit(35 * 45)

        self.maze = list(list(0 for i in range(self.mazeWidth)) for j in range(self.mazeHeight))

        #initializing UI
        self.initUI()

    #drawing the GUI and maze
    def paintEvent(self, event):

        #initializing the painter and fonts
        qp = QPainter()
        qp.begin(gui)
        pen = QPen(Qt.black, 3, Qt.SolidLine)
        qp.setPen(pen)
        qp.setFont(QFont('Decorative', 22))
        
        qp.drawText(868, 86, "x")

        #drawing the box around the maze output
        qp.drawLine(55, 615, 55, 55)
        qp.drawLine(780, 615, 780, 55)
        qp.drawLine(55, 53, 780, 53)
        qp.drawLine(55, 615, 780, 615)


        #drawing the maze
        drawWidth = 80
        drawHeight = 70
        #drawing the top line
        for i in range(self.mazeWidth):
            qp.drawLine(drawWidth,drawHeight,drawWidth + 15,drawHeight)
            drawWidth += 15
        #drawing the rest of the maze
        for j in range(self.mazeHeight):
            drawWidth = 80
            drawHeight += 15
            #drawing the left wall of the maze
            if j != 0:
                qp.drawLine(drawWidth, drawHeight, drawWidth, drawHeight - 15)
            for i in range(self.mazeWidth ):
                #leave gap if there is no wall to the south else draw south most wall 
                if self.maze[j][i] & S != 0:
                    drawWidth += 15
                else:
                    qp.drawLine(drawWidth,drawHeight,drawWidth + 15,drawHeight)
                    drawWidth += 15
                #don't do anything if at the west most wall
                if self.maze[j][i] & E != 0 and i + 1 < self.mazeWidth:
                    if (self.maze[j][i] | self.maze[j][i+1]) & S == 0:
                        drawWidth += 0
                #don't draw to the west if at exit
                elif (i == self.mazeWidth-1) & (j == self.mazeHeight-1):
                    drawWidth += 15
                #draw wall to the west
                else:
                    qp.drawLine(drawWidth, drawHeight, drawWidth, drawHeight - 15)

        qp.end()
        

    #generating the UI
    def initUI(self):

        #initializing app window
        self.setGeometry(30, 30, 980, 670)
        self.setWindowTitle('Maze Maker')

        #initializing boxes for maze size input
        self.boxWidth = QLineEdit(self)
        self.boxWidth.move(830, 70)
        self.boxWidth.resize(30,20)

        self.boxHeight = QLineEdit(self)
        self.boxHeight.move(890, 70)
        self.boxHeight.resize(30,20)

        #initializing button for maze generation
        self.generateButton = QPushButton('Generate maze with RecB', self)
        self.generateButton.move(817,100)

        self.generateButton1 = QPushButton('Generate maze with HnK', self)
        self.generateButton1.move(819,130)

        self.generateButton.clicked.connect(self.on_click)
        self.generateButton1.clicked.connect(self.on_click1)

        #drawing all the UI components
        self.show()

    def on_click(self):
        #checking input
        inputWidth = self.boxWidth.text()
        inputHeight = self.boxHeight.text()
        
        try:
            self.mazeWidth = int(inputWidth)
            self.mazeHeight = int(inputHeight)
        except:
            QMessageBox.about(self, 'Error','Maze size input can only be a number')
            return
            pass

        if (self.mazeWidth > 45 or self.mazeHeight > 35):
            QMessageBox.about(self, 'Error','Maze size has to be less than 45 x 35')
            return

        if (self.mazeWidth < 3 and self.mazeHeight < 3):
            QMessageBox.about(self, 'Error','Maze size has to be more than 2 x 3 or 3 x 2')
            return

        #generating bidimensional array for the maze and building it
        self.maze = list(list(0 for i in range(self.mazeWidth)) for j in range(self.mazeHeight))
        self.buildMazeRecBack(0, 0)

        #updating the screen
        self.update()

    def on_click1(self):
        #checking input
        inputWidth = self.boxWidth.text()
        inputHeight = self.boxHeight.text()
        
        try:
            self.mazeWidth = int(inputWidth)
            self.mazeHeight = int(inputHeight)
        except:
            QMessageBox.about(self, 'Error','Maze size input can only be a number')
            return
            pass

        if (self.mazeWidth > 45 or self.mazeHeight > 35):
            QMessageBox.about(self, 'Error','Maze size has to be less than 45 x 35')
            return

        if (self.mazeWidth < 3 and self.mazeHeight < 3):
            QMessageBox.about(self, 'Error','Maze size has to be more than 2 x 3 or 3 x 2')
            return

        #generating bidimensional array for the maze and building it
        self.maze = list(list(0 for i in range(self.mazeWidth)) for j in range(self.mazeHeight))

        #Hunt and kill driver code
        y = 0
        x = 0
        while x != -1:
            started = 1
            while 1:
                try: 
                    y, x = self.walk(y,x, started)
                    started = 0
                except:
                    break
            x, y = self.hunt()

        #updating the screen
        self.update()

    #Recursive backtracking algorithm
    def buildMazeRecBack(self, originX, originY):
        #generate rendom list of all 4 directions
        directions = random.sample([N,S,E,W], 4)

        #loop through the list
        for direction in directions:
            #convert direction into maze coordinates
            if direction == S:
                nextX, nextY = originX, originY + 1
            elif direction == N:
                nextX, nextY = originX, originY -  1
            elif direction == E:
                nextX, nextY = originX + 1, originY
            else:
                nextX, nextY = originX - 1, originY

            #check if there is a cell to go to and break the wall there
            if nextY in range(self.mazeHeight) and\
                (nextX in range(self.mazeWidth)) and\
                self.maze[nextY][nextX] == 0:
                self.maze[originY][originX] |= direction
                self.maze[nextY][nextX] |= REVERSE[direction]
                #do that recursively
                self.buildMazeRecBack(nextX, nextY)

    #Walk routine for Hunt and Kill
    def walk(self, originX, originY, started):
        #generate rendom list of all 4 directions
        directions = random.sample([N,S,E,W], 4)

        #if first call after a hunt routine connect the maze to a random visited cell nearby
        if started == 1:
            for direction in directions:
                #convert direction into maze coordinates
                if direction == S:
                    nextX, nextY = originX, originY + 1
                elif direction == N:
                    nextX, nextY = originX, originY -  1
                elif direction == E:
                    nextX, nextY = originX + 1, originY
                else:
                    nextX, nextY = originX - 1, originY

                if nextY in range(self.mazeHeight) and\
                    nextX in range(self.mazeWidth) and self.maze[nextY][nextX] != 0:
                    self.maze[originY][originX] |= direction
                    self.maze[nextY][nextX] |= REVERSE[direction]
                    break
        
        #go to a random unvisited cell and return its coordinates        
        for direction in directions:
            #convert direction into maze coordinates
            if direction == S:
                nextX, nextY = originX, originY + 1
            elif direction == N:
                nextX, nextY = originX, originY -  1
            elif direction == E:
                nextX, nextY = originX + 1, originY
            else:
                nextX, nextY = originX - 1, originY
                
            if nextY in range(self.mazeHeight) and\
                nextX in range(self.mazeWidth) and self.maze[nextY][nextX] == 0:
                self.maze[originY][originX] |= direction
                self.maze[nextY][nextX] |= REVERSE[direction]
                return nextX, nextY

    #Hunt routine for Hunt and Kill
    def hunt(self):
        #iterate through the maze and return an unvisited cell
        for i in range(self.mazeHeight):
            for j in range(self.mazeWidth):
                if self.maze[i][j] == 0:
                    return i, j
        # return -1, -1 if all cell are visited
        return -1, -1


    #Utilitarian blocks to print maze values and draw the maze in the terminal
    def printMaze(self):
        for i in range(self.mazeHeight):
            print ('\n')
            for j in range(self.mazeWidth):
                print(self.maze[i][j], end=' ')
        print('\n')

    def draw(self):
        print("_" * (self.mazeWidth * 2))
        for j in range(self.mazeHeight):
            if j!=0:
                print("|", end='')
            else:
                print ("_", end='')
            for i in range(self.mazeWidth):
                if (self.maze[j][i] & S != 0):
                    print(" ", end='')
                else:
                    print("_", end='')
                if self.maze[j][i] & E != 0 and i + 1 < self.mazeWidth:
                    if ((self.maze[j][i] | self.maze[j][i+1]) & S != 0):
                        print(" ", end='')
                    else:
                        print("_", end='')
                elif (i==self.mazeWidth-1) & (j==self.mazeHeight-1):
                    print("_", end='')
                else:
                    print("|", end='')
            print("")

#Create App and GUI Objects and connect to the system
app = QApplication(sys.argv)
gui = MazeMakerGUI()
sys.exit(app.exec_())

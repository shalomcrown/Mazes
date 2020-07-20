#!/usr/bin/python3
'''
Author: Shalom Crown
Licence: GPL3
'''

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, \
    QVBoxLayout, QLabel, QHBoxLayout, QFrame, QLineEdit, QSizePolicy, QCheckBox

from PyQt5.QtCore import QObject, Qt, pyqtSignal, QSize
from PyQt5.QtGui import QPainter, QFont, QColor, QPen

import random
import time
import threading

class Cell:
    EAST = 0
    SOUTH = 1
    WEST = 2
    NORTH = 3
    
    RELATIONSHIP = {EAST : (0, 1), SOUTH : (1, 0), WEST : (0, -1), NORTH : (-1, 0)}

    def __init__(self, row, col):
        self.walls = [True] * 4
        self.wallsTraversed = [False] * 4
        self.visited = False
        self.row = row
        self.col = col

    
class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.initialize()

    def initialize(self):
        self.cells = [[Cell(row, col) for col in range(self.width)] for row in range(self.height)]

    def removeMarks(self):
        for row in self.cells:
            for cell in row:
                cell.wallsTraversed = [False] * 4
                cell.visited = False

    def getNeighbours(self, currentCell):
        neighbours = []
        if currentCell.col > 0:
            neighbours.append(self.cells[currentCell.row][currentCell.col - 1])
        if currentCell.col < self.width - 1:
            neighbours.append(self.cells[currentCell.row][currentCell.col + 1])
        if currentCell.row > 0:
            neighbours.append(self.cells[currentCell.row - 1][currentCell.col])
        if currentCell.row < self.height - 1:
            neighbours.append(self.cells[currentCell.row + 1][currentCell.col])
        return neighbours


    def getNonEdgeCells(self):
        return [row[1:-1] for row in self.cells[1:-1]]
    
    def getNeighbour(self, cell, relationship):
        rowInc, colInc = Cell.RELATIONSHIP[relationship]
        return self.cells[cell.row + rowInc][cell.col + colInc]
    
    
    def removeCommonWall(self, cellA, cellB):
        if cellA.col == cellB.col:
            if cellA.row < cellB.row:
                cellA.walls[Cell.SOUTH] = False
                cellB.walls[Cell.NORTH] = False
            else:
                cellA.walls[Cell.NORTH] = False
                cellB.walls[Cell.SOUTH] = False
        else:
            if cellA.col < cellB.col:
                cellA.walls[Cell.EAST] = False
                cellB.walls[Cell.WEST] = False
            else:
                cellA.walls[Cell.WEST] = False
                cellB.walls[Cell.EAST] = False        
    
    
    def removeWall(self, cell, wall):
        self.removeCommonWall(cell, self.getNeighbour(cell, wall))


    def randomizeBacktracker(self, start = (0,0), entrance=Cell.WEST, finish=None, exit=Cell.EAST, callback = None, loops = 0, finished = None):
        stack = []
        currentCell = self.cells[start[0]][start[1]]
        currentCell.walls[entrance] = False
        currentCell.visited = True
        stack.append(currentCell)

        if finish is None:
            finish = (self.height - 1, self.width - 1)

        self.exitCell = self.cells[finish[0]][finish[1]]
        self.exitCell.walls[exit] = False

        self.finish = finish
        self.exit = exit
        self.start = start
        self.entrance = entrance

        while len(stack):
            currentCell = stack.pop()
            neighbours = self.getNeighbours(currentCell)
            neighbours = [n for n in neighbours if not n.visited]

            if len(neighbours) > 0:
                stack.append(currentCell)
                selectedNeighbour = random.choice(neighbours)
                selectedNeighbour.visited = True

                self.removeCommonWall(currentCell, selectedNeighbour)

                stack.append(selectedNeighbour)

                if callback is not None:
                    callback()

        if loops:
            nonEdge = self.getNonEdgeCells()
            targets = [cell for row in nonEdge for cell in row]
            targets = random.sample(targets, loops)
            for cell in targets:
                walls = [i for i,w in enumerate(cell.walls) if w]
                if len(walls):
                    wallToRemove = random.choice(walls)
                    print(f"Removing wall {wallToRemove} in cell {cell.row}, {cell.col}")
    
                    self.removeWall(cell, wallToRemove)
                    
                    if callback is not None:
                            callback()

        if finished is not None:
            finished()



    def wallToucher(self, rightHand = True, callback = None, finished = None):
        self.removeMarks()
        startCell = currentCell = self.cells[self.start[0]][self.start[1]]
        currentDirection = (self.entrance + 2) % 4
        currentCell.visited = True

        print(f'exit {self.exitCell.row} {self.exitCell.col}')
        
        cellOrder = range(1, -3, -1) if rightHand else range(-1, 3, 1)

        while currentCell.row != self.exitCell.row or currentCell.col != self.exitCell.col:
            print(f'Cell {currentCell.row} {currentCell.col}')
            for direction in cellOrder:
                tryDirection = (currentDirection + direction) % 4
                print(f'Curernt {currentDirection} Try {tryDirection} wall {currentCell.walls[tryDirection]}')

                if currentCell == startCell and tryDirection == self.entrance:
                    continue

                if not currentCell.walls[tryDirection]:
                    currentCell = self.getNeighbour(currentCell, tryDirection)
                    currentDirection = tryDirection
                    print(f'Selected {currentCell.row} {currentCell.col} direction {currentDirection}')
                    if currentCell.visited:
                        print("Already been here")
                    currentCell.visited = True
                    if callback is not None:
                        callback()
                    break
                else:
                    currentCell.wallsTraversed[tryDirection] = True


        print("Finished")
        if finished is not None:
            finished()


      



class MazeWidget(QWidget):

    def __init__(self, maze):
        super(MazeWidget, self).__init__()
        self.maze = maze
        self.padding = 10


    def paintEvent(self, _e):
        qp = QPainter()
        qp.begin(self)
        qp.setBrush(QColor(255,0,0))

        size = self.size()
        cellWidth = (size.width() - self.padding * 2) / self.maze.width
        cellHeight = (size.height() - self.padding * 2) / self.maze.height

        for rowIndex, row in enumerate(maze.cells):
            for cellIndex, cell in enumerate(row):
                cellTopY = self.padding + cellHeight * rowIndex
                cellLeftX = self.padding + cellWidth * cellIndex
                
                traverseNorthExtra = 10
                traverseSouthExtra = 10
                traverseEastExtra = 10
                traverseWestExtra = 10

                if cell.visited:
                    qp.drawEllipse(cellLeftX + cellWidth / 2, cellTopY + cellHeight / 2, 4, 4)

                qp.setPen(QColor(0,0,0))

                if cell.walls[Cell.NORTH]:
                    qp.drawLine(cellLeftX, cellTopY, cellLeftX + cellWidth, cellTopY)
                    traverseNorthExtra = -10

                if cell.walls[Cell.SOUTH]:
                    qp.drawLine(cellLeftX, cellTopY + cellHeight, cellLeftX + cellWidth, cellTopY + cellHeight)
                    traverseSouthExtra = -10

                if cell.walls[Cell.WEST]:
                    qp.drawLine(cellLeftX, cellTopY, cellLeftX, cellTopY + cellHeight)
                    traverseWestExtra = -10
                
                if cell.walls[Cell.EAST]:
                    qp.drawLine(cellLeftX + cellWidth, cellTopY, cellLeftX + cellWidth, cellTopY + cellHeight)
                    traverseEastExtra = -10
                    
                qp.setPen(QColor(64,64,255))
                
                if cell.wallsTraversed[Cell.NORTH]:
                    qp.drawLine(cellLeftX - traverseWestExtra, cellTopY + 10, 
                                        cellLeftX + cellWidth + traverseEastExtra, cellTopY + 10)
                
                if cell.wallsTraversed[Cell.SOUTH]:
                    qp.drawLine(cellLeftX - traverseWestExtra, cellTopY + cellHeight - 10, 
                                        cellLeftX + cellWidth + traverseEastExtra, cellTopY + cellHeight - 10)

                if cell.wallsTraversed[Cell.WEST]:
                    qp.drawLine(cellLeftX + 10, cellTopY - traverseNorthExtra, 
                                cellLeftX + 10, cellTopY + cellHeight + traverseSouthExtra)
                
                if cell.wallsTraversed[Cell.EAST]:
                    qp.drawLine(cellLeftX + cellWidth - 10, cellTopY - traverseNorthExtra, 
                                cellLeftX + cellWidth - 10, cellTopY + cellHeight + traverseSouthExtra)

        qp.end()


def update(widget):
    widget.update()
    time.sleep(1.0 / (widget.maze.height * widget.maze.width) * 5)
    
    
def generate(widget):
    generateButton.setEnabled(False)
    
    rows = int(rowsWidget.text())
    cols = int(colsWidget.text())
    loops = int(loopsWidget.text())

    widget.maze.height = rows
    widget.maze.width = cols
    widget.maze.initialize()
    widget.update()
    
    threading.Thread(target = lambda: \
             widget.maze.randomizeBacktracker(loops = loops, 
                                              callback = lambda: update(widget),
                                              finished = lambda : generateButton.setEnabled(True),
                                              )).start()
    widget.update()
    
    
def traverserWallToucher(widget):
    wallToucherButton.setEnabled(False)
    right = rightLeftWidget.checkState()
    threading.Thread(target = lambda: \
             widget.maze.wallToucher(rightHand=right, callback = lambda: update(widget),
                                              finished = lambda : wallToucherButton.setEnabled(True),
                                              )).start()
    widget.update()

    

if __name__ == "__main__":
    app = QApplication([])
    window = QWidget()
    layout = QVBoxLayout()
    maze = Maze(10, 12)
    mazeWidget = MazeWidget(maze)
    mazeWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    layout.addWidget(mazeWidget)
    
    generateButton = QPushButton("Generate")
    layout.addWidget(generateButton)
    generateButton.clicked.connect(lambda: generate(mazeWidget))
    
    paramFrame = QFrame()
    paramFrame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    hbox = QHBoxLayout()
    
    hbox.addWidget(QLabel("Rows"))
    rowsWidget = QLineEdit("10")
    hbox.addWidget(rowsWidget)
    
    hbox.addWidget(QLabel("Cols"))
    colsWidget = QLineEdit("12")
    hbox.addWidget(colsWidget)
    
    hbox.addWidget(QLabel("Loops"))
    loopsWidget = QLineEdit("0")
    hbox.addWidget(loopsWidget)
    
    paramFrame.setLayout(hbox)
    layout.addWidget(paramFrame)


    wallToucherFrame = QFrame()
    wallToucherFrame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    hbox = QHBoxLayout()
    wallToucherFrame.setLayout(hbox)

    wallToucherButton = QPushButton("Traverse - wall toucher")
    wallToucherButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    hbox.addWidget(wallToucherButton)
    rightLeftWidget = QCheckBox("Turn Right")
    hbox.addWidget(rightLeftWidget)
    
    wallToucherButton.clicked.connect(lambda: traverserWallToucher(mazeWidget))
    layout.addWidget(wallToucherFrame)

    
    window.setLayout(layout)
    window.setGeometry(100, 100, 600, 600)
    window.setWindowTitle("Mazes")
    window.show()
    app.exec_()

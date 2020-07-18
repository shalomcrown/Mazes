#!/usr/bin/python3
'''
Author: Shalom Crown
Licence: GPL3
'''

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, \
    QVBoxLayout, QLabel, QHBoxLayout, QFrame, QLineEdit, QSizePolicy

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
        currentCell = self.cells[start[1]][start[0]]
        currentCell.walls[entrance] = False
        currentCell.visited = True
        stack.append(currentCell)

        if finish is None:
            finish = (self.width - 1, self.height - 1)

        exitCell = self.cells[finish[1]][finish[0]]
        exitCell.walls[exit] = False

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
                wallToRemove = random.choice(walls)
                print(f"Removing wall {wallToRemove} in cell {cell.row}, {cell.col}")

                self.removeWall(cell, wallToRemove)
                
                if callback is not None:
                        callback()

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
        qp.setPen(QColor(0,0,0))
        qp.setBrush(QColor(255,0,0))

        size = self.size()
        cellWidth = (size.width() - self.padding * 2) / self.maze.width
        cellHeight = (size.height() - self.padding * 2) / self.maze.height

        for rowIndex, row in enumerate(maze.cells):
            for cellIndex, cell in enumerate(row):
                cellTopY = self.padding + cellHeight * rowIndex
                cellLeftX = self.padding + cellWidth * cellIndex

                if cell.visited:
                    qp.drawEllipse(cellLeftX + cellWidth / 2, cellTopY + cellHeight / 2, 4, 4)

                if cell.walls[Cell.NORTH]:
                    qp.drawLine(cellLeftX, cellTopY, cellLeftX + cellWidth, cellTopY)

                if cell.walls[Cell.SOUTH]:
                    qp.drawLine(cellLeftX, cellTopY + cellHeight, cellLeftX + cellWidth, cellTopY + cellHeight)

                if cell.walls[Cell.WEST]:
                    qp.drawLine(cellLeftX, cellTopY, cellLeftX, cellTopY + cellHeight)
                
                if cell.walls[Cell.EAST]:
                    qp.drawLine(cellLeftX + cellWidth, cellTopY, cellLeftX + cellWidth, cellTopY + cellHeight)

        qp.end()


def update(widget):
    widget.update()
    time.sleep(0.1)
    
    
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
    
    window.setLayout(layout)
    window.setGeometry(100, 100, 600, 600)
    window.setWindowTitle("Mazes")
    window.show()
    app.exec_()

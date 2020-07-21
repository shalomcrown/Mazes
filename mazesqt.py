#!/usr/bin/python3
'''
Author: Shalom Crown
Licence: GPL3
'''


from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, \
    QVBoxLayout, QLabel, QHBoxLayout, QFrame, QLineEdit, QSizePolicy, QCheckBox


from PyQt5.QtGui import QPainter,  QColor
import threading
import time
from mazegen import *

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

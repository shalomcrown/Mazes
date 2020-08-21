#!/usr/bin/python3
"""
Author: Shalom Crown
Licence: GPL3
"""

import random


class Cell:
    EAST = 0
    SOUTH = 1
    WEST = 2
    NORTH = 3

    RELATIONSHIP = {EAST: (0, 1), SOUTH: (1, 0), WEST: (0, -1), NORTH: (-1, 0)}

    def __init__(self, row, col):
        self.walls = [True] * 4
        self.wallsTraversed = [False] * 4
        self.visited = False
        self.row = row
        self.col = col
        self.exitCell = None
        self.finish = None
        self.exit = None
        self.start = None
        self.entrance = None


class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = []
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

    def randomizeBacktracker(self, start=(0, 0), entrance=Cell.WEST, finish=None, exit_direction=Cell.EAST, callback=None,
                             loops=0, finished=None):
        stack = []
        currentCell = self.cells[start[0]][start[1]]
        currentCell.walls[entrance] = False
        currentCell.visited = True
        stack.append(currentCell)

        if finish is None:
            finish = (self.height - 1, self.width - 1)

        self.exitCell = self.cells[finish[0]][finish[1]]
        self.exitCell.walls[exit_direction] = False

        self.finish = finish
        self.exit = exit_direction
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
                walls = [i for i, w in enumerate(cell.walls) if w]
                if len(walls):
                    wallToRemove = random.choice(walls)
                    print(f'Removing wall {wallToRemove} in cell {cell.row}, {cell.col}')

                    self.removeWall(cell, wallToRemove)

                    if callback is not None:
                        callback()

        if finished is not None:
            finished()

    def wallToucher(self, rightHand=True, callback=None, finished=None):
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

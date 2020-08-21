#!/usr/bin/python3

from vpython import *
import logging
import sys
from mazegen import Maze, Cell


log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def generate_walls(maze):
    """
    :param maze: The maze to generate walls for
    :return: List of walls as list of list of vertices (in -1..1 for x,y,z)

    For each cell, only the east and south walls are created,
    except for first row and column, for which the north and west are added respectively
    """
    cellWidth = 2 / maze.width
    cellHeight = 2 / maze.height
    wallWidth = 0.01
    wallHeight = 1
    
    for rowIndex, row in enumerate(maze.cells):
        for cellIndex, cell in enumerate(row):
            cellTopY = cellWidth * rowIndex - 1
            cellLeftX = cellHeight * cellIndex -1
            
            if not 'walls3d' in cell.__dict__:
                cell.walls3d = {}
                
            # ------------------
        
            if cell.walls[Cell.EAST] and not Cell.EAST in cell.walls3d:
                cell.walls3d[Cell.EAST] = box(pos=vector(cellLeftX + cellWidth - wallWidth / 2,
                                          cellTopY + cellHeight / 2,
                                          wallHeight / 2),
                                size=vector(wallWidth, cellHeight, wallHeight)
                               )
            elif not cell.walls[Cell.EAST] and Cell.EAST in cell.walls3d:
                cell.walls3d.pop(Cell.EAST).visible = False

            # ------------------

            if cell.walls[Cell.SOUTH] and not Cell.SOUTH in cell.walls3d:
                cell.walls3d[Cell.SOUTH] = box(pos=vector(cellLeftX + cellHeight / 2,
                                          cellTopY + cellWidth - wallWidth / 2,
                                          wallHeight / 2),
                                size=vector(cellWidth, wallWidth, wallHeight)
                               )
            elif not cell.walls[Cell.SOUTH] and Cell.SOUTH in cell.walls3d:
                cell.walls3d.pop(Cell.SOUTH).visible = False

            # ------------------

            if cell.walls[Cell.WEST] and cellIndex == 0 and not Cell.WEST in cell.walls3d:
                cell.walls3d[Cell.WEST] = box(pos=vector(cellLeftX - wallWidth / 2,
                                          cellTopY + cellHeight / 2,
                                          wallHeight / 2),
                                size=vector(wallWidth, cellHeight, wallHeight)
                               )
            elif not cell.walls[Cell.WEST] and Cell.WEST in cell.walls3d:
                cell.walls3d.pop(Cell.WEST).visible = False

            # ------------------
                
            if cell.walls[Cell.NORTH] and rowIndex == 0 and not Cell.NORTH in cell.walls3d:
                cell.walls3d[Cell.NORTH] = box(pos=vector(cellLeftX + cellWidth / 2,
                                          cellTopY - wallWidth / 2,
                                          wallHeight / 2),
                                size=vector(cellWidth, wallWidth, wallHeight)
                               )
            elif not cell.walls[Cell.NORTH] and Cell.NORTH in cell.walls3d:
                cell.walls3d.pop(Cell.NORTH).visible = False

#------------------------------------------------------------------------------------------

def draw(maze):
    rate(10)
    generate_walls(maze)
    
#------------------------------------------------------------------------------------------

def main():
    scene = canvas(title='Mazes',
                   width=1200, height=900,
                   center=vector(0,0,-5), background=color.cyan)
    
    floor = box(pos=vector(0,0,0), size=vector(2,2,0.2), background=color.gray)
    sphere(pos=vector(0.5,0.5,0.5), radius=0.1)
    
    maze = Maze(10, 10)
    generate_walls(maze)

    maze.randomizeBacktracker(loops = 2, callback=lambda: draw(maze))
    

if __name__ == "__main__":
    main()
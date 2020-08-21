#!/usr/bin/python3

from vpython import *
import logging
import sys
from mazegen import Maze, Cell


log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

class MazePv:
    def generate_walls(self, maze):
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
                    text(pos=vector(cellLeftX + cellWidth / 2,
                                    cellTopY + cellHeight / 2,
                                    0.1
                                    ),
                                    text=f"{rowIndex},{cellIndex}",
                                    align='center',
                                    height=cellWidth / 3,
                                    color=color.red)
                    
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
    
    def draw(self, maze):
        rate(maze.width * maze.height / 10)
        self.generate_walls(maze)
        
    #------------------------------------------------------------------------------------------
    
    def generate(self, _p):
        self.maze = Maze(int(self.widthWidget.text), int(self.heightWidget.text))
        self.generate_walls(self.maze)
        self.maze.randomizeBacktracker(loops = int(self.loopWidget.text), callback=lambda: self.draw(self.maze))
        
    def what(self):
        pass
    
    #------------------------------------------------------------------------------------------
    
    def __init__(self):
        scene = canvas(title='Mazes',
                       width=1000, height=800,
                       center=vector(0,0,-5), background=color.cyan)
        
        _floor = box(pos=vector(0,0,0), size=vector(2.1,2.1,0.2), background=color.gray)
        sphere(pos=vector(0.5,0.5,0.5), radius=0.1)
        
        wtext(text="Width:")
        self.widthWidget = winput(prompt="Width", text="10", type="numeric", bind=self.what)
        wtext(text="&nbsp;Height:")
        self.heightWidget = winput(prompt="Height", text="10", type="numeric", bind=self.what)
        wtext(text="&nbsp;Loops:")
        self.loopWidget = winput(prompt="Loops", text="0", type="numeric", bind=self.what)
        button(bind=self.generate, text="Generate")
        scene.append_to_caption('\n\n')    
        
#------------------------------------------------------------------------------------------

if __name__ == "__main__":
    MazePv()
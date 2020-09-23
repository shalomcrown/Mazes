'''
Created on Sep 12, 2020

@author: shalomc
'''

from ursina import *            # import everything we need with one line.
import logging
import sys
import threading
from mazegen import Maze, Cell


log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)




def generate_walls(maze):
    cellWidth = 2.4 / maze.width
    cellHeight = 2.4 / maze.height
    wallWidth = 0.01
    wallHeight = 3
    
        #     sphere(pos=vector(0.5,0.5,0.5), radius=0.1)
        
        
    if not 'floor' in maze.__dict__:
        maze.floor = Entity(model='cube',
                   world_position=Vec3(cellWidth,cellHeight,0), scale=Vec3(3,3,0.2), background=color.gray)    
    
    for rowIndex, row in enumerate(maze.cells):
        for cellIndex, cell in enumerate(row):
            cellTopY = cellWidth * rowIndex - 1
            cellLeftX = cellHeight * cellIndex -1
            
            if not 'walls3d' in cell.__dict__:
                cell.walls3d = {}
#                 cell.text = text(position=Vec3(cellLeftX + cellWidth / 2,
#                                 cellTopY + cellHeight / 2 - cellHeight / 6,
#                                 0.1
#                                 ),
#                                 text=f"{rowIndex},{cellIndex}",
#                                 align='center',
#                                 height=cellWidth / 3,
#                                 color=color.red)

            # ------------------
        
            #Text(parent=maze.floor, text=f'{rowIndex},{cellIndex}', origin=(cellLeftX,cellTopY), color=color.red)
        
            if cell.walls[Cell.EAST] and not Cell.EAST in cell.walls3d:
                cell.walls3d[Cell.EAST] = Entity(model='cube', parent=maze.floor, texture='crate_texture',
                    world_position=Vec3(cellLeftX + cellWidth - wallWidth / 2,
                                          cellTopY + cellHeight / 2,
                                          0.4),
                                scale=Vec3(wallWidth, cellHeight / 2, wallHeight)
                               )
            elif not cell.walls[Cell.EAST] and Cell.EAST in cell.walls3d:
                cell.walls3d.pop(Cell.EAST).visible = False


            # ------------------

            if cell.walls[Cell.SOUTH] and not Cell.SOUTH in cell.walls3d:
                cell.walls3d[Cell.SOUTH] = Entity(model='cube', parent=maze.floor, texture='crate_texture',
                    world_position=Vec3(cellLeftX + cellHeight / 2,
                                          cellTopY + cellWidth - wallWidth / 2,
                                          0.4),
                                scale=Vec3(cellWidth / 2, wallWidth, wallHeight)
                               )
            elif not cell.walls[Cell.SOUTH] and Cell.SOUTH in cell.walls3d:
                cell.walls3d.pop(Cell.SOUTH).visible = False

            # ------------------

            if cell.walls[Cell.WEST] and not Cell.WEST in cell.walls3d:
                cell.walls3d[Cell.WEST] = Entity(model='cube', parent=maze.floor, texture='crate_texture',
                    world_position=Vec3(cellLeftX - wallWidth / 2,
                                          cellTopY + cellHeight / 2,
                                          0.4),
                                scale=Vec3(wallWidth, cellHeight / 2, wallHeight)
                               )
            elif not cell.walls[Cell.WEST] and Cell.WEST in cell.walls3d:
                cell.walls3d.pop(Cell.WEST).visible = False

            # ------------------
                
            if cell.walls[Cell.NORTH] and not Cell.NORTH in cell.walls3d:
                cell.walls3d[Cell.NORTH] = Entity(model='cube', parent=maze.floor, texture='crate_texture',
                    world_position=Vec3(cellLeftX + cellWidth / 2,
                                          cellTopY - wallWidth / 2,
                                          0.4),
                                scale=Vec3(cellWidth / 2, wallWidth, wallHeight)
                               )
            elif not cell.walls[Cell.NORTH] and Cell.NORTH in cell.walls3d:
                cell.walls3d.pop(Cell.NORTH).visible = False

    return maze.floor

app = Ursina()

window.title = 'Mazes'
window.borderless = False
window.fullscreen = False
window.cog_button.enabled = True



def draw(maze):
    time.sleep(maze.width * maze.height / 1000)
    generate_walls(maze)
    
maze = Maze(10, 10)
floor = generate_walls(maze)

thread = threading.Thread(target=lambda: maze.randomizeBacktracker(callback=lambda: draw(maze)))
thread.start()


Text.scale = 0.05
Text.default_resolution = 1080 * Text.scale
info = Text(text="Box", color=color.white)
info.x = -0.5
info.y = 0.4
info.background = True
info.visible = True

floor.rotation_x = -45
floor.rotation_y = 190



def update():   # update gets automatically called.
    floor.x += held_keys['d'] * .1
    floor.x -= held_keys['a'] * .1
    #floor.rotation_y += time.dt * 100
    #floor.rotation_x += time.dt * 10
    floor.rotation_z += time.dt * 10
    generate_walls(maze)
    
       
app.run()

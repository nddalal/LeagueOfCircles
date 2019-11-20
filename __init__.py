#Pathfinding Algorithm


from cmu_112_graphics import *
from tkinter import *


from pathing import *
from minionClass import *

import copy



def appStarted(app):
    app.rows = 10
    app.cols = 20
    app.board = [[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
            [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0],
            [0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0],
            [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 3]]
    app.margin = 0 # margin around grid
    app.cellSize = min(app.width,app.height)/10
    app.selection = (-1, -1) # (row, col) of selection, (-1,-1) for none
    app.startPos = (5,4)
    app.scrollX = 0
    app.scrollY = 0
    app.currentPos = app.startPos
    app.minSpawnCounter = 0
    app.allyMinionList = []
    app.enemyMinionList = []
    app.path = []
    
    


        
    
#Adapted from https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
def pointInGrid(app, x, y):
    # return True if (x, y) is inside the grid defined by app.
    return ((app.margin <= x <= app.width-app.margin) and
            (app.margin <= y <= app.height-app.margin))

def getCell(app, x, y):
    # aka "viewToModel"
    # return (row, col) in which (x, y) occurred or (-1, -1) if outside grid.
    if (not pointInGrid(app, x, y)):
        return (-1, -1)
    #gridWidth  = app.width - 2*app.margin
    #gridHeight = app.height - 2*app.margin
    cellWidth  = app.cellSize
    cellHeight = app.cellSize

    # Note: we have to use int() here and not just // because
    # row and col cannot be floats and if any of x, y, app.margin,
    # cellWidth or cellHeight are floats, // would still produce floats.
    row = int((y - app.margin) / cellHeight)
    col = int((x - app.margin) / cellWidth)

    return (row, col)

def getCellBounds(app, row, col):
    # aka "modelToView"
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
    #gridWidth  = app.width - 2*app.margin
    #gridHeight = app.height - 2*app.margin
    columnWidth = app.cellSize
    rowHeight = app.cellSize
    x0 = app.margin + col * columnWidth
    x1 = app.margin + (col+1) * columnWidth
    y0 = app.margin + row * rowHeight
    y1 = app.margin + (row+1) * rowHeight
    return (x0, y0, x1, y1)


# My Adapted Code:    
def timerFired(app):
    
    if app.minSpawnCounter % 20 == 0:
        app.allyMinionList.append(AllyMinion(app))
        app.enemyMinionList.append(EnemyMinion(app))

    if len(app.path) > 0:
        app.prevPos, app.currentPos = app.currentPos, app.path.pop(0)
        #app.scrollY = (app.currentPos[0]-app.prevPos[0])*app.cellSize
        #app.scrollX = (app.currentPos[1]-app.prevPos[1])*app.cellSize
    
    if app.minSpawnCounter % 2 == 0: 
        for minion in app.allyMinionList:
            if len(minion.path) > 0:
                minion.pos = minion.path.pop(0)
                
        for minion in app.enemyMinionList:
            if len(minion.path) > 0:
                minion.pos = minion.path.pop(0)
            
    app.minSpawnCounter += 1

def mousePressed(app, event):
    (row, col) = getCell(app, event.x, event.y)
    # select this (row, col) unless it is selected
    if (app.selection == (row, col)) or app.board[row][col] != 0:
        app.selection = (-1, -1)
    else:
        app.selection = (row, col)
        app.path = aStar(app, app.currentPos, app.selection)
        

def redrawAll(app, canvas):
    # draw grid of cells
    
    for row in range(app.rows):
        for col in range(app.cols):
            (x0, y0, x1, y1) = getCellBounds(app, row, col)
            if app.selection == (row, col) and app.board[row][col] == 0:
                fill = 'blue'
            elif app.board[row][col] == 1:
                fill = 'black'
            elif app.board[row][col] == 2:
                fill = 'lightblue'
            elif app.board[row][col] == 3:
                fill = 'red'
            else:
                fill = 'white'
            canvas.create_rectangle(x0-app.scrollX, y0-app.scrollY, 
                                    x1-app.scrollX, y1-app.scrollY, 
                                    fill=fill, outline = 'white')
    
    for minion in app.allyMinionList:
        r = app.cellSize//2
        (x0, y0, x1, y1) = getCellBounds(app, minion.pos[0], minion.pos[1])
        canvas.create_oval(x0+r/2, y0+r/2, x1-r/2, y1-r/2, fill = 'lightblue')
    for minion in app.enemyMinionList:
        r = app.cellSize//2
        (x0, y0, x1, y1) = getCellBounds(app, minion.pos[0], minion.pos[1])
        canvas.create_oval(x0+r/2, y0+r/2, x1-r/2, y1-r/2, fill = 'red')
        
    canvas.create_oval(getCellBounds(app, app.currentPos[0], app.currentPos[1])
    , fill = 'green')
    


runApp(width=1600, height=800)

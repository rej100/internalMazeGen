import tkinter as tk
import os
import random
import time
import threading
from tkinter import filedialog, Text

eBlack = "#131515"
jet = "#2B2C28"
albaster = "#E0E2DB"
pGreen = "#2BA84A"
oRed = "#FE5F55"

borderColor = "white"
cellColor = eBlack

cellSize = 8
gridSize = 80


# cellSize = 32
# gridSize = 20

class cell:
    def __init__(self, x, y, cellId, rightId, leftId, upId, downId):
        self.x = x
        self.y = y
        self.cellId = cellId
        self.rightId = rightId
        self.leftId = leftId
        self.upId = upId
        self.downId = downId
        self.visited = False

    x = 0
    y = 0
    cellId = 0
    rightId = 0
    leftId = 0
    upId = 0
    downId = 0
    visited = False

cells = [[0 for i in range(gridSize)] for j in range(gridSize)]

def placeCell(size, x, y):
    tCellId = mCanvas.create_rectangle(x, y, x+size, y+size, fill=cellColor, width=0)
    tRigthId = mCanvas.create_line(x+size, y, x+size, y + size, width=2, fill=borderColor)
    tLeftId = mCanvas.create_line(x, y, x, y+size, width=2, fill=borderColor)
    tUpId = mCanvas.create_line(x, y, x+size, y, width=2, fill=borderColor)
    tDownId = mCanvas.create_line(x, y+size, x+size, y+size, width=2, fill=borderColor)
    return cell(x, y, tCellId, tRigthId, tLeftId, tUpId, tDownId)


def buildCells(gSize, cSize):
    for x in range(gSize):
        for y in range(gSize):
            tempCell = placeCell(cSize, cSize * x, cSize * y)
            tempCell.x = x
            tempCell.y = y
            cells[x][y] = tempCell
    return 0

def hasUnvisted(cell):

    uNeigh = []

    r = True
    l = True
    u = True
    d = True

    if cell.y == 0:
        u = False
    if cell.y == gridSize-1:
        d = False
    if cell.x == 0:
        l = False
    if cell.x == gridSize - 1:
        r = False

    if r and not cells[cell.x+1][cell.y].visited:
        uNeigh.append("r")
    if l and not cells[cell.x-1][cell.y].visited:
        uNeigh.append("l")
    if u and not cells[cell.x][cell.y-1].visited:
        uNeigh.append("u")
    if d and not cells[cell.x][cell.y+1].visited:
        uNeigh.append("d")

    return uNeigh

def removeWall(cellA, cellB):
    if cellA.y == cellB.y:
        if cellA.x > cellB.x:
            mCanvas.delete(cellA.leftId)
            mCanvas.delete(cellB.rightId)
        else:
            mCanvas.delete(cellA.rightId)
            mCanvas.delete(cellB.leftId)
    if cellA.x == cellB.x:
        if cellA.y > cellB.y:
            mCanvas.delete(cellA.upId)
            mCanvas.delete(cellB.downId)
        else:
            mCanvas.delete(cellA.downId)
            mCanvas.delete(cellB.upId)

def flashCell(cell, color, duration):
    prev = cellColor
    mCanvas.itemconfig(cell.cellId, fill=color)
    mCanvas.update_idletasks()
    time.sleep(duration)
    mCanvas.itemconfig(cell.cellId, fill=prev)
    mCanvas.update_idletasks()
    return 0

def genMaze(cx, cy, anim):

    mCanvas.delete(cells[0][0].leftId)
    mCanvas.delete(cells[gridSize-1][gridSize-1].rightId)

    stack = []

    cells[0][0].visited = True

    currCell = cells[0][0]

    stack.append(cells[0][0])

    while stack:
        mCanvas.update_idletasks()

        currCell = stack.pop()
        neigh = hasUnvisted(currCell)
        #print(currCell.x, currCell.y)
        if neigh:
            stack.append(cells[currCell.x][currCell.y])

            side = random.choice(neigh)
            targetCell = 0
            if side == "r":
                targetCell = cells[currCell.x + 1][currCell.y]
            elif side == "l":
                targetCell = cells[currCell.x - 1][currCell.y]
            elif side == "u":
                targetCell = cells[currCell.x][currCell.y - 1]
            elif side == "d":
                targetCell = cells[currCell.x][currCell.y + 1]
            removeWall(currCell, targetCell)
            cells[targetCell.x][targetCell.y].visited = True
            stack.append(cells[targetCell.x][targetCell.y])
            if anim:
                time.sleep(0.001)
        elif anim:
            flashCell(currCell, pGreen, 0.015)

    return 0

root = tk.Tk()

canvas = tk.Canvas(root, width=1220, height=720 , bg=eBlack)
canvas.pack()

fOptions = tk.Frame(root, bg=jet)
fOptions.place(relwidth=0.3, relheight=1)

root.update()

fMBack = tk.Frame(root, bg=eBlack)
fMBack.place(relwidth=0.7, relheight=1, x=fOptions.winfo_width())

root.update()

mCanvas = tk.Canvas(fMBack, bg=pGreen, highlightthickness=0, relief='ridge')
mCanvas.place(width=cellSize*gridSize, height=cellSize*gridSize, x=(fMBack.winfo_width()-(cellSize*gridSize))/2, y=(fMBack.winfo_height()-(cellSize*gridSize))/2)

root.update()

buildCells(gridSize, cellSize)

mazeThread = threading.Thread(target=genMaze, args=[0, 0, False])
mazeThread.start()

root.mainloop()
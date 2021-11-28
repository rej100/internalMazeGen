import tkinter as tk
import os
import random
import time
import threading
from tkinter import filedialog, Text
from tkinter.colorchooser import askcolor

from PIL import Image

eBlack = "#131515"
jet = "#2B2C28"
albaster = "#E0E2DB"
pGreen = "#2BA84A"
oRed = "#FE5F55"

borderColor = "white"
cellColor = oRed
entryColor = pGreen
exitColor = "blue"

vertFramePad = 5

cellSize = 32
gridSize = 20

defaultMazeSize = 10

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
    global cells
    #mCanvas.create_rectangle(0,0,gridSize*cellSize,gridSize*cellSize, fill=cellColor, width=0)
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
            mCanvas.itemconfig(cellA.leftId, fill=cellColor)
            mCanvas.itemconfig(cellB.rightId, fill=cellColor)
        else:
            mCanvas.itemconfig(cellA.rightId, fill=cellColor)
            mCanvas.itemconfig(cellB.leftId, fill=cellColor)
    if cellA.x == cellB.x:
        if cellA.y > cellB.y:
            mCanvas.itemconfig(cellA.upId, fill=cellColor)
            mCanvas.itemconfig(cellB.downId, fill=cellColor)
        else:
            mCanvas.itemconfig(cellA.downId, fill=cellColor)
            mCanvas.itemconfig(cellB.upId, fill=cellColor)

def removeWall2(cellA, cellB):
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

def setTerminals(entryCell, exitCell, entryc, exitc):
    mCanvas.itemconfig(entryCell.leftId, fill=entryc, width=10)
    mCanvas.itemconfig(exitCell.rightId, fill=exitc, width=10)
    mCanvas.update_idletasks()

def genMaze(cx, cy, anim):
    global cells
    #mCanvas.delete(cells[0][0].leftId)
    #mCanvas.delete(cells[gridSize-1][gridSize-1].rightId)

    stack = []

    cells[0][0].visited = True

    currCell = cells[0][0]

    stack.append(cells[0][0])

    while stack:
        if anim:
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

    setTerminals(cells[0][0], cells[gridSize-1][gridSize-1], entryColor, exitColor)

    return 0

def saveImage():
    print("clicked")
    mCanvas.postscript(file="file_name.ps", colormode='color')
    psimg = Image.open("file_name.ps")
    psimg.save("file_name.png")
    return 0

def buttonGenMaze():
    global cells
    global gridSize
    global cellSize
    global mCanvas

    mCanvas.delete("all")

    gridSize = int(sizeEntry.get())
    factor = 20/gridSize
    cellSize = 32*factor


    cells = [[0 for i in range(gridSize)] for j in range(gridSize)]

    print(sizeEntry.get())
    buildCells(gridSize, cellSize)

    mazeThread = threading.Thread(target=genMaze, args=[0, 0, False])
    mazeThread.start()
    return 0

def buttonChangeMazeColor():
    global cellColor
    cellColor = askcolor(color=cellColor, title="Choose maze color")[1]
    mazeBackColorLabelS.config(bg=cellColor)
    return 0

def buttonChangeWallColor():
    global borderColor
    borderColor = askcolor(color=borderColor, title="Choose wall color")[1]
    mazeWallColorLabelS.config(bg=borderColor)
    return 0

def buttonChangeEntryColor():
    global entryColor
    entryColor = askcolor(color=entryColor, title="Choose wall color")[1]
    mazeEntryColorLabelS.config(bg=entryColor)
    return 0

def buttonChangeExitColor():
    global exitColor
    exitColor = askcolor(color=exitColor, title="Choose exit color")[1]
    mazeExitColorLabelS.config(bg=exitColor)
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

vertFrame1 = tk.Frame(fOptions, bg=jet)
vertFrame1.pack(pady=10)

sizeLabel = tk.Label(vertFrame1, text="Maze size:")
sizeLabel.pack(side="left")

sizeEntry = tk.Entry(vertFrame1, width=3)
sizeEntry.insert(0, defaultMazeSize)
sizeEntry.pack(side="left", padx=10)

#Maze background color change
vertFrame2 = tk.Frame(fOptions, bg=jet)
vertFrame2.pack(pady=vertFramePad)

mazeBackColorLabel = tk.Label(vertFrame2, text="Maze color:")
mazeBackColorLabel.pack(side="left")

mazeBackColorLabelS = tk.Label(vertFrame2, text="", bg=cellColor)
mazeBackColorLabelS.pack(side="left", padx=10)

changeMazeColorB = tk.Button(vertFrame2, text="Change", command=buttonChangeMazeColor)
changeMazeColorB.pack()

#Maze wall color change
vertFrame3 = tk.Frame(fOptions, bg=jet)
vertFrame3.pack(pady=vertFramePad)

mazeWallColorLabel = tk.Label(vertFrame3, text="Maze wall color:")
mazeWallColorLabel.pack(side="left")

mazeWallColorLabelS = tk.Label(vertFrame3, text="", bg=borderColor)
mazeWallColorLabelS.pack(side="left", padx=10)

changeWallColorB = tk.Button(vertFrame3, text="Change", command=buttonChangeWallColor)
changeWallColorB.pack()

#Maze entrance color change
vertFrame4 = tk.Frame(fOptions, bg=jet)
vertFrame4.pack(pady=vertFramePad)

mazeEntryColorLabel = tk.Label(vertFrame4, text="Entrance color:")
mazeEntryColorLabel.pack(side="left")

mazeEntryColorLabelS = tk.Label(vertFrame4, text="", bg=entryColor)
mazeEntryColorLabelS.pack(side="left", padx=10)

changeEntryColorB = tk.Button(vertFrame4, text="Change", command=buttonChangeEntryColor)
changeEntryColorB.pack()

#Maze exit color change
vertFrame5 = tk.Frame(fOptions, bg=jet)
vertFrame5.pack(pady=vertFramePad)

mazeExitColorLabel = tk.Label(vertFrame5, text="Exit color:")
mazeExitColorLabel.pack(side="left")

mazeExitColorLabelS = tk.Label(vertFrame5, text="", bg=entryColor)
mazeExitColorLabelS.pack(side="left", padx=10)

changeExitColorB = tk.Button(vertFrame5, text="Change", command=buttonChangeExitColor)
changeExitColorB.pack()

genMazeB = tk.Button(fOptions, text="Generate Maze", command=buttonGenMaze, padx=10, pady=10)
genMazeB.pack(pady=10)

saveMazeB = tk.Button(fOptions, text="Save Maze", command=saveImage, padx=10, pady=10)
saveMazeB.pack(pady=10)

root.update()

root.mainloop()
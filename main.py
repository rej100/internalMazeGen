import tkinter as tk
import os
from tkinter import filedialog, Text

eBlack = "#131515"
jet = "#2B2C28"
albaster = "#E0E2DB"
pGreen = "#2BA84A"
oRed = "#FE5F55"

cellSize = 32
gridSize = 20

class cell:
    def __init__(self, x, y, cellId, rightId, leftId, upId, downId):
        self.x = x
        self.y = y
        self.cellId = cellId
        self.rightId = rightId
        self.leftId = leftId
        self.upId = upId
        self.downId = downId

    x = 0
    y = 0
    cellId = 0
    rightId = 0
    leftId = 0
    upId = 0
    downId = 0

cells = []

def placeCell(size, x, y):
    tCellId = mCanvas.create_rectangle(x, y, x+size, y+size, fill=oRed, width=0)
    tRigthId = mCanvas.create_line(x+size, y, x+size, y + size, width=2)
    tLeftId = mCanvas.create_line(x, y, x, y+size, width=2)
    tUpId = mCanvas.create_line(x, y, x+size, y, width=2)
    tDownId = mCanvas.create_line(x, y+size, x+size, y+size, width=2)
    return cell(x, y, tCellId, tRigthId, tLeftId, tUpId, tDownId)


def buildCells(gSize, cSize):
    for i in range(gSize):
        for y in range(gSize):
            cells.append(placeCell(cSize, cSize*i, cSize*y))
    return 0

def genMaze():


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

# placeCell(cellSize, cellSize*0, cellSize*0)
# placeCell(cellSize, cellSize*1, cellSize*0)
# placeCell(cellSize, cellSize*5, cellSize*5)

buildCells(gridSize, cellSize)

root.mainloop()
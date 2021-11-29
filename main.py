import tkinter as tk
import os
import random
import time
import threading
import json
from tkinter import filedialog, Text
from tkinter.colorchooser import askcolor

from PIL import Image

eBlack = "#131515"
jet = "#2B2C28"
albaster = "#E0E2DB"
pGreen = "#2BA84A"
oRed = "#FE5F55"

labelColor = jet
labelTextColor = albaster
buttonColor = albaster
buttonTextColor = eBlack
buttonRelief = "flat"
vertFramePad = 5
cellSize = 32
gridSize = 20

gOptions = {
    "borderColor": "white",
    "cellColor": oRed,
    "entryColor": pGreen,
    "exitColor": "blue",
    "defaultMazeSize": 10,
    "gAnimate": False
}

# class pOptions:
#     def __init__(self, name, borderColor, cellColor, entryColor, exitColor, defaultMazeSize, gAnimate):
#         self.name = name
#         self.borderColor = borderColor
#         self.cellColor = cellColor
#         self.entryColor = entryColor
#         self.exitColor = exitColor
#         self.defaultMazeSize = defaultMazeSize
#         self.gAnimate = gAnimate
#
#     name="defn"
#     borderColor = "white"
#     cellColor = oRed
#     entryColor = pGreen
#     exitColor = "blue"
#     defaultMazeSize = 10
#     gAnimate = False

class pOptions:
    def __init__(self, name, options):
        self.name = name
        self.options = options

    name = "defn"
    options = gOptions

gPresets = []

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


def loadDefaults():
    global gOptions
    if not os.path.exists("./defaults.json"):
        defaultsFile = open("defaults.json", "w")
        json.dump(gOptions, defaultsFile)
        defaultsFile.close()
    else:
        defaultsFile = open("defaults.json")
        gOptions = json.load(defaultsFile)
        defaultsFile.close()


def placeCell(size, x, y):
    tCellId = mCanvas.create_rectangle(x, y, x+size, y+size, fill=gOptions["cellColor"], width=0)
    tRigthId = mCanvas.create_line(x+size, y, x+size, y + size, width=2, fill=gOptions["borderColor"])
    tLeftId = mCanvas.create_line(x, y, x, y+size, width=2, fill=gOptions["borderColor"])
    tUpId = mCanvas.create_line(x, y, x+size, y, width=2, fill=gOptions["borderColor"])
    tDownId = mCanvas.create_line(x, y+size, x+size, y+size, width=2, fill=gOptions["borderColor"])
    return cell(x, y, tCellId, tRigthId, tLeftId, tUpId, tDownId)

def buildCells(gSize, cSize):
    global cells
    #mCanvas.create_rectangle(0,0,gridSize*cellSize,gridSize*cellSize, fill=gOptions["cellColor"], width=0)
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
            mCanvas.itemconfig(cellA.leftId, fill=gOptions["cellColor"])
            mCanvas.itemconfig(cellB.rightId, fill=gOptions["cellColor"])
        else:
            mCanvas.itemconfig(cellA.rightId, fill=gOptions["cellColor"])
            mCanvas.itemconfig(cellB.leftId, fill=gOptions["cellColor"])
    if cellA.x == cellB.x:
        if cellA.y > cellB.y:
            mCanvas.itemconfig(cellA.upId, fill=gOptions["cellColor"])
            mCanvas.itemconfig(cellB.downId, fill=gOptions["cellColor"])
        else:
            mCanvas.itemconfig(cellA.downId, fill=gOptions["cellColor"])
            mCanvas.itemconfig(cellB.upId, fill=gOptions["cellColor"])

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
    prev = gOptions["cellColor"]
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

    setTerminals(cells[0][0], cells[gridSize-1][gridSize-1], gOptions["entryColor"], gOptions["exitColor"])

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
    global gOptions

    mCanvas.delete("all")

    gOptions["defaultMazeSize"] = int(sizeEntry.get())

    gridSize = gOptions["defaultMazeSize"]
    factor = 20/gridSize
    cellSize = 32*factor


    cells = [[0 for i in range(gridSize)] for j in range(gridSize)]

    buildCells(gridSize, cellSize)

    mazeThread = threading.Thread(target=genMaze, args=[0, 0, gOptions["gAnimate"]])
    mazeThread.start()
    return 0


def buttonChangeMazeColor():
    gOptions["cellColor"] = askcolor(color=gOptions["cellColor"], title="Choose maze color")[1]
    mazeBackColorLabelS.config(bg=gOptions["cellColor"])
    return 0

def buttonChangeWallColor():
    gOptions["borderColor"] = askcolor(color=gOptions["borderColor"], title="Choose wall color")[1]
    mazeWallColorLabelS.config(bg=gOptions["borderColor"])
    return 0

def buttonChangeEntryColor():
    gOptions["entryColor"] = askcolor(color=gOptions["entryColor"], title="Choose wall color")[1]
    mazeEntryColorLabelS.config(bg=gOptions["entryColor"])
    return 0

def buttonChangeExitColor():
    gOptions["exitColor"] = askcolor(color=gOptions["exitColor"], title="Choose exit color")[1]
    mazeExitColorLabelS.config(bg=gOptions["exitColor"])
    return 0


def updateAnimate():
    gOptions["gAnimate"] = bool(animatecvar.get())

def updateDefaults():
    global gOptions
    defaultsFile = open("defaults.json")
    gOptions = json.load(defaultsFile)
    defaultsFile.close()

    sizeEntry.insert(0, gOptions["defaultMazeSize"])
    mazeBackColorLabelS.config(bg=gOptions["cellColor"])
    mazeWallColorLabelS.config(bg=gOptions["borderColor"])
    mazeEntryColorLabelS.config(bg=gOptions["entryColor"])
    mazeExitColorLabelS.config(bg=gOptions["exitColor"])
    if gOptions["gAnimate"]:
        animateCheckB.select()
    else:
        animateCheckB.deselect()


def buttonSaveDefaults():
    global gOptions
    defaultsFile = open("defaults.json", "w")
    json.dump(gOptions, defaultsFile)
    defaultsFile.close()

def buttonLoadDefaults():
    global gOptions
    defaultsFile = open("defaults.json")
    gOptions = json.load(defaultsFile)
    defaultsFile.close()
    updateConfiguration()

def buttonResetDefaults():
    gOptions = {
        "borderColor": "white",
        "cellColor": oRed,
        "entryColor": pGreen,
        "exitColor": "blue",
        "defaultMazeSize": 10,
        "gAnimate": False
    }
    defaultsFile = open("defaults.json", "w")
    json.dump(gOptions, defaultsFile)
    defaultsFile.close()
    return


def updatePresetList():

    for widget in pListFrame.winfo_children():
        widget.destroy()

    for i in gPresets:
        vertFrame = tk.Frame(pListFrame, bg=albaster, highlightthickness=1, highlightbackground=jet)
        vertFrame.pack(fill="x", pady=(5,0))

        label = tk.Label(vertFrame, text=i.name, bg=buttonColor)
        label.pack(side="left", padx=(89,0))

        deletePresetB= tk.Button(vertFrame, text="Delete", command=lambda name=i.name: deletePreset(name), bg=buttonColor)
        deletePresetB.pack(side="right", padx=(0,5))

        loadPresetB = tk.Button(vertFrame, text="Load", command=lambda name=i.name: loadPreset(name), bg=buttonColor)
        loadPresetB.pack(side="right", padx=(0,5))

def deletePreset(name):
    count = 0
    for i in gPresets:
        if i.name == name:
            gPresets.pop(count)
            break
        count += 1
    updatePresetList()

def loadPreset(name):
    global gOptions
    count = 0
    for i in gPresets:
        if i.name == name:
            gOptions = gPresets[count].options
            break
        count += 1
    updatePresetList()
    updateConfiguration()

def savePreset():
    killSwitch = False

    for i in gPresets:
        if i.name == presetNameEntry.get():
            killSwitch=True

    if killSwitch:
        return

    gPresets.append(pOptions(presetNameEntry.get(), gOptions))

    updatePresetList()

def openPresetsW():
    global presetNameEntry
    global pListFrame

    #Presets window creation
    presetsW = tk.Toplevel()
    presetsW.title("Presets")

    #Background frame creation
    pBackFrame = tk.Frame(presetsW, width=377, height=720, bg=albaster)
    pBackFrame.pack()

    #Options frame creation
    pOptionsFrame = tk.Frame(presetsW, bg=jet)
    pOptionsFrame.place(relwidth=1, relheight=0.1)
    presetsW.update()

    #Preset name entry creation
    presetNameL = tk.Label(pOptionsFrame, text="Preset name:", bg=labelColor, fg=labelTextColor)
    presetNameL.pack(side="left", padx=10)

    presetNameEntry = tk.Entry(pOptionsFrame, width=20, bg=buttonColor, fg=buttonTextColor, relief=buttonRelief)
    # presetNameEntry.insert(0, gOptions["defaultMazeSize"])
    presetNameEntry.pack(side="left")

    #Preset save button creation
    savePresetB = tk.Button(pOptionsFrame, text="Save", command=savePreset, bg=buttonColor, fg=buttonTextColor, relief=buttonRelief)
    savePresetB.pack(side="left", padx=10)

    #Preset list frame creation
    pListFrame = tk.Frame(presetsW, bg=albaster)
    pListFrame.place(relwidth=1, relheight=0.9, y=pOptionsFrame.winfo_height())

    updatePresetList()

def updateConfiguration():
    mazeBackColorLabelS.config(bg=gOptions["cellColor"])
    mazeWallColorLabelS.config(bg=gOptions["borderColor"])
    mazeEntryColorLabelS.config(bg=gOptions["entryColor"])
    mazeExitColorLabelS.config(bg=gOptions["exitColor"])
    animatecvar.set(int(gOptions["gAnimate"]))

#Load options
loadDefaults()

#Tkinter setup
root = tk.Tk()
root.title("Maze Generator")
animatecvar = tk.IntVar()

#Background canvas creation
canvas = tk.Canvas(root, width=1220, height=720 , bg=eBlack)
canvas.pack()

#Menu frame creation
fOptions = tk.Frame(root, bg=jet)
fOptions.place(relwidth=0.3, relheight=1)

root.update()

#Maze generation part frame creation
fMBack = tk.Frame(root, bg=eBlack)
fMBack.place(relwidth=0.7, relheight=1, x=fOptions.winfo_width())

root.update()

#Maze canvas creation
mCanvas = tk.Canvas(fMBack, bg=eBlack, highlightthickness=0, relief='ridge')
mCanvas.place(width=cellSize*gridSize, height=cellSize*gridSize, x=(fMBack.winfo_width()-(cellSize*gridSize))/2, y=(fMBack.winfo_height()-(cellSize*gridSize))/2)

root.update()

#Maze size change
vertFrame1 = tk.Frame(fOptions, bg=jet)
vertFrame1.pack(pady=10)

sizeLabel = tk.Label(vertFrame1, text="Maze size:", bg=labelColor, fg=labelTextColor)
sizeLabel.pack(side="left")

sizeEntry = tk.Entry(vertFrame1, width=3, bg=buttonColor, fg=buttonTextColor, relief=buttonRelief)
sizeEntry.insert(0, gOptions["defaultMazeSize"])
sizeEntry.pack(side="left", padx=10)

#Maze background color change
vertFrame2 = tk.Frame(fOptions, bg=jet)
vertFrame2.pack(pady=vertFramePad)

mazeBackColorLabel = tk.Label(vertFrame2, text="Maze color:", bg=labelColor, fg=labelTextColor)
mazeBackColorLabel.pack(side="left")

mazeBackColorLabelS = tk.Label(vertFrame2, text="", bg=gOptions["cellColor"])
mazeBackColorLabelS.pack(side="left", padx=10)

changeMazeColorB = tk.Button(vertFrame2, text="Change", command=buttonChangeMazeColor, bg=buttonColor, fg=buttonTextColor, relief=buttonRelief)
changeMazeColorB.pack()

#Maze wall color change
vertFrame3 = tk.Frame(fOptions, bg=jet)
vertFrame3.pack(pady=vertFramePad)

mazeWallColorLabel = tk.Label(vertFrame3, text="Maze wall color:", bg=labelColor, fg=labelTextColor)
mazeWallColorLabel.pack(side="left")

mazeWallColorLabelS = tk.Label(vertFrame3, text="", bg=gOptions["borderColor"])
mazeWallColorLabelS.pack(side="left", padx=10)

changeWallColorB = tk.Button(vertFrame3, text="Change", command=buttonChangeWallColor, bg=buttonColor, fg=buttonTextColor, relief=buttonRelief)
changeWallColorB.pack()

#Maze entrance color change
vertFrame4 = tk.Frame(fOptions, bg=jet)
vertFrame4.pack(pady=vertFramePad)

mazeEntryColorLabel = tk.Label(vertFrame4, text="Entrance color:", bg=labelColor, fg=labelTextColor)
mazeEntryColorLabel.pack(side="left")

mazeEntryColorLabelS = tk.Label(vertFrame4, text="", bg=gOptions["entryColor"])
mazeEntryColorLabelS.pack(side="left", padx=10)

changeEntryColorB = tk.Button(vertFrame4, text="Change", command=buttonChangeEntryColor, bg=buttonColor, fg=buttonTextColor, relief=buttonRelief)
changeEntryColorB.pack()

#Maze exit color change
vertFrame5 = tk.Frame(fOptions, bg=jet)
vertFrame5.pack(pady=vertFramePad)

mazeExitColorLabel = tk.Label(vertFrame5, text="Exit color:", bg=labelColor, fg=labelTextColor)
mazeExitColorLabel.pack(side="left")

mazeExitColorLabelS = tk.Label(vertFrame5, text="", bg=gOptions["exitColor"])
mazeExitColorLabelS.pack(side="left", padx=10)

changeExitColorB = tk.Button(vertFrame5, text="Change", command=buttonChangeExitColor, bg=buttonColor, fg=buttonTextColor, relief=buttonRelief)
changeExitColorB.pack()

#Animate checkbox
animateCheckB = tk.Checkbutton(fOptions, text="Animate generation", command=updateAnimate, variable=animatecvar, bg=buttonColor, fg=buttonTextColor)
animateCheckB.pack(pady=vertFramePad)

#Defaults options array
vertFrame6 = tk.Frame(fOptions, bg=jet)
vertFrame6.pack(pady=vertFramePad)

saveDefaultsB = tk.Button(vertFrame6, text="Save current options as default", command=buttonSaveDefaults, bg=buttonColor, fg=buttonTextColor, relief=buttonRelief)
saveDefaultsB.pack(side="left", padx=5)

loadDefaultsB = tk.Button(vertFrame6, text="Load defaults", command=buttonLoadDefaults, bg=buttonColor, fg=buttonTextColor, relief=buttonRelief)
loadDefaultsB.pack(side="left", padx=5)

resetDefaultsB = tk.Button(vertFrame6, text="Reset defaults", command=buttonResetDefaults, bg=buttonColor, fg=buttonTextColor, relief=buttonRelief)
resetDefaultsB.pack(side="left", padx=5)

#Presets button
presetsB = tk.Button(fOptions, text="Presets", command=openPresetsW, padx=10, pady=10, bg=buttonColor, fg=buttonTextColor, relief=buttonRelief)
presetsB.pack(pady=10)
root.update()

#Maze generation button
genMazeB = tk.Button(fOptions, text="Generate Maze", command=buttonGenMaze, padx=10, pady=10, bg=buttonColor, fg=buttonTextColor, relief=buttonRelief)
genMazeB.pack(pady=10)

#Maze save button
saveMazeB = tk.Button(fOptions, text="Save Maze", command=saveImage, padx=10, pady=10, bg=buttonColor, fg=buttonTextColor, relief=buttonRelief)
saveMazeB.pack(pady=10)

#Tkinter initialization stuff
root.mainloop()
import subprocess
import time
import sys
from random import random

generationGap = 0.2    #seconds between generations
populationDensity = 23  #pecent of cells that should be populated at start of game
cellSize = 9    #pixel width and height of each cell
cellGap = 1     #pixels between cells

#set universe size to terminal screen
terminalLines = subprocess.Popen(["tput", "cols"], stdout=subprocess.PIPE)
terminalRows = subprocess.Popen(["tput", "lines"], stdout=subprocess.PIPE)
columns = int(terminalLines.communicate()[0])
rows = int(terminalRows.communicate()[0]) - 1


#Life truth table is a multidemtional array.
#  the first dimension is dead or alive (0 or 1)
#  the second dimension is whether a cell will be dead or alive
#  based on the number of neighbors
lifeTruthTable = [
    [ 0, 0, 0, 1, 0, 0, 0, 0, 0 ],
    [ 0, 0, 1, 1, 0, 0, 0, 0, 0 ]
    ]

#Set a variable that allows a QUIT event to break the infinite loop
running = True

#Trackers to tell when evolution has stopped
parentGeneration = [[0] * rows] * columns
grandparentGeneration = parentGeneration
generation = 1

def BigBang():
    global lifeTracker, rows, columns
    lifeTracker = []
    for column in range(columns):
        nextRow = []
        for row in range(rows):
            nextRow.append(lifeLottery())
        lifeTracker.append(nextRow)

def lifeLottery():
    if (random() < (float(populationDensity)/100)):
        return 1
    else:
        return 0

#Populate an array full of cells
lifeTracker = []
cells = []

#Draw cells on screen
def revealOrganisms():
    gameScreenString = ""    #ASCII command clears screen and moves cursor to 0,0

    #Note: this is a hack... I've consistently mixed up my columns and rows to this point
    #      For the rest of this function indexes will be backwards compared to rest of program
    for i in range(rows):
        for j in range(columns):
            if lifeTracker[j][i]:
                gameScreenString += "\xE2\x96\x89"
            else:
                gameScreenString += " "
    subprocess.call(["tput", "cup", "0,0"]) #return cursor to top of terminal
    subprocess.call(["echo", "-e", gameScreenString[:-2]])

    

#calculte who live and who dies
def reproduce():
    global generation
    global grandparentGeneration
    global parentGeneration
    global lifeTracker
    workingArray = []
    #iterate all cells
    for column in range(columns):
        nextRow = []
        for row in range(rows):
            
            #calculate live neighbors
            thisCellStatus = lifeTracker[column][row]
            liveNeighbors = 0
            for k in range(-1,2):
                for l in range(-1,2):
                    liveNeighbors += lifeTracker[(column+k)%columns][(row+l)%rows]
            #account for adding in thisCell
            liveNeighbors -= thisCellStatus
                
            #set cell in buffer
            nextRow.append(lifeTruthTable[thisCellStatus][liveNeighbors])
        workingArray.append(nextRow)

    #check for stagnant evolution
    if (workingArray == grandparentGeneration) or (workingArray == parentGeneration):
        print "Generations before stagnation: " + str(generation)
        sys.exit()
    else:
        grandparentGeneration = parentGeneration
        parentGeneration = lifeTracker
        generation += 1
    lifeTracker = workingArray
    

#main program

#generate universe
BigBang()
subprocess.call("clear")

while 1:
    revealOrganisms()
    reproduce()
    time.sleep(generationGap)

import pygame
from pygame.locals import *
from random import random

generationGap = 200    #milliseconds between generations
populationDensity = 23  #pecent of cells that should be populated at start of game
columns = 64
rows = 48
cellSize = 9    #pixel width and height of each cell
cellGap = 1     #pixels between cells

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
stagnant = 0

nextGeneration = USEREVENT+1

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
for i in range(columns):
    nextRow = []
    for j in range(rows):
        nextRow.append(pygame.Rect(((cellSize+cellGap)*i,(cellSize+cellGap)*j), (cellSize,cellSize)))
    cells.append(nextRow)

#Draw cells on screen
def revealOrganisms():
    updateRect = []
    for i in range(columns):
        for j in range(rows):
            #only redraw cells that have changed.
            if (lifeTracker[i][j] != parentGeneration[i][j]):
                if lifeTracker[i][j]:
                    updateRect.append(pygame.draw.rect(screen, (255,255,255),cells[i][j]))
                else:
                    updateRect.append(pygame.draw.rect(screen, (0,0,0),cells[i][j]))
    pygame.display.update(updateRect)

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
        stagnant = 1
        print "Generations before stagnation: " + str(generation)
        pygame.time.set_timer(nextGeneration, 0)
        pygame.display.set_caption("Life - Generations before stagnation: " + str(generation))
        
    else:
        grandparentGeneration = parentGeneration
        parentGeneration = lifeTracker
        generation += 1
    lifeTracker = workingArray
    

#main program

#setup screen
pygame.init()
screen = pygame.display.set_mode((columns*(cellSize+cellGap)-cellGap,rows*(cellSize+cellGap)-cellGap))
pygame.display.set_caption("Life")
background = pygame.Surface(screen.get_size())
background.fill((0,0,0))
screen.blit(background,(0,0))

#Set a timer to initiate each geneartional event
pygame.time.set_timer(nextGeneration, generationGap)

#generate universe
BigBang()
revealOrganisms()

while running:
    for event in pygame.event.get():
        if (event.type == nextGeneration):
            reproduce()
            revealOrganisms()
        elif (event.type == pygame.QUIT):
            running = False
pygame.quit()

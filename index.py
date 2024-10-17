import pygame
import numpy as np
import random

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 100, 100
CELL_SIZE = WIDTH // COLS
GRID = np.empty((ROWS, COLS),object)

pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))

COLORS = [(255, 255, 255)#White
         ,(255, 231, 76)#yellow
         ,(255, 89, 100)#red
         ,(107, 241, 120)#green
         ,(53, 167, 255)#blue
         ,(0, 0, 0)#Black
         ,(192, 192, 192)#Gray
]

for row in range(ROWS):
    for col in range(COLS):
        GRID[row][col] = {'state':0,'color':COLORS[5]}

mouseDown = False

current_color = 0
clock = pygame.time.Clock()
FPS = 30

def DrawGrid():
    for row in range(ROWS):
        for col in range(COLS):
            if GRID[row][col]['state'] == 1:
                pygame.draw.rect(window,GRID[row][col]['color'],(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def UpdateSand():
    for row in range(ROWS-2,-1,-1):
        for col in range(COLS):
            if GRID[row][col]['state'] == 1 and GRID[row+1][col]['state'] == 0:
                cellColor = GRID[row][col]['color']
                GRID[row][col]['state'] = 0
                GRID[row][col]['color'] = COLORS[5]
                GRID[row+1][col]['state'] = 1
                GRID[row+1][col]['color'] = cellColor
            elif GRID[row][col]['state'] == 1 and GRID[row+1][col]['state'] == 1:
                if col-1>=0 and col+1<COLS:
                    cellColor = GRID[row][col]['color']
                    if GRID[row+1][col+1]['state'] == 0 and GRID[row+1][col-1]['state'] == 0:
                        choice = random.choice([-1,1])
                        GRID[row][col]['state'] = 0
                        GRID[row][col]['color'] = COLORS[5]
                        GRID[row][col+choice]['state'] = 1
                        GRID[row][col+choice]['color'] = cellColor
                    elif GRID[row+1][col+1]['state'] == 0:
                        GRID[row][col]['state'] = 0
                        GRID[row][col]['color'] = COLORS[5]
                        GRID[row][col+1]['state'] = 1
                        GRID[row][col+1]['color'] = cellColor
                    elif GRID[row+1][col-1]['state'] == 0:
                        GRID[row][col]['state'] = 0
                        GRID[row][col]['color'] = COLORS[5]
                        GRID[row][col-1]['state'] = 1
                        GRID[row][col-1]['color'] = cellColor

def GetCellPosition(mousePosition):
    x, y = mousePosition
    cellX = x // CELL_SIZE
    cellY = y // CELL_SIZE
    return cellY, cellX

def SpawnSand(position):
    row, col=GetCellPosition(position)
    if 0<=col<COLS and 0<=row<ROWS:
        GRID[row][col]['state'] = 1
        GRID[row][col]['color'] = COLORS[current_color]
    

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mousePosition = pygame.mouse.get_pos()
                mouseDown = True
                SpawnSand(mousePosition)
            if event.button == 3:
                if current_color == 4:
                    current_color = 0 
                else:
                    current_color += 1
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mouseDown = False
        
        elif event.type == pygame.MOUSEMOTION:
            if mouseDown:
                mousePosition = pygame.mouse.get_pos()
                SpawnSand(mousePosition)
    
    UpdateSand()

    window.fill(COLORS[5])

    DrawGrid()

    pygame.display.flip()

    clock.tick(FPS)


pygame.quit()
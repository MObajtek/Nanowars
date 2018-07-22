from Cells import *


def newLevel(levelNumber):
    cells = []
    enemies = []
    neutrals = []
    myCurrentViruses = []
    enemyCurrentViruses = []
    level = levels[levelNumber]
    allItems = [cells, neutrals, enemies, myCurrentViruses, enemyCurrentViruses]
    for i in range(len(level['cells'])):
        cells.append(spawnCell(level['cells'][i][0], level['cells'][i][1], level['cells'][i][2]))
    for i in range(len(level['enemies'])):
        enemies.append(spawnEnemy(level['enemies'][i][0], level['enemies'][i][1], level['enemies'][i][2]))
    for i in range(len(level['neutrals'])):
        neutrals.append(spawnNeutral(level['neutrals'][i][0], level['neutrals'][i][1], level['neutrals'][i][2]))
    return allItems


displayWidth = 800
displayHeight = 700

black = (0, 0, 0)
white = (255, 255, 255)
red = (155, 0, 0)
lightBlue = (155, 239, 255)
yellow = (255, 255, 0)

# Tworzenie poziomu


levels = [
    # LEVEL ONE
    {'cells':
         [
            [[100, 175], 20, 40],
            [[100, 350], 30, 60],
            [[100, 525], 45, 90]
         ],
     'enemies':
         [
            [[700, 175], 45, 90],
            [[700, 350], 30, 60],
            [[700, 525], 20, 40]
         ],
     'neutrals':
         [
            [[400, 175], 10, 10],
            [[400, 350], 30, 30],
            [[400, 525], 10, 10]
         ],
     },
    # LEVEL TWO
    {'cells':
         [
            [[100, 300], 20, 40]
         ],
     'enemies':
         [
            [[400, 600], 20, 40]
         ],
     'neutrals':
         [
            [[400, 250], 10, 10],
            [[400, 350], 30, 30],
            [[400, 450], 10, 10],
            [[200, 200], 30, 60],
            [[300, 100], 45, 90],
            [[600, 400], 45, 90],
            [[500, 500], 30, 60]
         ]
     }
]

gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))  # Wielkosc okna
pygame.display.set_caption('Nanowars')  # Nazwa okna
clock = pygame.time.Clock()  # Zegar gry
enemySpeed = 5000  # Szybkosc ruchow AI w ms
pygame.time.set_timer(pygame.USEREVENT + 1, enemySpeed)

# cells = 0
# neutrals = 1
# enemies = 2
# myCurrentViruses = 3
# enemyCurrentViruses = 4

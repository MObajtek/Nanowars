from Cells import *

displayWidth = 800
displayHeight = 700



SPEED = 10

black = (0, 0, 0)
white = (255, 255, 255)
red = (155, 0, 0)
lightBlue = (155, 239, 255)
yellow = (255, 255, 0)

# Tworzenie poziomu
level = [[100, 175],
         [100, 350],
         [100, 525],
         [400, 175],
         [400, 350],
         [400, 525],
         [700, 175],
         [700, 350],
         [700, 525]]

gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))  # Wielkosc okna
pygame.display.set_caption('Nanowars')  # Nazwa okna
clock = pygame.time.Clock()  # Zegar gry
pygame.time.set_timer(pygame.USEREVENT + 1, 5000)

# Ladowanie obrazkow


circleLg1 = Cell('CircleLg.png', 'CircleLgl.png', level[0], 20, 40)
circleLg2 = Cell('CircleLg.png', 'CircleLgl.png', level[1], 30, 60)
circleLg3 = Cell('CircleLg.png', 'CircleLgl.png', level[2], 45, 90)

circleG1 = Neutral('circleG.png', level[3], 10)
circleG2 = Neutral('circleG.png', level[4], 30)
circleG3 = Neutral('circleG.png', level[5], 10)

circleLr1 = Enemies('CircleLr.png', level[6], 45, 90)
circleLr2 = Enemies('CircleLr.png', level[7], 30, 60)
circleLr3 = Enemies('CircleLr.png', level[8], 20, 40)

cells = [circleLg1, circleLg2, circleLg3]
neutrals = [circleG1, circleG2, circleG3]
enemies = [circleLr1, circleLr2, circleLr3]
myCurrentViruses = []
enemyCurrentViruses = []
circles = [cells,neutrals,enemies,myCurrentViruses,enemyCurrentViruses]
# cells = 0
# neutrals = 1
# enemies = 2
# myCurrentViruses = 3
# enemyCurrentViruses = 4
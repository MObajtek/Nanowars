from Level import *
from Cells import *

class Text(pygame.sprite.Sprite):
    def __init__(self, string, fontSize, plane, offset):
        super().__init__()
        self.string = string
        self.fontSize = fontSize
        self.plane = plane
        self.offset = offset
        self.myfont = pygame.font.SysFont("arialblack", self.fontSize)
        self.size = (self.text().get_rect().width, self.text().get_rect().height)
        x = displayWidth // 2 - self.size[0] // 2 + self.offset[0]
        y = displayHeight // 2 - self.size[1] // 2 + self.offset[1]
        self.position = (x,y)


    def text(self):
        return self.myfont.render(self.string, 1, yellow)

    def checkClick(self):
        if pygame.mouse.get_pressed() == (1, 0, 0):
            x, y = pygame.mouse.get_pos()
            if self.position[0] <= x <= self.position[0] + self.size[0]:
                if self.position[1] <= y <= self.position[1] + self.size[1]:
                    return True
            else:
                return False
        return


    def dis(self):

        self.plane.blit(self.text(), self.position)
        return

def gameIntro():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    intro = False



        gameDisplay.fill(lightBlue)
        Text("NANOWARS", 60, gameDisplay,(0,-50)).dis()
        playtext = Text("Play", 20,gameDisplay,(0,30))
        playtext.dis()
        if playtext.checkClick():
            intro = False
        helptext = Text("Help", 20, gameDisplay, (0, 70))
        helptext.dis()
        if helptext.checkClick():
            helpScreen()
        pygame.display.update()
        clock.tick(15)

def gamePause():
    pause = True
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause = False

        gameDisplay.fill(lightBlue)
        Text("PAUSE",60, gameDisplay, (0,-50)).dis()
        pygame.display.update()
        clock.tick(0)

def helpScreen():
    help = True

    while help:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    help = False

        gameDisplay.fill(lightBlue)
        Text("Help will be here", 60, gameDisplay, (0, -50)).dis()
        pygame.display.update()
        clock.tick(15)

def checkClickCircle(cell):
    posx = cell.position[0]
    posy = cell.position[1]
    size = cell.size
    if pygame.mouse.get_pressed() == (1, 0, 0):
        x, y = pygame.mouse.get_pos()
        if posx-size//2 <= x <= posx + size//2:
            if posy-size//2 <= y <= posy + size//2:
                return True
        else:
            return False

def checkWin(enemies, enemyViruses):
    return enemies == [] and enemyViruses == []

def checkLose(cells, myViruses):
    return cells == [] and myViruses == []




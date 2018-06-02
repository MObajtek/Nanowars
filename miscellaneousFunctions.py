from Level import *

class Text(pygame.sprite.Sprite):
    def __init__(self, string, size, plane, offset):
        super().__init__()
        self.string = string
        self.size = size
        self.plane = plane
        self.offset = offset
        self.myfont = pygame.font.SysFont("arialblack", self.size)


    def text(self):
        return self.myfont.render(self.string, 1, yellow)


    def dis(self):
        x = displayWidth // 2 - self.text().get_rect().width // 2 + self.offset[0]
        y = displayHeight // 2 - self.text().get_rect().height // 2 + self.offset[1]
        self.plane.blit(self.text(), (x,y))
        return

def gameIntro():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    intro = False



        gameDisplay.fill(lightBlue)
        Text("NANOWARS", 60, gameDisplay,(0,-50)).dis()
        pygame.display.update()
        clock.tick(15)

def checkClick(cell):
    posx = cell.position[0]
    posy = cell.position[1]
    size = cell.size
    if pygame.mouse.get_pressed() == (1, 0, 0):
        x, y = pygame.mouse.get_pos()
        if posx <= x <= posx + size:
            if posy <= y <= posy + size:
                return True
        else:
            return False

def lostWon(enemies, cells):
    if enemies == []:
        gameDisplay.fill(lightBlue)
        Text("CONGRATULATIONS! YOU WON!",40,gameDisplay,(0,-50)).dis()
        Text("press ENTER to exit",15,gameDisplay,(0,0)).dis()
        return True
    elif cells == []:
        gameDisplay.fill(lightBlue)
        Text("Sorry, you lost",40,gameDisplay,(0,-50)).dis()
        Text("press ENTER to exit",15,gameDisplay,(0,0)).dis()
        return True
    return False


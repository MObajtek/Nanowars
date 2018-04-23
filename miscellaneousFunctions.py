from Level import *

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
    myfont = pygame.font.SysFont("arialblack", 15)
    winfont = pygame.font.SysFont("arialblack", 40)
    if enemies == []:
        gameDisplay.fill(lightBlue)
        label = winfont.render("CONGRATULATIONS! YOU WON!", 1, (255, 255, 0))
        labelx = displayWidth // 2 - label.get_rect().width // 2
        labely = displayHeight // 2 - label.get_rect().height // 2
        gameDisplay.blit(label, (labelx, labely))
        label = myfont.render("press ENTER to exit", 1, (255, 255, 0))
        labelx = displayWidth // 2 - label.get_rect().width // 2
        labely = displayHeight // 2 - label.get_rect().height // 2
        gameDisplay.blit(label, (labelx, labely + 75))
        return True
    elif cells == []:
        gameDisplay.fill(lightBlue)
        label = winfont.render("Sorry, you lost", 1, (255, 255, 0))
        labelx = displayWidth // 2 - label.get_rect().width // 2
        labely = displayHeight // 2 - label.get_rect().height // 2
        gameDisplay.blit(label, (labelx, labely))
        label = myfont.render("press ENTER to exit", 1, (255, 255, 0))
        labelx = displayWidth // 2 - label.get_rect().width // 2
        labely = displayHeight // 2 - label.get_rect().height // 2
        gameDisplay.blit(label, (labelx, labely + 75))
        return True
    return False


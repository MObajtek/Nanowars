import pygame
import copy




class Virus(pygame.sprite.Sprite):
    def __init__(self, img, startCell, destinationCell):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(img).convert()
        self.image.set_colorkey((255, 255, 255))
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.destinationCell = destinationCell
        self.startCell = startCell
        self.size = self.image.get_rect().width
        self.center = copy.deepcopy(startCell.center)
        self.volume = startCell.volume // 2
        self.direction = [destinationCell.center[0] - self.center[0], destinationCell.center[1] - self.center[1]]

        magnitude = (self.direction[0] ** 2 + self.direction[1] ** 2) ** 0.5
        if magnitude == 0:
            self.direction = [0, 0]
        else:
            self.direction[0] /= magnitude
            self.direction[1] /= magnitude
        self.speed = 2

    def send(self, allList):

        self.center[0] += self.direction[0] * self.speed
        self.center[1] += self.direction[1] * self.speed
        # jesli x i y w odleglosci conajwyzej 5 od celu
        if abs(self.center[0] - self.destinationCell.center[0]) < 5:
            if abs(self.center[1] - self.destinationCell.center[1]) < 5:
                for i in range(3):
                    for circle in allList[i]:
                        if circle.center == self.destinationCell.center:
                            self.destinationCell = circle
                if type(self.startCell) == type(self.destinationCell):
                    myself = True
                else:
                    myself = False
                # 1. przekaz komorki
                if myself:
                    self.destinationCell.volume += self.volume
                else:
                    self.destinationCell.volume -= self.volume
                # 2. usun sie z listy wirusow
                if type(self.startCell) == Cell:
                    for i in range(len(allList[3])):
                        if self == allList[3][i]:
                            allList[3].pop(i)
                            return True
                else:
                    for i in range(len(allList[4])):
                        if self == allList[4][i]:
                            allList[4].pop(i)
                            return True
    def text(self):
        myfont = pygame.font.SysFont("arialblack", 15)
        return myfont.render(str(int(self.volume)), 1, (255, 255, 0))
    def dis(self, plane):
        plane.blit(self.image, (self.center[0] - self.size//2, self.center[1] - self.size//2))
        number = self.text()
        x = self.center[0]  - number.get_rect().width / 2
        y = self.center[1]  - number.get_rect().height / 2
        plane.blit(number, (x, y))

class Neutral(pygame.sprite.Sprite):
    def __init__(self, img, center, limit):
        pygame.sprite.Sprite.__init__(self)
        self.limit = limit
        self.volume = limit * 0.5
        self.image = pygame.image.load(img).convert()
        self.image = pygame.transform.scale(self.image, (int(self.limit) + 30, int(self.limit) + 30))
        self.image.set_colorkey((255, 255, 255))
        self.size = self.image.get_width()
        self.center = center
        self.position = [self.center[0] - self.size//2, self.center[1] - self.size//2]
        self.volume = limit

    def text(self):
        myfont = pygame.font.SysFont("arialblack", 15)
        return myfont.render(str(int(self.volume)), 1, (255, 255, 0))
    def dis(self, plane):
        plane.blit(self.image, (self.position[0], self.position[1]))
        number = self.text()
        x = self.position[0] + self.size / 2 - number.get_rect().width / 2
        y = self.position[1] + self.size / 2 - number.get_rect().height / 2
        plane.blit(number, (x, y))

class Enemies(pygame.sprite.Sprite):
    def __init__(self, img, center, volume, limit):
        pygame.sprite.Sprite.__init__(self)
        self.limit = limit
        self.volume = volume
        self.image = pygame.image.load(img).convert()
        self.image = pygame.transform.scale(self.image, (int(self.limit) + 30, int(self.limit) + 30))
        self.image.set_colorkey((255, 255, 255))
        self.size = self.image.get_width()
        self.center = center
        self.position = [self.center[0] - self.size//2, self.center[1] - self.size//2]


    def text(self):
        myfont = pygame.font.SysFont("arialblack", 15)
        return myfont.render(str(int(self.volume)), 1, (255, 255, 0))
    def dis(self, plane):
        plane.blit(self.image, (self.position[0], self.position[1]))
        number = self.text()
        x = self.position[0] + self.size / 2 - number.get_rect().width / 2
        y = self.position[1] + self.size / 2 - number.get_rect().height / 2
        plane.blit(number, (x, y))
        if self.volume < self.limit:
            self.volume += 0.02
        elif abs(self.volume - self.limit) < 0.5:
            pass
        elif self.volume - self.limit < 10:
            self.volume -= 0.03
        elif self.volume - self.limit < 30:
            self.volume -= 0.06
        elif self.volume - self.limit < 50:
            self.volume -= 0.12
        else:
            self.volume -= 0.24

class Cell(pygame.sprite.Sprite):
    def __init__(self, imgD, imgL, center, volume, limit):
        pygame.sprite.Sprite.__init__(self)
        self.volume = volume
        self.limit = limit
        self.imageD = pygame.image.load(imgD).convert()
        self.imageD = pygame.transform.scale(self.imageD, (int(self.volume) + 30, int(self.volume) + 30))
        self.imageD.set_colorkey((255, 255, 255))
        self.size = self.imageD.get_width()
        self.imageL = pygame.image.load(imgL).convert()
        self.imageL = pygame.transform.scale(self.imageL, (int(self.volume) + 30, int(self.volume) + 30))
        self.imageL.set_colorkey((255, 255, 255))
        self.center = center
        self.position = [self.center[0] - self.size//2, self.center[1] - self.size//2]



    def text(self):
        myfont = pygame.font.SysFont("arialblack", 15)
        return myfont.render(str(int(self.volume)), 1, (255, 255, 0))
    def dis(self, plane, D = 1):
        if D == 1:
            plane.blit(self.imageD, (self.position[0], self.position[1]))
        else:
            plane.blit(self.imageL, (self.position[0], self.position[1]))
        number = self.text()
        x = self.position[0] + self.size / 2 - number.get_rect().width / 2
        y = self.position[1] + self.size / 2 - number.get_rect().height / 2
        plane.blit(number, (x, y))
        if self.volume < self.limit:
            self.volume += 0.02
        elif abs(self.volume - self.limit) < 0.5:
            pass
        elif self.volume - self.limit < 10:
            self.volume -= 0.03
        elif self.volume - self.limit < 30:
            self.volume -= 0.06
        elif self.volume - self.limit < 50:
            self.volume -= 0.12
        else:
            self.volume -= 0.24


def spawnEnemyVirus(startCell, destinationCell):
    newVirus = Virus(
        "enemyVirus.png",
        startCell,
        destinationCell
    )
    return newVirus

def spawnMyVirus(startCell, destinationCell):
    newVirus = Virus(
        "myVirus.png",
        startCell,
        destinationCell
    )
    return newVirus

def spawnEnemy(position, volume, limit):
    newEnemy = Enemies(
        'CircleLr.png',
        position,
        volume,
        limit
    )
    return newEnemy

def spawnCell(position, volume, limit):
    newCell = Cell(
        "CircleLg.png",
        "CircleLgl.png",
        position,
        volume,
        limit
    )
    return newCell


def despawn(cell,myList):
    for i in range(len(myList)):
        if cell == myList[i]:
            myList.pop(i)
            return True

import pygame
import copy

# Docelowo ładować obrazek Cell i jasny ogkąg zewnętrzny osobno
# tak, żeby nie ładować całego nowego obrazka

# Nowe poziomy

# Klasy dziedziczące (parent do Cell, Neutral i Enemy zawierający center, volume, limit)

# Bardziej precyzyjne klikanie (na podstawie maski?)

# Siła ataku, siła obrony, prędkość, szybkość rozmnażania

# Chce zrobic parenta "circle" i dziecko "neutral". "Circle" ma miec w konstruktorze limit i center. "Neutral" ma miec image.
# jak wywolac neutral zeby ustawic wszystkie trzy rzeczy (czy sie da?)

# chce zrobic parenta. Ma w nim byc "resize" ktory musi dostawac i zmieniac "self.volume". Jego dziecko ma miec dodatkowe zmienne "self." i funkcje.
# Jak zainicjowac dziecko, zeby ustawic w nim jednoczesnie zmienne swoje i parenta?

# kiedy neutral zmienia sie w cell, limit nowego cella powinien byc taki sam jak poczatkowa wielkosc neutrala

class Circle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


class Virus(pygame.sprite.Sprite):
    def __init__(self, img, startCell, destinationCell):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(img).convert()
        self.image.set_colorkey((255, 255, 255))
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.destinationCell = destinationCell
        self.startCell = startCell
        self.size = self.image.get_rect().width
        self.position = copy.deepcopy(startCell.position)
        self.volume = startCell.volume // 2
        self.direction = [destinationCell.position[0] - self.position[0], destinationCell.position[1] - self.position[1]]

        magnitude = (self.direction[0] ** 2 + self.direction[1] ** 2) ** 0.5
        if magnitude == 0:
            self.direction = [0, 0]
        else:
            self.direction[0] /= magnitude
            self.direction[1] /= magnitude
        self.speed = 2

    def send(self, allList):

        self.position[0] += self.direction[0] * self.speed
        self.position[1] += self.direction[1] * self.speed
        # jesli x i y w odleglosci conajwyzej 5 od celu
        if abs(self.position[0] - self.destinationCell.position[0]) < 5:
            if abs(self.position[1] - self.destinationCell.position[1]) < 5:
                for i in range(3):
                    for circle in allList[i]:
                        if circle.position == self.destinationCell.position:
                            self.destinationCell = circle
                if type(self.startCell) == type(self.destinationCell):
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
        plane.blit(self.image, (self.position[0] - self.size//2, self.position[1] - self.size//2))
        number = self.text()
        x = self.position[0] - number.get_rect().width / 2
        y = self.position[1] - number.get_rect().height / 2
        plane.blit(number, (x, y))

class Neutral(pygame.sprite.Sprite):
    def __init__(self, img, position, limit):
        pygame.sprite.Sprite.__init__(self)
        self.limit = limit
        self.volume = limit * 0.5
        self.image = pygame.image.load(img).convert()
        self.image = pygame.transform.scale(self.image, (int(self.limit) + 30, int(self.limit) + 30))
        self.image.set_colorkey((255, 255, 255))
        self.size = self.image.get_width()
        self.position = position
        self.volume = limit

    def text(self):
        myfont = pygame.font.SysFont("arialblack", 15)
        return myfont.render(str(int(self.volume)), 1, (255, 255, 0))
    def dis(self, plane):
        scaled = pygame.transform.scale(self.image, (int(self.volume*1.5) + 20, int(self.volume*1.5) + 20))
        self.size = scaled.get_width()
        plane.blit(scaled, (self.position[0]-self.size//2, self.position[1]-self.size//2))
        number = self.text()
        x = self.position[0] - number.get_rect().width / 2
        y = self.position[1] - number.get_rect().height / 2
        plane.blit(number, (x, y))

class Enemies(pygame.sprite.Sprite):
    def __init__(self, img, position, volume, limit):
        pygame.sprite.Sprite.__init__(self)
        self.limit = limit
        self.volume = volume
        self.image = pygame.image.load(img).convert()
        self.image.set_colorkey((255, 255, 255))
        self.size = self.image.get_width()
        self.position = position

    def text(self):
        myfont = pygame.font.SysFont("arialblack", 15)
        return myfont.render(str(int(self.volume)), 1, (255, 255, 0))

    def dis(self, plane):
        scaled = pygame.transform.scale(self.image, (int(self.volume*1.5) + 20, int(self.volume*1.5) + 20))
        self.size = scaled.get_width()
        plane.blit(scaled, (self.position[0]-self.size//2, self.position[1]-self.size//2))
        number = self.text()
        x = self.position[0] - number.get_rect().width / 2
        y = self.position[1] - number.get_rect().height / 2
        plane.blit(number, (x, y))
        # zmniejszanie objetosci komorki zaleznie od wielkosci przekroczenia limitu
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
    def __init__(self, imgD, imgL, position, volume, limit):
        pygame.sprite.Sprite.__init__(self)
        self.volume = volume
        self.limit = limit
        self.imageD = pygame.image.load(imgD).convert()
        self.imageD.set_colorkey((255, 255, 255))
        self.size = self.imageD.get_width()
        self.imageL = pygame.image.load(imgL).convert()
        self.imageL.set_colorkey((255, 255, 255))
        self.position = position

    def text(self):
        myfont = pygame.font.SysFont("arialblack", 15)
        return myfont.render(str(int(self.volume)), 1, (255, 255, 0))
    def dis(self, plane, D = 1):
        if D == 1:
            scaled = pygame.transform.scale(self.imageD, (int(self.volume*1.5) + 20, int(self.volume*1.5) + 20))
        else:
            scaled = pygame.transform.scale(self.imageL, (int(self.volume*1.5) + 20, int(self.volume*1.5) + 20))
        self.size = scaled.get_width()
        plane.blit(scaled, (self.position[0] - self.size // 2, self.position[1] - self.size // 2))

        number = self.text()
        x = self.position[0] - number.get_rect().width / 2
        y = self.position[1] - number.get_rect().height / 2
        plane.blit(number, (x, y))
        # zmniejszanie objetosci komorki zaleznie od wielkosci przekroczenia limitu
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

def spawnNeutral(position,limit,none):
    newNeutral = Neutral(
        'circleG.png',
        position,
        limit
    )
    return newNeutral

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

from Level import *
from miscellaneousFunctions import *


def gameLoop():
    l = 0
    d = 1

    x = False
    y = False
    end = False

    activeCell = None
    activeEnemy = None
    attackN = None
    attackC = None

    gameExit = False

    while not gameExit:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                gameExit = True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # new onMouseClick:
                #   -select cell as active if none was selected
                #   -send viruses from active to clicked cell if there was one selected
                # pamietamy czy kliknelismy na jakakolwiek komorke zeby po przejsciu petli
                # i nie kliknieciu na zadna z istniejacych ustawic activeCell na None
                clickedCell = False
                if activeCell is not None:
                    for neutral in neutrals:
                        if checkClick(neutral):
                            myCurrentViruses.append(spawnMyVirus(activeCell, neutral))
                            activeCell.volume -= activeCell.volume // 2
                    #            tu powinno byc activeCell = None ---- CZYŻBY????
                    for enemy in enemies:
                        if checkClick(enemy):
                            myCurrentViruses.append(spawnMyVirus(activeCell, enemy))
                            activeCell.volume -= activeCell.volume // 2
                            activeCell = None

                for cell in cells:
                    if checkClick(cell):
                        clickedCell = True
                        # clicked on a cell
                        if activeCell and activeCell != cell:
                            # there was an active cell before - send viruses and reset activeCell
                            myCurrentViruses.append(spawnMyVirus(activeCell, cell))
                            activeCell.volume -= activeCell.volume // 2
                            activeCell = None
                        else:
                            # no current active cell, make that one the new active
                            activeCell = cell
                            break

                if not clickedCell:
                    activeCell = None

            elif event.type == pygame.USEREVENT + 1:
                maxi = 0
                mini = 1000
                # Wyszukaj największą komorkę wsrod przeciwnikow i z niej:
                for enemy in enemies:
                    if enemy.volume > maxi:
                        maxi = enemy.volume
                        activeEnemy = enemy
                # Jeżeli istnieją jakies komorki neutralne, wyslij wirusa do komorki neutralnej o najmniejszej wielkosci
                if neutrals != []:
                    for neutral in neutrals:
                        if neutral.volume < mini:
                            mini = neutral.volume
                            attackN = neutral
                    enemyCurrentViruses.append(spawnEnemyVirus(activeEnemy, attackN))
                    activeEnemy.volume -= activeEnemy.volume // 2
                # Jeżeli nie istnieją żadne komorki neutralne, wyslij wirusa do mojej komorki najmniejszej wielkosci
                else:
                    for cell in cells:
                        if cell.volume < mini:
                            mini = cell.volume
                            attackC = cell
                    enemyCurrentViruses.append(spawnEnemyVirus(activeEnemy, attackC))
                    activeEnemy.volume -= activeEnemy.volume // 2

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if end:
                        gameExit = True

        gameDisplay.fill(lightBlue)

        # ============= Nowe wyświetlanie ===============
        for enemy in enemies:
            enemy.dis(gameDisplay)

        for cell in cells:
            if cell == activeCell:
                cell.dis(gameDisplay,l)
            else:
                cell.dis(gameDisplay,d)

        for neutral in neutrals:
            neutral.dis(gameDisplay)

        for virus in myCurrentViruses:
            x = virus.send(circles)
            virus.dis(gameDisplay)

        for virus in enemyCurrentViruses:
            y = virus.send(circles)
            virus.dis(gameDisplay)

        # ============= Zmiana właściciela komórki ===============
        if x:
            for neutral in neutrals:
                if neutral.volume < 0:
                    neutral.volume = abs(neutral.volume)
                    despawn(neutral,neutrals)
                    cells.append(spawnCell(neutral.center, neutral.volume, neutral.limit * 2))

            for enemy in enemies:
                if enemy.volume < 0:
                    enemy.volume = abs(enemy.volume)
                    despawn(enemy, enemies)
                    cells.append(spawnCell(enemy.center, enemy.volume, enemy.limit))

        if y:
            for neutral in neutrals:
                if neutral.volume < 0:
                    neutral.volume = abs(neutral.volume)
                    despawn(neutral, neutrals)
                    enemies.append(spawnEnemy(neutral.center, neutral.volume, neutral.limit * 2))

            for cell in cells:
                if cell.volume < 0:
                    cell.volume = abs(cell.volume)
                    despawn(cell, cells)
                    enemies.append(spawnEnemy(cell.center, cell.volume, cell.limit))


        x = False
        y = False

        end = lostWon(enemies, cells)

        pygame.display.update()
        clock.tick(60)  # FPS

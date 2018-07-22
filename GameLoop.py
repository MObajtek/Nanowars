from miscellaneousFunctions import *


def gameLoop():

    for currentLevelNumber in range(0, len(levels)):
        allItems = newLevel(currentLevelNumber)
        l = 0
        d = 1

        x = False
        y = False
        loadNext = False
        endGame = False

        activeCell = None
        activeEnemy = None
        attackN = None
        attackC = None

        loopExit = False

        while not loopExit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        loopExit = True
                    # new onMouseClick:
                    #   -select cell as active if none was selected
                    #   -send viruses from active to clicked cell if there was one selected
                    # pamietamy czy kliknelismy na jakakolwiek komorke zeby po przejsciu petli
                    # i nie kliknieciu na zadna z istniejacych ustawic activeCell na None
                    clickedCell = False
                    if activeCell is not None:
                        for neutral in allItems[1]:
                            if checkClickCircle(neutral):
                                allItems[3].append(spawnMyVirus(activeCell, neutral))
                                activeCell.volume -= activeCell.volume // 2
                        #            tu powinno byc activeCell = None ---- CZYŻBY????
                        for enemy in allItems[2]:
                            if checkClickCircle(enemy):
                                allItems[3].append(spawnMyVirus(activeCell, enemy))
                                activeCell.volume -= activeCell.volume // 2
                                activeCell = None

                    for cell in allItems[0]:
                        if checkClickCircle(cell):
                            clickedCell = True
                            # clicked on a cell
                            if activeCell and activeCell != cell:
                                # there was an active cell before - send viruses and reset activeCell
                                allItems[3].append(spawnMyVirus(activeCell, cell))
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
                    for enemy in allItems[2]:
                        if enemy.volume > maxi:
                            maxi = enemy.volume
                            activeEnemy = enemy
                    # Jeżeli istnieją jakies komorki neutralne, wyslij wirusa do komorki neutralnej o najmniejszej wielkosci
                    if allItems[1] != []:
                        for neutral in allItems[1]:
                            if neutral.volume < mini:
                                mini = neutral.volume
                                attackN = neutral
                        allItems[4].append(spawnEnemyVirus(activeEnemy, attackN))
                        activeEnemy.volume -= activeEnemy.volume // 2
                    # Jeżeli nie istnieją żadne komorki neutralne, wyslij wirusa do mojej komorki najmniejszej wielkosci
                    else:
                        for cell in allItems[0]:
                            if cell.volume < mini:
                                mini = cell.volume
                                attackC = cell
                        allItems[4].append(spawnEnemyVirus(activeEnemy, attackC))
                        activeEnemy.volume -= activeEnemy.volume // 2

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if loadNext:
                            loopExit = True
                        elif endGame:
                            pygame.quit()
                            quit()
                    if event.key == pygame.K_ESCAPE:
                        gamePause()


            gameDisplay.fill(lightBlue)

            # ============= Nowe wyświetlanie ===============
            # for gameObject in allItems[0] + allItems[1] + allItems[2] + allItems[3] + allItems[4]:
            #     gameObject.dis(gameDisplay)
            #     gameObject.tick()

            for enemy in allItems[2]:
                enemy.dis(gameDisplay)
                # enemy.tick()

            for cell in allItems[0]:
                if cell == activeCell:
                    cell.dis(gameDisplay,l)
                else:
                    cell.dis(gameDisplay,d)

            for neutral in allItems[1]:
                neutral.dis(gameDisplay)

            for virus in allItems[3]:
                x = virus.send(allItems)
                virus.dis(gameDisplay)

            for virus in allItems[4]:
                y = virus.send(allItems)
                virus.dis(gameDisplay)

            # ============= Zmiana właściciela komórki ===============
            if x:
                for neutral in allItems[1]:
                    if neutral.volume < 0:
                        neutral.volume = abs(neutral.volume)
                        despawn(neutral,allItems[1])
                        allItems[0].append(spawnCell(neutral.position, neutral.volume, neutral.limit * 2))

                for enemy in allItems[2]:
                    if enemy.volume < 0:
                        enemy.volume = abs(enemy.volume)
                        despawn(enemy, allItems[2])
                        allItems[0].append(spawnCell(enemy.position, enemy.volume, enemy.limit))

            if y:
                for neutral in allItems[1]:
                    if neutral.volume < 0:
                        neutral.volume = abs(neutral.volume)
                        despawn(neutral, allItems[1])
                        allItems[2].append(spawnEnemy(neutral.position, neutral.volume, neutral.limit * 2))

                for cell in allItems[0]:
                    if cell.volume < 0:
                        cell.volume = abs(cell.volume)
                        despawn(cell, allItems[0])
                        allItems[2].append(spawnEnemy(cell.position, cell.volume, cell.limit))


            x = False
            y = False

            if checkWin(allItems[2],allItems[4]):
                gameDisplay.fill(lightBlue)
                Text("CONGRATULATIONS! YOU WON!", 40, gameDisplay, (0, -50)).dis()
                Text("press ENTER to go to next level", 15, gameDisplay, (0, 0)).dis()
                loadNext = True
            if checkLose(allItems[0],allItems[3]):
                gameDisplay.fill(lightBlue)
                Text("Sorry, you lost", 40, gameDisplay, (0, -50)).dis()
                Text("press ENTER to exit", 15, gameDisplay, (0, 0)).dis()
                endGame = True


            pygame.display.update()
            clock.tick(60)  # FPS

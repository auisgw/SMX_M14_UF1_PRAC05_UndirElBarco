"""
 Pygame base template for opening a window
"""

import pygame


def genera_tauler():
    tauler = [["-" for _ in range(3)] for _ in range(3)]
    return tauler


def comprovar_victoria(tauler):
    empat = True
    for fila in tauler:
        victoria_fila = True
        casella_anterior = fila[0]
        for casella in fila:
            if casella == "-":
                empat = False
            if casella != casella_anterior:
                victoria_fila = False
            casella_anterior = casella
        if victoria_fila and casella_anterior != "-":
            return True, casella_anterior

    if empat:
        return True, "-"

    for y in range(3):
        victoria_columna = True
        casella_anterior = tauler[0][y]
        for x in range(3):
            casella = tauler[x][y]
            if casella != casella_anterior:
                victoria_columna = False
            casella_anterior = casella
        if victoria_columna and casella_anterior != "-":
            return True, casella_anterior

    victoria_diagonal1 = True
    victoria_diagonal2 = True
    casella_anterior1 = tauler[0][0]
    casella_anterior2 = tauler[0][2]
    for i in range(3):
        casella1 = tauler[i][i]
        casella2 = tauler[i][2-i]

        if casella1 != casella_anterior1:
            victoria_diagonal1 = False
        if casella2 != casella_anterior2:
            victoria_diagonal2 = False
        casella_anterior1 = casella1
        casella_anterior2 = casella2
    if victoria_diagonal1 and casella_anterior1 != "-":
        return True, casella_anterior1
    if victoria_diagonal2 and casella_anterior2 != "-":
        return True, casella_anterior2

    return False, "-"


def calcular_posicio_maquina(tauler, simbol):
    import random

    # Revisamos si la máquina puede ganar en el siguiente turno
    for filas in range(3):
        for columna in range(3):
            # Si la fila/columna esta vacia:
            if tauler[filas][columna] == "-":

                tauler[filas][columna] = simbol
                if hay_ganador(tauler, simbol):
                    return filas, columna
                tauler[filas][columna] = "-"

    # Revisamos si el jugador puede ganar en el siguiente turno y bloqueamos
    simbol_oponente = 'O' if simbol == 'X' else 'X'
    for filas in range(3):
        for columnas in range(3):
            if tauler[filas][columnas] == "-":
                tauler[filas][columnas] = simbol_oponente
                if hay_ganador(tauler, simbol_oponente):
                    return filas, columnas
                tauler[filas][columnas] = "-"

    # Si no se dan las condiciones anteriores, escogemos una posición al azar
    posicio_valida = False
    while not posicio_valida:
        fila = random.randint(0, 2)
        columna = random.randint(0, 2)
        if tauler[fila][columna] == "-":
            posicio_valida = True

    return fila, columna


def hay_ganador(tauler, simbol):
    # Comprobamos las filas
    for i in range(3):
        if tauler[i] == [simbol]*3:
            return True
    # Comprobamos las columnas
    for columna in range(3):
        if [tauler[i][columna] for i in range(3)] == [simbol]*3:
            return True
    # Comprobamos las diagonales
    if [tauler[i][i] for i in range(3)] == [simbol]*3 or [tauler[i][2-i] for i in range(3)] == [simbol]*3:
        return True

    return False


def mostrar_tauler(screen, tauler, tauler_sprite, o_sprite, x_sprite, posicions_columnes, posicions_files):
    # Mostrem el tauler:
    screen.blit(tauler_sprite, (0, 0))

    # Mostrem les caselles omplertes:
    for y, fila in enumerate(tauler):
        for x, casella in enumerate(fila):
            if casella != "-":
                if casella == "O":
                    sprite = o_sprite
                else:
                    sprite = x_sprite
                screen.blit(
                    sprite, (posicions_columnes[x][0] + 16, posicions_files[y][0] + 16))


def mostrar_guanyador(screen, guanyador, font, color):
    if guanyador == "-":
        text = "Hi ha hagut un empat!"
    else:
        text = "Ha guanyat el jugador de les " + guanyador + "."
    text += " Fes clic per tornar a jugar..."
    text = font.render(text, True, color)
    # text_rect = text.get_rect(center=(700 / 2, 500 / 2))
    # screen.blit(text, text_rect)
    temp_surface = pygame.Surface(text.get_size())
    temp_surface.fill((192, 192, 192))
    temp_surface.blit(text, (0, 0))
    screen.blit(temp_surface, text.get_rect(center=(700 / 2, 500 / 2)))


def fer_moviment(tauler, posicions_columnes, posicions_files):
    pos = pygame.mouse.get_pos()
    pos_x = pos[0]
    pos_y = pos[1]
    columna = -1
    for index, rang in enumerate(posicions_columnes):
        if pos_x > rang[0] and pos_x < rang[1]:
            columna = index
            break
    if columna != -1:
        fila = -1
        for index, rang in enumerate(posicions_files):
            if pos_y > rang[0] and pos_y < rang[1]:
                fila = index
                break
        if fila != -1:
            if tauler[fila][columna] == "-":
                tauler[fila][columna] = "X"
                victoria, guanyador = comprovar_victoria(tauler)
                if not victoria:
                    fila, columna = calcular_posicio_maquina(tauler, "O")
                    tauler[fila][columna] = "O"
    victoria, guanyador = comprovar_victoria(tauler)
    return victoria, guanyador


def main():
    # Define some colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    pygame.init()

    # Set the width and height of the screen [width, height]
    size = (700, 500)
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Tres en ratlla")

    # Definim la font de lletra
    font = pygame.font.Font(None, 25)

    # Variables de les imatges:
    tauler_sprite = pygame.image.load("sprites/Tauler.png")
    o_sprite = pygame.image.load("sprites/O.png")
    x_sprite = pygame.image.load("sprites/X.png")

    # Variables posicionals:
    posicions_columnes = [(111, 256), (271, 432), (447, 592)]  # <- Són X
    posicions_files = [(31, 160), (175, 320), (335, 464)]  # <- Són Y

    # Variables lògiques
    tauler = genera_tauler()
    victoria = False
    guanyador = None

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # -------- Main Program Loop -----------
    while not done:
        # --- Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONUP:
                if not victoria:
                    victoria, guanyador = fer_moviment(
                        tauler, posicions_columnes, posicions_files)
                else:
                    victoria = False
                    tauler = genera_tauler()
        # --- Game logic should go here

        # --- Screen-clearing code goes here

        # Here, we clear the screen to white. Don't put other drawing commands
        # above this, or they will be erased with this command.

        # If you want a background image, replace this clear with blit'ing the
        # background image.
        screen.fill(WHITE)

        # --- Drawing code should go here
        mostrar_tauler(screen, tauler, tauler_sprite, o_sprite,
                       x_sprite, posicions_columnes, posicions_files)

        if victoria:
            mostrar_guanyador(screen, guanyador, font, BLACK)
        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # --- Limit to 60 frames per second
        clock.tick(60)

    # Close the window and quit.
    pygame.quit()


if __name__ == '__main__':
    main()

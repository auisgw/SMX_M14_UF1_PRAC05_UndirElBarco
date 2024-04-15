import pygame
import random


def generar_tauler():
    return [["-" for _ in range(10)] for _ in range(10)]


def comprovar_dispar(tauler, fila, columna, vaixell):
    return 0 <= fila < 10 and 0 <= columna < 10 and tauler[fila][columna] == vaixell and (tauler[fila][columna] := "X")


def col·locar_vaixells(tauler):
    vaixells = [(5, "Portaavions"), (4, "Creuer"),
                (3, "Destructor"), (2, "Submarí")]
    for longitud, nom in vaixells:
        while True:
            orientacio = random.choice(("horitzontal", "vertical"))
            fila_inicial = random.randint(
                0, 10 - longitud if orientacio == "horitzontal" else 9)
            columna_inicial = random.randint(0, 10)
            if es_posicio_valida(tauler, fila_inicial, columna_inicial, longitud, orientacio):
                colocar_vaixell(tauler, fila_inicial,
                                columna_inicial, longitud, orientacio, nom)
                break


def es_posicio_valida(tauler, fila_inicial, columna_inicial, longitud, orientacio):
    if orientacio == "horitzontal":
        return fila_inicial + longitud - 1 < 10 and all(tauler[fila_inicial][columna] == "-" for columna in range(columna_inicial, columna_inicial + longitud))
    else:
        return columna_inicial + longitud - 1 < 10 and all(tauler[fila][columna_inicial] == "-" for fila in range(fila_inicial, fila_inicial + longitud))


def col·locar_vaixell(tauler, fila_inicial, columna_inicial, longitud, orientacio, nom):
    if orientacio == "horitzontal":
        for columna in range(columna_inicial, columna_inicial + longitud):
            tauler[fila_inicial][columna] = nom
    else:
        for fila in range(fila_inicial, fila_inicial + longitud):
            tauler[fila][columna] = nom


def mostrar_tauler(tauler):
    for fila in tauler:
        print(" ".join(fila))


def fer_dispar_jugador(tauler, vaixells):
    while True:
        try:
            fila = int(input("Fila (0-9): "))
            columna = int(input("Columna (0-9): "))
            if 0 <= fila < 10 and 0 <= columna < 10:
                break
            else:
                print("Posició no vàlida. Introdueix una fila i columna entre 0 i 9.")
        except ValueError:
            print("Entrada no vàlida. Introdueix números enters.")

    encertat = comprovar_dispar(tauler, fila, columna, "Portaavions")
    if not encertat:
        encertat = comprovar_dispar(tauler, fila, columna, "Creuer")
    if not encertat:
        encertat = comprovar_dispar(tauler, fila, columna, "Destructor")
    if not encertat:
        encertat = comprovar_dispar(tauler, fila, columna, "Submarí")

    if encertat:
        print("Toca un vaixell!")
    else:
        print("Aigua!")

    vaixells_enfonsats = comprovar_vaixells_enfonsats(tauler, vaixells)
    return encertat, vaixells_enfonsats


def comprovar_vaixells_enfonsats(tauler, vaixells):
    vaixells_enfonsats = 0
    for nom, longitud in vaixells:
        tots_enfonsats = True
        for fila in range(10):
            for columna in range(10):
                if tauler[fila][columna] == nom:
                    tots_enfonsats = False
                    break
        if tots_enfonsats:
            vaixells_enfonsats += 1
    return vaixells_enfonsats
huidgifsdcdfauidvfa

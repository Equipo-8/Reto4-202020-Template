"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal
 *
 """


import sys
import config
from App import controller
from DISClib.ADT import stack
import timeit
assert config

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Variables
# ___________________________________________________

bikefile = '201801-2-citibike-tripdata.csv'
initialStation = 0

recursionLimit = 20000
# ___________________________________________________
#  Menu principal
# ___________________________________________________


def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de citibike")
    print("3- Calcular componentes conectados ")
    print("4- Determinar si existe una ruta circular")
    print("5- Hallar las estaciones criticas ")
    print("6- Ruta turistica por resistencia ")
    print("7- Recomendador de rutas por rango de edad ")
    print("8- Ruta de interes turistico ")
    print("9- Identificacion de estaciones para publicidad ")
    print("10- Identificacion de bicicletas para mantenimiento ")
    print("0- Salir")
    print("*******************************************")


def optionTwo():
    print("\nCargando información de rutas de bicicletas en NY ....")
    controller.loadTrips(cont)
    numedges = controller.totalConnections(cont)
    numvertex = controller.totalStops(cont)
    print('Numero de vertices: ' + str(numvertex))
    print('Numero de arcos: ' + str(numedges))
    print('El limite de recursion actual: ' + str(sys.getrecursionlimit()))
    sys.setrecursionlimit(recursionLimit)
    print('El limite de recursion se ajusta a: ' + str(recursionLimit))


def optionThree():
    print('El número de componentes conectados es: ' +
          str(controller.connectedSCC(cont)))
    e=controller.searchSCC(cont,id1,id2)
    if e:
        print("La estación "+id1+" está fuertemente conectada con la estación "+id2)
    else:
        print("Las estaciones no están fuertemente conectadas")


def optionFour():
    asd = controller.sccGraph(cont)
    print(asd)



def optionFive():
    haspath = controller.getCriticalStations(cont, destStation)
    print('Las estaciones criticas son las siguientes : ')
    print(haspath)


def optionSix():
    path = controller.resistance_paths(cont, station, resistance)
    print('Los caminos posibles son :')
    for i in path.keys():
        if path[i] is not None :
            print('Hacia '+str(i)+'= ')
            print(path[i])
            print('')


def optionSeven():
    maxvert, maxdeg = controller.recomendPaths(cont)
    print('Estación: ' + maxvert + '  Total rutas servidas: '
          + str(maxdeg))

def optionEight():
    woow= controller.amazingPlace(cont)

    print(woow)


def optionNine():
    woow= controller.identifyforpublicity(cont)

    print(woow)


def optionTen():
    woow= controller.identifybikesformaintenance(cont)

    print(woow)
"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs[0]) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init()

    elif int(inputs[0]) == 2:
        executiontime = timeit.timeit(optionTwo, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 3:
        id1=str(input('Ingrese el id de la primera estación: '))
        id2=str(input('Ingrese el id de la segunda estación: '))
        executiontime = timeit.timeit(optionThree, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 4:
        idstart= input('Ingrese el identificador de la estacion de inicio :')
        range_time= input('Ingrese el rango de tiempo disponible en minutos (Ej: 120-180) ')
        executiontime = timeit.timeit(optionFour, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 5:
        destStation = input("Estación destino (Ej: 15151-10): ")
        executiontime = timeit.timeit(optionFive, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 6:
        station = input("Estación inicial (Ej: 15151-10): ")
        resistance = int(input("cuanto aguantas bro???? : "))
        executiontime = timeit.timeit(optionSix, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 7:
        executiontime = timeit.timeit(optionSeven, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 8:
        executiontime = timeit.timeit(optionEight, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 9:
        executiontime = timeit.timeit(optionNine, number=1)
        print("Tiempo de ejecución: " + str(executiontime))
    
    elif int(inputs[0]) == 10:
        executiontime = timeit.timeit(optionTen, number=1)
        print("Tiempo de ejecución: " + str(executiontime))


    else:
        sys.exit(0)
sys.exit(0)

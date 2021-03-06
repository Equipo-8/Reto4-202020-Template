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

bikefile = '201801-4-citibike-tripdata.csv'
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
    print("9- Identificacion de bicicletas para mantenimiento ")
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
    asd = controller.sccGraph(cont,range_time,range_time2,idstart)
    if len(asd)>0:
        for each in asd:
            print("\n")
            print("Resultados: \n")
            print("La primera estación que debes tomar después de la estación "+idstart+" es: "+each['First'])
            print("La última estación a la cuál debes llegar antes de volver al inicio es: "+each['Last'])
            print("Esta opción de ruta durará: "+str(round(each['Duracion'],2))+" minutos")
            print("\n")
    else:
        print("No existen recomendaciones con los parámetros brindados")



def optionFive():
    execution=controller.estacionescirticas(cont)
    print(execution)


def optionSix():
    path = controller.resistance_paths(cont, station, resistance)
    print('Los caminos posibles son :')
    for i in path.keys():
        if path[i] is not None :
            print('Hacia '+str(i)+'= ')
            print(path[i])
            print('')


def optionSeven():
    haspath = controller.recomendadorRutas(cont, range_age,range_age2)
    if len(haspath)> 0:
        dtotal=0
        for each in haspath:
            dtotal+=each['Duracion']
            print("\n")
            print("Resultado: \n")
            print("Inicia en: "+each['Desde'])
            print("Termina en: "+each['Hasta'])
            print("Tardarás: "+str(round(each['Duracion'],2))+" minutos")
        print("En total tardarás: "+str(round(dtotal,2))+" minutos")
    else:
        "En este rango de edad no te podemos brindar una recomendación"

def optionEight():
    woow= controller.requerimiento_6(cont,la1,lo1,la2,lo2)
    print('')
    print('')
    print(woow[0])
    print(woow[1])
    print(woow[2])
    print(woow[3])
    print(woow[4])


def optionNine():
    woow=controller.bonito(cont,identificador,fecha)
    print('Las estaciones visitadas por esta bicicleta son : ')
    print(woow[0])
    print('Tiempo total de uso : ' + str(woow[1]//60)+ ' minutos.')
    print('Tiempo total en desuso : ' + str(woow[2]//60)+ ' minutos.')


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
        range_time= int(input('Ingresa el límite inferior de tu disponibilidad de tiempo: '))
        range_time2= int(input('Ingresa el límite superior de tu disponibilidad de tiempo: '))
        executiontime = timeit.timeit(optionFour, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 5:
        executiontime = timeit.timeit(optionFive, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 6:
        station = input("Estación inicial (Ej: 15151-10): ")
        resistance = int(input("Ingrese su resistencia en minutos : "))
        executiontime = timeit.timeit(optionSix, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 7:
        range_age= int(input('Ingresa el límite inferior de tu edad: '))
        range_age2= int(input('Ingresa el límite superior de tu edad: '))
        executiontime = timeit.timeit(optionSeven, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 8:
        la1= float(input('Ingrese la latitud de su ubicacion actual : '))
        lo1= float(input('Ingrese la longitud de su ubicacion actual : '))
        la2= float(input('Ingrese la latitud de su lugar de destino : '))
        lo2= float(input('Ingrese la longitud de su lugar de destino : '))
        executiontime = timeit.timeit(optionEight, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 9:
        identificador= int(input('Ingresa el identificador de la bici: '))
        fecha= input('Ingrese una fecha en el formato "AA-MM-DD" :')
        executiontime = timeit.timeit(optionNine, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    else:
        sys.exit(0)
sys.exit(0)

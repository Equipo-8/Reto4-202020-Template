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

import config as cf
from App import model
import csv

"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________
def init():
    citibike = model.newAnalyzer()
    return citibike

# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________

def loadTrips(citibike):
    for filename in cf.os.listdir(cf.data_dir):
        if filename.endswith('.csv'):
            print('Cargando archivo: ' + filename)
            loadFile(citibike, filename)
    return citibike

def loadFile(citibike, tripfile):
    """
    """
    tripfile = cf.data_dir + tripfile
    input_file = csv.DictReader(open(tripfile, encoding="utf-8"),
                                delimiter=",")
    for trip in input_file:
        model.addTrip(citibike, trip)
    return citibike




# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________



def totalStops(analyzer):
    """
    Total de paradas de autobus
    """
    return model.totalStops(analyzer)


def totalConnections(analyzer):
    """
    Total de enlaces entre las paradas
    """
    return model.totalConnections(analyzer)


def connectedComponents(analyzer):
    """
    Numero de componentes fuertemente conectados
    """
    return model.connectedComponents(analyzer)


def minimumCostPaths(analyzer, initialStation):
    """
    Calcula todos los caminos de costo minimo de initialStation a todas
    las otras estaciones del sistema
    """
    return model.minimumCostPaths(analyzer, initialStation)


def hasPath(analyzer, destStation):
    """
    Informa si existe un camino entre initialStation y destStation
    """
    return model.hasPath(analyzer, destStation)


def minimumCostPath(analyzer, destStation):
    """
    Retorna el camino de costo minimo desde initialStation a destStation
    """
    return model.minimumCostPath(analyzer, destStation)


def servedRoutes(analyzer):
    """
    Retorna el camino de costo minimo desde initialStation a destStation
    """
    maxvert, maxdeg = model.servedRoutes(analyzer)
    return maxvert, maxdeg

def connectedSCC(analyzer):
    return model.numSCC(analyzer['connections'],analyzer) 
def searchSCC(analyzer,st1,st2):
    return model.sameCC(analyzer, st1, st2)
def sccGraph(graph):
    return model.rutacircular(graph['connections'])

def resistance_paths(analyzer,station,resistance):
    return model.requerimiento_4(analyzer,station,resistance)

def requerimiento_6(analyzer,la1,lo1,la2,lo2):
    return model.requerimiento_6(analyzer,la1,lo1,la2,lo2)


def sccGraph(graph,limit,limit2,vertex):
    return model.req2(graph['connections'],limit*60,limit2*60,vertex)

def recomendadorRutas(graph,limit,limit2):
    return model.recomendadorRutas(graph,limit,limit2)


def identifybikesformaintenance(cont,identificador,fecha):
    return model.identifybikesformaintenance(cont,identificador,fecha)
def estacionescirticas(citibike,trip):
    return model.req3(citibike,trip)

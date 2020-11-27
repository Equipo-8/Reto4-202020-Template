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
import config
import math 
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Graphs import bfs
from DISClib.Utils import error as error
assert config

"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""

# -----------------------------------------------------
#                       API
# -----------------------------------------------------
def newAnalyzer():
    """ Inicializa el analizador

   stops: Tabla de hash para guardar los vertices del grafo
   connections: Grafo para representar las rutas entre estaciones
   components: Almacena la informacion de los componentes conectados
   paths: Estructura que almancena los caminos de costo minimo desde un
           vertice determinado a todos los otros vértices del grafo
    """
    try:
        analyzer = {
                    'stops': None,
                    'connections': None,
                    'components': None,
                    'paths': None
                    }

        analyzer['stops'] = m.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=compareStopIds)

        analyzer['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              comparefunction=compareStopIds)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')




# Funciones para agregar informacion al grafo

def addTrip(citibike, trip):
    try:
        origin=trip['start station id']
        destination = trip['end station id']
        duration = int(trip['tripduration'])
        addStation(citibike, origin)
        addStation(citibike, destination)
        addConnection(citibike, origin, destination, duration)
    except Exception as exp:
        error.reraise(exp, 'model:addTrip')

def addStation(citibike, stationid):
    """
    Adiciona una estación como un vertice del grafo
    """
    if not gr.containsVertex(citibike ['connections'], stationid):
            gr.insertVertex(citibike ['connections'], stationid)
    return citibike

def addConnection(citibike, origin, destination, duration):
    """
    Adiciona un arco entre dos estaciones
    """
    edge = gr.getEdge(citibike ['connections'], origin, destination)
    if edge is None:
        gr.addEdge(citibike['connections'], origin, destination, duration)
    return citibike

def numSCC(graph,sc):
    sc = scc.KosarajuSCC(graph)
    return scc.connectedComponents(sc)
def sameCC(sc, station1, station2):
    sc = scc.KosarajuSCC(sc['connections'])
    return scc.stronglyConnected(sc, station1, station2)
def rutacircular(graph):
    sc = scc.KosarajuSCC(graph)
    listakeys=m.keySet(sc['idscc'])
    iterador=it.newIterator(listakeys)
    diccionarioconteito={}
    while it.hasNext(iterador):
        key=it.next(iterador)
        e=m.get(sc['idscc'], key)
        if e['value'] != None:
            lt=diccionarioconteito.get(e['value'],[])
            lt.append(key)
            diccionarioconteito[e['value']]=lt
    dictpekenho={}
    for each in diccionarioconteito:
        if len(diccionarioconteito[each])>1:
            dictpekenho[each]=diccionarioconteito[each]
    return dictpekenho


# ==============================
# Funciones de consulta
# ==============================
def connectedComponents(analyzer):
    """
    Calcula los componentes conectados del grafo
    Se utiliza el algoritmo de Kosaraju
    """
    analyzer['components'] = scc.KosarajuSCC(analyzer['connections'])
    return scc.connectedComponents(analyzer['components'])


def minimumCostPaths(analyzer, initialStation):
    """
    Calcula los caminos de costo mínimo desde la estacion initialStation
    a todos los demas vertices del grafo
    """
    analyzer['paths'] = djk.Dijkstra(analyzer['connections'], initialStation)
    return analyzer


def hasPath(analyzer, destStation):
    """
    Indica si existe un camino desde la estacion inicial a la estación destino
    Se debe ejecutar primero la funcion minimumCostPaths
    """
    return djk.hasPathTo(analyzer['paths'], destStation)


def minimumCostPath(analyzer, destStation):
    """
    Retorna el camino de costo minimo entre la estacion de inicio
    y la estacion destino
    Se debe ejecutar primero la funcion minimumCostPaths
    """
    path = djk.pathTo(analyzer['paths'], destStation)
    return path


def totalStops(analyzer):
    """
    Retorna el total de estaciones (vertices) del grafo
    """
    return gr.numVertices(analyzer['connections'])


def totalConnections(analyzer):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(analyzer['connections'])


def servedRoutes(analyzer):
    """
    Retorna la estación que sirve a mas rutas.
    Si existen varias rutas con el mismo numero se
    retorna una de ellas
    """
    lstvert = m.keySet(analyzer['stops'])
    itlstvert = it.newIterator(lstvert)
    maxvert = None
    maxdeg = 0
    while(it.hasNext(itlstvert)):
        vert = it.next(itlstvert)
        lstroutes = m.get(analyzer['stops'], vert)['value']
        degree = lt.size(lstroutes)
        if(degree > maxdeg):
            maxvert = vert
            maxdeg = degree
    return maxvert, maxdeg


def requerimiento_4(analyzer,station,resistance):

    try:
        recorrido= bfs.BreadhtFisrtSearch(analyzer['connections'],station)
        size= gr.numVertices(analyzer['connections'])
        vertexxx= gr.vertices(analyzer['connections'])
        dicc= {}
        for i in range(1,size):
            vertice= lt.getElement(vertexxx,i)
            if bfs.hasPathTo(recorrido,vertice):
                path= bfs.pathTo(recorrido,vertice)
                print(path)
            
                sizep= st.size(path)
                if sizep != 1 :
                    init= st.pop(path)
                    summ= 0
                    dicc[str(vertice)]= []
                    while sizep >= 2:
                        vertex2= st.pop(path)
                        if vertex2 is None :
                            break
                        arco= gr.getEdge(analyzer['connections'],init,vertex2)
                        summ+= arco['weight']
                        init= vertex2
                        if summ > resistance :
                            dicc[str(vertice)]= None
                        else: 
                            dicc[str(vertice)].append(arco)
                break
        return dicc
    except Exception as exp:
        error.reraise(exp, 'model;Req_4')


def requerimiento_6(analyzer,la1, lo1, la2, lo2):
    try:
        size= gr.numVertices(analyzer['connections'])
        vertexxx= gr.vertices(analyzer['connections'])
        min_s= 0 
        start= ''
        min_e= 0
        end= ''
        for i in range(0,size):
            vertice= lt.getElement(vertexxx,i)
            print(vertice)
            lat= vertice["start station latitude"]
            lon= vertice["start station longitude"]
            distance_to_start= get_distance(la1,lo1,lat,lon)
            distance_to_end= get_distance(la2,lon2,lat,lon)
            if i == 0 :
                min_s= distance_to_start
                start= vertice
                min_e= distance_to_end
                end= vertice
            else:
                if distance_to_start < min_s :
                    min_s= distance_to_start
                    start= vertice
                if distance_to_end < min_e :
                    min_e= distance_to_end
                    end= vertice
        init= start['start station id']
        des= end['start station id']
        search= djk.Dijkstra(analyzer['connections'],init)
        path= djk.pathTo(search,des)
        time= 0
        sizep= st.size(path)
        rutaa= []
        for i in range(0,sizep):
            element= st.pop(path)
            rutaa.append(element)
        for i in range(0,len(rutaa),2):
            vertex1= rutaa[i]
            vertex2= rutaa[i+1]
            arco= gr.getEdge(analyzer['connections'],vertex1,vertex2)
            time+= arco['weight']
        p1='La estacion mas cercana a donde usted se encuentra en este momento es :' + str(init)
        p2='La estacion mas cercana a su destino es :' + str(des)
        p3='El camino mas corto entre estas dos estaciones es :'
        p4='El tiempo estimado para realizar esta ruta es :' + str(time)
        return p1,p2,p3,rutaa,p4
    except Exception as exp:
        error.reraise(exp, 'model;Req_6')

        

                 


            









        
# ==============================
# Funciones Helper
# ==============================
 
def get_distance(lat1,lon1,lat2,lon2):
    R= 6373.0
    lat1= math.radians(lat1)
    lat2= math.radians(lat2)
    lon1= math.radians(lon1)
    lon2= math.radians(lon2)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance= R * c
    return distance
# ==============================
# Funciones de Comparacion
# ==============================

def compareStopIds(stop, keyvaluestop):
    """
    Compara dos estaciones
    """
    stopcode = keyvaluestop['key']
    stop=int(stop)
    stopcode=int(stopcode)
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1


def compareroutes(route1, route2):
    """
    Compara dos rutas
    """
    if (route1 == route2):
        return 0
    elif (route1 > route2):
        return 1
    else:
        return -1

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
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.ADT import stack
from DISClib.DataStructures import graphstructure as gs
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dfs
from DISClib.Algorithms.Graphs import dijsktra as djk
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





def addTrip(citibike, trip):
    try:
        origin=trip['start station id']
        destination = trip['end station id']
        duration = int(trip['tripduration'])
        if not (origin==destination):
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
def rutacircular(graph,limite,verticestart):
    rutas=lt.newList()
    buskeda=dfs.DepthFirstSearch(graph,verticestart)
    sc = scc.KosarajuSCC(graph)
    componente_inicio=m.get(sc['idscc'],verticestart)
    iterator=it.newIterator(m.keySet(sc['idscc']))
    verticesfuertementeconec=lt.newList(cmpfunction=compareStopIds)
    while it.hasNext(iterator):
        proximo=it.next(iterator)
        c_proximo=m.get(sc['idscc'],proximo)
        if c_proximo == componente_inicio and proximo != verticestart: #Que el componente sea el mismo, y que a su vez sea diferente al vértice de inicio
            lt.addLast(verticesfuertementeconec, proximo)
    iterator=newIterator(verticesfuertementeconec)
    validadora=lt.newList(cmpfunction=compareroutes)
    while it.hasNext(iterator):
        rutanueva=it.next(iterator)
        busquedaruta=dfs.DepthFirstSearch(graph,rutanueva)
        path=dfs.pathTo(buskeda,rutanueva)
        path_or=dfs.pathTo(busquedaruta,verticestart)
        size=st.size(path)
        sizeor=st.size(path_or)
        timeextra=size*1200 #1200 segundos -> 20 mins
        timeextra2=(sizeor-1)*1200
        timefull=timeextra+timeextra2
        infoarc={'time':timefull,
                'i':0,
                'path':{}}
        if timefull<limite:
            info,info=construirRuta(graph,path,infoarc),construirRuta(graph,path_or,infoarc)
            info['Ending']=info['path'][info['i']-1]
        time=info['time']
        if time<=limit:
            info['path']=buildCadena(info)
            if lt.isPresent(validadora,info['path']) == 0:
                lt.addLast(rutas,info)
                lt.addLast(validador,info['path'])
    return rutas

def req2(grafo,limiteinf,limite,verticei):
    sc = scc.KosarajuSCC(grafo)
    componente_inicio=m.get(sc['idscc'],verticei)['value']
    iterator=it.newIterator(m.keySet(sc['idscc']))
    verticesfc=lt.newList(cmpfunction=compareroutes)
    while it.hasNext(iterator):
        proximo=it.next(iterator)
        c_proximo=m.get(sc['idscc'],proximo)['value']
        if c_proximo == componente_inicio: #Que el componente sea el mismo, y que a su vez sea diferente al vértice de inicio
            lt.addLast(verticesfc,proximo)
    adyacentes=gr.adjacents(grafo,verticei)
    iterator=it.newIterator(verticesfc)
    rutasposibles=[]
    while it.hasNext(iterator):
        proximo=it.next(iterator)
        if lt.isPresent(adyacentes,proximo):
            dfs3 = dfs.DepthFirstSearchSCC(grafo,proximo,verticesfc)
            if dfs.pathTowithLimiter(dfs3,verticei,grafo,limite) != None:
                rutachikita,tiempo=dfs.pathTowithLimiter(dfs3,verticei,grafo,limite)
                lt.removeLast(rutachikita)
                if limiteinf<tiempo<limite:
                    rutasposibles.append({"First":lt.firstElement(rutachikita),"Last":lt.lastElement(rutachikita),"Duracion":tiempo/60})
        
    return rutasposibles



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




# ==============================
# Funciones Helper
# ==============================

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
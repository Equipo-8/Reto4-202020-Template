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
import datetime
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
                    'agestartrank': None,
                    'agefinishrank': None,
                    'stops': None,
                    'connections': None,
                    'components': None,
                    'paths': None,
                    'nameverteces':None
                    }

        analyzer['stops'] = m.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=compareStopIds)

        analyzer['agestartrank'] = m.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=compareStopIds)

        analyzer['agefinishrank'] = m.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=compareStopIds)

        analyzer['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              comparefunction=compareStopIds)
        analyzer['nameverteces'] = m.newMap(numelements=10000,
                                     maptype='PROBING',
                                     comparefunction=compareStopIds)                                              
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')





def addTrip(citibike, trip):
    try:
        origin=trip['start station id']
        destination = trip['end station id']
        duration = int(trip['tripduration'])
        name=trip["start station name"]
        year=int(trip['birth year'])
        if not (origin==destination):
            addStation(citibike, origin)
            addStation(citibike, destination)
            addRankingstart(citibike,origin,year)
            addRankingfinish(citibike,destination,year)
            addConnection(citibike, origin, destination, duration)
            addnametrip(citibike,origin,name)
            addnametrip(citibike,destination,name)
    except Exception as exp:
        error.reraise(exp, 'model:addTrip')
def addnametrip(citybike,viaje,name):
    try:
        m.put(citybike["nameverteces"],viaje,name)
    except Exception as exp:
        error.reraise(exp, 'model:addnametrip')    




def addRankingstart(citibike,vertex,year):
    now=datetime.datetime.now()
    age=int(now.year)-year
    bigmap=citibike['agestartrank']
    if m.contains(bigmap,vertex):
        diccionario=m.get(bigmap,vertex)['value']
        quantity=diccionario.get(age,0)+1
        diccionario[age]=quantity
        m.put(bigmap,vertex,diccionario)  
    else:
        m.put(bigmap,vertex,{age:1})    
    return citibike
def addRankingfinish(citibike,vertex,year):
    now=datetime.datetime.now()
    age=int(now.year)-year
    bigmap=citibike['agefinishrank']
    if m.contains(bigmap,vertex):
        diccionario=m.get(bigmap,vertex)['value']
        quantity=diccionario.get(age,0)+1
        diccionario[age]=quantity
        m.put(bigmap,vertex,diccionario)  
    else:
        m.put(bigmap,vertex,{age:1})   
    return citibike 

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

def req2(grafo,limiteinf,limite,verticei):
    sc = scc.KosarajuSCC(grafo)
    componente_inicio=m.get(sc['idscc'],verticei)['value']
    iterator=it.newIterator(m.keySet(sc['idscc']))
    verticesfc=lt.newList(cmpfunction=compareroutes)
    while it.hasNext(iterator):
        proximo=it.next(iterator)
        c_proximo=m.get(sc['idscc'],proximo)['value']
        if c_proximo == componente_inicio: #Que el componente sea el mismo
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
def req3(citibike):
    

def recomendadorRutas(analizador,limiteinf,limitesup):
    listvertices=gr.vertices(analizador['connections'])
    iterator=it.newIterator(listvertices)
    mostsalida=[None,0]
    mostllegada=[None,0]
    ruta=[]
    while it.hasNext(iterator):
        verticerevisado=it.next(iterator)
        ctotal=0
        ctotal2=0
        for age in range(limiteinf,limitesup+1):
            if m.contains(analizador['agestartrank'],verticerevisado):
                diccionario=m.get(analizador['agestartrank'],verticerevisado)['value']
                cantidad=diccionario.get(age,0)
                ctotal+=cantidad
            if m.contains(analizador['agefinishrank'],verticerevisado):
                diccionario2=m.get(analizador['agefinishrank'],verticerevisado)['value']
                cantidad2=diccionario2.get(age,0)
                ctotal2+=cantidad2
        if ctotal>mostsalida[1]:
            mostsalida[1]=ctotal
            mostsalida[0]=verticerevisado
        if ctotal2>mostllegada[1]:
            mostllegada[1]=ctotal2
            mostllegada[0]=verticerevisado
    if mostsalida[0] != mostllegada[0]:
        search=djk.Dijkstra(analizador['connections'],mostsalida[0])
        resultado=djk.pathTo(search,mostllegada[0])
        iterator=it.newIterator(resultado)
        while it.hasNext(iterator):
            informacion=it.next(iterator)
            ruta.append({'Desde':informacion['vertexA'],'Hasta':informacion['vertexB'],'Duracion':informacion['weight']/60})
    return ruta

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
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
import datetime
import math
from DISClib.ADT.graph import gr
from DISClib.ADT import stack as st
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.DataStructures import arraylist
from DISClib.ADT import stack as st
from DISClib.DataStructures import listiterator as it
from DISClib.ADT import stack
from DISClib.DataStructures import graphstructure as gs
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import bfs
from DISClib.Algorithms.Graphs import dfs
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Graphs import bfs
from DISClib.DataStructures import heap
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
                    'nameverteces':None,
                    'countllegada':None,
                    'countsalida':None,
                    'heapsalida':None,
                    'heapllegada':None,
                    'heapllegadasalida':None,
                    'countllegadasalida':None
                    }

        analyzer['stops'] = m.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=compareStopIds)
        analyzer['coordinates']= m.newMap(numelements=2000,
                                     maptype='PROBING',
                                     comparefunction=compareStopIds)
        analyzer['coordinates_destiny']= m.newMap(numelements=2000,
                                     maptype='PROBING',
                                     comparefunction=compareStopIds)

        analyzer['agestartrank'] = m.newMap(numelements=2000,
                                     maptype='PROBING',
                                     comparefunction=compareStopIds)
        analyzer['countllegada'] = m.newMap(numelements=2000,
                                     maptype='PROBING',
                                     comparefunction=compareStopIds)
        analyzer['countllegadasalida'] = m.newMap(numelements=2000,
                                     maptype='PROBING',
                                     comparefunction=compareStopIds)
        analyzer['countsalida'] = m.newMap(numelements=2000,
                                     maptype='PROBING',
                                     comparefunction=compareStopIds)
        analyzer['heapsalida'] = heap.newHeap(comparadorheap)
        analyzer['heapllegada'] = heap.newHeap(comparadorheap)
        analyzer['heapllegadasalida'] = heap.newHeap(comparadorheap)
        analyzer['agefinishrank'] = m.newMap(numelements=2000,
                                     maptype='PROBING',
                                     comparefunction=compareStopIds)

        analyzer['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              comparefunction=compareStopIds)
        analyzer['nameverteces'] = m.newMap(numelements=2000,
                                     maptype='PROBING',
                                     comparefunction=compareStopIds) 
        analyzer['bikeid'] = m.newMap(numelements=1000,
                                     maptype='PROBING',
                                     comparefunction=compareStopIds) 
                                                     
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')





def addTrip(citibike, trip):
    try:
        origin=trip['start station id']
        olatitude= trip['start station latitude']
        olongitude= trip["start station longitude"]
        oname= trip["start station name"]
        destination = trip['end station id']
        dlatitude= trip['end station latitude']
        dlongitude= trip["end station longitude"]
        dname= trip["end station name"]
        duration = int(trip['tripduration'])
        name=trip["start station name"]
        year=int(trip['birth year'])
        identificador= int(trip['bikeid'])
        start= trip['starttime']
        end= trip['stoptime']
        if not (origin==destination):
            addStation(citibike, origin)
            addCoordinates(citibike,oname,origin,olatitude,olongitude)
            addStation(citibike, destination)
            addCoordinates_destiny(citibike,dname,destination,dlatitude,dlongitude)
            addRankingstart(citibike,origin,year)
            addRankingfinish(citibike,destination,year)
            addConnection(citibike, origin, destination, duration)
            addnametrip(citibike,origin,name)
            addnametrip(citibike,destination,name)
            addBikeID(citibike,identificador,oname,dname,duration,start,end)
            countllegada(citibike,origin,destination)
    except Exception as exp:
        error.reraise(exp, 'model:addTrip')
def countllegada(citibike,vertexa,vertexb):
    llegada=citibike['countllegada']
    salida=citibike['countsalida']
    llegadasalida=citibike['countllegadasalida']
    if not m.contains(llegada,vertexa):
        m.put(llegada,vertexa,1)
    else:
        m.put(llegada,vertexa,m.get(llegada,vertexa)['value']+1)
    if not m.contains(salida,vertexb):
        m.put(salida,vertexb,1)
    else:
        m.put(salida,vertexb,m.get(salida,vertexb)['value']+1)
    if not m.contains(llegadasalida,vertexa):
        m.put(llegadasalida,vertexa,1)
    else:
        m.put(llegadasalida,vertexa,m.get(llegadasalida,vertexa)['value']+1)
    if not m.contains(llegadasalida,vertexb):
        m.put(llegadasalida,vertexb,1)
    else:
        m.put(llegadasalida,vertexb,m.get(llegadasalida,vertexb)['value']+1)
    return citibike


def addCoordinates(citibike,name,origin,latitude,longitude):
    if not m.contains(citibike['coordinates'],origin):
        m.put(citibike['coordinates'],origin,{'name': name, 'latitude': latitude, 'longitude':longitude})
    return citibike

def addCoordinates_destiny(citibike,name,origin,latitude,longitude):
    if not m.contains(citibike['coordinates_destiny'],origin):
        m.put(citibike['coordinates_destiny'],origin,{'name': name, 'latitude': latitude, 'longitude':longitude})
    return citibike

def addnametrip(citybike,viaje,name):
    try:
        m.put(citybike["nameverteces"],viaje,name)
    except Exception as exp:
        error.reraise(exp, 'model:addnametrip')    



def addBikeID(citibike, identificador, vertexA , vertexB, weight,start,end):
    """
    Crea '
    """
    if m.contains(citibike['bikeid'],identificador):        
        value= m.get(citibike['bikeid'],identificador)['value'].append({'V1':vertexA,'V2':vertexB,'peso':weight,'start':start,'end':end})
    else:
        value= [{'V1':vertexA,'V2':vertexB,'peso':weight,'start':start,'end':end}]
        m.put(citibike['bikeid'],identificador,value)
    return citibike

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

def req2(analizer,limiteinf,limite,verticei):
    grafo=analizer['connections']
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
                    rutasposibles.append({"First":m.get(analizer['nameverteces'],lt.firstElement(rutachikita))['value'],"Last":m.get(analizer['nameverteces'],lt.lastElement(rutachikita))['value'],"Duracion":tiempo/60})
        
    return rutasposibles

def req3(analizador):
    llegada,salida,salidallegada=generateheap(analizador)
    topllegada=[]
    topsalida=[]
    lessvisited=[]
    for x in range(1,4):
        nombrellegada=m.get(analizador['nameverteces'],llegada[len(llegada)-x]['key'])['value']
        llegada[len(llegada)-x]['key']=nombrellegada
        
        nombresalida=m.get(analizador['nameverteces'],salida[len(salida)-x]['key'])['value']
        salida[len(salida)-x]['key']=nombresalida

        nombresalidallegada=m.get(analizador['nameverteces'],salidallegada[x]['key'])['value']
        salidallegada[x]['key']=nombresalidallegada

        topllegada.append(llegada[len(llegada)-x])
        topsalida.append(salida[len(salida)-x])
        lessvisited.append(salidallegada[x])
    return topllegada,topsalida,lessvisited
def generateheap(analizador):
    
    llavesllegada=m.keySet(analizador['countllegada']) 
    
    llavessalida=m.keySet(analizador['countsalida'])
    
    llavessalidallegada=m.keySet(analizador['countllegadasalida'])
    
    iterator=it.newIterator(llavesllegada)

    llegada=[]
    salida=[]
    salidallegada=[]
    while it.hasNext(iterator):
        revisado=m.get(analizador['countllegada'],it.next(iterator))
        llegada.append(revisado)
    iterator2=it.newIterator(llavessalida)
    while it.hasNext(iterator2):
        revisado=m.get(analizador['countsalida'],it.next(iterator2))
        salida.append(revisado)
    iterator3=it.newIterator(llavessalidallegada)
    while it.hasNext(iterator3):
        revisado=m.get(analizador['countllegadasalida'],it.next(iterator3))
        salidallegada.append(revisado)
    llegada=sorted(llegada, key = lambda i: i['value'])
    salida=sorted(salida, key = lambda i: i['value'])
    salidallegada=sorted(salidallegada, key = lambda i: i['value'])
    return llegada,salida,salidallegada
        
def comparadorheap(ruta1,ruta2):
    route1=ruta1['value']
    route2=ruta2['value']
    if (route1 == route2):
        return 0
    elif (route1 > route2):
        return 1
    else:
        return -1
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
            ruta.append({'Desde':m.get(analizador['nameverteces'],informacion['vertexA'])['value'],'Hasta':m.get(analizador['nameverteces'],informacion['vertexB'])['value'],'Duracion':informacion['weight']/60})
    return ruta

def requerimiento_4(analyzer,station,resistance):

    try:
        resistance=resistance*60
        recorrido= bfs.BreadhtFisrtSearch(analyzer['connections'],station)
        size= gr.numVertices(analyzer['connections'])
        vertexxx= gr.vertices(analyzer['connections'])
        dicc= {}
        for i in range(1,size):
            ids= lt.getElement(vertexxx,i)
            vertice= m.get(analyzer['coordinates_destiny'],ids)['value']['name']
            if bfs.hasPathTo(recorrido,ids):
                path= bfs.pathTo(recorrido,ids)
                sizep= st.size(path)
                if sizep != 1 :
                    init= st.pop(path)
                    summ= 0
                    dicc[vertice]= []
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
                            dicc[str(vertice)].append(poner_bonita_la_ruta(analyzer,arco))
        return dicc
    except Exception as exp:
        error.reraise(exp, 'model;Req_4')


def requerimiento_6(analyzer,la1, lo1, la2, lo2):
    try:
        start= minor_distance_to(analyzer['coordinates'],la1,lo1)
        end= minor_distance_to(analyzer['coordinates_destiny'],la2,lo2)
        init= start[0]
        des= end[0]
        search= djk.Dijkstra(analyzer['connections'],init)
        path= djk.pathTo(search,des)
        time= 0
        if path is not None :
            rutaa= []
            while not st.isEmpty(path) :
                element= st.pop(path)
                rutaa.append(poner_bonita_la_ruta(analyzer,element))
                time+= element['weight']
            p1='La estacion mas cercana a donde usted se encuentra en este momento es : ' + start[1]
            p2='La estacion mas cercana a su destino es : ' + end[1]
            p3='El camino mas corto entre estas dos estaciones es : '
            p4='El tiempo estimado para realizar esta ruta es : ' + str(time/60) + ' minutos'
            return p1,p2,p3,rutaa,p4
    except Exception as exp:
        error.reraise(exp, 'model;Req_6')

def bonito(analyzer,bikeid,fecha_dada):
    try:
        time_use= 0
        visitados= []
        data= m.get(analyzer['bikeid'],bikeid)['value']
        for i in range(0,len(data)):
            fecha = data[i]['start'].split()
            if fecha[0] == fecha_dada:
                time_use+= data[i]['peso']
                if  data[i]['V1'] not in visitados:
                    visitados.append(data[i]['V1'])
                if  data[i]['V2'] not in visitados:
                    visitados.append(data[i]['V2'])
        time_no_use = 24*3600 - time_use
        return visitados,time_use,time_no_use
    except Exception as exp:
        error.reraise(exp, 'model;Fallo en el bono')



def poner_bonita_la_ruta(analyzer,arco):
    vertexA= m.get(analyzer['coordinates'],arco['vertexA'])['value']['name']
    vertexB= m.get(analyzer['coordinates_destiny'],arco['vertexB'])['value']['name']
    hola= {'From':vertexA,'To':vertexB,'duracion en minutos':arco['weight']/60}
    return hola


def minor_distance_to(map,lat,lon):
    size= m.size(map)
    lista= m.keySet(map)
    minimo= 0
    vertex= None
    name= None
    for i in range(0,size):
        key= lt.getElement(lista,i)
        element= m.get(map,key)
        lat2= float(element['value']['latitude'])
        lon2= float(element['value']['longitude'])
        distance= get_distance(lat,lon,lat2,lon2)
        if i==0:
            minimo= distance
            vertex= key
            name= element['value']['name']
        else:
            if distance < minimo :
                minimo= distance
                vertex= key
                name= element['value']['name']
    return vertex,name



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
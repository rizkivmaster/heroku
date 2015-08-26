#ultimate busway parser
from bs4 import BeautifulSoup
import urllib2
import re



def scrap(link):
    html = urllib2.urlopen(link)
    scrapper = BeautifulSoup(html,'html.parser')
    return scrapper

def rowParser(text):
    innerText = re.findall('[a-zA-Z0-9 ]+[a-zA-Z0-9]',text)
    if(not len(innerText)==0):
        return re.sub('[^a-zA-Z0-9 ]+','',innerText[0]).strip()
    else:
        return ''
    
def multiRowParser(text):
    textLines = text.split('\n')
    returnLine = []
    for line in textLines:
        innerText = re.findall('[a-zA-Z0-9 ]+[a-zA-Z0-9]',line)
        if(not len(innerText)==0):
            returnLine.append(re.sub('[^a-zA-Z0-9 ]+','',innerText[0]))
        else:
            return ''
    return ','.join(returnLine)

def multiHrefParser(element):
    aBuffers = []
    returnLists = set()
    returnMaps = dict()
    items = element.find_all('a')
    for item in items:
        if(item.name=='a'):
            if(item.has_attr('class') and item['class'][0]=='image'):
                aBuffers.append(item['title'])
            else:
                for abuffer in aBuffers:
                    returnLists.add(abuffer+'_'+str(item.getText()))
                    returnMaps[abuffer+'_'+str(item.getText())]=((abuffer,str(item.getText())))
                aBuffers = []
        if(not item.next_sibling==None):
            if(not item.next_sibling.string==None):
                if((not item.next_sibling.strip()=='')):
                    for abuffer in aBuffers:
                        returnLists.add(abuffer+'_'+str(item.next_sibling).strip())
                        returnMaps[abuffer+'_'+str(item.next_sibling).strip()]=((abuffer,str(item.next_sibling).strip()))
                    aBuffers = []
    return returnLists,returnMaps
    
scapper = scrap("https://en.wikipedia.org/wiki/TransJakarta_Corridors")
mainContent = scapper.find('div',attrs={'id':'mw-content-text'})
tables = mainContent.find_all('table',{'class':'wikitable'})
stationSet = set()
stationMap = dict()
trayek= []
suggestionList = list()
print('finish busway list')
# main train route
for table in tables:
    rows = table.find_all('tr')
    title = rows[0].find('th').find('a')['title']
#     print('========================================')
#     print(title)
#     print('========================================')
    newrows = rows[2:]
    points = []
    for row in newrows:
        name = rowParser(row.find_all('td')[1].getText())
        stationSet.add(title+'_'+name)
        stationMap[title+'_'+name]=(title,name)
        points.append(title+' '+name)
        suggestionList.append((title+' '+name,name))
        suggestionList.append((title+' '+name,name.lower()))
        suggestionList.append((title+' '+name,title+' '+name))
        suggestionList.append((title+' '+name,(title+' '+name).lower()))
#         print(title+'_'+name)
    trayek.extend(map(lambda x: '{0},{1},{2},1000,20'.format(x[0],x[1],title),zip(points[:-1],points[1:])))
    
#     train transfer lines
for table in tables:
    rows = table.find_all('tr')
    title = rows[0].find('th').find('a')['title']
#     print('========================================')
#     print(title)
#     print('========================================')
    newrows = rows[2:]
    for row in newrows:
       #print(re.sub('[^a-zA-Z0-9 ]+','',row.find_all('td')[1].text))
        text=rowParser(row.find_all('td')[1].getText())
        transferSet,transferMap = multiHrefParser(row.find_all('td')[2])
        for transferKey in transferSet:
            if(text in transferMap[transferKey][1]):
                trayek.append('{0} {1},{2} {3},Jalan Kaki,0,10'.format(title,text,transferMap[transferKey][0],transferMap[transferKey][1]))    
#                 print('Transfer : from {0}_{1} to {2}_{3}'.format(title,text,transferMap[transferKey][0],transferMap[transferKey][1]))
#           train station nearbies          
for table in tables:
    rows = table.find_all('tr')
    title = rows[0].find('th').find('a')['title']
#     print('========================================')
#     print(title)
#     print('========================================')
    newrows = rows[2:]
    for row in newrows:
       #print(re.sub('[^a-zA-Z0-9 ]+','',row.find_all('td')[1].text))
        text=rowParser(row.find_all('td')[1].getText())
        try:
            nearbySet,nearbyMap = multiHrefParser(row.find_all('td')[3])
            for key in nearbySet:
                cleanedNearby = re.sub('Bus Terminal','',nearbyMap[key][1])
                cleanedNearby = re.sub('Station','',cleanedNearby)
                cleanedNearby = cleanedNearby.strip()
                suggestionList.append((nearbyMap[key][0]+' '+cleanedNearby,cleanedNearby))
                suggestionList.append((nearbyMap[key][0]+' '+cleanedNearby,cleanedNearby.lower()))
                suggestionList.append((nearbyMap[key][0]+' '+cleanedNearby,nearbyMap[key][0]+' '+cleanedNearby))
                suggestionList.append((nearbyMap[key][0]+' '+cleanedNearby,(nearbyMap[key][0]+' '+cleanedNearby).lower()))
#                 print('{0}_{1} is near to {2}_{3}'.format(title,text,nearbyMap[key][0],cleanedNearby))
                trayek.append('{3} {0},{1} {2},Jalan Kaki,0,10'.format(text,nearbyMap[key][0],cleanedNearby,title))
        except Exception,err:
            pass

kascrapper= scrap('https://en.wikipedia.org/wiki/KA_Commuter_Jabodetabek')
class LinkedHash(list):
    def __hash__(self):
        return '.'.join(self).__hash__()
print('finish train list')
# trayek = []
waypoints = set()
waypointMap = dict()
for ka in kascrapper.select('dl > dd > b'):
    line = re.findall('[a-zA-Z0-9 ]+[a-zA-Z0-9]',ka.parent.parent.previousSibling.previousSibling.string)[0].strip()
    waypoint = LinkedHash(map(lambda x:x.strip(),re.sub(u'\u2192',',',re.sub('\\.','',ka.parent.getText())).split(',')))
    suggestionList.extend(map(lambda x:('Train Station '+x,x),waypoint))
    suggestionList.extend(map(lambda x:('Train Station '+x,x.lower()),waypoint))
    suggestionList.extend(map(lambda x:('Train Station '+x,'Train Station '+x),waypoint))
    suggestionList.extend(map(lambda x:('Train Station '+x,('Train Station '+x).lower()),waypoint))
    waypointMap[line] = waypoint
for key in waypointMap.keys():
    waypoint = waypointMap[key]
    trayek.extend(map(lambda x:'Train Station {0},Train Station {1},Commuter {2},1000,20'.format(x[0],x[1],key),zip(waypoint[1:],waypoint[:-1])))
    
# print('=================================TRAYEK==================================')
# for tray in trayek:
#     print(tray)
    
class TrieNode:
    def __init__(self):
        self.childNodes = dict()
        self.words = set()
        self.prefixCount = 0
        

    
def addWord(node,word,rest):
    node.words.add(word)
    if(len(rest)==0):
        return node
    nextchar = rest[0]
    if(node.childNodes.has_key(nextchar)):
        node.childNodes[nextchar] = addWord(node.childNodes[rest[0]],word,rest[1:])
    else:
        newnode = TrieNode()
        newnode.prefixCount = node.prefixCount+1
        node.childNodes[nextchar] = addWord(newnode,word,rest[1:])    
    return node

def dfs(node,rest):
    if(len(rest)==0):
        return node;
    else:
        if(node.childNodes.has_key(rest[0])):
            return dfs(node.childNodes[rest[0]],rest[1:]);
        else:
            return None;
        
node = TrieNode()

for name,key in suggestionList:
    node = addWord(node,name,key)


class PQueue(object):
    def __init__(self):
        self.datas = list()
    
    def put(self,data,priority):
        pair = (data,priority)
        self.datas.append(pair)
        self.datas.sort(cmp=lambda x,y: x[1]-y[1])
        
    def deque(self):
        if(len(self.datas)==0):
            return None
        else:
            return self.datas.pop(0)[0]
    def size(self):
        return len(self.datas)
    
class Graph():
    #vertices in list of integer or string
    #edges in dict; vertices as key; vertices X distance as value
    def __init__(self,vertices,edges):
        self.vertices =vertices
        self.edges = edges
        
class Mode(object):
        trnsName = None
        price = None
        eta = None
        destination = None
        origin = None
        
        def cost(self):
            return self.eta
        def __str__(self):
            return '{0} {1} {2} {3} {4}'.format(self.origin,self.trnsName,self.destination,self.price,self.eta)
import copy
def parseMode(text):
    arr = text.split(',')
    mode = Mode()
    mode.trnsName = arr[2]
    mode.price = int(arr[3])
    mode.eta = int(arr[4])
    mode.origin = arr[0]
    mode.destination = arr[1]
    mode2 = copy.deepcopy(mode)
    mode2.origin = mode.destination
    mode2.destination = mode.origin
    return (mode,mode2)
def parseModeList(modeList):
    newModeList = map(parseMode,modeList)
    refinedList = []
    for modes in newModeList:
        refinedList.append(modes[0])
        refinedList.append(modes[1])
    return refinedList   

def buildGraph(modeList):
    vertices = set()
    edges = dict()
    for mode in modeList:
        vertices.add(mode.origin)
        vertices.add(mode.destination)
        if(not edges.has_key(mode.origin)):
            edges[mode.origin] = []
        edges[mode.origin].append(mode)
    return Graph(vertices,edges)
#     transportList = ['Jakarta,Bekasi,Busway,5,30',
#                     'Bekasi,Bogor,Ojek,3,10',
#                     'Bekasi,Bogor,Busway,5,30',
#                     'Jakarta,Bogor,Busway,4,25',
#                     'Jakarta,Bogor,Ojek,2,8',
#                     'Jakarta,Depok,Busway,2,13',
#                     'Jakarta,Depok,Ojek,1,20',
#                     'Depok,Bogor,Busway,1,5',
#                     'Depok,Bogor,Ojek,1,3']
transportList=trayek
graph = buildGraph(parseModeList(transportList))
def find(graph, source):
    MAX_DIST = 10000000000
    #dict <city,list of transports>
    transport = dict()
    #dict <city,real>
    cost = dict()
    #dict <city,city>
    previous = dict()
    #dict <city,boolean>
    visited = dict()
    pq = PQueue()
        
    previous[source] = source         
    cost[source]= 0
    transport[source] = [(0,0,[])]
    visited[source]=False
    
    for city in graph.vertices:
        if(city != source):
            cost[city] = MAX_DIST
            transport[city] = []
            previous[city] = None
            visited[city]=False
        pq.put(city,cost[city])
        
#     print(pq.datas)
    while(pq.size()>0):
        city = pq.deque()
#         print("take ",city)
        visited[city]=True
        modeList = graph.edges[city]
        for mode in modeList: 
                    nextCity = mode.destination
                    if(not visited[nextCity]):
#                         print(" observe {0} using {2} from {1}".format(nextCity,city,mode.trnsName))
                        relativeCost = mode.cost()
                        globalCost = cost[nextCity]
                        alternativeCost = cost[city]+relativeCost
                        if(alternativeCost < globalCost):
                            cost[nextCity] = alternativeCost
                            previous[nextCity] = city
                            pq.put(nextCity,cost[nextCity])
#                             print("  assign cost to {0} as {1}".format(nextCity,cost[nextCity]))
                        for trans in transport[city]:
                            #debug
                            #TODO make hashable pathway to elude the pathway duplication
#                             print('   append trans from {0}'.format(city))
                            costCurrent = trans[0]
                            priceCurrent = trans[1]
                            newModeList = copy.deepcopy(trans[2])
                            newModeList.append(mode)
                            transport[nextCity].append((costCurrent+mode.cost(),priceCurrent+mode.price,newModeList))    
                            #debug
#                             for modeX in newModeList:
#                                 print('     '+str(modeX))
                        tempMap = dict()
                        tempList = list()
                        for trx in transport[nextCity]:
                            tempMap[str(trx[0])+str(trx[1])]=trx
                        for key in tempMap.keys():
                            tempList.append(tempMap[key])
                        tempList.sort(cmp=lambda x,y: x[0]-y[0])
                        transport[nextCity] = tempList[:3]
    return cost,previous,transport

def getDirection(source,destination):
    result = list()
    cost,previous,transport = find(graph,source)
    for key in [destination]:
        trans = transport[key]
        for tran in trans:
            temp = list()
            cost = tran[0]
            price = tran[1]
            modeList = tran[2]
            temp.append('cost time for {0} is {1} with price {2}'.format(key,cost,price))
            for mode in modeList:
                temp.append('     '+str(mode))
            result.append(temp)
    return result
    
def retrieveSuggestion(node,word):
    node = dfs(node,word)
    if(node==None):
        return []
    else:
        return list(node.words)
    



__author__ = 'traveloka'
import copy

from app.meloentjoer.common.util.PriorityQueue import PriorityQueue


class ConnectedGraph(object):
    """
    vertices in list of integer or string
    #edges in dict; vertices as key; vertices X distance as value

    """
    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.edges = edges

    def find_shortest_path(self, source):
        """
        :type source: str
        :param source:
        :return:
        cost: dict (city:str -> time_cost:int)
        transport:
        """
        max_dist = 10000000000
        # dict <city,list of transports>
        transport = dict()
        # dict <city,real>
        cost = dict()
        # dict <city,city>
        previous = dict()
        # dict <city,boolean>
        visited = dict()
        pq = PriorityQueue()

        previous[source] = source
        cost[source] = 0
        transport[source] = [(0, [])]
        visited[source] = False

        for city in self.vertices:
            if city != source:
                cost[city] = max_dist
                transport[city] = []
                previous[city] = None
                visited[city] = False
            pq.put(city, cost[city])

        while pq.size() > 0:
            city = pq.deque()
            visited[city] = True
            mode_list = self.edges[city]
            for mode in mode_list:
                next_city = mode.destination
                if not visited[next_city]:
                    relative_cost = mode.cost()
                    global_cost = cost[next_city]
                    alternative_cost = cost[city]+relative_cost
                    if alternative_cost < global_cost:
                        cost[next_city] = alternative_cost
                        previous[next_city] = city
                        pq.put(next_city, cost[next_city])
                    for trans in transport[city]:
                        current_cost = trans[0]
                        new_mode_list = copy.deepcopy(trans[1])
                        new_mode_list.append(mode)
                        transport[next_city].append((current_cost+mode.cost(), new_mode_list))
                temp_map = dict()
                temp_list = list()
                for trx in transport[next_city]:
                    temp_map['_'.join(x.origin+'_'+x.destination for x in trx[1])] = trx
                for key in temp_map.keys():
                    temp_list.append(temp_map[key])
                temp_list.sort(cmp=lambda x, y: x[0]-y[0])
                transport[next_city] = temp_list[:3]
        return cost, previous, transport

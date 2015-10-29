__author__ = 'traveloka'
from app.meloentjoer.search.GraphSearchService import ConnectedGraph
from app.meloentjoer.search.RealtimeBuswayGenerator import RealtimeBuswayGenerator


class TransportationGraphBuilder(object):
    def __generate_graph(self, mode_list):
        vertices = set()
        edges = dict()
        for mode in mode_list:
            vertices.add(mode.origin)
            vertices.add(mode.destination)
            if mode.origin not in edges:
                edges[mode.origin] = []
            edges[mode.origin].append(mode)
        return_graph = ConnectedGraph(vertices, edges)
        return return_graph

    def generate_realtime_graph(self):
        realtime_busway_generator = RealtimeBuswayGenerator()
        mode_list = realtime_busway_generator.generate_modes()
        return_graph = self.__generate_graph(mode_list)
        return return_graph

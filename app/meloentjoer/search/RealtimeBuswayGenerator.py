from app.meloentjoer.search.BuswayMode import BuswayMode
from app.meloentjoer.search.SearchComponent import busway_fetcher
from app.meloentjoer.tracking.TrackerComponent import busETAEstimator


class RealtimeBuswayGenerator(object):
    def __parse_mode(self, text):
        """
        parse mode spec into mode object
        :param text: mode spec format: originName, destinationName, name, corridor, price ordinal, eta ordinal
        :return: TransportationMode
        """
        arr = text.split(',')
        mode = BuswayMode()
        mode.origin = arr[0]
        mode.destination = arr[1]
        mode.name = arr[2]
        mode.corridor = arr[3]
        mode.price = int(arr[4])
        mode.eta = int(arr[5])
        return mode

    def generate_modes(self):
        busway_spec_list = []
        routes_table = busway_fetcher.get_busway_routes()
        default_price = 0
        default_eta = 60
        default_name = 'Transjakarta'
        for corridor in routes_table.keys():
            points = routes_table[corridor]
            origins = points[:-1]
            destinations = points[1:]
            for origin, destination in zip(origins, destinations):
                eta = busETAEstimator.predict_eta(origin, destination)
                if eta is None:
                    eta = default_eta
                busway_spec = '{0},{1},{2},{3},{4},{5}'.format(origin, destination, default_name, corridor,
                                                               default_price, eta)
                busway_spec_list.append(busway_spec)

            for destination, origin in zip(origins, destinations):
                eta = busETAEstimator.predict_eta(origin, destination)
                if eta is None:
                    eta = default_eta
                busway_spec = '{0},{1},{2},{3},{4},{5}'.format(origin, destination, default_name, corridor,
                                                               default_price, eta)
                busway_spec_list.append(busway_spec)

        busway_list = map(self.__parse_mode, busway_spec_list)
        return busway_list

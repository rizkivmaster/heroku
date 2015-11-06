import numpy


class BusLocator:
    # coordinates_mapper: triple of station name,lat,lon(string,float,float)
    def __init__(self, coordinates_mapper, threshold):
        self.coordinates_mapper = coordinates_mapper
        self.threshold = float(threshold)

    # coordinates: list of coordinate(tuple of float)
    def locate(self, bus_coordinates):
        station_list = []
        for bus_coordinate in bus_coordinates:
            bus_coordinate = np.array(bus_coordinate)
            closest_coordinate, closest_station = min(map(lambda x: (np.linalg.norm(bus_coordinate-np.array((x[1], x[2]))), x), self.coordinates_mapper))
            station_list.append(closest_station[0] if(closest_coordinate < self.threshold) else None)
        return station_list
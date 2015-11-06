from BusRoutePostgresAccessorImpl import BusRoutePostgresAccessorImpl
from app.meloentjoer.accessors.bus_routes.BusRoute import BusRoute
from app.meloentjoer.config.GeneralConfig import GeneralConfig

config = GeneralConfig()

bus_route_accessor = BusRoutePostgresAccessorImpl(config.get_database_url())

bus_route = BusRoute()
bus_route.stations = ['Station1', 'Station 2']
bus_route.corridor_name = 'Test'

bus_route_accessor.reset()
bus_route_accessor.upset_bus_route(bus_route)

post_bus_route = bus_route_accessor.get_bus_route_by_corridor('Test')

assert(post_bus_route.stations[1] == bus_route.stations[1])
assert(post_bus_route.stations[0] == bus_route.stations[0])

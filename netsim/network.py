from netsim.fleet import Fleet
from netsim.leg import Leg
from netsim.route import Route
from netsim.airport import Airport

class Network:

    def __init__(self):
        self.airports = {}
        self.fleets = {}
        self.routes = {}
        self.legs = {}
        self.__add_known_fleets()

    def __add_known_fleets(self):
        self.fleets[('B738', '738')] = Fleet(main='B738', sub='738', crew_need=[1, 1, 0, 0, 0, 1, 0, 0, 3, 0, 0, 0])
        self.fleets[('B738', '73A')] = Fleet(main='B738', sub='73A', crew_need=[1, 1, 0, 0, 0, 1, 0, 0, 3, 0, 0, 0])
        self.fleets[('B738', '73M')] = Fleet(main='B738', sub='73M', crew_need=[1, 1, 0, 0, 0, 1, 0, 0, 3, 0, 0, 0])
        self.fleets[('B73H', '73H')] = Fleet(main='B73H', sub='73H', crew_need=[1, 1, 0, 0, 0, 1, 0, 0, 3, 0, 0, 0])
        self.fleets[('B73G', '73G')] = Fleet(main='B73G', sub='73G', crew_need=[1, 1, 0, 0, 0, 1, 0, 0, 2, 0, 0, 0])

    def add(self, flight_number, fr, to, sdt, sat, main, sub, route_number):
        key = (flight_number, sdt)
        if key not in self.legs:
            if fr not in self.airports:
                self.airports[fr] = Airport(fr)
            if to not in self.airports:
                self.airports[to] = Airport(to)
            if route_number not in self.routes:
                self.routes[route_number] = Route(route_number, self.fleets[(main, sub)])
            frapt = self.airports[fr]
            toapt = self.airports[to]
            route = self.routes[route_number]
            leg = Leg(flight_number, frapt, toapt, sdt, sat, route)
            self.legs[key] = leg
            route.add(leg)

    def sort_routes(self):
        for route in self.routes.values():
            route.sort()

    def __str__(self):
        sb = []
        for number in sorted(self.routes):
            sb.append(str(self.routes[number]))
        return '\n'.join(sb)
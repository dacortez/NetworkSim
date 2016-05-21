class Route:

    def __init__(self, fleet, number=None, aircraft=None):
        self.fleet = fleet
        self.number = number
        self.aircraft = aircraft
        self.legs = []

    def add(self, leg):
        self.legs.append(leg)
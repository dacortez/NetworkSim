class Airport:

    def __init__(self, code):
        self.code = code

    def __str__(self):
        return self.code


class Fleet:

    def __init__(self, main, sub, crew_need=None):
        self.main = main
        self.sub = sub
        if crew_need is None:
            crew_need = [1, 1, 0, 0, 0, 1, 0, 0, 3, 0, 0, 0]
        self.crew_need = crew_need

    def __str__(self):
        return '%s/%s' % (self.main, self.sub)


class Leg:

    def __init__(self, number, fr, to, sdt, sat, route):
        self.number = number
        self.fr = fr
        self.to = to
        self.sdt = sdt
        self.sat = sat
        self.adt = None
        self.aat = None
        self.route = route
        self.crew_from = {}

    def __str__(self):
        return '%s %s %s %s %s %s' % (self.number, self.fr.code, self.to.code, self.sdt, self.sat, self.route.number)


class Route:

    def __init__(self, number, fleet):
        self.number = number
        self.fleet = fleet
        self.legs = []

    def add(self, leg):
        if leg not in self.legs:
            self.legs.append(leg)

    def sort(self):
        self.legs = sorted(self.legs, key=lambda leg: leg.sdt)

    def __str__(self):
        sb = []
        for leg in self.legs:
            sdtstr = leg.sdt.strftime('%d/%m/%y %H:%M')
            satstr = leg.sat.strftime('%H:%M')
            sb.append('%s %s %s %s %s' % (leg.number.strip(), sdtstr, leg.fr.code, leg.to.code, satstr))
        return 'ROUTE %9s [%s]: %s' %(self.number, str(self.fleet), ' -> '.join(sb))


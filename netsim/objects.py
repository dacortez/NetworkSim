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
        self.crew_from_legs = {}
        self.next = None
        self.prev = None

    def add_crew_from(self, crew_complement, leg):
        for p in range(len(crew_complement)):
            if p not in self.crew_from_legs:
                self.crew_from_legs[p] = [leg] * crew_complement[p]
            else:
                self.crew_from_legs[p].extend([leg] * crew_complement[p])

    def __str__(self):
        sdtstr = self.sdt.strftime('%d/%m/%y %H:%M')
        satstr = self.sat.strftime('%H:%M')
        return '%s %s %s %s %s %s %s' % (
            self.number, self.fr.code, self.to.code, sdtstr, satstr, self.route.number, str(self.route.fleet)
        )


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
        self.__assign_prev_next()

    def __assign_prev_next(self):
        prev = None
        for i in range(len(self.legs) - 1):
            current = self.legs[i]
            current.prev = prev
            current.next = self.legs[i + 1]
            prev = current
        self.legs[-1].prev = prev
        self.legs[-1].next = None

    def __str__(self):
        sb = []
        for leg in self.legs:
            sdtstr = leg.sdt.strftime('%d/%m/%y %H:%M')
            satstr = leg.sat.strftime('%H:%M')
            sb.append('%s %s %s %s %s' % (leg.number.strip(), sdtstr, leg.fr.code, leg.to.code, satstr))
        return 'ROUTE %9s [%s]: %s' %(self.number, str(self.fleet), ' -> '.join(sb))


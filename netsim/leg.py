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

    def __str__(self):
        return '%s %s %s %s %s %s' % (self.number, self.fr.code, self.to.code, self.sdt, self.sat, self.route.number)

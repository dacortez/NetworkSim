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


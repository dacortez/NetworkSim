from datetime import datetime, timedelta


class Simulator:

    def __init__(self, network, btsim):
        self.network = network
        self.btsim = btsim
        self.legs = []

    def simulate(self, begin, end):
        self.legs = filter(lambda x: begin <= x.sdt <= end, self.network.legs.values())
        self.legs = sorted(self.legs, key=lambda leg: leg.sdt)
        for leg in self.legs:
            max_time = Simulator.__get_max_turn_around_time(leg)
            block = self.btsim.get_block(leg.fr.code, leg.to.code)
            leg.adt = max_time if max_time and max_time > leg.sdt else leg.sdt
            leg.block = block if block else (leg.sat - leg.sdt).seconds / 3600.0
            leg.aat = leg.adt + timedelta(hours=leg.block)
            adtstr = leg.adt.strftime('%d/%m/%y %H:%M')
            aatstr = leg.aat.strftime('%H:%M')
            print '%s : %s %s [%s]' % (leg, adtstr, aatstr, (leg.adt - leg.sdt).seconds / 60)

    @staticmethod
    def __get_max_turn_around_time(leg):
        times = []
        if leg.prev and leg.prev.aat:
            turn_around = Simulator.__get_aircraft_turn_around(leg.fr, leg.route.fleet)
            times.append(leg.prev.aat + timedelta(minutes=turn_around))
        turn_around = Simulator.__get_crew_turn_around(leg.fr, leg.route.fleet)
        for p in leg.crew_from_legs:
            for from_leg in leg.crew_from_legs[p]:
                if from_leg and from_leg.aat:
                    times.append(from_leg.aat + timedelta(minutes=turn_around))
        return max(times) if len(times) > 0 else None

    @staticmethod
    def __get_aircraft_turn_around(airport, fleet):
        if fleet.main == 'B73G':
            if airport.code in ['CGH', 'GRU', 'BSB', 'POA', 'GIG', 'SDU']:
                return 25
            else:
                return 20
        else:
            if airport.code in ['CGH', 'GRU', 'BSB', 'POA', 'GIG', 'SDU']:
                return 30
            else:
                return 25

    @staticmethod
    def __get_crew_turn_around(airport, fleet):
        if fleet.main == 'B73G':
            if airport.code in ['CGH', 'GRU', 'BSB', 'POA', 'GIG', 'SDU']:
                return 25
            else:
                return 20
        else:
            if airport.code in ['CGH', 'GRU', 'BSB', 'POA', 'GIG', 'SDU']:
                return 30
            else:
                return 25

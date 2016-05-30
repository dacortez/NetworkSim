from datetime import datetime, timedelta


class Simulator:

    def __init__(self, network, btsim):
        self.network = network
        self.btsim = btsim
        self.legs = []

    def clear(self):
        for leg in self.legs:
            leg.adt = None
            leg.aat = None
            leg.block = None
            leg.delay_reason = None
        self.legs = []

    def output_legs(self, file_name):
        with open(file_name, 'a') as f:
            for leg in self.legs:
                sdtstr = leg.sdt.strftime('%d/%m/%y %H:%M')
                satstr = leg.sat.strftime('%d/%m/%y %H:%M')
                adtstr = leg.adt.strftime('%d/%m/%y %H:%M')
                aatstr = leg.aat.strftime('%d/%m/%y %H:%M')
                block = '%02d:%02d' % (int(leg.block), 60 * (leg.block - int(leg.block)))
                delay = (leg.adt - leg.sdt).seconds / 60
                output = '%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%d\n' % (
                    leg.number.strip(),
                    leg.fr.code,
                    leg.to.code,
                    sdtstr,
                    satstr,
                    adtstr,
                    aatstr,
                    block,
                    leg.route.number,
                    str(leg.route.fleet),
                    leg.delay_reason,
                    delay
                )
                f.write(output)

    def output_connections(self, file_name):
        with open(file_name, 'a') as f:
            for leg in self.legs:
                next = leg.next
                plan_cnx = (next.sdt - leg.sat).seconds / 60 if next and next.sdt else ''
                exec_cnx = (next.adt - leg.aat).seconds / 60 if next and next.adt else ''
                sdtstr = leg.sdt.strftime('%d/%m/%y %H:%M')
                satstr = leg.sat.strftime('%H:%M')
                output = '%s;%s;%s;%s;%s;%s;%s\n' % (
                    leg.number.strip(),
                    leg.fr.code,
                    leg.to.code,
                    sdtstr,
                    satstr,
                    plan_cnx,
                    exec_cnx
                )
                f.write(output)

    def simulate_static(self, begin, end):
        self.__filter_and_sort_legs(begin, end)
        for leg in self.legs:
            block = self.btsim.get_block(leg.fr.code, leg.to.code)
            leg.block = block if block else (leg.sat - leg.sdt).seconds / 3600.0
            leg.adt = leg.sdt
            leg.aat = leg.sdt + timedelta(hours=leg.block)
            leg.delay_reason = 'ST'

    def simulate_dynamic(self, begin, end):
        self.__filter_and_sort_legs(begin, end)
        for leg in self.legs:
            aircraft_time = Simulator.__get_aircraft_time(leg)
            crew_time = Simulator.__get_crew_time(leg)
            max_time = Simulator.__get_max_time(aircraft_time, crew_time)
            if max_time and max_time > leg.sdt:
                leg.adt = max_time
                leg.delay_reason = 'CR' if max_time == crew_time else 'TR'
            else:
                leg.adt = leg.sdt
                leg.delay_reason = 'NA'
            block = self.btsim.get_block(leg.fr.code, leg.to.code)
            leg.block = block if block else (leg.sat - leg.sdt).seconds / 3600.0
            leg.aat = leg.adt + timedelta(hours=leg.block)

    def __filter_and_sort_legs(self, begin, end):
        self.legs = filter(lambda x: begin <= x.sdt <= end, self.network.legs.values())
        self.legs = sorted(self.legs, key=lambda leg: leg.sdt)

    @staticmethod
    def __get_max_time(aircraft_time, crew_time):
        if aircraft_time and crew_time:
            return max(aircraft_time, crew_time)
        elif aircraft_time:
            return aircraft_time
        elif crew_time:
            return crew_time
        return None

    @staticmethod
    def __get_aircraft_time(leg):
        if leg.prev and leg.prev.aat:
            turn_around = Simulator.__get_aircraft_turn_around(leg.fr, leg.route.fleet)
            return leg.prev.aat + timedelta(minutes=turn_around)
        return None

    @staticmethod
    def __get_aircraft_turn_around(airport, fleet):
        if fleet.main == 'B73G':
            if airport.code in ['CGH', 'GRU', 'BSB', 'POA', 'GIG', 'SDU']:
                return 40
            else:
                return 30
        else:
            if airport.code in ['CGH', 'GRU', 'BSB', 'POA', 'GIG', 'SDU']:
                return 40
            else:
                return 30

    @staticmethod
    def __get_crew_time(leg):
        times = []
        turn_around = Simulator.__get_crew_turn_around(leg.fr, leg.route.fleet)
        for p in leg.crew_from_legs:
            for from_leg in leg.crew_from_legs[p]:
                if from_leg and from_leg.aat:
                    times.append(from_leg.aat + timedelta(minutes=turn_around))
        return max(times) if len(times) > 1 else None

    @staticmethod
    def __get_crew_turn_around(airport, fleet):
        if fleet.main == 'B73G':
            if airport.code in ['CGH', 'GRU', 'BSB', 'POA', 'GIG', 'SDU']:
                return 40
            else:
                return 30
        else:
            if airport.code in ['CGH', 'GRU', 'BSB', 'POA', 'GIG', 'SDU']:
                return 40
            else:
                return 30

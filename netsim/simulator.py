from datetime import datetime, timedelta


class Simulator:

    def __init__(self, network, btgen):
        self.network = network
        self.btgen = btgen
        self.legs = []

    def clear(self):
        for leg in self.legs:
            leg.adt = None
            leg.aat = None
            leg.block = None
            leg.delay_reason = None
        self.legs = []

    def output(self, file_name):
        with open(file_name, 'a') as f:
            for number in sorted(map(int, self.network.routes)):
                for leg in self.network.routes[str(number)].legs:
                    if leg.delay_reason is not None:
                        sdtstr = leg.sdt.strftime('%d/%m/%y %H:%M:%S')
                        satstr = leg.sat.strftime('%d/%m/%y %H:%M:%S')
                        adtstr = leg.adt.strftime('%d/%m/%y %H:%M:%S')
                        aatstr = leg.aat.strftime('%d/%m/%y %H:%M:%S')
                        block_m = (leg.sat - leg.sdt).total_seconds() / 60
                        plan_block = '%02d:%02d' % (int(block_m / 60), block_m % 60)
                        exec_block = '%02d:%02d' % (int(leg.block / 60), leg.block % 60)
                        dep_delay = (leg.adt - leg.sdt).total_seconds() / 60
                        arr_delay = (leg.aat - leg.sat).total_seconds() / 60
                        next = leg.next
                        plan_cnx = int((next.sdt - leg.sat).total_seconds() / 60) if next and next.sdt else ''
                        exec_cnx = int((next.adt - leg.aat).total_seconds() / 60) if next and next.adt else ''
                        output = '%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%d;%d;%s;%s\n' % (
                            leg.route.number,
                            str(leg.route.fleet),
                            leg.number.strip(),
                            leg.fr.code,
                            leg.to.code,
                            sdtstr,
                            satstr,
                            plan_block,
                            adtstr,
                            aatstr,
                            exec_block,
                            leg.delay_reason,
                            dep_delay,
                            arr_delay,
                            plan_cnx,
                            exec_cnx
                        )
                        f.write(output)

    def simulate_static(self, begin, end):
        self.__filter_and_sort_legs(begin, end)
        for leg in self.legs:
            self.__set_block_time(leg)
            leg.adt = leg.sdt
            leg.aat = leg.sdt + timedelta(minutes=leg.block)
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
            self.__set_block_time(leg)
            leg.aat = leg.adt + timedelta(minutes=leg.block)

    def __filter_and_sort_legs(self, begin, end):
        self.legs = filter(lambda x: begin <= x.sdt <= end, self.network.legs.values())
        self.legs = sorted(self.legs, key=lambda leg: leg.sdt)

    def __set_block_time(self, leg):
        block_h = self.btgen.get_block(leg.fr.code, leg.to.code)
        block_m = round(60.0 * block_h, 0) if block_h else None
        leg.block = block_m if block_m else (leg.sat - leg.sdt).seconds / 60

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
            if airport.code in ['CGH', 'GRU', 'BSB', 'GIG', 'EZE']:
                return 40
            else:
                return 30
        else:
            if airport.code in ['CGH', 'GRU', 'BSB', 'GIG', 'EZE']:
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
            if airport.code in ['CGH', 'GRU', 'BSB', 'GIG', 'EZE']:
                return 0
            else:
                return 0
        else:
            if airport.code in ['CGH', 'GRU', 'BSB', 'GIG', 'EZE']:
                return 0
            else:
                return 0

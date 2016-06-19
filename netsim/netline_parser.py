from datetime import datetime, timedelta
from network import Network


class NetLineParser:

    def __init__(self, file_name):
        self.file_name = file_name
        self.network = Network()

    def parse(self):
        self.__parse_legs__()
        self.__parse_crew_flow__()
        self.network.sort_routes()

    # PLEG|20150506|G3 1567|IGU|CGH|20150506|1630|1805|20150506|1630|1805|B738|73M|G3|G3
    # POPT|-82678574|
    def __parse_legs__(self):
        with open(self.file_name, 'r') as f:
            line = f.readline()
            while line:
                fields = line.split('|')
                if fields[0] == 'PLEG':
                    flight_number = fields[2]
                    fr = fields[3]
                    to = fields[4]
                    sdt = datetime.strptime('%s %s' % (fields[5], fields[6]), '%Y%m%d %H%M')
                    sat = datetime.strptime('%s %s' % (fields[5], fields[7]), '%Y%m%d %H%M')
                    if sat <= sdt:
                        sat = sat + timedelta(days=1)
                    main = fields[11]
                    sub = fields[12]
                    popt = f.readline()
                    route_number = popt.split('|')[1].strip()
                    self.network.add(flight_number, fr, to, sdt, sat, main, sub, route_number)
                line = f.readline()

    # PPRG|1|1|0|0|0|1|0|0|1|0|0|0|A|NL3574381||Y||19700101||||
    # PLEG|20150423|G31726|BSB|PMW|20150423|1912|2030|20150423|1912|2030|B738|738|G3|G3
    # POPT|-82678625|
    # PLEG|20150423|G31729|PMW|BSB|20150423|2100|2218|20150423|2100|2218|B738|738|G3|G3
    # POPT|-82678625|
    # POPT|4:45|28:56
    # PLEG|20150425|G31239|THE|BSB|20150425|0826|1037|20150425|0826|1037|B738|738|G3|G3
    # POPT|41|
    # POPT|2:11|0:00
    # PFTR|20150424|G31313|CNF|CGH|20150424|1728|1840|20150424|1728|1840
    def __parse_crew_flow__(self):
        with open(self.file_name, 'r') as f:
            line = f.readline()
            while line:
                fields = line.split('|')
                if fields[0] == 'PPRG':
                    crew_complement = map(int, fields[1:13])
                    from_leg = None
                elif fields[0] == 'PLEG':
                    current_leg = self.__get_leg__(fields)
                    if current_leg is not None:
                        current_leg.add_crew_from(crew_complement, from_leg)
                    from_leg = current_leg
                elif fields[0] == 'PFTR':
                    from_leg = self.__get_leg__(fields)
                elif fields[0] == 'POPT' and ':' in fields[1]:
                    from_leg = None
                line = f.readline()

    def __get_leg__(self, fields):
        flight_number = fields[2]
        sdt = datetime.strptime('%s %s' % (fields[5], fields[6]), '%Y%m%d %H%M')
        key = (flight_number, sdt)
        return self.network.legs[key] if key in self.network.legs else None

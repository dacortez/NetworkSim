from datetime import datetime, timedelta
from network import Network


class NetLineParser:

    def __init__(self, file_name):
        self.file_name = file_name
        self.network = Network()

    # PLEG|20150506|G3 1567|IGU|CGH|20150506|1630|1805|20150506|1630|1805|B738|73M|G3|G3
    # POPT|-82678574|
    def parse(self):
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
                        sat = sat + timedelta(days = 1)
                    main = fields[11]
                    sub = fields[12]
                    popt = f.readline()
                    route_number = popt.split('|')[1]
                    self.network.add(flight_number, fr, to, sdt, sat, main, sub, route_number)
                line = f.readline()
        self.network.sort_routes()

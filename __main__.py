import sys
import random
from netsim.netline_parser import NetLineParser
from netsim.stat import BlockTimeSim
from netsim.simulator import Simulator
from datetime import datetime

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print 'Uso: python NetworkSim <netline.txt> <data_folder> <begin:yyyymmdd> <end:yyyymmdd>'
        exit(0)

    random.seed()

    file_name = sys.argv[1]
    print 'Processando Network - Arquivo: %s ...' % file_name
    parser = NetLineParser(file_name)
    parser.parse()
    print 'Airports = %d' % len(parser.network.airports)
    print 'Fleets   = %d' % len(parser.network.fleets)
    print 'Legs     = %d' % len(parser.network.legs)
    print 'Routes   = %d' % len(parser.network.routes)

    data_folder = sys.argv[2]
    print 'Processando dados - Pasta: %s ...' % data_folder
    btsim = BlockTimeSim(data_folder)
    btsim.init()

    begin = datetime.strptime('%s 0000' % sys.argv[3], '%Y%m%d %H%M')
    end = datetime.strptime('%s 2359' % sys.argv[4], '%Y%m%d %H%M')
    print 'Iniciando simulação ...'
    netsim = Simulator(parser.network, btsim)
    netsim.simulate_dynamic(begin, end)
    netsim.output_legs('legs.csv')
    netsim.output_connections('connections.csv')
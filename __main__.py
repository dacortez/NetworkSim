import sys
import random
from netsim.netline_parser import NetLineParser
from netsim.stat import KernelBlockTime, MedianBlockTime
from netsim.simulator import Simulator
from datetime import datetime

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print 'Uso: python NetworkSim <pairings.txt> <block_folder> <begin:yyyymmdd> <end:yyyymmdd>'
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
    btgen = MedianBlockTime(data_folder)
    #btgen = KernelBlockTime(data_folder)
    btgen.init()

    begin = datetime.strptime('%s 0000' % sys.argv[3], '%Y%m%d %H%M')
    end = datetime.strptime('%s 2359' % sys.argv[4], '%Y%m%d %H%M')
    print 'Iniciando simulação ...'
    netsim = Simulator(parser.network, btgen)
    netsim.simulate(begin, end)
    netsim.output('legs.csv')
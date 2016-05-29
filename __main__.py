import sys
from netsim.netline_parser import NetLineParser
from netsim.stat import BlockTimeSim

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print 'Uso: python NetworkSim <netline.txt> <data_folder>'
        exit(0)

    file_name = sys.argv[1]
    parser = NetLineParser(file_name)

    print 'Processando Network - Arquivo: %s ...' % file_name
    parser.parse()

    print 'Airports = %d' % len(parser.network.airports)
    print 'Fleets   = %d' % len(parser.network.fleets)
    print 'Legs     = %d' % len(parser.network.legs)
    print 'Routes   = %d' % len(parser.network.routes)
    parser.network.print_crew_flow()

    data_folder = sys.argv[2]
    btsim = BlockTimeSim(data_folder)

    print 'Processando dados - Pasta: %s ...' % data_folder
    btsim.init()

    print btsim.get_block('CGH', 'SSA')
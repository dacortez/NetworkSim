import sys
from netsim.netline_parser import NetLineParser

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print 'Uso: python NetworkSim <netline.txt>'
        exit(0)

    file_name = sys.argv[1]
    parser = NetLineParser(file_name)

    print 'Processando arquivo %s...' % file_name
    parser.parse()

    print 'Airports = %d' % len(parser.network.airports)
    print 'Fleets   = %d' % len(parser.network.fleets)
    print 'Legs     = %d' % len(parser.network.legs)
    print 'Routes   = %d' % len(parser.network.routes)
    print parser.network

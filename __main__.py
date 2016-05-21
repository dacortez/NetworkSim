import sys
from netsim.netline_parser import NetLineParser

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print 'Uso: python NetworkSim <netline.txt>'
        exit(0)

    parser = NetLineParser(sys.argv[1])
    parser.parse()
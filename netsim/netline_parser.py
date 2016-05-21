from network import Network


class NetLineParser:

    def __init__(self, file_name):
        self.file_name = file_name
        self.network = Network()

    def parse(self):
        print self.file_name
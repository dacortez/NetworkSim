class Fleet:

    def __init__(self, main, sub, crew_need=None):
        self.main = main
        self.sub = sub
        if crew_need is None:
            crew_need = [1, 1, 0, 0, 0, 1, 0, 0, 3, 0, 0, 0]
        self.crew_need = crew_need

    def __str__(self):
        return '%s/%s' % (self.main, self.sub)

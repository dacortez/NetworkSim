class Fleet:

    def __init__(self, name, crew_need=None):
        self.name = name
        if crew_need is None:
            crew_need = [1, 1, 0, 1, 0, 3, 0, 0, 0, 0, 0, 0]
        self.crew_need = crew_need
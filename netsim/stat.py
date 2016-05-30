import os
import numpy as np
from scipy import stats


class BlockTimeSim:

    def __init__(self, data_folder):
        self.data_folder = data_folder
        self.data = {}
        self.kdes = {}

    def init(self):
        for fname in os.listdir(self.data_folder):
            path = '%s/%s' % (self.data_folder, fname)
            x = np.fromfile(path, dtype=float, sep='\n')
            pair = fname.split('_')
            key = '%s%s' % (pair[0], pair[1])
            self.data[key] = x
            if len(x) > 1:
                self.kdes[key] = stats.gaussian_kde(x)

    def get_block(self, fr, to):
        key = '%s%s' % (fr, to)
        return self.kdes[key].resample(1)[0][0] if key in self.kdes else None

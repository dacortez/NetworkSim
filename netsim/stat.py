import os
import numpy as np
from scipy import stats


class KernelBlockTime:

    def __init__(self, data_folder):
        self.data_folder = data_folder
        self.kdes = {}

    def init(self):
        for fname in os.listdir(self.data_folder):
            path = '%s/%s' % (self.data_folder, fname)
            x = np.fromfile(path, dtype=float, sep='\n')
            pair = fname.split('_')
            key = '%s%s' % (pair[0], pair[1])
            if len(x) > 1:
                try:
                    self.kdes[key] = stats.gaussian_kde(x)
                except:
                    print 'KDE ERROR %s %s' % (pair[0], pair[1])

    def get_block(self, fr, to):
        key = '%s%s' % (fr, to)
        return self.kdes[key].resample(1)[0][0] if key in self.kdes else None


class MedianBlockTime:
    def __init__(self, data_folder):
        self.data_folder = data_folder
        self.data = {}

    def init(self):
        for fname in os.listdir(self.data_folder):
            path = '%s/%s' % (self.data_folder, fname)
            x = np.fromfile(path, dtype=float, sep='\n')
            pair = fname.split('_')
            key = '%s%s' % (pair[0], pair[1])
            self.data[key] = x

    def get_block(self, fr, to):
        key = '%s%s' % (fr, to)
        return np.median(self.data[key]) if key in self.data else None

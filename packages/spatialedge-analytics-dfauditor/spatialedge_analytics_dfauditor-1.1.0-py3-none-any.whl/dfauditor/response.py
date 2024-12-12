import numpy as np

class StatsResponse(object):

    def __init__(self):
        self.__dict__.update(dict().fromkeys({'attr', 'type'}))


class Numeric(StatsResponse):

    def __init__(self):
        super(Numeric, self).__init__()
        self.__dict__.update(dict().fromkeys(
            {'mean', 'std', 'variance',
             'min', 'max', 'range', 'kurtosis', 'skewness',
             'mad', 'p_zeros', 'p_nan', 'median', 'iqr'
             }
        ))
        self.type = 'NUMERIC'


class String(StatsResponse):

    def __init__(self):
        super(String, self).__init__()
        self.__dict__.update(dict().fromkeys(
            {'distinct', 'freq'}
        ))
        self.type = 'STRING'
        self.freq = list()


class Bins(StatsResponse):

    def __init__(self, size, lower_bound=0, upper_bound=1):
        self.type = 'HISTOGRAM'
        self.attr = None
        self.size = size
        self.bin_config = np.linspace(lower_bound, upper_bound, size + 1)
        self.__dict__.update(dict().fromkeys(
            ['bin_count_{}'.format(x) for x in range(0, size)]
        ))
        self.__dict__.update(dict().fromkeys(
            ['bin_range_{}'.format(x) for x in range(0, size)]
        ))


    def load(self, counts):
        """
        Load the histogram bin values/counts into the response object
        :param counts: a pandas Series containing counts per bin
        :return:
        """
        if len(counts) != self.size:
            raise ValueError(f"Counts do not match number of bins {self.size}")
    
        i = 0
        for content in counts:
            if i < self.size:
                self.__dict__['bin_count_{}'.format(i)] = content
                
                bin_range = self.bin_config[i]
                next_bin_range = self.bin_config[i + 1]
                
                if i == 0:
                    bin_range_str = f'[{bin_range:.3f}, {next_bin_range:.3f}]'
                elif i == self.size - 1:
                    bin_range_str = f'({bin_range:.3f}, {next_bin_range:.3f}]'
                else:
                    bin_range_str = f'({bin_range:.3f}, {next_bin_range:.3f}]'
                
                self.__dict__['bin_range_{}'.format(i)] = bin_range_str
                
                i += 1
    
        del self.__dict__['bin_config']

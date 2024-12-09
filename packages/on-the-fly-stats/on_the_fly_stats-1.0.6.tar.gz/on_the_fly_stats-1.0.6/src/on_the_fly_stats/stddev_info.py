import math


# --------------------
## tracks the Standard deviation of the values given to it
class StddevInfo:
    # --------------------
    ## constructor
    def __init__(self):
        self._num_elems = None
        self._sum = None
        self._mean = None
        self._mean2 = None
        self._variance = None
        self._stddev = None

        self.init()

    # --------------------
    ## initialize the std dev to 0
    #
    # @return None
    def init(self):
        ## holds the number of elements so far
        self._num_elems = 0
        ## holds the current sum of all elementss
        self._sum = 0.0
        ## holds the current mean
        self._mean = float('nan')
        ## holds the current mean2
        self._mean2 = 0.0
        ## holds the current variance
        self._variance = float('nan')
        ## holds the current standard deviation
        self._stddev = float('nan')

    # --------------------
    ## property: the current standard deviation
    #
    # @return the standard deviation
    @property
    def stddev(self):
        return self._stddev

    # --------------------
    ## property: the current mean
    #
    # @return the mean
    @property
    def mean(self):
        return self._mean

    # --------------------
    ## property: the current variance
    #
    # @return the mean
    @property
    def variance(self):
        return self._variance

    # --------------------
    @property
    ## property: the number of elements used in the average
    #
    # @return the number of elementss
    def num_elements(self):
        return self._num_elems

    # --------------------
    ## add the given value to the list of values
    # see https://www.johndcook.com/blog/standard_deviation/
    # see https://en.wikipedia.org/wiki/Algorithms_for_calculating_variance
    #
    # @param val the current value
    # @return None
    def update(self, val):
        self._num_elems += 1
        if math.isnan(self._mean):
            delta = val
            self._mean = val
        else:
            delta = val - self._mean
            self._mean += delta / self._num_elems
        delta2 = val - self._mean
        self._mean2 += delta * delta2
        if self._num_elems < 2:
            self._variance = float('nan')
            self._stddev = float('nan')
        else:
            self._variance = self._mean2 / (self._num_elems - 1)
            self._stddev = math.sqrt(self._variance)

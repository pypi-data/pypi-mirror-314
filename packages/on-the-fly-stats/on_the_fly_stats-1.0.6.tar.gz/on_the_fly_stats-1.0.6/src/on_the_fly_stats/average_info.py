# --------------------
## tracks the average of the values given to it
class AverageInfo:
    # --------------------
    ## constructor
    def __init__(self):
        ## holds the running average
        self._avg = 0
        ## holds the number of elements used in the average
        self._num_elems = 0

        self.init()

    # --------------------
    ## property: the current average
    #
    # @return the average
    @property
    def average(self):
        if self._num_elems == 0:
            return float('nan')

        return self._avg

    # --------------------
    ## property: the number of elements used in the average
    #
    # @return the number of elementss
    @property
    def num_elements(self):
        return self._num_elems

    # --------------------
    ## initialize the average
    #
    # @return None
    def init(self):
        self._avg = 0
        self._num_elems = 0

    # --------------------
    ## update the average based on the given value
    #
    # @param val the current value
    # @return None
    def update(self, val):
        old_avg = self._avg
        old_num_elems = self._num_elems
        self._num_elems += 1
        self._avg = ((old_num_elems * old_avg) + val) / self._num_elems

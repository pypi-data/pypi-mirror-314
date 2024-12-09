# --------------------
## tracks the minimum and maximum values given to it
class MinMaxInfo:
    # --------------------
    ## constructor
    def __init__(self):
        ## holds the minimum of all the values provided
        self._min = None

        ## holds the maximum of all the values provided
        self._max = None

        ## holds the number of elementss
        self._num_elems = 0

        self.init()

    # --------------------
    ## initialize the min/max values
    #
    # @return None
    def init(self):
        self._min = None
        self._max = None
        self._num_elems = 0

    # --------------------
    ## the minimum value found
    #
    # @return None if no values added, otherwise the minimum value found
    @property
    def minimum(self):
        return self._min

    # --------------------
    ## the maximum value found
    #
    # @return None if no values added, otherwise the maximum value found
    @property
    def maximum(self):
        return self._max

    # --------------------
    ## property: the number of elements used in the min/max
    #
    # @return the number of elementss
    @property
    def num_elements(self):
        return self._num_elems

    # --------------------
    ## update the min/max values depending on the given value
    #
    # @param val   the current value
    # @return None
    def update(self, val):
        self._num_elems += 1
        if self._min is None:
            self._min = val
        elif val < self._min:
            self._min = val

        if self._max is None:
            self._max = val
        elif val > self._max:
            self._max = val

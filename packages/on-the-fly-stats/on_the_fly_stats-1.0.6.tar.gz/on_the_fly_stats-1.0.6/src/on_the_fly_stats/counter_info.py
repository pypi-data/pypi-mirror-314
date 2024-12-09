# --------------------
## tracks simple integer counters (+ve or -ve)
class CounterInfo:
    # --------------------
    ## constructor
    def __init__(self):
        ## holds the current counter value
        self._count = None

        self.init()

    # --------------------
    ## initialize the counter to 0
    #
    # @return None
    def init(self):
        self._count = 0

    # --------------------
    ## the self._current counter
    #
    # @return None
    @property
    def count(self):
        return self._count

    # --------------------
    ## increment the counter
    #
    # @return None
    def inc(self):
        self._count += 1

    # --------------------
    ## decrement the counter
    #
    # @return None
    def dec(self):
        self._count -= 1

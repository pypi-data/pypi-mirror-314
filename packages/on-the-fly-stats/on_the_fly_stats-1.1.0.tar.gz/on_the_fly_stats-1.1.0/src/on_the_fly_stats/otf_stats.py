from .average_info import AverageInfo
from .counter_info import CounterInfo
from .min_max_info import MinMaxInfo
from .stddev_info import StddevInfo


# --------------------
## track statistics for various items.
# Generate a report at the end of the run.
class OTFStats:
    # --------------------
    ## constructor
    def __init__(self):
        ## holds a list of stddev counters
        self.stddev = {}

        ## holds a list of integer counters
        self.counters = {}

        ## holds a list of min/max counters
        self.min_max = {}

        ## holds a list of average counters
        self.average = {}

        ## holds the function pointer for writing a line
        self._writeln = self._default_writeln

    # --------------------
    ## initialize
    #
    # @return None
    def init(self):
        for _, info in self.counters.items():
            info.init()
        for _, info in self.min_max.items():
            info.init()
        for _, info in self.stddev.items():
            info.init()
        for _, info in self.average.items():
            info.init()

    # --------------------
    ## set the function pointer for writing a line
    #
    # @param fn
    # @return None
    def set_report_writer(self, fn):
        self._writeln = fn

    # === std deviation related

    # --------------------
    ## create a stddev counter with the given tag
    #
    # @param tag  the name/tag of the counter
    # @return None
    def create_stddev(self, tag):
        if tag not in self.stddev:
            self.stddev[tag] = StddevInfo()

    # --------------------
    ## update a stddev counter with the given tag
    #
    # @param tag  the name/tag of the counter
    # @param val  the new value
    # @return None
    def update_stddev(self, tag, val):
        if tag not in self.stddev:
            self.create_stddev(tag)
        self.stddev[tag].update(val)

    # === min/max related

    # --------------------
    ## create a min/max counter with the given tag
    #
    # @param tag  the name/tag of the counter
    # @return None
    def create_min_max(self, tag):
        if tag not in self.min_max:
            self.min_max[tag] = MinMaxInfo()

    # --------------------
    ## update a min/max counter with the given tag
    #
    # @param tag  the name/tag of the counter
    # @param val  the new value
    # @return None
    def update_min_max(self, tag, val):
        if tag not in self.min_max:
            self.create_min_max(tag)
        self.min_max[tag].update(val)

    # === average related

    # --------------------
    ## create an average counter with the given tag
    #
    # @param tag  the name/tag of the counter
    # @return None
    def create_average(self, tag):
        if tag not in self.average:
            self.average[tag] = AverageInfo()

    # --------------------
    ## update an average counter with the given tag
    #
    # @param tag  the name/tag of the counter
    # @param val  the new value
    # @return None
    def update_average(self, tag, val):
        if tag not in self.average:
            self.create_average(tag)
        self.average[tag].update(val)

    # === counter related

    # --------------------
    ## create an integer counter with the given tag
    #
    # @param tag  the name/tag of the counter
    # @return None
    def create_counter(self, tag):
        if tag not in self.counters:
            self.counters[tag] = CounterInfo()

    # --------------------
    ## increment an integer counter with the given tag
    #
    # @param tag  the name/tag of the counter
    # @return None
    def inc_counter(self, tag):
        if tag not in self.counters:
            self.create_counter(tag)
        self.counters[tag].inc()

    # --------------------
    ## decrement an integer counter with the given tag
    #
    # @param tag  the name/tag of the counter
    # @return None
    def dec_counter(self, tag):
        if tag not in self.counters:
            self.create_counter(tag)
        self.counters[tag].dec()

    # --------------------
    ## init an integer counter with the given tag
    #
    # @param tag  the name/tag of the counter
    # @return None
    def init_counter(self, tag):
        if tag not in self.counters:
            self.create_counter(tag)
        self.counters[tag].init()

    # --------------------
    ## report the statistics held in all items
    #
    # @return None
    def report(self):
        self._writeln()
        self._writeln('---- Stats:')

        if self.min_max:
            self._writeln()
            self._writeln(f'     {"Min": >15} {"Max": >15} {"statistic"}')
            self._writeln(f'     {"-" * 15} {"-" * 15} {"-" * 66}')

            for name, info in sorted(self.min_max.items()):
                if isinstance(info.maximum, float):
                    min_str = f'{info.minimum: >15.6f}'
                else:
                    min_str = f'{info.minimum: >15}'

                if isinstance(info.maximum, float):
                    max_str = f'{info.maximum: >15.6f}'
                else:
                    max_str = f'{info.maximum: >15}'
                self._writeln(f'     {min_str} {max_str} {name}')
            self._writeln('     >>> end of min/max')

        if self.average:
            self._writeln()
            self._writeln(f'     {"Average": >15} {"statistic"}')
            self._writeln(f'     {"-" * 15} {"-" * 66}')

            for name, info in sorted(self.average.items()):
                self._writeln(f'     {info.average: >15.6f} {name}')
            self._writeln('     >>> end of Averages')

        if self.stddev:
            self._writeln()
            self._writeln(f'     {"StdDev": >15} {"statistic"}')
            self._writeln(f'     {"-" * 15: >15} {"-" * 66}')

            for name, info in sorted(self.stddev.items()):
                self._writeln(f'     {info.stddev: 15.6f} {name}')
            self._writeln('     >>> end of StdDev')

        if self.counters:
            self._writeln()
            self._writeln(f'     {"Total": >15} {"statistic"}')
            self._writeln(f'     {"-" * 15} {"-" * 66}')

            for name, info in sorted(self.counters.items()):
                self._writeln(f'     {info.count: >15} {name}')
            self._writeln('     >>> end of counters')

    # --------------------
    ## report the statistics held in all items
    # the format of this report is minimal as possible
    #
    # @param headers (optional) if True (default), add header lines in the report
    # @return None
    def report_minimal(self, headers=True):  # pylint: disable=too-many-branches
        if self.min_max:
            if headers:
                self._writeln('Min/Max:')
            for name, info in sorted(self.min_max.items()):
                if isinstance(info.maximum, float):
                    min_str = f'{info.minimum: >15.6f}'
                else:
                    min_str = f'{info.minimum: >15}'

                if isinstance(info.maximum, float):
                    max_str = f'{info.maximum: >15.6f}'
                else:
                    max_str = f'{info.maximum: >15}'
                self._writeln(f'{min_str} {max_str} {name}')

        if self.average:
            if headers:
                self._writeln('Average:')
            for name, info in sorted(self.average.items()):
                self._writeln(f'     {info.average: >15.6f} {name}')

        if self.stddev:
            if headers:
                self._writeln('Stddev')
            for name, info in sorted(self.stddev.items()):
                self._writeln(f'{info.stddev: 15.6f} {name}')

        if self.counters:
            if headers:
                self._writeln('Counters:')
            for name, info in sorted(self.counters.items()):
                self._writeln(f'{info.count: >15} {name}')

    # --------------------
    ## default routine to write the line to stdout
    #
    # @param msg  the line to write. If not provided, an empty line is written
    # @return None
    def _default_writeln(self, msg=''):
        print(msg)

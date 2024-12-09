* website: <https://arrizza.com/python-on-the-fly-stats>
* installation: see <https://arrizza.com/setup-common>

## Summary

This Python module contains various statistic functions (e.g. standard deviation) that can
be updated on the fly i.e. the entire dataset is not needed up front.

* See [Quick Start](https://arrizza.com/user-guide-quick-start) for information on using scripts.
* See [xplat-utils submodule](https://arrizza.com/xplat-utils) for information on the submodule.

## Sample code

see sample.py for a full example

```python
from on_the_fly_stats import OTFStats

stats = OTFStats()

# create an instance of the std deviation
stats.create_stddev('some_tag')
# add some values to it
stats.update_stddev('some_tag', 1)
stats.update_stddev('some_tag', 2)
stats.update_stddev('some_tag', 3)

# have other instances of it
stats.update_stddev('other_tag', 0.1)
stats.update_stddev('other_tag', 0.2)
stats.update_stddev('other_tag', 0.3)

# show the current data for a specific instance
print(stats.stddev['some_tag'].stddev)
print(stats.stddev['some_tag'].variance)
print(stats.stddev['some_tag'].mean)
print(stats.stddev['some_tag'].num_elements)

# show the current data for a specific instance
print(stats.stddev['other_tag'].stddev)

# some a summary report
stats.set_report_writer(print)
stats.report_minimal()
# skip the headers for even less data
stats.report_minimal(headers=False)
```

## Min/Max

Holds the minimum and maximum of the values provided so far

```python
import random

from on_the_fly_stats import OTFStats

stats = OTFStats()

stats.create_min_max('minmax1')
for _ in range(10):
    stats.update_min_max('minmax1', random.randint(0, 10))

print(stats.min_max['minmax1'].minimum)
print(stats.min_max['minmax1'].maximum)
print(stats.min_max['minmax1'].num_elements)
```

## Average

Holds the average of the values provided so far

```python
import random

from on_the_fly_stats import OTFStats

stats = OTFStats()
stats.create_average('avg1')
stats.update_average('avg1', random.uniform(0, 10))
stats.update_average('avg1', random.uniform(0, 10))

print(stats.average['avg1'].average)
print(stats.average['avg1'].anum_elementss)
```

## Standard Deviation

Holds the standard deviation, mean and variance of the values provided so far

```python
import random

from on_the_fly_stats import OTFStats

stats = OTFStats()
stats.create_stddev('sd1')
stats.update_stddev('sd1', random.random())
stats.update_stddev('sd1', random.random())
stats.update_stddev('sd1', random.random())

print(stats.stddev['sd1'].stddev)
print(stats.stddev['sd1'].mean)
print(stats.stddev['sd1'].variance)
print(stats.stddev['sd1'].num_elementss)
```

### Counters

Holds counters of the values provided so far

```python
from on_the_fly_stats import OTFStats

stats = OTFStats()

# automatically create a counter
stats.inc_counter('counter1')
stats.inc_counter('counter1')  # should be 2
stats.dec_counter('counter2')  # should be -1
stats.inc_counter('counter3')
stats.dec_counter('counter3')  # should be 0

print(stats.counters['counter1'].count)
print(stats.counters['counter2'].count)
print(stats.counters['counter3'].count)
```

### Reports

There are two builtin reports:

* a minimal report
* a full report

To use the builtin reports a function that writes a single line must be provided.
The simplest is to use print().

```python
stats.set_report_writer(print)
stats.report_minimal()
stats.report()
```

## Minimal report output

The minimal report shows each stat kept and minimal data with minimal formatting

```text
Min/Max:
              0               7 minmax1
       0.019647        0.825751 minmax2
Average:
            4.495221 avg1
Stddev
     111.109474 stddev1
       0.300395 stddev2
Counters:
              2 counter1
             -1 counter2
              0 counter3
```

## Full report output

The full report has more formatting and layout

```text
---- Stats:

                 Min             Max statistic
     --------------- --------------- ------------------------------------------------------------------
                   0               7 minmax1
            0.019647        0.825751 minmax2
     >>> end of min/max

             Average statistic
     --------------- ------------------------------------------------------------------
            4.495221 avg1
     >>> end of Averages

              StdDev statistic
     --------------- ------------------------------------------------------------------
          111.109474 stddev1
            0.300395 stddev2
     >>> end of StdDev

               Total statistic
     --------------- ------------------------------------------------------------------
                   2 counter1
                  -1 counter2
                   0 counter3
     >>> end of counters
```

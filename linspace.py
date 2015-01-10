#!/usr/bin/env python3

import collections
import collections.abc
import numbers

# This implementation should be "better" than the other... but it's not.
# See below.
class linspace(collections.abc.Sequence):
    """linspace(start, stop, num) -> linspace object
    
    Return a virtual sequence of num numbers from start to stop (inclusive).
    
    If you need a half-open range, use linspace(start, stop, num+1)[:-1].
    """
    
    def __init__(self, start, stop, num):
        if not isinstance(num, numbers.Integral) or num <= 0:
            raise ValueError('num must be a positive integer')
        self.start, self.stop, self.num = start, stop, num
    def __len__(self):
        return self.num
    def __getitem__(self, i):
        if isinstance(i, slice):
            return [self[x] for x in range(*i.indices(len(self)))]
        if i < 0:
            i = self.num + i
        if i >= self.num:
            raise IndexError('linspace object index out of range')
        return (self.stop*i + self.start*(self.num-i-1))/(self.num-1)
    def __repr__(self):
        return '{}({}, {}, {})'.format(type(self).__name__,
                                       self.start, self.stop, self.num)

linspace1 = linspace

# This implementation is the naive "start + i * step", with a small
# fix to make sure the last value is == stop instead of possibly off
# by one digit.
#
# From a quick test, it's a tiny bit faster--e.g., 6.49us vs. 6.89us for
# linspace(1, 2, 5000). It doesn't accumulate rounding errors--for
# the same test, every 5th element is different by one digit, and sometimes
# the following element, but the one after that is not; when I test with
# very small numbers, I get a similar pattern, and linspace2 actually looks
# like the better of the two. Also, not multiplying start and stop by i
# means that it works with types that can't be multiplied by i but their
# differences can (like datetimes), and with types that might overflow
# (like fixed-point numbers). And it's exactly what numpy does:
# https://github.com/numpy/numpy/blob/v1.9.1/numpy/core/function_base.py#L9
class linspace(collections.abc.Sequence):
    """linspace(start, stop, num) -> linspace object
    
    Return a virtual sequence of num numbers from start to stop (inclusive).
    
    If you need a half-open range, use linspace(start, stop, num+1)[:-1].
    """
    
    def __init__(self, start, stop, num):
        if not isinstance(num, numbers.Integral) or num <= 0:
            raise ValueError('num must be a positive integer')
        self.start, self.stop, self.num = start, stop, num
        self.step = (stop-start)/(num-1)
    def __len__(self):
        return self.num
    def __getitem__(self, i):
        if isinstance(i, slice):
            return [self[x] for x in range(*i.indices(len(self)))]
        if i < 0:
            i = self.num + i
        if i >= self.num:
            raise IndexError('linspace object index out of range')
        if i == self.num-1:
            return self.stop
        return self.start + i*self.step
    def __repr__(self):
        return '{}({}, {}, {})'.format(type(self).__name__,
                                       self.start, self.stop, self.num)

linspace2 = linspace

if __name__ == '__main__':
    print(list(linspace(1, 2, 5)))
    import datetime
    print(list(map(str, linspace(datetime.datetime(2014, 1, 1),
                        datetime.datetime(2015, 1, 1),
                        13))))

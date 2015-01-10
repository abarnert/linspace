#!/usr/bin/env python3

import collections
import collections.abc
import numbers

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

if __name__ == '__main__':
    print(list(linspace(1, 2, 5)))

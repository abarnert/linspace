#!/usr/bin/env python3

import collections
import collections.abc

class linspace(collections.abc.Sequence):
    def __init__(self, start, stop, num):
        self.start, self.stop, self.num = start, stop, num
    def __len__(self):
        return self.num
    def __getitem__(self, i):
        if i >= self.num:
            raise IndexError('linspace object index out of range')
        return (self.stop*i + self.start*(self.num-i-1))/(self.num-1)

if __name__ == '__main__':
    print(list(linspace(1, 2, 5)))

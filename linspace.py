def linspace(start, stop, num):
    return [(stop*i + start*(num-i)) / num
            for i in range(num+1)]

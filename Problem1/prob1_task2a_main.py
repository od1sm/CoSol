import random
import numpy as np

N = 1000  # random walk steps
repeats = 10000
rval = np.zeros(repeats)
for l in range(repeats):
    random.seed(4397 + l)
    y = 0
    for i in range(N):
        if random.random() > 0.5:
            y = y + 1
        else:
            y = y - 1
    rval[l] = y ** 2
print(np.average(rval))

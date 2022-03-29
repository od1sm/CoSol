import timeit
import numpy as np
import matplotlib.pyplot as plt
from tqdm import trange  # progress bar
from cycler import cycler

density=10**(-2)
seed=4397
def traps_creator(density, seed, size):
    answer = set()
    # size = round(density * 500 * 500 / 2)
    rng = np.random.default_rng(seed=seed)
    while len(answer) < size:
        r = rng.integers(low=0, high=499, size=(size, 2))
        for i in range(r.shape[0]):
            if (r[i].flat[0], r[i].flat[1]) not in answer:
                answer.add((r[i].flat[0], r[i].flat[1]))
            if len(answer) - 1 < size:
                # Break the inner loop
                break
            else:
                # Continue if the inner loop wasn't broken.
                continue
            # Inner loop was broken, break the outer.
            break
    return answer

timeit.Timer(traps_creator(density,4397,100)).timeit(number=10000)
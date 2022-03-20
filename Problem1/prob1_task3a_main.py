import random
import numpy as np
import pathlib  # needed to create folder
import matplotlib.pyplot as plt  # needed for graphs


#####################################
# Function to save images to folder #
#####################################

def savim(dir, name):
    path = pathlib.Path(f"./{dir}")
    path.mkdir(exist_ok=True,  # Without exist_ok=True,FileExistsError show up if folder already exists
               parents=True)  # Missing parents of the path are created.
    plt.savefig(f'./{dir}/{name}.png', dpi=dpisiz)
    print(f'Saved image at location: ./{dir}/{name}.png')

print('Program started running!')
dpisiz = 1000
N = 100  # random walk steps
repeats = 10000
rval = np.zeros(repeats)
for l in range(repeats):
    random.seed(4397 + l)
    y = 0
    for i in range(N):
        if random.randrange(1, 1000) > 500:
            y = y + 1
        else:
            y = y - 1
    rval[l] = y ** 2
fig = plt.figure()
ax = plt.axes()
irange = np.arange(1, 1000, dtype=int)


def f(x):
    return np.average(rval[0:int(x)])


f2 = np.vectorize(f)
plt.plot(irange, f2(irange))
ax.set_ylabel('$<R^{2}>$')
ax.set_title('$<R^{2}>$ - N in 1D')
ax.set_xlabel('N')
savim('images', 'problem1_task3a_plot')
print('Program finished running!')

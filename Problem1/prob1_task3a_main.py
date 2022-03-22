import random
import numpy as np
import pathlib  # needed to create folder
import matplotlib.pyplot as plt  # needed for graphs
from tqdm import trange # progress bar


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
N = 1000  # random walk steps
repeats = 10000
rval = np.zeros((repeats,10))
a = {99,199,299,399,499,599,699,799,899,999}
for l in trange(repeats):
    random.seed(4397 + l)
    y = 0
    for i in range(N):
        if random.random() > 0.5:
            y = y + 1
        else:
            y = y - 1
        if i in a: #https://stackoverflow.com/a/58844693 change in to a faster method
            k=round(0.01*i-0.99)
            rval[l,k] = y ** 2
fig = plt.figure()
ax = plt.axes()
for i in range(10):
    plt.plot(100*i+99,np.average(rval[:,i]),'o')
ax.set_ylabel('$<R^{2}>$')
ax.set_title('$<R^{2}>$ - N in 1D')
ax.set_xlabel('N')
savim('images', 'problem1_task3a_plot')
print('Program finished running!')

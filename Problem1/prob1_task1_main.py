import random
import pathlib  # needed to create folder
import matplotlib.pyplot as plt  # needed for graphs
import numpy as np
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
dpisiz = 1000  # for images resolution
n=1000000
numtests=6 # number for N
np.random.seed(4397)
ar=np.random.rand(n) # array with random numbers
vals=np.fromfunction(lambda j,i: 10*10**i,(1,numtests))
means=np.zeros(numtests)

for i in trange(numtests):
    means[i]=np.mean(ar[0:int(vals[0][i])])
fig = plt.figure()
ax=plt.axes()
ax.plot(vals[0],means)
ax.set_ylabel('Mean')
ax.set_title('Mean - logN')
ax.set_xlabel('N')
ax.set_xscale('log')
savim('images','problem1_task1_randplot')
print('Program finished running!')
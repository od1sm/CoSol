import random
import pathlib  # needed to create folder
import matplotlib.pyplot as plt  # needed for graphs
import numpy as np
from scipy.stats import norm
from tqdm import trange  # progress bar

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
repeats = 100000
rval1 = np.zeros(repeats)
print('Calculating for N = 1000:')
for l in trange(repeats):
    random.seed(4397 + l)
    y = 0
    for i in range(N):
        if random.random() > 0.5:
            y = y + 1
        else:
            y = y - 1
    rval1[l] = y

fig = plt.figure()
ax = plt.axes()
# plt.hist(rval1)
# ax.set_ylabel('Frequency')
# ax.set_title('Histogram of R')
# ax.set_xlabel('R')
# Fit a normal distribution to the data:
mu, std = norm.fit(rval1)

# Plot the histogram.
plt.hist(rval1, bins=15, density=True, alpha=0.6, color='g')

# Plot the PDF.
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p = norm.pdf(x, mu, std)
plt.plot(x, p, 'k', linewidth=2)
title = "Fit results: mu = %.2f,  std = %.2f, n=1000" % (mu, std)
plt.title(title)
savim('images', 'problem1_task4a_plot')

N = 2000  # random walk steps
rval2 = np.zeros(repeats)
print('Calculating for N = 2000:')
for l in trange(repeats):
    random.seed(4397 + l)
    y = 0
    for i in range(N):
        if random.random() > 0.5:
            y = y + 1
        else:
            y = y - 1
    rval2[l] = y

fig1 = plt.figure()
ax1 = plt.axes()
# plt.hist(rval1)
# ax.set_ylabel('Frequency')
# ax.set_title('Histogram of R')
# ax.set_xlabel('R')
# Fit a normal distribution to the data:
mu1, std1 = norm.fit(rval2)

# Plot the histogram.
plt.hist(rval2, bins=15, density=True, alpha=0.6, color='r')

# Plot the PDF.
xmin1, xmax1 = plt.xlim()
x1 = np.linspace(xmin1, xmax1, 100)
p1 = norm.pdf(x1, mu1, std1)
plt.plot(x1, p1, 'k', linewidth=2)
title = "Fit results: mu = %.2f,  std = %.2f, n=1000" % (mu1, std1)
plt.title(title)
savim('images', 'problem1_task4b_plot')

fig2 = plt.figure()
ax2 = plt.axes()
plt.hist(rval1, bins=25, alpha=0.5, label="rval1")
plt.hist(rval2, bins=25, alpha=0.5, label="rval2")
plt.xlabel("Data", size=14)
plt.ylabel("Count", size=14)
plt.title("Multiple Histograms")
plt.legend(loc='upper right')
savim('images', 'problem1_task4c_plot')
print('Program finished running!')
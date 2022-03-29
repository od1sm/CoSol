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
    path.mkdir(
        exist_ok=True,  # Without exist_ok=True, FileExistsError show up if folder already exists
        parents=True,
    )  # Missing parents of the path are created.
    plt.savefig(f"./{dir}/{name}.png", dpi=dpisiz)
    print(f"Saved image at location: ./{dir}/{name}.png")


def ProbabilityDensityFunctionPlot(rval1, clr, num):
    fig = plt.figure()
    ax = plt.axes()
    # Fit a normal distribution to the data:
    mu, std = norm.fit(rval1)

    # Plot the histogram.
    plt.hist(rval1, bins=30, density=True, alpha=0.6, color=clr, label=f"N = 1000")

    # Plot the PDF.
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = norm.pdf(x, mu, std)
    plt.xlabel("Final position", size=13)
    plt.ylabel("Probability density", size=13)
    plt.plot(x, p, "k", linewidth=2, label=f"$\mu$ = {mu:0.1f}\n$\sigma$ = {std:0.1f}")
    title = f"Histogram with PDF for N = {num}"
    plt.legend(loc="best", fancybox=True, framealpha=1, borderpad=1)
    plt.title(title)


print("Program started running!")
dpisiz = 1000
N = 1000  # random walk steps
repeats = 100000  # change to 100000
rval1 = np.zeros(repeats)
print("Calculating for N = 1000:")
for l in trange(repeats):
    random.seed(4397 + l)
    y = 0
    for i in range(N):
        if random.random() > 0.5:
            y = y + 1
        else:
            y = y - 1
    rval1[l] = y

# Plot the PDF.
ProbabilityDensityFunctionPlot(rval1, "g", 1000)
plt.tight_layout()
savim("images", "prob1_task4a_plot")

N = 2000  # random walk steps
rval2 = np.zeros(repeats)
print("Calculating for N = 2000:")
for l in trange(repeats):
    random.seed(4397 + l)
    y = 0
    for i in range(N):
        if random.random() > 0.5:
            y = y + 1
        else:
            y = y - 1
    rval2[l] = y

# Plot the PDF.
ProbabilityDensityFunctionPlot(rval2, "r", 2000)
plt.tight_layout()
savim("images", "prob1_task4b_plot")

# Plot two histograms in one plot
fig = plt.figure()
ax = plt.axes()
mu, std = norm.fit(rval1)
mu1, std1 = norm.fit(rval2)
plt.hist(
    rval1,
    alpha=0.5,
    label=f"N = 1000\n$\mu$ = {mu:0.1f}\n$\sigma$ = {std:0.1f}",
    bins=30,
    color="tab:blue",
)
plt.hist(
    rval2,
    alpha=0.5,
    label=f"N = 2000\n$\mu$ = {mu1:0.1f}\n$\sigma$ = {std1:0.1f}",
    bins=30,
    color="tab:red",
)
plt.xlabel("Final position", size=13)
plt.ylabel("Frequency", size=13)
plt.title("Histograms for the two values of N")
plt.legend(loc="best", fancybox=True, framealpha=1, borderpad=1)
plt.tight_layout()
savim("images", "prob1_task4c_plot")

# Plot the two PDFs
fig = plt.figure()
ax = plt.axes()
xmin, xmax = -150, 150
x = np.linspace(xmin, xmax, 1000)
p = norm.pdf(x, mu, std)
x1 = np.linspace(xmin, xmax, 1000)
p1 = norm.pdf(x1, mu1, std1)
plt.xlabel("Final position", size=13)
plt.ylabel("Probability density", size=13)
plt.plot(
    x,
    p,
    color="xkcd:bordeaux",
    alpha=0.6,
    label=f"N=1000\n$\mu$ = {mu:0.1f}\n$\sigma$ = {std:0.1f}",
)
plt.plot(
    x1,
    p1,
    color="xkcd:bluegreen",
    alpha=0.5,
    label=f"N=2000\n$\mu$ = {mu1:0.1f}\n$\sigma$ = {std1:0.1f}",
)
plt.title("PDFs for the two values of N")
plt.legend()
plt.tight_layout()
savim("images", "prob1_task4d_plot")
print("Program finished running!")

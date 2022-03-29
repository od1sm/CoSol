import random
import numpy as np
import pathlib  # needed to create folder
import matplotlib.pyplot as plt  # needed for graphs
from tqdm import trange  # progress bar
from cycler import cycler
from scipy.optimize import curve_fit

plt.rcParams["axes.prop_cycle"] = cycler(
    color=[
        "#4E79A7",
        "#F28E2B",
        "#E15759",
        "#76B7B2",
        "#59A14E",
        "#EDC949",
        "#B07AA2",
        "#FF9DA7",
        "#9C755F",
        "#BAB0AC",
    ]
)

#####################################
# Function to save images to folder #
#####################################


def savim(dir, name):
    path = pathlib.Path(f"./{dir}")
    path.mkdir(
        exist_ok=True,  # Without exist_ok=True,FileExistsError show up if folder already exists
        parents=True,
    )  # Missing parents of the path are created.
    plt.savefig(f"./{dir}/{name}.png", dpi=dpisiz)
    print(f"Saved image at location: ./{dir}/{name}.png")


print("Program started running!")
dpisiz = 1000
N = 1000  # random walk steps
repeats = 10000
rval = np.zeros((repeats, 10))
steps_checking = {
    i for i in range(99, 1000, 100)
}  # Steps where we determine our values
for l in trange(repeats):
    random.seed(4397 + l)
    y = 0
    for i in range(N):
        if random.random() > 0.5:
            y = y + 1
        else:
            y = y - 1
        if i in steps_checking:
            rval[l, i % 99] = y**2
fig = plt.figure()
ax = plt.axes()
for i in range(10):
    plt.plot(100 * i + 99, np.average(rval[:, i]), "o")
ax.set_ylabel("$<R^{2}>$")
ax.set_title("$<R^{2}>$ - N in 1D")
ax.set_xlabel("N")
iterable = (np.average(rval[:, i]) for i in range(0, 10, 1))
array = np.fromiter(iterable, float)
xaxis_for_array = np.arange(99, 1000, 100)


def f(x, a):
    return a * x


iterable = (np.average(rval[:, i]) for i in range(0, 10, 1))
array = np.fromiter(iterable, float)
xaxis_for_array = np.arange(99, 1000, 100)
# parameters and parameter covariances
popt, pcov = curve_fit(f, xaxis_for_array, array)
plt.plot(xaxis_for_array, f(xaxis_for_array, *popt), alpha=0.4)
plt.text(200, 800, "y = " + "{:.4f}".format(popt[0]) + "x")
savim("images", "prob1_task3_2D_plot")
# a, b = np.polyfit(xaxis_for_array, array, 1)
# plt.plot(xaxis_for_array, a*xaxis_for_array+b,alpha=0.5,zorder=1)
# plt.text(200, 800, 'y = ' + '{:.2f}'.format(b) + ' + {:.2f}'.format(a) + 'x')
# savim("images", "prob1_task3_1D_plot")
# print("Program finished running!")

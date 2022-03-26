import random
import numpy as np
import pathlib  # needed to create folder
import matplotlib.pyplot as plt  # needed for graphs
from tqdm import trange  # progress bar
from cycler import cycler

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
    x = 0
    for i in range(N):
        rand = random.random()
        if rand < 0.25:
            y = y + 1
        elif rand < 0.5:
            y = y - 1
        elif rand < 0.75:
            x = x + 1
        else:
            x = x - 1
        if i in steps_checking:
            rval[l, i % 99] = y**2 + x**2
fig = plt.figure()
ax = plt.axes()
for i in range(10):
    plt.plot(100 * i + 99, np.average(rval[:, i]), "o")
ax.set_ylabel("$<R^{2}>$")
ax.set_title("$<R^{2}>$ - N in 2D")
ax.set_xlabel("N")
savim("images", "problem1_task3_2D_plot")
print("Program finished running!")

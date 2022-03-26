import random
import numpy as np
import pathlib  # needed to create folder
import matplotlib.pyplot as plt
from tqdm import trange  # progress bar
from cycler import cycler

plt.rcParams["axes.prop_cycle"] = cycler(
    color=[
        "#2D2D32",
        "#bdbdbd",
        "#1976d2",
        "#b71c1c",
        "#ffb300",
        "#388e3c",
        "#5c6bc0",
        "#4527a0",
        "#0277bd",
        "#558b2f",
        "#f9a825",
        "#ef6c00",
        "#6d4c41",
        "#424242",
        "#455a64",
        "#00838f",
        "#f4511e",
        "#9e9d24",
        "#8e24aa",
        "#ad1457",
        "#004d40",
        "#880e4f",
    ]
)


def check_if_visited(
    x,
    y,
):  # function that checks if a grid position has been visited already
    if grid[x, y] == False:
        grid[x, y] = True


def savim(dir, name):
    path = pathlib.Path(f"./{dir}")
    path.mkdir(
        exist_ok=True,  # Without exist_ok=True,FileExistsError show up if folder already exists
        parents=True,
    )  # Missing parents of the path are created.
    plt.savefig(f"./{dir}/{name}.png", dpi=dpisiz)
    print(f"Saved image at location: ./{dir}/{name}.png")


dpisiz = 1000  # change to 1000
repeats = 10000  # change to 10000
total_random_walk_steps = 1000  # random walk steps
s_values = np.zeros(
    (repeats, 10), dtype=np.int16
)  # int16 since our values are from [0,2000] and int16 ([-23768,32767]) covers that space easily
start_point = 999  # for grid. Since final walk position is inside [-1000,1000]

steps_checking = set(range(99, 1000, 100))  # Steps where we determine our values

for l in trange(repeats):
    grid = np.zeros((2000, 2000), dtype=np.bool8)  # 4k bytes vs 32k for int0
    random.seed(4387 + l)
    y = start_point
    x = start_point
    for i in range(total_random_walk_steps):
        rand = random.random()
        if rand < 0.25:
            y = y + 1
            check_if_visited(x, y)
        elif rand < 0.5:
            y = y - 1
            check_if_visited(x, y)
        elif rand < 0.75:
            x = x + 1
            check_if_visited(x, y)
        else:
            x = x - 1
            check_if_visited(x, y)
        if i in steps_checking:
            s_values[l, i % 99] = np.count_nonzero(grid)
fig = plt.figure()
ax = plt.axes()
for i in range(10):
    plt.plot(
        100 * i + 99,
        np.average(s_values[:, i]),
        "o",
        zorder=2,  # greater values -> drawn later
        label="<S>",
        markersize=7,
    )
ax.set_ylabel("$<S>$")
ax.set_title("$<S>$ - t in 2D")
ax.set_xlabel("t")
with np.errstate(divide="ignore", invalid="ignore"):  # RuntimeWarning: divide by zero
    x_analytical_linspace = np.linspace(0, 1000, 1000)
    c = [
        1.000000,
        0.422784,
        -0.466187,
        -1.146547,
        -0.589260,
        2.117429,
        5.77676,
        4.05382,
        -14.5490,
        -52.8339,
        -63.6704,
        103.344,
        641.144,
        1279.49,
        -13.91,
        -8206.5,
        -26647.0,
        -32844.0,
        76848.0,
        513400.0,
        1275000.0,
    ]
    y_analytical = (
        x_analytical_linspace
        * np.pi
        / (np.log(8 * x_analytical_linspace))
        * sum(c[j] / np.log(8 * x_analytical_linspace) ** j for j in range(0, 20, 1))
    )
    analytical_line_plot = plt.plot(
        x_analytical_linspace,
        y_analytical,
        zorder=1,
        color="xkcd:ocre",
        alpha=0.8,
        label="Analytical solution",
    )
ax.legend()
# Fixing our legend so it doesn't have all our points differently
handles, labels = plt.gca().get_legend_handles_labels()
i = 1
while i < len(labels):
    if labels[i] in labels[:i]:
        del labels[i]
        del handles[i]
    else:
        i += 1
plt.legend(handles, labels, loc="best", fancybox=True, framealpha=1, borderpad=1)
savim("images", "problem1_task5_2D_plot")
print("Program finished running!")

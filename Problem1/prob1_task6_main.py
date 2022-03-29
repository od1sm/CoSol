import random
import numpy as np
import pathlib  # needed to create folder
import matplotlib.pyplot as plt
from tqdm import trange  # progress bar
from cycler import cycler
import time as tm


plt.rcParams["axes.prop_cycle"] = cycler(
    color=[
        "#3c0008",
        "#c20078",
        "#36013f",
        "#638b27",
        "#880e4f",
        "#388e3c",
        "#2D2D32",
        "#638b27",
        "#bdbdbd",
        "#1976d2",
        "#b71c1c",
        "#ffb300",
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
    ]
)


def check_borders(
    x,
    y,
):  # function that checks if a grid position is at the borders
    if x in check_values or y in check_values or x < 0 or y < 0:
        return 1


def check_traps(
    x, y, traps
):  # function that checks if a grid position is at the borders
    if (x, y) in traps:
        return 1


def savim(dir, name):
    path = pathlib.Path(f"./{dir}")
    path.mkdir(
        exist_ok=True,  # Without exist_ok=True,FileExistsError show up if folder already exists
        parents=True,
    )  # Missing parents of the path are created.
    plt.savefig(f"./{dir}/{name}.png", dpi=dpisiz)
    print(f"Saved image at location: ./{dir}/{name}.png")


dpisiz = 1000  # change to 1000
repeats = 100000  # change to 100000
density = 10 ** (-2)
check_values = {0, 499}
trap_time = np.zeros((repeats))


def traps_creator(density, seed):
    answer = set()
    size = round(density * 500 * 500)
    rng = np.random.default_rng(seed=seed)
    while len(answer) < size:
        r = rng.integers(low=0, high=499, size=(1, 2))
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


def random_walk_step(density):
    for l in trange(repeats):
        time = 0
        # grid = np.zeros((500, 500), dtype=np.int8)
        np.random.seed(4397 + l)
        traps = traps_creator(density, 4397 + l)
        y = np.random.randint(low=1, high=498, dtype=np.uintc)
        x = np.random.randint(low=1, high=498, dtype=np.uintc)
        while True:
            if check_traps(x, y, traps):
                trap_time[l] = time
                break
            time += 1
            rand = np.random.rand()
            if rand < 0.25:
                if check_borders(x, y + 1):
                    continue
                if check_traps(x, y + 1, traps):
                    trap_time[l] = time
                    break
                y = y + 1
            elif rand < 0.5:
                if check_borders(x, y - 1):
                    continue
                if check_traps(x, y - 1, traps):
                    trap_time[l] = time
                    break
                y = y - 1
            elif rand < 0.75:
                if check_borders(x + 1, y):
                    continue
                if check_traps(x + 1, y, traps):
                    trap_time[l] = time
                    break
                x = x + 1
            else:
                if check_borders(x - 1, y):
                    continue
                if check_traps(x - 1, y, traps):
                    trap_time[l] = time
                    break
                x = x - 1
    fig = plt.figure()
    ax = plt.axes()
    ax.set_ylabel("$\Phi(t)$")
    ax.set_title(f"Plot of Probability of survival $\Phi(t)$ - t for c={density:0.1e}")
    ax.set_xlabel("t")
    max_xaxis_value = int(trap_time.max()) + 1
    survivability_iterable = (
        np.size(np.where(trap_time > k)) / int(np.size(trap_time))
        for k in range(0, max_xaxis_value, 1)
    )
    survivability_array = np.fromiter(
        survivability_iterable, float
    )  # Create a new 1-dimensional array from an iterable object.
    xaxis_for_survivability_array = np.arange(
        0, max_xaxis_value, 1
    )  # array required to match the dimension of above array
    plt.plot(
        xaxis_for_survivability_array,
        survivability_array,
        alpha=0.8,
        label=f"Probability of survival $\Phi(t)$",
    )
    with np.errstate(
        divide="ignore", invalid="ignore"
    ):  # RuntimeWarning: divide by zero
        x_analytical_linspace = np.linspace(0, max_xaxis_value, 1000)
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
        y_analytical = pow(
            1 - density,
            x_analytical_linspace
            * np.pi
            / (np.log(8 * x_analytical_linspace))
            * sum(
                c[j] / np.log(8 * x_analytical_linspace) ** j for j in range(0, 20, 1)
            ),
        )
        plt.plot(
            x_analytical_linspace,
            y_analytical,
            zorder=1,
            alpha=0.6,
            label="Rosenstock's approach\n$(1-c)^{<S(t)>}$",
        )
    ax.legend(loc="best", fancybox=True, framealpha=1, borderpad=1)
    plt.tight_layout()
    savim("images", f"prob1_task6_lin_{density:0.1e}_plot")
    fig = plt.figure()
    ax = plt.axes()
    ax.set_ylabel("log$\Phi(t)$")
    ax.set_title(
        f"Plot of Probability of survival log$\Phi(t)$ - logt for c={density:.1e}"
    )
    plt.plot(
        xaxis_for_survivability_array,
        survivability_array,
        alpha=0.6,
        label=f"Probability of survival $\Phi(t)$",
    )
    plt.plot(
        x_analytical_linspace,
        y_analytical,
        zorder=1,
        alpha=0.6,
        label="Rosenstock's approach\n$(1-c)^{<S(t)>}$",
    )
    ax.legend(loc="best", fancybox=True, framealpha=1, borderpad=1)
    ax.set_yscale("log")
    ax.set_xscale("log")
    ax.set_xlabel("logt")
    plt.tight_layout()
    savim("images", f"prob1_task6_log_{density:0.1e}_plot")
    return (
        trap_time,
        xaxis_for_survivability_array,
        survivability_array,
        x_analytical_linspace,
        y_analytical,
    )


(
    trap_time1,
    xaxis_for_survivability_array1,
    survivability_array1,
    x_analytical_linspace1,
    y_analytical1,
) = random_walk_step(density)
density2 = 10 ** (-3)
(
    trap_time2,
    xaxis_for_survivability_array2,
    survivability_array2,
    x_analytical_linspace2,
    y_analytical2,
) = random_walk_step(density2)

fig = plt.figure()
ax = plt.axes()
plt.tight_layout()
plt.plot(
    xaxis_for_survivability_array1,
    survivability_array1,
    alpha=0.8,
    label=f"Probability of survival $\Phi(t)$ for c={density:0.3f}",
)
plt.plot(
    x_analytical_linspace1,
    y_analytical1,
    zorder=1,
    alpha=0.6,
    label=f"Rosenstock's approach for c={density:0.3f}",
)
plt.plot(
    xaxis_for_survivability_array2,
    survivability_array2,
    alpha=0.6,
    label=f"Probability of survival $\Phi(t)$ for c={density2:0.3f}",
)
plt.plot(
    x_analytical_linspace2,
    y_analytical2,
    zorder=1,
    alpha=0.6,
    label=f"Rosenstock's approach for c={density2:0.3f}",
)
ax.set_ylabel("$\Phi(t)$")
ax.set_xlabel("t")
ax.set_title(f"Plot of Probability of survival $\Phi(t)$ - t")
ax.legend(loc="best", fancybox=True, framealpha=1, borderpad=1)
plt.tight_layout()
savim("images", f"prob1_task6_lin_comb_plot")
fig = plt.figure()
ax = plt.axes()
plt.plot(
    xaxis_for_survivability_array1,
    survivability_array1,
    alpha=0.6,
    label=f"Probability of survival $\Phi(t)$ for c={density:0.3f}",
)
plt.plot(
    x_analytical_linspace1,
    y_analytical1,
    zorder=1,
    alpha=0.6,
    label=f"Rosenstock's approach for c={density:0.3f}",
)
plt.plot(
    xaxis_for_survivability_array2,
    survivability_array2,
    alpha=0.6,
    label=f"Probability of survival $\Phi(t)$ for c={density2:0.3f}",
)
plt.plot(
    x_analytical_linspace2,
    y_analytical2,
    zorder=1,
    alpha=0.6,
    label=f"Rosenstock's approach for c={density2:0.3f}",
)
ax.set_ylabel("log$\Phi(t)$")
ax.set_title(f"Plot of Probability of survival log$\Phi(t)$ - logt")
ax.legend(loc="best", fancybox=True, framealpha=1, borderpad=1)
ax.set_yscale("log")
ax.set_xscale("log")
ax.set_xlabel("logt")
plt.tight_layout()
savim("images", f"prob1_task6_log_comb_plot")

from typing import Set
import numpy as np
import pathlib  # needed to create folder
import matplotlib.pyplot as plt
from tqdm import trange  # progress bar
from cycler import cycler


def main(bounding_type):
    """main _summary_

    Returns:
        _type_: _description_
    """
    dpisiz = 1000  # change to 1000

    def bounding_vals_creator(bounding_type: str) -> set:
        match bounding_type:
            case "circle":
                # for i in range(-500, 500, 1):
                #     for j in range(-501, 501, 1):
                #         if (i - 225) ** 2 + (j - 225) ** 2 == (200) ** 2:
                #             bounding_vals.add((i, j))
                return set(
                    (i, j)
                    for i in range(-500, 500, 1)
                    for j in range(-501, 501, 1)
                    if (i - 225) ** 2 + (j - 225) ** 2 == 200**2
                )
            case "manhattan":
                return set(
                    (i, j)
                    for i in range(-500, 500, 1)
                    for j in range(-501, 501, 1)
                    if abs(i - 225) + abs(j - 225) == 200
                )
            case _:
                raise TypeError("Bad input on bounding type")

    bounding_vals = bounding_vals_creator(bounding_type)

    def savim(dir: str, name: str) -> None:
        path = pathlib.Path(f"./{dir}")
        path.mkdir(
            exist_ok=True,  # Without exist_ok=True,
            # FileExistsError show up if folder already exists
            parents=True,
        )  # Missing parents of the path are created.
        plt.savefig(f"./{dir}/{name}.png", dpi=dpisiz)
        print(f"Saved image at location: ./{dir}/{name}.png")

    check_values = {0, 450}

    def check_borders(
        x: int,
        y: int,
    ) -> int:
        """check_borders function that checks if a grid position is at the borders or out of the borders

        Args:
            x (int): x axis value
            y (int): y axis value

        Returns:
            int: 1, which is basically True
        """
        #
        if x in check_values or y in check_values or x < 0 or y < 0:
            return 1

    def check_occupied(x: int, y: int, sets: set) -> int:
        """check_occupied function that determines whether a grid position
        is adjacent to any preoccupied positions

        Args:
            x (int): x axis value
            y (int): y axis value
            sets (set): set that contains all positions.
                using sets because it's faster to search through them

        Returns:
            int: 1, which is basically True
        """
        # function that checks if a grid position is at the borders
        if (x, y) in sets:
            return 1

    occupied_positions = {(225, 225)}
    bounding_vals_list = list(bounding_vals)
    bounding_vals_list.sort()

    repeats = 100000  # change to 100000
    for i in trange(repeats):
        if bool(occupied_positions & bounding_vals):
            break
        np.random.seed(4397 + 18072 + i)
        val = np.random.randint(low=1, high=len(bounding_vals_list), dtype=np.uintc)
        x = bounding_vals_list[val][0]
        y = bounding_vals_list[val][1]
        time = 0
        while True:
            if check_occupied(x, y, occupied_positions):
                break
            time += 1
            rand = np.random.rand()
            if rand < 0.25:
                if check_borders(x, y + 1):
                    continue
                if check_occupied(x, y + 1, occupied_positions):
                    occupied_positions.add((x, y))
                    break
                y = y + 1
            elif rand < 0.5:
                if check_borders(x, y - 1):
                    continue
                if check_occupied(x, y - 1, occupied_positions):
                    occupied_positions.add((x, y))
                    break
                y = y - 1
            elif rand < 0.75:
                if check_borders(x + 1, y):
                    continue
                if check_occupied(x + 1, y, occupied_positions):
                    occupied_positions.add((x, y))
                    break
                x = x + 1
            else:
                if check_borders(x - 1, y):
                    continue
                if check_occupied(x - 1, y, occupied_positions):
                    occupied_positions.add((x, y))
                    break
                x = x - 1
    fig = plt.figure()
    ax = plt.axes()
    ax.scatter(225, 225)
    for i in range(len(bounding_vals_list)):
        ax.plot(
            bounding_vals_list[i][0], bounding_vals_list[i][1], marker="o", c="green"
        )

    pointvalues = list(occupied_positions)
    for i in range(len(pointvalues)):
        ax.plot(pointvalues[i][0], pointvalues[i][1], marker=".", c="black", ms=1)
    savim(f"images/{bounding_type}", "DLA")

    def sites_occupied_in_square_calc(
        origset: set, centerx: int, centery: int, distanceonx: int, distanceony: int
    ) -> set:
        """sites_occupied_in_square_calc A function that computes the number of sites occupied within a predefined square.
        This is used to calculate the fractal dimension of the structure created previously.
        We're filtering based on distance from the set and center provided by the input.
        We're doing this with a set comprehension and an if condition that satisfies
        our inequality for both x and y axis values.

        Args:
            origset (set): set that contains the occupied positions
            centerx (int): Grid center in the x axis (for us, 250)
            centery (int): Grid center in the y axis (for us, 250)
            distanceonx (int): The distance in the x axis from the center
            distanceony (int): The distance in the y axis from the center

        Returns:
            set: a set containing all grid positions that are inside the square based
            on the above-mentioned filtering arguments
        """
        filtered_set = {
            (x, y)
            for x, y in origset
            if centerx - distanceonx <= x <= centerx + distanceonx
            and centery - distanceony <= y <= centery + distanceony
        }
        return filtered_set.__len__()

    def mean_of_N_runs(centerx, centery):
        vals_to_take = 10
        number_of_sites_m_in_square = np.zeros(vals_to_take)
        for distance in np.arange(1, vals_to_take + 1, 1):
            print(
                f"{distance}\t { sites_occupied_in_square_calc(occupied_positions, centerx, centery, 10*distance, 10*distance)}"
            )
            number_of_sites_m_in_square[distance - 1] = sites_occupied_in_square_calc(
                occupied_positions, 250, 250, 10 * distance, 10 * distance
            )
        m_values = list(number_of_sites_m_in_square)
        return m_values

    m_values = np.zeros(20)
    vals_to_take = 10
    for i in range(-10, 10):
        centerx = 250
        centery = 250
        testvalue = mean_of_N_runs(centerx + i * 2, centery + i * 2)
        for j in range(0, vals_to_take):
            m_values[j] = testvalue[j]

    for i in range(0, vals_to_take):
        m_values[i] = m_values[i] / (vals_to_take + 1)
    fig = plt.figure()
    ax = plt.axes()
    ax.set_xscale("log")
    ax.set_yscale("log")
    for i in range(len(m_values)):
        ax.plot(
            10 * np.arange(1, vals_to_take + 1, 1),
            m_values,
            marker=".",
            c="black",
            ms=1,
        )
    savim(f"images/{bounding_type}", "logLlogM")
    slope = np.polyfit(10 * np.arange(1, vals_to_take + 1, 1), m_values, 1)[0]
    print(slope)


if __name__ == "__main__":
    # main("circle") #100
    main("manhattan")

import random
import os
import sys


def random_tree(n=500, origin=(0, 0, 0), height=200, max_width=120, min_width=60):
    count = 0
    while count < n:
        x = random.uniform(-max_width, max_width)
        y = random.uniform(-max_width, max_width)
        h = random.uniform(0, height)
        max_w = (height - h) / height * max_width
        min_w = max(max_w - max_width + min_width, 0)
        if min_w**2 <= x**2 + y**2 <= max_w**2:
            count += 1
            yield (x + origin[0], y + origin[1], origin[2] + h)


def get_positions(filenames: "list[str]") -> "dict[int, tuple[float, float, float]]":
    for filename in filenames:
        if not os.path.isfile(filename):
            continue

        with open(filename) as file:
            print(f"Loading positions from '{filename}'.", file=sys.stderr, flush=True)

            positions = {}

            for line in file.readlines():
                line = line.strip()
                if line == "":
                    continue
                i, x, y, z = line.split(",")
                positions[int(i)] = (float(x), float(y), float(z))

            return positions

    print("No valid file found to load positions from. Using random positions.", file=sys.stderr, flush=True)
    return {i: pos for i, pos in enumerate(random_tree())}

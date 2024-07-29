from heapq import heappop, heappush

class Brick:
    def __init__(self, name, start, end):
        self.name = name

        # Bricks directly below and above the current brick
        self.below = set()
        self.above = set()

        # Profile and Height
        start_x, start_y, start_z = start
        end_x, end_y, end_z = end
        self.profile = tuple((x, y) for x in range(start_x, end_x + 1)
                        for y in range(start_y, end_y + 1))
        self.min_z = start_z
        self.max_z = end_z
        if start_z == end_z:
            self.vertical = False
        else:
            self.vertical = True

    def __lt__(self, other):
        return self.min_z < other.min_z

    def __hash__(self):
        return hash(self.name)

    def hard_drop(self, playfield):
        drop_z = 0
        # Finds highest bricks directly below self (i.e., the ones that self
        # will land on.)
        for x, y in self.profile:
            if playfield[(x, y)]:
                _, brick_below, below_height = playfield[(x, y)][-1]
                if below_height == drop_z:
                    self.below.add((brick_below.name, brick_below))
                if below_height > drop_z:
                    self.below = {(brick_below.name, brick_below)}
                    drop_z = below_height

        drop_z += 1
        delta_z = self.min_z - drop_z
        self.min_z = drop_z
        self.max_z -= delta_z

        for x, y in self.profile:
            playfield[(x, y)].append((self.name, self, self.max_z))

        # Notify supporting brick that this brick is directly above them
        for _, brick_below in self.below:
            brick_below.above.add((self.name, self))

        return playfield


def name_from_number(integer: int) -> str:
    assert integer < 17576
    first_cha = integer % 26 + 65
    second_cha = (integer // 26) % 26 + 65
    third_cha = integer // 676 + 65
    return chr(third_cha) + chr(second_cha) + chr(first_cha)


def create_bricks(filename: str):
    with open(filename, encoding = "utf-8") as f:
        raw_bricks = f.read().strip().split("\n")
        raw_bricks = [(tuple(int(i) for i in line.split("~")[0].split(",")),
                      tuple(int(j) for j in line.split("~")[1].split(",")))
                      for line in raw_bricks]
    bricks = []
    for index, start_end in enumerate(raw_bricks):
        name = name_from_number(index)
        start, end = start_end
        bricks.append((Brick(name, start, end), name))
    bricks = tuple(bricks)

    return bricks


def cascade_bricks(brick):

    layer = {(brick.name, brick)}
    vert_bricks = set()
    collapsed_bricks = 0

    while layer or vert_bricks:
        next_vert_bricks = set()
        next_layer = set()

        # Check if we're at the proper z layer for the vertical brick to support
        for name, vert_brick, timer in vert_bricks:
            if timer == 0:
                layer.add((name, vert_brick))
            else:
                next_vert_bricks.add((name, vert_brick, timer - 1))

        # Find which bricks in the next z layer are being held up by the current
        # layer.
        layer_check = {above_brick for _, below_brick in layer
                       for above_brick in below_brick.above}
        for above_name, above_brick in layer_check:
            if above_brick.below.issubset(layer):
                collapsed_bricks += 1
                if above_brick.vertical:
                    timer = above_brick.max_z - above_brick.min_z
                    next_vert_bricks.add((above_name, above_brick, timer))
                else:
                    next_layer.add((above_name, above_brick))

        layer = next_layer.union(set())
        vert_bricks = next_vert_bricks.union(set())

    return collapsed_bricks


def play_tetris(bricks):

    tetris_playfield = {(x, y): [] for x in range(10) for y in range(10)}

    heap = []
    for brick in bricks:
        heappush(heap, brick)
    while heap:
        brick, _ = heappop(heap)
        tetris_playfield = brick.hard_drop(tetris_playfield)

    return bricks


def main():
    bricks = create_bricks("day_22.txt")
    bricks = play_tetris(bricks)
    part_1 = 0
    part_2 = 0
    for brick, _ in bricks:
        brick_answer = cascade_bricks(brick)
        part_2 += brick_answer
        if brick_answer == 0:
            part_1 += 1
    print(f"The answer to part 1 is {part_1}.")
    print(f"The answer to part 2 is {part_2}.")


if __name__ == "__main__":
    main()

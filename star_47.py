def parse_input(filename):
    with open(filename, encoding = "utf-8") as f:
        text = f.read().strip().split("\n")
        hailstones = []
        for line in text:
            line = line.replace(",", "").split("@")
            position, velocity = line
            position = tuple(int(pos) for pos in position.strip().split())
            velocity = tuple(int(vel) for vel in velocity.strip().split())
            hailstones.append((position, velocity))

    return tuple(hailstones)


MIN_BOUND = 200000000000000
MAX_BOUND = 400000000000000
TEST_MIN_BOUND = 7
TEST_MAX_BOUND = 27
def do_lines_intersect(hstone_1, hstone_2, test):
    pos_1, vel_1 = hstone_1
    x_1, y_1, _ = pos_1
    dx_1, dy_1, _ = vel_1

    pos_2, vel_2 = hstone_2
    x_2, y_2, _ = pos_2
    dx_2, dy_2, _ = vel_2

    slope_1 =  dy_1 / dx_1
    y_int_1 = y_1 - slope_1 * x_1
    slope_2 =  dy_2 / dx_2
    y_int_2 = y_2 - slope_2 * x_2

    if slope_1 == slope_2:
        if y_int_1 == y_int_2:
            return 1
        return 0

    x_3 = (y_int_2 - y_int_1) / (slope_1 - slope_2)
    y_3 = slope_1 * x_3 + y_int_1
    if test:
        if TEST_MIN_BOUND <= x_3 <= TEST_MAX_BOUND and \
           TEST_MIN_BOUND <= y_3 <= TEST_MAX_BOUND and \
           (x_3 <= x_1 and dx_1 <= 0 or x_1 <= x_3 and dx_1 > 0) and \
           (x_3 <= x_2 and dx_2 <= 0 or x_2 <= x_3 and dx_2 > 0):
            return 1
        return 0
    if MIN_BOUND <= x_3 <= MAX_BOUND and \
       MIN_BOUND <= y_3 <= MAX_BOUND and \
       (x_3 <= x_1 and dx_1 <= 0 or x_1 <= x_3 and dx_1 > 0) and \
       (x_3 <= x_2 and dx_2 <= 0 or x_2 <= x_3 and dx_2 > 0):
        return 1
    return 0



def check_hailstones(filename, test = False):
    hailstones = parse_input(filename)

    answer = 0
    for index, hstone_1 in enumerate(hailstones):
        for hstone_2 in hailstones[index + 1:]:
            answer += do_lines_intersect(hstone_1, hstone_2, test)

    return answer


print(check_hailstones("day_24.txt", False))
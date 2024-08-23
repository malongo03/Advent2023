"""
Module to solve the second star of Day 23 of the Advent of Code 2023, which is
the 46th star overall.
"""
import sys
from sympy import Matrix, linsolve

# Four dimensional line with three dependent variables, one degree of freedom

# For a hailstone_n = (x_n, y_n, z_n), (dx_n, dy_0, dz_0), there will be some
# intersection at a time t_n such that:
# dx_0 * t_n + x_0 = dx_n * t_n + x_n,
# dy_0 * t_n + y_0 = dy_n * t_n + y_n,
# dz_0 * t_n + z_0 = dz_n * t_n + z_n

# Therefore:

# t_n = (x_n - x_0) / (dx_0 - dx_n) = (y_n - y_0) / (dy_0 - dy_n) = (z_n - z_0) / (dz_0 - dz_n)

# Cross-multiplying to get three seperate equations:

# x_n*dy_0 - x_0*dy_0 + x_0*dy_n - y_n*dx_0 + y_0*dx_0 - y_0*dx_n = x_n*dy_n - y_n*dx_n
# y_n*dz_0 - y_0*dz_0 + y_0*dz_n - z_n*dy_0 + z_0*dy_0 - z_0*dy_n = y_n*dz_n - z_n*dy_n
# z_n*dx_0 - z_0*dx_0 + z_0*dx_0 - x_n*dz_0 + x_0*dz_0 - x_0*dz_n = z_n*dx_n - x_n*dz_n

# Subtracting one n from another gets you the linear equations:
# (dy_1 - dy_2)x_0 + (dx_2 - dx_1)*y_0 + (y_2 - y_1)dx_0 + (x_1 - x_2)dy_0 = x_1*dy_1 - y_1*dx_1 - x_2*dy_2 + y_2*dx_2
# (dy_2 - dy_3)x_0 + (dx_3 - dx_2)*y_0 + (y_3 - y_2)dx_0 + (x_2 - x_3)dy_0 = x_2*dy_2 - y_2*dx_2 - x_3*dy_3 + y_3*dx_3
# and so on for y and z and z and x. This makes the final matrix:

#             x,           y,           z,        dx,        dy,        dz =                                  constant
# ---------------------------------------------------------------------------------------------------------------------
# | dy_1 - dy_2, dx_2 - dx_1,           0, y_2 - y_1, x_1 - x_2,         0|| x_1*dy_1 - y_1*dx_1 - x_2*dy_2 + y_2*dx_2|
# | dy_2 - dy_3, dx_3 - dx_2,           0, y_3 - y_2, x_2 - x_3,         0|| x_2*dy_2 - y_2*dx_2 - x_3*dy_3 + y_3*dx_3|
# |           0, dz_1 - dz_2, dy_2 - dy_1,         0, z_2 - z_1, y_1 - y_2|| y_1*dz_1 - z_1*dy_1 - y_2*dz_2 + z_2*dy_2|
# |           0, dz_2 - dz_3, dy_3 - dy_2,         0, z_3 - z_2, y_2 - y_3|| y_2*dz_2 - z_2*dy_2 - y_3*dz_3 + z_3*dy_3|
# | dz_2 - dz_1,           0, dx_1 - dx_2, z_1 - z_2,         0, x_2 - x_1|| z_1*dx_1 - x_1*dz_1 - z_2*dx_2 + x_2*dz_2|
# | dz_2 - dz_3,           0, dx_2 - dx_3, z_2 - z_3,         0, x_3 - x_2|| z_2*dx_2 - x_2*dz_2 - z_3*dx_3 + x_3*dz_3|
# ---------------------------------------------------------------------------------------------------------------------

def create_solution_matrix(hstone_1, hstone_2, hstone_3):
    (x_1, y_1, z_1), (dx_1, dy_1, dz_1) = hstone_1
    (x_2, y_2, z_2), (dx_2, dy_2, dz_2) = hstone_2
    (x_3, y_3, z_3), (dx_3, dy_3, dz_3) = hstone_3

    coeff_matrix = Matrix([[dy_1 - dy_2, -dx_1 + dx_2, 0, -y_1 + y_2, x_1 - x_2, 0], #3#
                           [dy_2 - dy_3, -dx_2 + dx_3, 0, -y_2 + y_3, x_2 - x_3, 0], #6#
                           [0, dz_1 - dz_2, -dy_1 + dy_2, 0, -z_1 + z_2, y_1 - y_2], #1#
                           [0, dz_2 - dz_3, -dy_2 + dy_3, 0, -z_2 + z_3, y_2 - y_3], #4#
                           [-dz_1 + dz_2, 0, dx_1 - dx_2, z_1 - z_2, 0, -x_1 + x_2], #2#
                           [-dz_2 + dz_3, 0, dx_2 - dx_3, z_2 - z_3, 0, -x_2 + x_3]]) #5#


    constant_matrix = Matrix([-dx_1 * y_1 + dx_2 * y_2 + dy_1 * x_1 - dy_2 * x_2,
                              -dx_2 * y_2 + dx_3 * y_3 + dy_2 * x_2 - dy_3 * x_3,
                              -dy_1 * z_1 + dy_2 * z_2 + dz_1 * y_1 - dz_2 * y_2,
                              -dy_2 * z_2 + dy_3 * z_3 + dz_2 * y_2 - dz_3 * y_3,
                              dx_1 * z_1 - dx_2 * z_2 - dz_1 * x_1 + dz_2 * x_2,
                              dx_2 * z_2 - dx_3 * z_3 - dz_2 * x_2 + dz_3 * x_3])

    solution = list(linsolve((coeff_matrix, constant_matrix)))[0]

    return solution


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


def check_hailstones(filename):
    hailstones = parse_input(filename)

    solution = create_solution_matrix(hailstones[0], hailstones[1], hailstones[2])

    return sum(solution[0:3])


print(check_hailstones(sys.argv[1]))

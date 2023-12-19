"""
Module to solve the first star of Day 17 of the Advent of Code 2023, which is
the 33rd star overall.
"""
from heapq import heappush, heappop

class Node:
    """
    A encapsulation of a tuple for storing the position and last direction of a
    node without the non-sortable nature of complex numbers interferring with
    the heapq functions.
    """
    def __init__(self, position, direction):
        self.pos = position
        self.direct = direction

    def __lt__(self, other):
        return False

    def __eq__(self, other):
        return (self.pos, self.direct) == (other.pos, other.direct)

    def __hash__(self):
        return hash((self.pos, self.direct))

    def __str__(self):
        return str((self.pos, self.direct))


def find_neighbors(node, height, width, cost_dict):
    """
    Given an input node, the bounds of a matrix, and the cost for each position,
    the function outputs a list of all valid movements from the node.

    The node has a position and a last moved direction. The new valid movements
    it can make are at right angles to the last direction and of lengths 1 to 3.
    We know we cannot reverse, and we do not have to consider further straight
    movements as those were already considered when this input node was
    originally pathed to. For the purposes of the modified dijkstra search,
    the found valid movements are treated as "neighbors" to the input node.

    Inputs:
        node [Node]: a node we need to find the "neighbors" to.
        height [int]: the height of the input matrix.
        width [int]: the width of the input matrix
        cost_dict [dict{Complex: int}]: a dictionary storing the cost of
            moving into a given position.

    Returns lst[Node]
    """
    neighbors = []
    if node.pos == 0j:
        # For the start of the path, we can move either left or down.
        directions = (1j, 1)
    else:
        # For all other nodes, we need to turn left or right with respect to the
        # last moved direction.
        directions = (node.direct * 1j, node.direct * -1j)

    # We consider both directions, finding the costs and position of a movement
    # of length 1 to 3, breaking once the movement becomes invalid to move to
    # the next direction/output.
    for new_direct in directions:
        move_cost = 0
        new_pos = node.pos
        for _ in range(1, 4):
            new_pos += new_direct
            if 0 <= new_pos.real < height and 0 <= new_pos.imag < width:
                move_cost += cost_dict[new_pos]
                neighbors.append((Node(new_pos, new_direct), move_cost))
            else:
                break

    return neighbors


def limited_straight_dijkstra(filename):
    """
    Finds the heat loss to a minimal cost path through the lava island city
    blocks with the stipulation that the carts of lava cannot reverse and cannot
    move more than three blocks in the same direction without turning (See Day
    17 of the Advent of Code 2023).

    It does this by using a modified dijkstra algorithm that treats each
    position on the board for each of four directions it could have been
    approached from as distinct nodes. The necessary edges/neighbors are then
    calculated using the find_neighbors function as each node is encountered.
    See the find_neighbors doc string for a more in-depth description of how the
    limitations of the problem are treated.

    Input:
        filename [str]: the filename of the input.

    Returns int
    """
    with open(filename, encoding = "utf-8") as f:
        text = f.read().split()
        height = len(text)
        width = len(text[0])
        cost_dict = {row + col * 1j: int(cost)
                    for row, line in enumerate(text)
                    for col, cost in enumerate(line)}

    queue = [(0, Node(0j, 1j))]
    seen = set()
    min_distance = {Node(0j, 1j): 0}
    while queue:
        cost, node = heappop(queue)
        if node not in seen:
            seen.add(node)
            if node.pos == complex(height - 1, width - 1):
                break

            neighbors = find_neighbors(node, height, width, cost_dict)
            for neighbor, move_cost in neighbors:
                if neighbor not in seen:
                    new_cost = move_cost + cost
                    prev_cost = min_distance.get(neighbor)
                    if prev_cost is None or new_cost < prev_cost:
                        min_distance[neighbor] = new_cost
                        heappush(queue, (new_cost, neighbor))

    print(cost)

if __name__ == "__main__":
    limited_straight_dijkstra("day_17.txt")

from dataclasses import dataclass
from maze.world import MazeWorld


@dataclass
class Coefficients:
    """
    Coefficients for tuning the cost function
    """
    pos_acc: float = 0.0000
    depth: float = 0.0
    length: float = 1.0
    ticks: float = 0.01
    failed: float = 50.0
    timeout: float = 10.0


class FitnessFunction:

    def compute_cost(self, world: MazeWorld, behavior_tree, ticks, coefficients=None, verbose=False):

        if coefficients is None:
            coefficients = Coefficients()

        # Length is just the number of nodes in the tree
        # depth = behavior_tree.depth
        length = behavior_tree.length
        # print('Length',length)
        # print('Cost',world.cost)
        # print('Ticks',ticks)
        cost = (coefficients.length * length + max(world.cost, ticks))
        dist, _ = world.distance(world.state.position, world.goal)
        # print(world.state.position.x)
        # print(world.state.position.y)
        cost += dist
        # print('Dist',dist)

        fitness = -cost
        return fitness
#!/usr/bin/env python3

import paths
paths.add_modules_to_path()

import os
from behavior_tree_learning.sbt import BehaviorTreeExecutor, ExecutionParameters
from behavior_tree_learning.sbt import BehaviorNodeFactory

from maze.paths import get_log_directory
from maze import bt_collection
from maze.execution_nodes import get_behaviors
from maze.world import MazeWorld
from maze.world import Pos as WorldPos

from maze.world import MazeWorldFactory
from maze.environment import MazeEnvironment


def run():
    node_factory = BehaviorNodeFactory(get_behaviors())

    sbt_0 = bt_collection.select_bt(0)
    trials = [sbt_0]

    start_position = WorldPos(0, 0)
    goal_position = WorldPos(100, 100)
    landmarks = [WorldPos(25, 25), WorldPos(40, 30), WorldPos(50, 60), WorldPos(80, 85), goal_position]

    for tdx, trial in zip(range(1, len(trials)+1), trials):

        print("Trial: %d" % tdx)

        sbt = list(trial)
        print("SBT: ", sbt)

        # simulated_world = MazeWorld(start_position, goal_position, landmarks)
        # bt_executor = BehaviorTreeExecutor(node_factory, simulated_world)

        node_factory = BehaviorNodeFactory(get_behaviors())
        world_factory = MazeWorldFactory(start_position, goal_position, landmarks)
        environment = MazeEnvironment(node_factory, world_factory, verbose=False)
        fitness, tree = environment.run_and_compute(sbt, verbose=False)
        print(fitness)

        # success, ticks, tree = bt_executor.run(sbt, ExecutionParameters(max_ticks=300, successes_required=1),
        #                                        verbose=False)
        #
        # try:
        #     os.mkdir(get_log_directory())
        # except OSError:
        #     pass
        #
        file_name = 'trial_%d' % tdx
        tree.save_figure(get_log_directory(), name=file_name)
        print("Succeed: ", success)

if __name__ == "__main__":
    run()
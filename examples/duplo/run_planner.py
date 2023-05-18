#!/usr/bin/env python3

import paths
paths.add_modules_to_path()

from behavior_tree_learning.planner import plan
from duplo.world import ApplicationWorld
from duplo.world import Pos as WorldPos
from duplo.planned_nodes import get_behaviors, get_condition_parameters

def run():
    scenario_name = 'croissant'
    start_position = [WorldPos(-0.05, -0.1, 0), WorldPos(0, -0.1, 0), WorldPos(0.05, -0.1, 0),
                      WorldPos(0.1, -0.1, 0)]
    goals = ['0 at pos (0.0, 0.0, 0.0)?', '1 at pos (0.0, 0.0, 0.0192)?', \
             '2 at pos (0.016, -0.032, 0.0)?', '3 at pos (0.016, 0.032, 0.0)?']
    simulated_world = ApplicationWorld(start_position, scenario=scenario_name)
    plan(simulated_world, get_behaviors(scenario_name), get_condition_parameters, goals, 'croissant_bt', 'plans')
    # simulated_world.run_and_compute(planned_bt, verbose=True)

if __name__ == "__main__":
    run()
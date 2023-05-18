#!/usr/bin/env python3

import paths
paths.add_modules_to_path()

import os
import logging

from behavior_tree_learning.sbt import BehaviorNodeFactory
from behavior_tree_learning.learning import BehaviorTreeLearner, GeneticParameters, GeneticSelectionMethods
from behavior_tree_learning.learning import TraceConfiguration
from behavior_tree_learning.core.logger import logplot

from maze.execution_nodes import get_behaviors
from maze.world import Pos as WorldPos
from maze import bt_collection
from maze.world import MazeWorldFactory
from maze.environment import MazeEnvironment

def _configure_logger(level, directory_path, name):

    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    try:
        file_path = os.path.join(directory_path, name + '.log')
        os.mkdir(directory_path)
    except:
        pass

    logging.basicConfig(filename=file_path,
                        format='%(filename)s: %(message)s')
    logging.getLogger("gp").setLevel(level)


def _prepare_scenarios():

    scenarios = []

    # maze_planner_baseline = 'maze_planner_boost_mut'
    maze_no_baseline = 'maze_no_baseline_2'
    start_position = WorldPos(0, 0)
    target_position = WorldPos(100, 100)
    landmark_positions = [WorldPos(25, 25), WorldPos(40, 30), WorldPos(50, 60), WorldPos(80, 85), target_position]
    scenarios.append((maze_no_baseline, start_position, target_position, landmark_positions))
    # scenarios.append((maze_planner_baseline, start_position, target_position, landmark_positions))

    return scenarios


def run():

    parameters = GeneticParameters()

    parameters.n_generations = 200
    parameters.fitness_threshold = 0.

    parameters.n_population = 16
    parameters.ind_start_length = 8
    parameters.f_crossover = 0.5
    parameters.n_offspring_crossover = 2
    parameters.replace_crossover = False
    parameters.f_mutation = 0.5
    parameters.n_offspring_mutation = 2
    parameters.parent_selection = GeneticSelectionMethods.RANK
    parameters.survivor_selection = GeneticSelectionMethods.RANK
    parameters.f_elites = 0.1
    parameters.f_parents = parameters.f_elites
    parameters.mutate_co_offspring = False
    parameters.mutate_co_parents = True
    parameters.mutation_p_add = 0.4
    parameters.mutation_p_delete = 0.3
    parameters.allow_identical = False

    # parameters.boost_baseline = True
    # parameters.boost_baseline_only_co = False

    tracer = TraceConfiguration()
    tracer.plot_fitness = True
    tracer.plot_best_individual = True
    tracer.plot_last_generation = True



    scenarios = _prepare_scenarios()
    for scenario_name, start_position, target_position, landmark_positions in scenarios:
        if scenario_name == 'maze_planner_boost_mut':
            planner_bt = bt_collection.select_bt(0)
        else:
            planner_bt = None


        num_trials = 10
        trials = []
        for tdx in range(1, num_trials+1):

            trial_name = scenario_name + '_' + str(tdx)
            trials.append(trial_name)
            print("Trial: %s" % trial_name)

            log_name = trial_name
            _configure_logger(logging.DEBUG, paths.get_example_directory()+'/logs_'+scenario_name+'/', log_name)

            parameters.log_name = log_name
            seed = tdx

            node_factory = BehaviorNodeFactory(get_behaviors())
            world_factory = MazeWorldFactory(start_position, target_position, landmark_positions)
            environment = MazeEnvironment(node_factory, world_factory, verbose=False)

            bt_learner = BehaviorTreeLearner.from_environment(environment)
            success = bt_learner.run(parameters, seed,
                                     outputs_dir_path=paths.get_example_directory()+'/results_'+scenario_name+'/',
                                     trace_conf=tracer,
                                     base_line=planner_bt,
                                     verbose=False)

            print("Trial: %d, Succeed: %s" % (tdx, success))


if __name__ == "__main__":
    run()
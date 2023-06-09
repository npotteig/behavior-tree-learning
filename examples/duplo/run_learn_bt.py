#!/usr/bin/env python3

import paths
paths.add_modules_to_path()

import os
import logging

from behavior_tree_learning.sbt import BehaviorNodeFactory
from behavior_tree_learning.learning import BehaviorTreeLearner, GeneticParameters, GeneticSelectionMethods
from behavior_tree_learning.learning import TraceConfiguration
from behavior_tree_learning.core.logger import logplot

from duplo.execution_nodes import get_behaviors
from duplo.world import Pos as WorldPos
from duplo import bt_collection
from duplo.world import ApplicationWorldFactory
from duplo.environment import ApplicationEnvironment


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


def _plot_summary(outputs_dir_path, scenario_name, trials):

    from behavior_tree_learning.core.logger import logplot

    parameters = logplot.PlotParameters()
    parameters.plot_std = True
    parameters.xlabel = 'Episodes'
    parameters.ylabel = 'Fitness'
    parameters.mean_color = 'r'
    parameters.std_color = 'r'
    parameters.horizontal = -3.0
    parameters.save_fig = True
    parameters.save_fig = True
    parameters.path = os.path.join(outputs_dir_path, scenario_name + '.pdf')

    logplot.plot_learning_curves(trials, parameters)


def _prepare_scenarios():

    scenarios = []

    # tower_planner_baseline = 'tower_planner_baseline'
    # tower_no_baseline = 'tower_no_baseline'
    #
    # start_position = [WorldPos(-0.05, -0.1, 0), WorldPos(0.0, -0.1, 0), WorldPos(0.05, -0.1, 0)]
    # target_position = [WorldPos(0.0, 0.05, 0), WorldPos(0.0, 0.05, 0.0192), WorldPos(0.0, 0.05, 2 * 0.0192)]
    # scenarios.append((tower_planner_baseline, start_position, target_position))
    #
    # scenarios.append((tower_no_baseline, start_position, target_position))

    cro_planner_baseline = 'croissant_planner_boost'
    cro_no_baseline = 'croissant_no_baseline'
    start_position = [WorldPos(-0.05, -0.1, 0), WorldPos(0, -0.1, 0), WorldPos(0.05, -0.1, 0),
                      WorldPos(0.1, -0.1, 0)]
    target_position = [WorldPos(0.0, 0.0, 0.0), WorldPos(0.0, 0.0, 0.0192), WorldPos(0.016, -0.032, 0.0),
                       WorldPos(0.016, 0.032, 0.0)]
    scenarios.append((cro_planner_baseline, start_position, target_position))

    # scenarios.append((cro_no_baseline, start_position, target_position))

    return scenarios


def run():

    parameters = GeneticParameters()

    parameters.n_generations = 1000
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

    parameters.boost_baseline = True

    tracer = TraceConfiguration()
    tracer.plot_fitness = True
    tracer.plot_best_individual = True
    tracer.plot_last_generation = True



    scenarios = _prepare_scenarios()
    for scenario_name, start_position, target_position in scenarios:
        if scenario_name == 'croissant_planner_boost':
            planner_bt = bt_collection.select_bt(3)
        else:
            planner_bt = None


        num_trials = 5
        trials = []
        for tdx in range(1, num_trials+1):

            trial_name = scenario_name + '_' + str(tdx)
            trials.append(trial_name)
            print("Trial: %s" % trial_name)

            log_name = trial_name
            _configure_logger(logging.DEBUG, paths.get_example_directory()+'/logs_'+scenario_name+'/', log_name)

            parameters.log_name = log_name
            seed = tdx

            name = 'croissant'
            node_factory = BehaviorNodeFactory(get_behaviors(name))
            world_factory = ApplicationWorldFactory(start_position, scenario=name)
            environment = ApplicationEnvironment(node_factory, world_factory, target_position, verbose=False)

            bt_learner = BehaviorTreeLearner.from_environment(environment)
            success = bt_learner.run(parameters, seed,
                                     outputs_dir_path=paths.get_example_directory()+'/results_'+scenario_name+'/',
                                     trace_conf=tracer,
                                     base_line=planner_bt,
                                     verbose=False)

            print("Trial: %d, Succeed: %s" % (tdx, success))


if __name__ == "__main__":
    run()


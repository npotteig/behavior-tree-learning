import paths
paths.add_modules_to_path()

import os
from behavior_tree_learning.core.logger import logplot

def run():
    n_logs = 10


    trials = []
    for i in range(1, n_logs + 1):
        trials.append(paths.get_example_directory() + '/results_maze_planner/maze_planner_' + str(i))
    plot_parameters = logplot.PlotParameters()
    plot_parameters.plot_std = True
    plot_parameters.xlabel = 'Episodes'
    plot_parameters.ylabel = 'Fitness'
    plot_parameters.x_max = 5000
    plot_parameters.label = 'With planner bootstrap'
    plot_parameters.mean_color = 'b'
    plot_parameters.std_color = 'b'
    plot_parameters.horizontal = -180
    plot_parameters.horizontal_label = 'Manual Plan Best'
    plot_parameters.save_fig = False

    logplot.plot_learning_curves(trials, plot_parameters)

    trials = []
    for i in range(1, n_logs + 1):
        trials.append(paths.get_example_directory() + '/results_maze_no_baseline/maze_planner_' + str(i))
    plot_parameters = logplot.PlotParameters()
    plot_parameters.plot_std = True
    plot_parameters.xlabel = 'Episodes'
    plot_parameters.ylabel = 'Fitness'
    plot_parameters.x_max = 5000
    plot_parameters.label = 'No bootstrap'
    plot_parameters.mean_color = 'r'
    plot_parameters.std_color = 'r'
    plot_parameters.plot_horizontal = False
    plot_parameters.save_fig = False

    logplot.plot_learning_curves(trials, plot_parameters)

    trials = []
    for i in range(1, n_logs + 1):
        trials.append(paths.get_example_directory() + '/results_maze_planner_boost/maze_planner_boost_' + str(i))
    plot_parameters = logplot.PlotParameters()
    plot_parameters.plot_std = True
    plot_parameters.xlabel = 'Episodes'
    plot_parameters.ylabel = 'Fitness'
    plot_parameters.x_max = 5000
    plot_parameters.label = 'Bootstrap boosted for crossover'
    plot_parameters.mean_color = 'g'
    plot_parameters.std_color = 'g'
    plot_parameters.save_fig = False
    plot_parameters.plot_horizontal = False
    # parameters.path = os.path.join(paths.get_example_directory()+'results_'+scenario_name+'/', scenario_name + '.pdf')

    logplot.plot_learning_curves(trials, plot_parameters)

    trials = []
    for i in range(1, n_logs + 1):
        trials.append(paths.get_example_directory() + '/results_maze_planner_boost_mut/maze_planner_boost_mut_' + str(i))
    plot_parameters = logplot.PlotParameters()
    plot_parameters.plot_std = True
    plot_parameters.xlabel = 'Episodes'
    plot_parameters.ylabel = 'Fitness'
    plot_parameters.label = 'Bootstrap boosted for mutation and crossover'
    plot_parameters.x_max = 5000
    plot_parameters.mean_color = 'black'
    plot_parameters.std_color = 'black'
    plot_parameters.plot_horizontal = False
    # plot_parameters.horizontal = -3.0
    # plot_parameters.horizontal_linestyle = 'dotted'
    # plot_parameters.horizontal_label = 'Planner'
    plot_parameters.save_fig = True
    plot_parameters.path = os.path.join(paths.get_example_directory() + '/results_maze_no_baseline/',
                                        'maze.pdf')

    logplot.plot_learning_curves(trials, plot_parameters)




if __name__ == "__main__":
    run()
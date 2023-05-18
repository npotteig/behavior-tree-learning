import random
from math import sqrt
from enum import IntEnum
from dataclasses import dataclass
from copy import copy
from interface import implements
from behavior_tree_learning.sbt import World

import numpy as np

@dataclass
class Pos:
    """
    Cartesian position
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Pos(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Pos(self.x - other.x, self.y - other.y)

    def __str__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ')'

@dataclass
class State:
    """
    Definition of substates
    """

    position = None
    subgoal = None
    landmark = None

@dataclass
class SMParameters:
    """Data class for parameters for the state machine simulator """

    move_fail = 0.9
    move_penalty = 2
    move_thresh = 15
    subgoal_fail = 0.9
    subgoal_fail_penalty = 2
    subgoal_thresh = 40
    subgoal_comp_penalty = 1
    comp_landmarks_penalty = 2
    max_cost = 300
    velocity = 1


class MazeWorld(implements(World)):

    def __init__(self, start_position, goal_position, landmarks, parameters=None):

        if parameters is None:
            self.sm_par = SMParameters()
        else:
            self.sm_par = parameters

        self.state = State()
        self.state.position = start_position
        self.goal = goal_position
        self.state.subgoal = self.goal
        self.landmarks = None
        self.holdout_landmarks = landmarks
        self.cur_ld_index = 0
        self.cost = 0
        self.done = False
        self.actions_since_sg = 0

    def startup(self, verbose):
        return True

    def shutdown(self):
        pass

    def is_alive(self):
        # return self.cost <= self.sm_par.max_cost
        return True

    def distance(self, start, target):
        disp = target - start
        disp_np = np.array([disp.x, disp.y])
        dist = np.linalg.norm(disp_np)

        return dist, disp_np

    def close_to_goal(self):
        dist, _ = self.distance(self.state.position, self.goal)

        return dist < 1.05

    def compute_lds(self):
        self.landmarks = self.holdout_landmarks
        self.cost += self.sm_par.comp_landmarks_penalty

    def close_to_ld(self):
        if self.landmarks is not None:
            dist, _ = self.distance(self.state.position, self.landmarks[self.cur_ld_index])

            return dist < 1.05
        else:
            return False

    def next_ld(self):
        # print('Landmark', self.landmarks[self.cur_ld_index])
        if self.cur_ld_index < len(self.holdout_landmarks) - 1 and self.landmarks is not None:
            self.cur_ld_index += 1

    def move_to(self):
        # print('Position', self.state.position.x, self.state.position.y)
        dist, disp_np = self.distance(self.state.position, self.state.subgoal)

        if dist >= self.sm_par.move_thresh and np.random.uniform() <= self.sm_par.move_fail:
            # print('HERE')
            # print(dist)
            self.cost += self.sm_par.move_penalty
            return False

        force_dir = (disp_np / dist) * self.sm_par.velocity if dist > 0 else [0, 0]

        self.state.position += Pos(force_dir[0], force_dir[1])

        self.cost += 1
        self.actions_since_sg += 1
        return True

    def retrieve_subgoal(self):
        goal_bool = False
        if self.landmarks is not None:
            dist, disp_np = self.distance(self.state.position, self.landmarks[self.cur_ld_index])
        else:
            goal_bool = True
            dist, disp_np = self.distance(self.state.position, self.goal)

        if dist >= self.sm_par.subgoal_thresh and np.random.uniform() <= self.sm_par.subgoal_fail:
            # print('SG HERE')
            self.cost += self.sm_par.subgoal_fail_penalty
            return False
        # print('Distance:', dist)

        if goal_bool and dist / self.sm_par.velocity <= 10:
            self.state.subgoal = self.goal
        else:
            sg_vec = (disp_np / dist) * self.sm_par.velocity * 10 if dist > 0 else [0, 0]
            self.state.subgoal = self.state.position + Pos(sg_vec[0], sg_vec[1])
        # print('Subgoal', self.state.subgoal.x, self.state.subgoal.y)

        self.cost += 1
        return True


class MazeWorldFactory:

    def __init__(self, start_position, goal_position, landmarks, parameters=None):
        self._start_position = start_position
        self._goal_position = goal_position
        self._landmarks = landmarks
        self._parameters = parameters

    def make(self):
        return MazeWorld(self._start_position, self._goal_position, self._landmarks, self._parameters)



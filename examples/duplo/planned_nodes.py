"""
Behaviors for automated planner.
Only difference is that pre and postconditions are added.
"""
import re
import py_trees as pt

from behavior_tree_learning.sbt import RSequence
from behavior_tree_learning.sbt import BehaviorRegister
import duplo.execution_nodes as behaviors
from duplo.world import Pos as WorldPos

def get_node_from_string(string, world_interface, condition_parameters):
    # pylint: disable=too-many-branches
    """
    Returns a py trees behavior or composite given the string
    """
    has_children = False
    if 'pick ' in string:
        node = Pick(string, world_interface, re.findall(r'\d+', string), condition_parameters)
    elif 'place at' in string:
        node = PlaceAt(string, world_interface, re.findall(r'-?\d+\.\d+|-?\d+', string), condition_parameters)
    elif 'place on' in string:
        node = PlaceOn(string, world_interface, re.findall(r'\d+', string), condition_parameters)
    elif 'put' in string and 'at' in string:
        node = PutAt(string, world_interface, re.findall(r'-?\d+\.\d+|-?\d+', string), condition_parameters)
    elif 'put' in string and 'on' in string:
        node = PutOn(string, world_interface, re.findall(r'\d+', string), condition_parameters)
    elif 'apply force' in string:
        node = ApplyForce(string, world_interface, re.findall(r'\d+', string), condition_parameters)

    elif 'picked ' in string:
        node = Picked(string, world_interface, re.findall(r'\d+', string), condition_parameters)
    elif 'hand empty' in string:
        node = HandEmpty(string, world_interface, condition_parameters)
    elif 'at pos ' in string:
        node = AtPos(string, world_interface, re.findall(r'-?\d+\.\d+|-?\d+', string), condition_parameters)
    elif ' on ' in string:
        node = On(string, world_interface, re.findall(r'\d+', string), condition_parameters)

    elif string == 'f(':
        node = pt.composites.Selector('Fallback')
        has_children = True
    elif string == 's(':
        node = RSequence()
        has_children = True
    elif string == 'p(':
        node = pt.composites.Parallel(
            name="Parallel",
            policy=pt.common.ParallelPolicy.SuccessOnAll(synchronise=False))
        has_children = True
    else:
        raise Exception("Unexpected character", string)
    return node, has_children

def get_condition_parameters(condition):
    """
    Returns a list of parameters associated with the condition entered
    """
    if 'picked ' in condition:
        return re.findall(r'\d+', condition)
    if 'at pos ' in condition:
        return re.findall(r'\d+\.\d+|\d+', condition)
    if ' on ' in condition:
        return re.findall(r'\d+', condition)

    return []

def get_position_string(position):
    """ Returns a string of the position for creating behavior names """
    return '(' + str(position[0]) + ', ' + str(position[1]) + ', ' + str(position[2]) + ')'

class PlannedBehavior():
    """
    Class template for planned behaviors
    """
    def __init__(self, preconditions, postconditions):
        self.preconditions = preconditions
        self.postconditions = postconditions

    def get_preconditions(self):
        """ Returns list of preconditions """
        return self.preconditions

    def get_postconditions(self):
        """ Returns list of postconditions """
        return self.postconditions

class HandEmpty(behaviors.HandEmpty, PlannedBehavior):
    """
    Check if hand is empty
    """

    @staticmethod
    def make(text, world, verbose=False, condition_parameters=None):
        return HandEmpty(text, world, condition_parameters)

    def __init__(self, name, world_interface, _condition_parameters):
        behaviors.HandEmpty.__init__(self, name, world_interface, verbose=False)
        PlannedBehavior.__init__(self, [], [])

class Picked(behaviors.Picked, PlannedBehavior):
    """
    Check if brick is picked
    """

    @staticmethod
    def make(text, world, verbose=False, condition_parameters=None):
        return Picked(text, world, re.findall(r'\d+', text), condition_parameters)

    def __init__(self, name, world_interface, brick, _condition_parameters):
        behaviors.Picked.__init__(self, name, world_interface, verbose=False, brick=brick)
        PlannedBehavior.__init__(self, [], [])


class AtPos(behaviors.AtPos, PlannedBehavior):
    """
    Check if brick is at goal
    """

    @staticmethod
    def make(text, world, verbose=False, condition_parameters=None):
        return AtPos(text, world, re.findall(r'-?\d+\.\d+|-?\d+', text), condition_parameters)

    def __init__(self, name, world_interface, brick_and_pos, _condition_parameters):
        behaviors.AtPos.__init__(self, name, world_interface, verbose=False, brick_and_pos=brick_and_pos)
        PlannedBehavior.__init__(self, [], [])

class On(behaviors.On, PlannedBehavior):
    """
    Check if brick is at goal
    """

    @staticmethod
    def make(text, world, verbose=False, condition_parameters=None):
        return On(text, world, re.findall(r'\d+', text), condition_parameters)

    def __init__(self, name, world_interface, bricks, _condition_parameters):
        behaviors.On.__init__(self, name, world_interface, verbose=False, bricks=bricks)
        PlannedBehavior.__init__(self, [], [])

class Pick(behaviors.Pick, PlannedBehavior):
    """
    Pick up a brick
    """

    @staticmethod
    def make(text, world, verbose=False, condition_parameters=None):
        return Pick(text, world, re.findall(r'\d+', text), condition_parameters)

    def __init__(self, name, world_interface, brick, _condition_parameters):
        behaviors.Pick.__init__(self, name, world_interface, brick, verbose=False)
        PlannedBehavior.__init__(self, [], ['picked ' + str(brick[0]) + '?'])

class PlaceAt(behaviors.Place, PlannedBehavior):
    """
    Place given brick at given position
    """

    @staticmethod
    def make(text, world, verbose=False, condition_parameters=None):
        return PlaceAt(text, world, re.findall(r'-?\d+\.\d+|-?\d+', text), condition_parameters)

    def __init__(self, name, world_interface, position, condition_parameters):
        behaviors.Place.__init__(self, name, world_interface, position=position, verbose=False)
        PlannedBehavior.__init__(self, ['picked ' + str(condition_parameters[0]) +  '?'], \
            ['hand empty?', str(condition_parameters[0]) + ' at pos ' + get_position_string(position) + '?'])

class PlaceOn(behaviors.Place, PlannedBehavior):
    """
    Place current brick on other given brick
    """

    @staticmethod
    def make(text, world, verbose=False, condition_parameters=None):
        return PlaceOn(text, world, re.findall(r'\d+', text), condition_parameters)

    def __init__(self, name, world_interface, brick, condition_parameters):
        behaviors.Place.__init__(self, name, world_interface, brick=brick, verbose=False)
        PlannedBehavior.__init__(self, ['picked ' + str(condition_parameters[0]) +  '?'], ['hand empty?'])
        self.condition_parameters = condition_parameters

    def get_postconditions(self):
        """
        This one is a bit special because the postcondition
        will depend on current state of the other brick
        """
        brickpos = [str(self.condition_parameters[0]) + ' on ' + str(self._brick) + '?']
        return self.postconditions + brickpos

class PutAt(behaviors.Put, PlannedBehavior):
    """
    Picks brick and places it at position
    """

    @staticmethod
    def make(text, world, verbose=False, condition_parameters=None):
        return PutAt(text, world, re.findall(r'-?\d+\.\d+|-?\d+', text), condition_parameters)

    def __init__(self, name, world_interface, brick_and_pos, _condition_parameters):
        behaviors.Put.__init__(self, name, world_interface, brick_and_pos, verbose=False)
        PlannedBehavior.__init__(self, [], \
                                 [str(brick_and_pos[0]) + ' at pos ' + get_position_string(brick_and_pos[1:]) + '?'])

class PutOn(behaviors.Put, PlannedBehavior):
    """
    Picks brick and places it on other brick
    """

    @staticmethod
    def make(text, world, verbose=False, condition_parameters=None):
        return PutOn(text, world, re.findall(r'\d+', text), condition_parameters)

    def __init__(self, name, world_interface, brick_and_pos, condition_parameters):
        behaviors.Put.__init__(self, name, world_interface, brick_and_pos, verbose=False)
        PlannedBehavior.__init__(self, [], [str(self._brick) + ' on ' + str(self._lower) + '?'])
        self.condition_parameters = condition_parameters

class ApplyForce(behaviors.ApplyForce, PlannedBehavior):
    """
    Apply force on given brick
    A bit of a cheaty implementation of pre and postconditions here to handle our experiments,
    but we are only using it to create a result that some planner theoretically could generate
    """

    @staticmethod
    def make(text, world, verbose=False, condition_parameters=None):
        return ApplyForce(text, world, re.findall(r'\d+', text), condition_parameters)

    def __init__(self, name, world_interface, brick, _condition_parameters):
        behaviors.ApplyForce.__init__(self, name, world_interface, brick, verbose=False)
        PlannedBehavior.__init__(self, [], [])

    def get_preconditions(self):
        if self._brick == 0:
            return ['1 at pos (0.0, 0.0, 0.0)?', '0 on 1?']
        if self._brick == 1:
            return ['1 on 0?']
        if self._brick == 2:
            return ['2 on 1?']
        return self.preconditions

    def get_postconditions(self):
        if self._brick > 0:
            brickpos = self._world.state.bricks[self._brick - 1] + \
                WorldPos(0, 0, self._world.sm_par.brick_height)
            self.postconditions = [str(self._brick) + ' at pos ' + str(brickpos) + '?']
        else:
            brickpos = WorldPos(0.0, 0.0, self._world.sm_par.brick_height)
            self.postconditions = [str(self._brick) + ' at pos ' + str(brickpos) + '?']
        return self.postconditions


def _make_tower_nodes():

    behavior_register = BehaviorRegister()
    behavior_register.add_condition('picked 0?', Picked)
    behavior_register.add_condition('picked 1?', Picked)
    behavior_register.add_condition('picked 2?', Picked)
    behavior_register.add_condition('0 at pos (0.0, 0.05, 0.0)?', AtPos)
    behavior_register.add_condition('1 at pos (0.0, 0.05, 0.0192)?', AtPos)
    behavior_register.add_condition('2 at pos (0.0, 0.05, 0.0384)?', AtPos)
    behavior_register.add_condition('0 on 1?', On)
    behavior_register.add_condition('0 on 2?', On)
    behavior_register.add_condition('1 on 0?', On)
    behavior_register.add_condition('1 on 2?', On)
    behavior_register.add_condition('2 on 0?', On)
    behavior_register.add_condition('2 on 1?', On)
    behavior_register.add_action('pick 0!', Pick)
    behavior_register.add_action('pick 1!', Pick)
    behavior_register.add_action('pick 2!', Pick)
    behavior_register.add_action('place at (0.0, 0.05, 0.0)!', PlaceAt)
    behavior_register.add_action('place on 0!', PlaceOn)
    behavior_register.add_action('place on 1!', PlaceOn)
    behavior_register.add_action('place on 2!', PlaceOn)
    behavior_register.add_action('apply force 0!', ApplyForce)
    behavior_register.add_action('apply force 1!', ApplyForce)
    behavior_register.add_action('apply force 2!', ApplyForce)

    return behavior_register

def _make_croissant_nodes():

    behavior_register = BehaviorRegister()
    behavior_register.add_condition('picked 0?', Picked)
    behavior_register.add_condition('picked 1?', Picked)
    behavior_register.add_condition('picked 2?', Picked)
    behavior_register.add_condition('picked 3?', Picked)
    behavior_register.add_condition('0 at pos (0.0, 0.0, 0.0)?', AtPos)
    behavior_register.add_condition('1 at pos (0.0, 0.0, 0.0192)?', AtPos)
    behavior_register.add_condition('2 at pos (0.016, -0.032, 0.0)?', AtPos)
    behavior_register.add_condition('3 at pos (0.016, 0.032, 0.0)?', AtPos)
    behavior_register.add_condition('0 on 1?', On)
    behavior_register.add_condition('0 on 2?', On)
    behavior_register.add_condition('0 on 3?', On)
    behavior_register.add_condition('1 on 0?', On)
    behavior_register.add_condition('1 on 2?', On)
    behavior_register.add_condition('1 on 3?', On)
    behavior_register.add_condition('2 on 0?', On)
    behavior_register.add_condition('2 on 1?', On)
    behavior_register.add_condition('2 on 3?', On)
    behavior_register.add_condition('3 on 0?', On)
    behavior_register.add_condition('3 on 1?', On)
    behavior_register.add_condition('3 on 2?', On)
    behavior_register.add_action('pick 0!', Pick)
    behavior_register.add_action('pick 1!', Pick)
    behavior_register.add_action('pick 2!', Pick)
    behavior_register.add_action('pick 3!', Pick)
    behavior_register.add_action('place at (0.0, 0.0, 0.0)!', PlaceAt)
    behavior_register.add_action('place at (0.016, -0.032, 0.0)!', PlaceAt)
    behavior_register.add_action('place at (0.016, 0.032, 0.0)!', PlaceAt)
    behavior_register.add_action('place on 0!', PlaceOn)
    behavior_register.add_action('place on 1!', PlaceOn)
    behavior_register.add_action('place on 2!', PlaceOn)
    behavior_register.add_action('place on 3!', PlaceOn)
    behavior_register.add_action('apply force 0!', ApplyForce)
    behavior_register.add_action('apply force 1!', ApplyForce)
    behavior_register.add_action('apply force 2!', ApplyForce)
    behavior_register.add_action('apply force 3!', ApplyForce)

    return behavior_register


def get_behaviors(name):

    if name == 'tower':
        return _make_tower_nodes()
    elif name == 'croissant':
        return _make_croissant_nodes()
    else:
        raise ValueError('Unknown %s name', name)
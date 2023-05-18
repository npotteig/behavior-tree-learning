import re
import py_trees as pt
from behavior_tree_learning.sbt import BehaviorRegister, BehaviorNode
from maze import world as sm

class ReachGoal(BehaviorNode):
    @staticmethod
    def make(text, world, verbose=False):
        return ReachGoal(text, world)

    def __init__(self, name, world):
        self._world = world
        super(ReachGoal, self).__init__(name)

    def update(self):
        if self._world.close_to_goal():
            self._world.done = True
            return pt.common.Status.SUCCESS
        return pt.common.Status.FAILURE

class NotReadyForSG(BehaviorNode):
    @staticmethod
    def make(text, world, verbose=False):
        return NotReadyForSG(text, world)

    def __init__(self, name, world):
        self._world = world
        if self._world is not None:
            self._cur_ld = self._world.cur_ld_index
        # self.steps = 0
        super(NotReadyForSG, self).__init__(name)


    def update(self):
        if self._world.actions_since_sg % 10 == 0 or self._cur_ld != self._world.cur_ld_index:
            # self.steps = 1
            self._world.actions_since_sg = 0
            self._cur_ld = self._world.cur_ld_index
            return pt.common.Status.FAILURE
        # self.steps += 1
        return pt.common.Status.SUCCESS

class LkGraph(BehaviorNode):
    @staticmethod
    def make(text, world, verbose=False):
        return LkGraph(text, world)

    def __init__(self, name, world):
        self._world = world
        super(LkGraph, self).__init__(name)


    def update(self):
        if self._world.landmarks is None:
            return pt.common.Status.FAILURE
        return pt.common.Status.SUCCESS

class LkClose(BehaviorNode):
    @staticmethod
    def make(text, world, verbose=False):
        return LkClose(text, world)

    def __init__(self, name, world):
        self._world = world
        super(LkClose, self).__init__(name)

    def update(self):
        if self._world.close_to_ld():
            return pt.common.Status.SUCCESS
        return pt.common.Status.FAILURE

class StateMachineBehavior(BehaviorNode):
    """
    Class template for state machine behaviors
    """

    def __init__(self, name, world):
        self._world = world
        self._state = None
        super(StateMachineBehavior, self).__init__(name)

    def update(self):
        pass

    def success(self):
        self._state = pt.common.Status.SUCCESS

    def failure(self):
        self._state = pt.common.Status.FAILURE


class MoveTo(StateMachineBehavior):
    @staticmethod
    def make(text, world, verbose=False):
        return MoveTo(text, world)

    def __init__(self, name, world):
        super(MoveTo, self).__init__(name, world)

    def initialise(self) -> None:
        self._state = None

    def update(self):
        if self._world.move_to():
            self.success()
        else:
            self.failure()
        return self._state

class GetSubGoal(StateMachineBehavior):
    @staticmethod
    def make(text, world, verbose=False):
        return GetSubGoal(text, world)

    def __init__(self, name, world):
        super(GetSubGoal, self).__init__(name, world)

    def initialise(self) -> None:
        self._state = None

    def update(self):
        if self._world.retrieve_subgoal():
            self.success()
        else:
            self.failure()
        return self._state

class CompLkGraph(StateMachineBehavior):
    @staticmethod
    def make(text, world, verbose=False):
        return CompLkGraph(text, world)

    def __init__(self, name, world):
        super(CompLkGraph, self).__init__(name, world)

    def initialise(self) -> None:
        self._state = None

    def update(self):
        self._world.compute_lds()
        self.success()
        return self._state

class GetLk(StateMachineBehavior):
    @staticmethod
    def make(text, world, verbose=False):
        return GetLk(text, world)

    def __init__(self, name, world):
        super(GetLk, self).__init__(name, world)

    def initialise(self) -> None:
        self._state = None

    def update(self):
        self._world.next_ld()
        self.success()
        return self._state

def _make_nodes():
    behavior_register = BehaviorRegister()
    behavior_register.add_condition('ReachGoal?', ReachGoal)
    behavior_register.add_condition('NotReadyForSG?', NotReadyForSG)
    behavior_register.add_condition('LkGraph?', LkGraph)
    behavior_register.add_condition('LkClose?', LkClose)
    behavior_register.add_action('MoveTo!', MoveTo)
    behavior_register.add_action('GetSubGoal!', GetSubGoal)
    behavior_register.add_action('CompLkGraph!', CompLkGraph)
    behavior_register.add_action('GetLk!', GetLk)

    return behavior_register

def get_behaviors():
    return _make_nodes()

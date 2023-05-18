import py_trees as pt
from behavior_tree_learning.core.sbt import BehaviorNodeFactory


class PlannerBehaviorNodeFactory:
    
    def __init__(self, make_execution_node, get_condition_parameters):

        self._behavior_factory = BehaviorNodeFactory(make_execution_node)
        # self._make_execution_node = make_execution_node
        self._get_condition_parameters = get_condition_parameters

    def get_condition_parameters(self, condition):
        
        return self._get_condition_parameters(condition)

    def get_node(self, name: str, world, condition_parameters):
        
        node, has_children = self.make_node(name, world, False, condition_parameters)

        return node, has_children

    def make_node(self, name, world=None, verbose=False, condition_parameters=None):

        if name == 'nonpytreesbehavior':
            return None, False

        has_children = True
        node = self._behavior_factory._make_control_node(name)

        if node is None and self._behavior_factory._execution_behavior_register is not None:

            has_children = False
            node = self._make_execution_node(name, world, verbose, condition_parameters)

            if node is None:
                raise Exception("Unexpected character", name)

        return node, has_children

    def _make_execution_node(self, name, world, verbose, condition_parameters):

        behaviors = self._behavior_factory._execution_behavior_register.behaviors()
        for key in behaviors.keys():
            if name == key:
                return behaviors[key][1].make(name, world, verbose, condition_parameters)

        return None

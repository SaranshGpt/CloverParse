from abc import abstractmethod
from enum import Enum, auto

class CFGNode:

    def __init__(self, type, children):
        self.type = type
        self.children = children

class CFGRuleSet:

    @property
    @abstractmethod
    def Nodes(self) -> Enum:
        pass

    @property
    @abstractmethod
    def Tokens(self) -> Enum:
        pass

    @property
    @abstractmethod
    def Types(self) -> Enum:
        pass

    @property
    @abstractmethod
    def ruleset(self) -> dict[tuple, Types]:
        pass

    def reduce(self, nodes: list[CFGNode]) -> bool:

        for start in range (len(nodes)):
            
            stack_slice = nodes[start:]

            stack_slice_types = tuple([node.type for node in stack_slice])

            keys = self.ruleset.keys()
            new_node_type = self.ruleset.get(stack_slice_types, None)

            if new_node_type is None:
                new_node_type = self.ruleset.get(stack_slice_types[0], None)

            if new_node_type is not None:

                new_node = CFGNode(new_node_type, stack_slice)

                del nodes[start:]
                nodes.append(new_node)
                return True

        return False
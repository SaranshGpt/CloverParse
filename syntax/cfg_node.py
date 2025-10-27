from abc import abstractmethod
from token import Token
from enum import Enum, auto


class CFGNode:

    def __init__(self, type, children):
        self.type = type
        self.children = children


class CFGRuleSet:

    class NodeTypes(Enum):
        NEW = auto()

    @property
    @abstractmethod
    def Nodes(self) -> NodeTypes:
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
    def ruleset(self) -> dict[list[Types], Types]:
        pass

    def reduce(nodes: list[CFGNode]) -> bool:

        for start in range (len(nodes)):
            
            stack_slice = nodes[start:]

            stack_slice_types = [node.type for node in stack_slice]

            if stack_slice_types in ruleset:
                new_node_type = ruleset[stack_slice_types]

                new_node = CFGNode(new_node_type, stack_slice)

                del nodes[start:]
                nodes.append(new_node)
                return True

        return False
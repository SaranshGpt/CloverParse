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

    def reduce(self, nodes: list[CFGNode]) -> bool:

        for start in range (len(nodes)):
            
            stack_slice = nodes[start:]

            if stack_slice in ruleset:
                new_node_type = ruleset[stack_slice]

                new_node = CFGNode(new_node_type, stack_slice)

                del nodes[start:]
                nodes.append(new_node)
                return True

        return False
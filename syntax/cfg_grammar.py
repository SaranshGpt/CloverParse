from cfg_node import CFGNodeType, CFGNode, CFGRuleSet
from enum import Enum, auto

class StandardRuleset(CFGRuleSet):
    
    class Nodes(CFGRuleSet.NodeTypes):
        ASSIGNMENT = auto()

        NUMBER = auto()
        VALUE = auto()
        VXOR = auto()
        VAND = auto()
        SUM = auto()
        TERM = auto()

        RANGE = auto()

        CONDITION = auto()
        CONDITION_BODY = auto()
        NUMBER_LIST = auto()

        ENDIANNESS = auto()

        EXPRESSION = auto()
        XOR_EXPR = auto()
        AND_EXPR = auto()
        COND_VAL = auto()

    class Tokens(Enum):
        EQUALS = auto()
        NUMBER = auto()
        
        SQUARE_START = auto()
        SQUARE_END = auto()
        CURLY_START = auto()
        CURLY_END = auto()
        BRACKET_START = auto()
        BRACKET_END = auto()
        LESS_THAN = auto()
        GREATER_THAN = auto()

        COMMA = auto()
        COLON = auto()

        PLUS = auto()
        MINUS = auto()
        MULTIPLY = auto()
        DIVIDE = auto()
        MODULO = auto()

        AND = auto()
        OR = auto()
        XOR = auto()

        NEGATION = auto()
        
        LITTLE_ENDIAN = auto()
        BIG_ENDIAN = auto()

    class Types(Enum):
        VALUE = auto()
        RANGE = auto()
        EXPRESSION = auto()
        CONDITION = auto()

        NEW = auto()

        UNKNOWN = auto()

    ruleset = {
        
        [Types.NEW, Tokens.EQUALS, Nodes.VALUE]:                                Types.ASSIGNMENT,
        [Types.NEW, Tokens.EQUALS, Nodes.RANGE]:                                Types.ASSIGNMENT,
        [Types.NEW, Tokens.EQUALS, Nodes.CONDITION]:                            Types.ASSIGNMENT,
        [Types.NEW, Tokens.EQUALS, Nodes.EXPRESSION]:                           Types.ASSIGNMENT,

        [Types.VALUE]:                                                          Nodes.NUMBER,
        [Tokens.NUMBER]:                                                        Nodes.NUMBER,
        [Tokens.BRACKET_START, Nodes.VALUE, Tokens.BRACKET_END]:                Nodes.NUMBER,
        [Tokens.NEGATION, Nodes.NUMBER]:                                        Nodes.NUMBER,

        [Nodes.VALUE, Tokens.OR, Nodes.VXOR]:                                   Nodes.VALUE,
        [Nodes.VXOR]:                                                           Nodes.VALUE,

        [Nodes.VXOR, Tokens.XOR, Nodes.VAND]:                                   Nodes.VXOR,
        [Nodes.VAND]:                                                           Nodes.VXOR,

        [Nodes.VAND, Tokens.AND, Nodes.SUM]:                                    Nodes.VAND,
        [Nodes.SUM]:                                                            Nodes.VAND,

        [Nodes.SUM, Tokens.PLUS, Nodes.TERM]:                                   Nodes.SUM,
        [Nodes.SUM, Tokens.MINUS, Nodes.TERM]:                                  Nodes.SUM,
        [Nodes.TERM]:                                                           Nodes.SUM,

        [Nodes.TERM, Tokens.MULTIPLY, Nodes.NUMBER]:                            Nodes.TERM,
        [Nodes.TERM, Tokens.DIVIDE, Nodes.NUMBER]:                              Nodes.TERM,
        [Nodes.TERM, Tokens.MODULO, Nodes.NUMBER]:                              Nodes.TERM,
        [Nodes.NUMBER]:                                                         Nodes.TERM,

        
        
        [Tokens.SQUARE_START, 
            Nodes.NUMBER, Tokens.COLON, Nodes.NUMBER, 
            Tokens.COMMA,
            Nodes.NUMBER, Tokens.COLON, Nodes.NUMBER, 
        Tokens.SQUARE_END]:                                                     Nodes.RANGE,
        [Tokens.SQUARE_START, 
            Nodes.NUMBER, Tokens.COLON, Nodes.NUMBER, 
            Tokens.COMMA,
            Nodes.NUMBER, 
        Tokens.SQUARE_END]:                                                     Nodes.RANGE,
        [Tokens.SQUARE_START, 
            Nodes.NUMBER, 
            Tokens.COMMA,
            Nodes.NUMBER, Tokens.COLON, Nodes.NUMBER,
        Tokens.SQUARE_END]:                                                     Nodes.RANGE,
        [Tokens.SQUARE_START, 
            Nodes.NUMBER, 
            Tokens.COMMA,
            Nodes.NUMBER,  
        Tokens.SQUARE_END]:                                                     Nodes.RANGE,
        [Nodes.RANGE, Nodes.RANGE]:                                             Nodes.RANGE,
        [Types.RANGE]:                                                          Nodes.RANGE,



        [Nodes.RANGE, Nodes.CONDITION_BODY, Nodes.ENDIANNESS]:                  Nodes.CONDITION,
        [Tokens.NEGATION, Nodes.CONDITION]:                                     Nodes.CONDITION,
        [Types.CONDITION]:                                                      Nodes.CONDITION,
        
        [Tokens.LESS_THAN, Nodes.NUMBER, 
            Tokens.COMMA, 
        Nodes.NUMBER, Tokens.GREATER_THAN]:                                     Nodes.CONDITION_BODY,
        [Nodes.NUMBER_LIST, Tokens.CURLY_END]:                                  Nodes.CONDITION_BODY,

        [Nodes.NUMBER_LIST, Tokens.COMMA, Nodes.NUMBER]:                        Nodes.NUMBER_LIST,
        [Tokens.CURLY_START, Nodes.NUMBER]:                                     Nodes.NUMBER_LIST,

        [Tokens.LITTLE_ENDIAN]:                                                 Nodes.ENDIANNESS,
        [Tokens.BIG_ENDIAN]:                                                    Nodes.ENDIANNESS,

        [Nodes.CONDITION]:                                                      Nodes.COND_VAL,
        [Tokens.BRACKET_START, Nodes.EXPRESSION, Tokens.BRACKET_END]:           Nodes.COND_VAL,
        [Types.CONDITION]:                                                      Nodes.COND_VAL,
        [Nodes.EXPRESSION]:                                                     Nodes.COND_VAL,
        [Types.EXPRESSION]:                                                     Nodes.COND_VAL,

        [Nodes.EXPRESSION, Tokens.OR, Nodes.XOR_EXPR]:                          Nodes.EXPRESSION,
        [Nodes.XOR_EXPR]:                                                       Nodes.EXPRESSION,

        [Nodes.XOR_EXPR, Tokens.XOR, Nodes.AND_EXPR]:                           Nodes.XOR_EXPR,
        [Nodes.AND_EXPR]:                                                       Nodes.XOR_EXPR,

        [Nodes.AND_EXPR, Tokens.AND, Nodes.COND_VAL]:                           Nodes.AND_EXPR,
        [Nodes.COND_VAL]:                                                       Nodes.AND_EXPR,

    }
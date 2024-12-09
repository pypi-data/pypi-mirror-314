from typing import Tuple, List


# Adds an indentation level to a multi-line string.
def indent(s):
    return ('    ' + s.replace('\n', '\n    '))[:-4]


# Class representing a length expression.
class Length:
    def __init__(self, value:str, bound:str, consts:set) -> None:
        self.value = value
        self.bound = bound
        self.consts = consts

    def __repr__(self) -> str:
        return 'Length(%s, %s, %s)' % (repr(self.value), repr(self.bound), repr(self.consts))

    def replace(self, d:dict) -> Tuple[str,str]:
        value = str(self.value)
        bound = str(self.bound)
        for k, v in d.items():
            value = value.replace(k, v)
            bound = bound.replace(k, v)
        return (value, bound)

# Class representing a type.
class VarType:
    def __init__(self, base:str, *dims:Length) -> None:
        self.base = base
        self.dims = list(dims)

    def __repr__(self) -> str:
        return 'VarType(%s)' % ', '.join([repr(self.base)] + list(map(repr, self.dims)))

    def values(self) -> List[str]:
        return [l.value for l in self.dims]

    def bounds(self) -> List[str]:
        return [l.bound for l in self.dims]

    def addIndex(self, idx:Length):
        self.dims.append(idx)
        return self

# Class representing a reference to a variable.
class VarReference:
    def __init__(self, name:str, *idx:str) -> None:
        self.name = name
        self.idx = list(idx)

    def __repr__(self) -> str:
        return 'VarReference("%s")' % '", "'.join([self.name] + self.idx)

    def addIndex(self, idx:str):
        self.idx.append(idx)
        return self


# Class supertype grouping instructions.
class Instruction:
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return "Instruction()"


# Class representing the code to be inserted by users.
class UserCode(Instruction):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return "UserCode()"

# Class representing a block of instructions.
class Block(Instruction):
    def __init__(self, *code:Instruction) -> None:
        self.code = []
        for c in code:
            self.append(c)
    
    def __repr__(self) -> str:
        return 'Block(%s)' % ', '.join(repr(c) for c in self.code)
    
    def get(self, i:int) -> Instruction:
        return self.code[i]

    def append(self, c:Instruction) -> None:
        if isinstance(c, Block):
            self.code += c.code
        else:
            self.code.append(c)

# Class representing a declaration of homgeneous variables.
class VarDeclaration(Instruction):
    def __init__(self, type:VarType, *name:str) -> None:
        self.type = type
        self.name = name

    def __repr__(self) -> str:
        return 'VarDeclaration(%s, "%s")' % (repr(self.type), '", "'.join(self.name))

    def addIndex(self, idx:Length):
        self.type.addIndex(idx)
        return self

# Class representing a repeated block of code.
class Repeat(Instruction):
    def __init__(self, idx:str, start:int, bound:str, code:Block) -> None:
        self.idx = idx
        self.start = start
        self.bound = bound
        self.code = code

    def __repr__(self) -> str:
        return 'Repeat(%s, %s, %s, %s)' % (repr(self.idx), repr(self.start), repr(self.bound), repr(self.code))

# Class representing a read or write instruction for an inlined vector or matrix row.
class InOutSequence(Instruction):
    def __init__(self, out:bool, type:VarType, var:VarReference) -> None:
        self.out = out
        self.type = type
        self.var = var

    def __repr__(self) -> str:
        return 'InOutSequence(%s, %s, %s)' % (repr(self.out), repr(self.type), repr(self.var))

    def addIndex(self, idx:str):
        self.var.addIndex(idx)
        return self

# Class representing a read or write instruction for a line of items.
class InOutLine(Instruction):
    def __init__(self, out:bool, *items:Tuple[str,VarReference]) -> None:
        self.out = out
        self.types = [x[0] for x in items]
        self.items = [x[1] for x in items]

    def __repr__(self) -> str:
        l = [repr((self.types[i], self.items[i])) for i in range(len(self.types))]
        return 'InOutLine(%s, %s)' % (repr(self.out), ', '.join(l))

    def append(self, line) -> None:
        assert self.out == line.out
        self.types += line.types
        self.items += line.items

    def addIndex(self, idx:str):
        for x in self.items:
            x.addIndex(idx)
        return self

# Class representing a write instruction for an integer with format string (without implicit newline).
class FormatLine(Instruction):
    def __init__(self, format:str, var:str) -> None:
        self.format = format
        self.var = var

    def __repr__(self) -> str:
        return 'FormatLine(%s, %s)' % (repr(self.format), repr(self.var))

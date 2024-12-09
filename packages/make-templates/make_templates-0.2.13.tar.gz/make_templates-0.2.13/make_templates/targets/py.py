import sys
sys.path.append('..')
from ..tree import *

template = """#!/usr/bin/env python3
# %s.

import sys

# %s
# sys.stdin = open('input.txt')
# sys.stdout = open('output.txt', 'w')

%s
sys.stdout.close()
"""

locale = {
    'en' : ["NOTE: it is recommended to use this even if you don't understand the following code", "uncomment the two following lines if you want to read/write from files", "INSERT YOUR CODE HERE"],
    'it' : ["NOTA: si raccomanda di usare questo template anche se non lo si capisce completamente", "decommenta le due righe seguenti se vuoi leggere/scrivere da file", "INSERISCI IL TUO CODICE QUI"]
}

type_dict = {
    'int'    : 'int',
    'long'   : 'int',
    'double' : 'float',
    'char'   : 'str',
    'string' : 'str'
}

type_val = {
    'int'    : '0',
    'long'   : '0',
    'double' : '0.0',
    'char'   : "'-'",
    'string' : '""'
}

def build_type(t:VarType):
    vals = [x.value for x in t.dims]
    type = t.base
    if type in type_dict:
        type = type_dict[type]
    if len(vals) == 0:
        init = "%s"
    elif len(vals) == 1:
        init = "[%%s for i in range(%s)]" % vals[0]
    elif len(vals) == 2:
        init = "[[%%s for j in range(%s)] for i in range(%s)]" % (vals[1], vals[0])
    else:
        assert False
    init = init % type_val[t.base]
    return type, init

def build_reference(r):
    if isinstance(r, str):
        return r
    assert isinstance(r, VarReference)
    return r.name + ''.join('[%s]' % i for i in r.idx)

def build_declaration(d:VarDeclaration):
    _, init = build_type(d.type)
    s = ""
    for n in d.name:
        s += n + " = " + init + "\n"
    return s

def build_for(v:str, k:int, b:str, c:str):
    return "for %s in range(%s):\n%s" % (v, b if k == 0 else "1, %s+1" % b, c)

def build_inout(out:bool, types:List[str], refs:List[VarReference], end:bool):
    if len(refs) == 0 and (not out) and end:
        return "input()\n"
    if len(refs) == 0 and not (out and end):
        return ""
    if out:
        return "print(%s%s)\n" % (', '.join(build_reference(r) for r in refs), '' if end else ", end=' '")
    s = ', '.join(build_reference(r) for r in refs) + " = "
    tt = [type_dict[t] for t in types]
    if len(tt) == 1:
        if tt[0] == 'str':
            return s + "input().strip()\n"
        return s + "%s(input().strip())\n" % tt[0]
    elif len(refs) == 1:
        return s + "list(map(%s, input().strip().split()))\n" % tt[0]
    elif len(set(tt)) == 1:
        return s + "map(%s, input().strip().split())\n" % tt[0]
    else:
        return s + "[f(v) for f, v in zip([%s], input().strip().split())]\n" % ', '.join(tt)

def build_block(prog:Block, lang:str):
    s = ""
    for i in range(len(prog.code)):
        c = prog.code[i]
        if isinstance(c, VarDeclaration):
            j = i+1
            while isinstance(prog.code[j], VarDeclaration):
                j = j+1
            if not isinstance(prog.code[j], InOutLine) and not isinstance(prog.code[j], InOutSequence):
            #if len(c.type.dims) > 0 or not isinstance(prog.code[j], InOutLine):
                s += build_declaration(c)
        elif isinstance(c, Repeat):
            s += build_for(c.idx, c.start,  c.bound, indent(build_block(c.code, lang)))
        elif isinstance(c, InOutSequence):
            if c.out:
                s += build_for('i', 0, c.type.dims[-1].value, indent(build_inout(c.out, [c.type.base], [c.var.addIndex('i')], False)))
                s += build_inout(c.out, [], [], True)
            else:
                s += build_inout(c.out, [c.type.base, c.type.base], [c.var], False)
        elif isinstance(c, InOutLine):
            s += build_inout(c.out, c.types, c.items, True)
        elif isinstance(c, FormatLine):
            format = c.format.replace('{}', '%d')
            s += "print(%s %% %s, end='')\n" % (format, c.var)
        elif isinstance(c, UserCode):
            s += "# %s\n" % locale[lang][2]
        elif isinstance(c, Instruction):
            s += "\n"
        else:
            raise Exception('Unrecognised instruction "%s"' % c)
    return s

def generate(name:str, prog:Block, lang:str, bounds:dict):
    return template % (locale[lang][0], locale[lang][1], build_block(prog, lang))

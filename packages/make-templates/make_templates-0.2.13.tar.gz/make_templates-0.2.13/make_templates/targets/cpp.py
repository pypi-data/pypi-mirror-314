import sys
sys.path.append('..')
from ..tree import *

template = """// %s.

#include <fstream>
#include <iostream>
#include <string>
#include <vector>

using namespace std;

int main() {
    // %s
    // ifstream cin("input.txt");
    // ofstream cout("output.txt");

%s
    return 0;
}
"""

locale = {
    'en' : ["NOTE: it is recommended to use this even if you don't understand the following code", "uncomment the two following lines if you want to read/write from files", "INSERT YOUR CODE HERE"],
    'it' : ["NOTA: si raccomanda di usare questo template anche se non lo si capisce completamente", "decommenta le due righe seguenti se vuoi leggere/scrivere da file", "INSERISCI IL TUO CODICE QUI"]
}

type_dict = {
    'long' : 'long long'
}

type_vals = {
    'int'    : '0',
    'long long' : '0',
    'double' : '0.0',
    'char'   : "'-'",
    'string' : '""'
}

def build_type(t:VarType, initialize:bool):
    vals = [x.value for x in t.dims]
    type = t.base
    if type in type_dict:
        type = type_dict[type]
    if len(vals) == 0:
        init = " = " + type_vals[type] if initialize else ""
    elif len(vals) == 1:
        init = "(%s)" % vals[0]
    elif len(vals) == 2:
        init = "(%s, vector<%s>(%s))" % (vals[0], type, vals[1])
    else:
        assert False
    for _ in range(len(vals)):
        type = "vector<%s>" % type
    return type, init

def build_reference(r):
    if isinstance(r, str):
        return r
    assert isinstance(r, VarReference)
    return r.name + ''.join('[%s]' % i for i in r.idx)

def build_declaration(d:VarDeclaration, initialize:bool):
    type, init = build_type(d.type, initialize)
    return type + ' ' + ', '.join(n + init for n in d.name) + ';\n'

def build_for(v:str, k:int, b:str, c:str):
    return ("for (int %s = %d; %s %s %s; ++%s)" + (" {\n%s}\n" if c.count('\n') > 1 else "\n%s")) % (v, k, v, "<" if k == 0 else "<=", b, v, c)

def build_inout(out:bool, refs:List[VarReference], end:bool, fmt:bool):
    if len(refs) == 0 and not (out and end):
        return ""
    s = "cout" if out else "cin"
    sep = " << " if out else " >> "
    ms = sep + '" "' + sep if out and not fmt else sep
    if len(refs) > 0:
        s += sep + ms.join(build_reference(r) for r in refs)
    if out and not fmt:
        s += sep + ("endl" if end else '" "')
    return s + ";\n"

def build_block(prog:Block, lang:str):
    s = ""
    for l, c in enumerate(prog.code):
        if isinstance(c, VarDeclaration):
            nl = l+1
            while isinstance(prog.code[nl], VarDeclaration):
                nl += 1
            s += build_declaration(c, type(prog.code[nl]) == Instruction)
        elif isinstance(c, Repeat):
            s += build_for(c.idx, c.start, c.bound, indent(build_block(c.code, lang)))
        elif isinstance(c, InOutSequence):
            s += build_for('i', 0, c.type.dims[-1].value, indent(build_inout(c.out, [c.var.addIndex('i')], False, False)))
            s += build_inout(c.out, [], True, False)
        elif isinstance(c, InOutLine):
            s += build_inout(c.out, c.items, True, False)
        elif isinstance(c, FormatLine):
            format = c.format[1:-1].split('{}')
            s += build_inout(True, ['"%s"'%format[0], c.var, '"%s"'%format[1]], False, True)
        elif isinstance(c, UserCode):
            s += "// %s\n" % locale[lang][2]
        elif isinstance(c, Instruction):
            s += "\n"
        else:
            raise Exception('Unrecognised instruction "%s"' % c)
    return s

def generate(name:str, prog:Block, lang:str, bounds:dict):
    return template % (locale[lang][0], locale[lang][1], indent(build_block(prog, lang)))

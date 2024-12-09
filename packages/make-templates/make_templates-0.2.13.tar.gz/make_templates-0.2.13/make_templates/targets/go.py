import sys
sys.path.append('..')
from ..tree import *

template = """// %s.

package main

import (
    "bufio"
    "fmt"
    "os"
    "strconv"
)

func NextString(scanner *bufio.Scanner) string {
    scanner.Scan()
    return scanner.Text()
}

func NextByte(scanner *bufio.Scanner) byte {
    return NextString(scanner)[0]
}

func NextInt(scanner *bufio.Scanner) int {
    i, _ := strconv.Atoi(NextString(scanner))
    return i
}

func NextInt64(scanner *bufio.Scanner) int64 {
    i, _ := strconv.ParseInt(NextString(scanner), 10, 64)
    return i
}

func NextFloat64(scanner *bufio.Scanner) float64 {
    i, _ := strconv.ParseFloat(NextString(scanner), 64)
    return i
}

func main() {
    fin := os.Stdin
    fout := os.Stdout

    // %s
    // fin, _ = os.Open("input.txt")
    // fout, _ = os.Create("output.txt")

    scn := bufio.NewScanner(fin)
    scn.Split(bufio.ScanWords)

%s}
"""

locale = {
    'en' : ["NOTE: it is recommended to use this even if you don't understand the following code", "uncomment the two following lines if you want to read/write from files", "INSERT YOUR CODE HERE", "avoid unused variable error"],
    'it' : ["NOTA: si raccomanda di usare questo template anche se non lo si capisce completamente", "decommenta le due righe seguenti se vuoi leggere/scrivere da file", "INSERISCI IL TUO CODICE QUI", "evita errore variabili non usate"]
}

type_dict = {
    'char'   : 'byte',
    'string' : 'string',
    'int'    : 'int',
    'long'   : 'int64',
    'double' : 'float64'
}

type_vals = {
    'int'     : '0',
    'int64'   : '0',
    'float64' : '0.0',
    'byte'    : "'-'",
    'string'  : '""'
}

type_formats = {
    'int'    : '%v',
    'long'   : '%v',
    'double' : '%v',
    'char'   : '%c',
    'string' : '%v'
}

pending_declarations = {}

unused_vars = set()
used_vars = set()

def build_type(t:VarType, name:str):
    vals = [x.value for x in t.dims]
    type = t.base
    if type in type_dict:
        type = type_dict[type]
    if len(vals) == 0:
        init = type_vals[type]
    else:
        type = ''.join('[]' for _ in vals) + type
        init = "make(%s, %s)" % (type, vals[0])
    if len(vals) > 1:
        assert(len(vals) == 2)
        init += "\n"
        init += "for i := range %s {\n" % name
        init += "    %s[i] = make(%s, %s)\n" % (name, type[2:], vals[1])
        init += "}"
    return type, init

def build_reference(r):
    if isinstance(r, str):
        return r
    assert isinstance(r, VarReference)
    return r.name + ''.join('[%s]' % i for i in r.idx)

def build_declaration(d:VarDeclaration):
    type, init = build_type(d.type, d.name[0])
    s = ""
    for n in d.name:
        if len(d.type.dims) > 0:
            s += n + ' := ' + init + '\n'
        else:
            s += 'var ' + n + ' ' + type + ' = ' + init + '\n'
    return s

def build_for(v:str, k:int, b:str, c:str):
    return ("for %s := %d; %s %s %s; %s++" + " {\n%s}\n") % (v, k, v, "<" if k == 0 else "<=", b, v, c)

def build_inout(out:bool, types:List[str], refs:List[VarReference], end:bool):
    if len(refs) == 0 and not (out and end):
        return ""
    if out:
        fmt = " ".join(type_formats[t] for t in types)
        if end is not None:
            fmt += '\\n' if end else ' '
        return 'fmt.Fprintf(fout, %s)\n' % ', '.join(['"%s"' % fmt] + [build_reference(r) for r in refs])
    s = ""
    for i in range(len(types)):
        t = types[i]
        r = refs[i]
        s += build_reference(r) + pending_declarations[r.name] + "Next" + type_dict[t].title() + "(scn)\n"
    return s

def build_block(prog:Block, lang:str):
    global unused_vars
    s = ""
    for i in range(len(prog.code)):
        c = prog.code[i]
        if isinstance(c, VarDeclaration):
            j = i+1
            while isinstance(prog.code[j], VarDeclaration):
                j = j+1
            if len(c.type.dims) > 0 or not isinstance(prog.code[j], InOutLine):
                s += build_declaration(c)
                for n in c.name:
                    pending_declarations[n] = " = "
            else:
                unused_vars |= set(c.name)
                t = build_type(c.type, c.name[0])[0] + " "
                for n in c.name:
                    pending_declarations[n] = " := "
        elif isinstance(c, Repeat):
            used_vars.add(c.bound)
            s += build_for(c.idx, c.start,  c.bound, indent(build_block(c.code, lang)))
        elif isinstance(c, InOutSequence):
            s += build_for('i', 0, c.type.dims[-1].value, indent(build_inout(c.out, [c.type.base], [c.var.addIndex('i')], False)))
            s += build_inout(c.out, [], [], True)
        elif isinstance(c, InOutLine):
            s += build_inout(c.out, c.types, c.items, True)
        elif isinstance(c, FormatLine):
            s += "fmt.Fprintf(fout, %s, %s)\n" % (c.format.replace("{}", "%v"), c.var)
        elif isinstance(c, UserCode):
            s += "// %s\n" % locale[lang][2]
            unused_vars -= used_vars
            if len(unused_vars) > 0:
                s += "%s = %s // %s\n" % (', '.join('_' for _ in unused_vars),  ', '.join(unused_vars), locale[lang][3])
        elif isinstance(c, Instruction):
            s += "\n"
        else:
            raise Exception('Unrecognised instruction "%s"' % c)
    return s

def generate(name:str, prog:Block, lang:str, bounds:dict):
    return template % (locale[lang][0], locale[lang][1], indent(build_block(prog, lang)))

import sys
sys.path.append('..')
from ..tree import *

template = """{ %s }

%s%s
begin
{
    %s
    assign(input,  'input.txt');  reset(input);
    assign(output, 'output.txt'); rewrite(output);
}

%s
end.
"""

locale = {
    'en' : ["NOTE: it is recommended to use this even if you don't understand the following code", "uncomment the two following lines if you want to read/write from files", "INSERT YOUR CODE HERE"],
    'it' : ["NOTA: si raccomanda di usare questo template anche se non lo si capisce completamente", "decommenta le due righe seguenti se vuoi leggere/scrivere da file", "INSERISCI IL TUO CODICE QUI"]
}

type_dict = {
    'int'  : 'LongInt',
    'long' : 'Int64',
    'double' : 'Double',
    'char'  : 'Char',
    'string' : 'AnsiString'
}

type_vals = {
    'LongInt'    : '0',
    'Int64'      : '0',
    'Double'     : '0.0',
    'Char'       : "'-'",
    'AnsiString' : "''"
}

def build_type(t:VarType):
    consts = set()
    for x in t.dims:
        consts |= x.consts
    vals = [x.bound for x in t.dims]
    type = t.base
    if type in type_dict:
        type = type_dict[type]
    for v in vals:
        type = "Array[0..%s-1] of " % v + type
    return type, consts

def build_reference(r):
    if isinstance(r, str):
        return r
    assert isinstance(r, VarReference)
    return r.name + ''.join('[%s]' % i for i in r.idx)

def build_declaration(d:VarDeclaration):
    type, consts = build_type(d.type)
    return consts, type, d.name

def build_for(v:str, k:int, b:str, c:str):
    return ("for %s:=%d to %s do" + (" begin\n%send;\n" if c.count('\n') > 1 else "\n%s")) % (v, k, b + ("-1" if k == 0 else ""), c)

def build_inout(out:bool, refs:List, end:bool):
    cmd = ("Write" if out else "Read") + ("Ln" if end else "")
    not_fmt = len(refs) == 0 or not isinstance(refs[0], str)
    return cmd + '(' + (", ' ', " if out and not_fmt else ", ").join(build_reference(r) for r in refs) + (", ' '" if out and not_fmt and not end else '') + ');\n'

def build_consts(consts:set, bounds:dict):
    if len(consts) == 0:
        return ""
    s = ""
    for c in consts:
        if c not in bounds:
            print(f"[ERROR] {c} missing in limits.py but {c[-1]} is used to define array lengths")
            exit(1)
        s += "%s = %s;\n" % (c, bounds[c])
    return "const\n" + indent(s) + "\n"

def build_vars(vs):
    s = ""
    maxlen = 0
    for type, vars in vs.items():
        maxlen = max(len(', '.join(vars)), maxlen)
    for type, vars in vs.items():
        v = list(vars)
        t = ', '.join(sorted([x for x in v if x == x.upper()]) + sorted([x for x in v if x != x.upper()]))
        s += t + ' '*(maxlen - len(t)) + ' : ' + type + ';\n'
    s = "var\n" + indent(s)
    return s

def build_block(prog:Block, lang:str):
    cs = set()
    vs = {}
    s = ""
    pending_declarations = []
    for c in prog.code:
        if isinstance(c, VarDeclaration):
            consts, type, ids = build_declaration(c)
            cs |= consts
            if type not in vs:
                vs[type] = set()
            vs[type] |= set(ids)
            pending_declarations.append((type, ids))
        elif isinstance(c, Repeat):
            bc, bv, bs = build_block(c.code, lang)
            cs |= bc
            for k,v in bv.items():
                if k not in vs:
                    vs[k] = set()
                vs[k] |= v
            if 'LongInt' not in vs:
                vs['LongInt'] = set()
            vs['LongInt'].add(c.idx)
            s += build_for(c.idx, c.start,  c.bound, indent(bs))
            pending_declarations = []
        elif isinstance(c, InOutSequence):
            if 'LongInt' not in vs:
                vs['LongInt'] = set()
            vs['LongInt'].add('i')
            s += build_for('i', 0, c.type.dims[-1].value, indent(build_inout(c.out, [c.var.addIndex('i')], False)))
            s += build_inout(c.out, [], True)
            pending_declarations = []
        elif isinstance(c, InOutLine):
            s += build_inout(c.out, c.items, True)
            pending_declarations = []
        elif isinstance(c, FormatLine):
            format = c.format[1:-1].split('{}')
            s += build_inout(True, ["'%s'"%format[0], c.var, "'%s'"%format[1]], False)
        elif isinstance(c, UserCode):
            s = s[:-1] + "{ %s }\n" % locale[lang][2]
        elif isinstance(c, Instruction):
            for type, ids in pending_declarations:
                for id in ids:
                    if type in type_vals:
                            s += id + " := " + type_vals[type] + ";\n"
                    else:
                        dimensions = type.count('Array')
                        if dimensions == 1:
                            l, t = type[9:].split('] of ')
                            s += "for i := 0 to %s do %s[i] := %s;\n" % (l, ids[0], type_vals[t])
                        elif dimensions == 2:
                            # Array[0..MAXM-1] of Array[0..MAXN-1] of LongInt
                            dim1 = type.split('..')[1].split(']')[0]
                            dim2 = type.split('..')[2].split(']')[0]
                            t = type.split(' of ')[-1]

                            s += "for i := 0 to %s do begin\n" % dim1
                            s += indent("    for j := 0 to %s do %s[i][j] := %s;\n" % (dim2, ids[0], type_vals[t]))
                            s += "end;\n"
                        else:
                            assert False

            pending_declarations = []
            s += "\n"
        else:
            raise Exception('Unrecognised instruction "%s"' % c)
    return cs, vs, s

def generate(name:str, prog:Block, lang:str, bounds:dict):
    bc, bv, bs = build_block(prog, lang)
    return template % (locale[lang][0], build_consts(bc, bounds), build_vars(bv), locale[lang][1], indent(bs))

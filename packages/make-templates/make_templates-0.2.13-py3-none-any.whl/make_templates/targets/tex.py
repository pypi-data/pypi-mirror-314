import sys
sys.path.append('..')
from ..tree import *

templates = {"it" : {}, "en" : {}}

templates['it']['rep'] = """
\\InputFile

La prima riga del file di input contiene un intero $%s$, il numero di casi di test. Seguono $%s$ casi di test, ognuno preceduto da una riga vuota.

Ogni caso di test è composto come segue:
\\begin{itemize}
%s\\end{itemize}


\\OutputFile

Il file di output deve contenere $%s$ righe relative ai diversi casi di test, ciascuna composta da%s
"""

templates['it']['fmt'] = """
\\InputFile

La prima riga del file di input contiene un intero $%s$, il numero di casi di test. Seguono $%s$ casi di test, numerati da $1$ a $%s$. Ogni caso di test è preceduto da una riga vuota.

Ogni caso di test è composto come segue:
\\begin{itemize}
%s\\end{itemize}


\\OutputFile

Il file di output deve contenere la risposta ai casi di test che sei riuscito a risolvere. Per ogni caso di test che hai risolto, il file di output deve contenere una riga con la dicitura ``\\texttt{%s}'', dove \\texttt{%s} è il numero del caso di test (a partire da $1$), seguita da%s
"""

templates['it']['std'] = """
\\InputFile

Il file di input è composto come segue:
\\begin{itemize}
%s\\end{itemize}


\\OutputFile

Il file di output deve contenere una riga composta da%s
"""

templates['en']['rep'] = """
\\InputFile

The first line of the input file contains a single integer $%s$, the number of test cases. $%s$ test cases follow, each preceded by an empty line.

Each test case consists of:
\\begin{itemize}
%s\\end{itemize}


\\OutputFile

The output file must contain $%s$ lines corresponding to the test cases, each consisting of %s
"""

templates['en']['fmt'] = """
\\InputFile

The first line of the input file contains a single integer $%s$, the number of test cases. $%s$ test cases follow, numbered from $1$ to $%s$, each preceded by an empty line.

Each test case consists of:
\\begin{itemize}
%s\\end{itemize}


\\OutputFile

The output file must contain the answer to the test cases you were able to solve. For each test case you solved, the output file must contain a line with ``\\texttt{%s}'', where \\texttt{%s} is the number of the test case (starting from $1$), followed by %s
"""

templates['en']['std'] = """
\\InputFile

The input file consists of:
\\begin{itemize}
%s\\end{itemize}


\\OutputFile

The output file must contain a single line consisting of %s
"""

locale = {
    'en' : [],
    'it' : []
}

type_dict = {
    'long' : 'long long'
}

itanum = [
    ["", "", "i due", "i tre", "i quattro", "i cinque", "i sei", "i sette", "gli otto", "i nove"],
    ["", "", "le due", "le tre", "le quattro", "le cinque", "le sei", "le sette", "le otto", "le nove"]
]

typegender = {
    'int' : (0, "l'intero", 'interi'),
    'long' : (0, "l'intero a 64 bit", 'interi a 64 bit'),
    'double' : (0, 'il numero con la virgola', 'numeri con la virgola'),
    'char' : (0, 'il carattere', 'caratteri'),
    'string' : (1, 'la stringa', 'stringhe')
}

engtypes = {
    'int' : 'integer',
    'long' : '64-bit integer',
    'double' : 'floating-point number',
    'char' : 'character',
    'string' : 'string'
}

def type_name(t:str, i:int, lang:str):
    if lang == 'en':
        return engtypes[t] + ('s' if i > 1 else '')
    if i == 1:
        return typegender[t][1]
    return itanum[typegender[t][0]][i] + ' ' + typegender[t][2]

def build_type(t:VarType):
    vals = [x.value for x in t.dims]
    type = t.base
    if type in type_dict:
        type = type_dict[type]
    if len(vals) == 0:
        init = ""
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
        return ("$%s$" if len(r) == 1 else "$\\mathtt{%s}$") % r
    assert isinstance(r, VarReference)
    s = r.name
    if len(s) > 1:
        s = "\\mathtt{%s}" % s
    if len(r.idx):
        s += "_{%s}" % ','.join(r.idx)
    return "$" + s + "$"

def build_declaration(d:VarDeclaration):
    type, init = build_type(d.type)
    return type + ' ' + ', '.join(n + init for n in d.name) + ';\n'

def build_for(v:str, k:int, b:str, c:str):
    return ("for (int %s = %d; %s %s %s; ++%s)" + (" {\n%s}\n" if c.count('\n') > 1 else "\n%s")) % (v, k, v, "<" if k == 0 else "<=", b, v, c)

def build_inout(types:List[str], refs:List[VarReference], lang:str):
    s = ""
    l = []
    for i in range(len(refs)):
        if i == 0 or types[i] != l[-1][0]:
            l.append((types[i], []))
        l[-1][1].append(build_reference(refs[i]))
    l = [type_name(t, len(vars), lang) + ' ' + ', '.join(vars) for t, vars in l]
    if len(l) == 1:
        s += l[0]
    else:
        s += "; ".join(l[:-1]) + (" e " if lang == 'it' else " and ") + l[-1]
    return s + ".\n"

def build_sequence(basetype:str, typedims:List[Length], ref:VarReference, lang:str):
    if lang == "en":
        s = "the "
    else:
        s = ["gli ", "le "][typegender[basetype][0]]
    s += build_reference(typedims[0].value)
    s += " " + (typegender[basetype][2] if lang == "it" else engtypes[basetype]+'s') + " "
    s += build_reference(ref.addIndex('0'))[:-1]
    s += ", \\, \\ldots, \\, "
    ref.idx[-1] = typedims[0].value + "-1"
    s += build_reference(ref)[1:]
    s += ".\n"
    return s

def build_block(prog:Block, lang:str):
    s = ""
    for c in prog.code:
        if isinstance(c, VarDeclaration):
            pass
        elif isinstance(c, Repeat):
            s += "  \\item " + build_reference(c.bound) + (" righe, la " if lang == "it" else " lines, the ") + build_reference(c.idx) +  ("-esima contenente " if lang == "it" else "-th of which consisting of ")
            if isinstance(c.code.code[0], InOutLine):
                s += build_inout(c.code.code[0].types, c.code.code[0].items, lang)
            elif isinstance(c.code.code[0], InOutSequence):
                s += build_sequence(c.code.code[0].type.base, c.code.code[0].type.dims, c.code.code[0].var, lang)
            else:
                assert False
        elif isinstance(c, InOutSequence):
            s += "  \\item " + ("una riga contenente " if lang == "it" else "a line containing ") + build_sequence(c.type.base, c.type.dims, c.var, lang)
        elif isinstance(c, InOutLine):
            s += "  \\item " + ("una riga contenente " if lang == "it" else "a line containing ") + build_inout(c.types, c.items, lang)
        elif isinstance(c, FormatLine):
            assert False
        elif isinstance(c, UserCode):
            pass
        elif isinstance(c, Instruction):
            pass
        else:
            raise Exception('Unrecognised instruction "%s"' % c)
    return s

def generate(name:str, prog:Block, lang:str, bounds:dict):
    if isinstance(prog.code[-1], Repeat):
        rep = prog.code[-1]
        fmt = rep.code.code[-2].format[1:-1] if len(rep.code.code) >1 and isinstance(rep.code.code[-2], FormatLine) else ""
        T = rep.bound
        out = rep.code.code[-1]
        prog.code = rep.code.code[1:-2]
        if fmt == "":
            t = templates[lang]['rep'] % (T, T, "%s", rep.bound, "%s")
        else:
            t = templates[lang]['fmt'] % (T, T, T, "%s", fmt.replace("{}", rep.idx), rep.idx, "%s")
    else:
        out = prog.code[-1]
        prog.code = prog.code[:-1]
        t = templates[lang]['std']
    prog = build_block(prog, lang)
    out = build_block(Block(out), lang)[28 if lang == "it" else 26:]
    if lang == "it":
        if out[:2] == "il":
            out = out[1:]
        elif out[0] == "l":
            out = "l" + out
    return t[1:] % (prog, out)

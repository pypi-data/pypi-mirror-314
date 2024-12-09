import sys
sys.path.append('..')
from ..tree import *

template = """// %s.

using System;
using System.IO;
using System.Linq;
using System.Collections.Generic;

namespace %s {

    class Program {
        static void Main(String[] args) {
            StreamReader streamReader = new StreamReader(Console.OpenStandardInput());
            StreamWriter streamWriter = new StreamWriter(Console.OpenStandardOutput());
            // %s
            // streamReader = new StreamReader("input.txt");
            // streamWriter = new StreamWriter("output.txt");

            IEnumerator<String> it = GetEnumerator(streamReader);

%s
            streamReader.Close();
            streamWriter.Close();
        }

        static IEnumerator<String> GetEnumerator(StreamReader sr) {
            String line;
            while ((line = sr.ReadLine()) != null) {
                String[] tokens = line.Split(' ').Where(t => t.Length > 0).ToArray();
                foreach (String t in tokens) {
                    yield return t;
                }
            }
        }

        static String Next(IEnumerator<String> iterator) {
            return iterator.MoveNext() ? iterator.Current : null;
        }
    }
}
"""

locale = {
    'en' : ["NOTE: it is recommended to use this even if you don't understand the following code", "uncomment the two following lines if you want to read/write from files", "INSERT YOUR CODE HERE"],
    'it' : ["NOTA: si raccomanda di usare questo template anche se non lo si capisce completamente", "decommenta le due righe seguenti se vuoi leggere/scrivere da file", "INSERISCI IL TUO CODICE QUI"]
}

type_dict = {
    'string' : 'String'
}

type_formats = {
    'int'    : '%d',
    'long'   : '%d',
    'double' : '%f',
    'char'   : '%c',
    'string' : '%s'
}

type_vals = {
    'int'    : '0',
    'long'   : '0',
    'double' : '0.0',
    'char'   : "'-'",
    'String' : '""'
}

read_dict = {
    'int'    : 'Int32',
    'long'   : 'Int64'
}

pending_declarations = {}

def build_type(t:VarType):
    vals = [x.value for x in t.dims]
    type = t.base
    if type in type_dict:
        type = type_dict[type]
    if len(vals) == 0:
        init = " = " + type_vals[type]
    else:
        init = " = new " + type + "[" + ', '.join('%s'%v for v in vals) + "]"
        type += "[" + ','*(len(vals)-1) + "]"
    return type, init

def build_reference(r):
    if isinstance(r, str):
        return r
    assert isinstance(r, VarReference)
    s = r.name
    if len(r.idx) > 0:
        s += "[" + ', '.join('%s' % i for i in r.idx) + "]"
    return s

def build_declaration(d:VarDeclaration):
    type, init = build_type(d.type)
    return type + ' ' + ', '.join(n + init for n in d.name) + ';\n'

def build_for(v:str, k:int, b:str, c:str):
    return ("for (int %s = %d; %s %s %s; ++%s)" + (" {\n%s}\n" if c.count('\n') > 1 else "\n%s")) % (v, k, v, "<" if k == 0 else "<=", b, v, c)

def build_inout(out:bool, types, refs:List[VarReference], end:bool):
    if len(refs) == 0 and not (out and end):
        return ""
    if out:
        v = ['{'+build_reference(r)+'}' for r in refs]
        fmt = types != ""
        if fmt:
            types = types % v[0]
            v = v[1:]
        return ('streamWriter.Write' + ('Line($"%s");\n' if end else '($"%s ");\n' if not fmt else '($"%s");\n')) % (types + " ".join(r for r in v))
    s = ""
    for i in range(len(types)):
        t = types[i]
        r = refs[i]
        s += pending_declarations[r.name] + build_reference(r) + " = Convert.To" + (read_dict[t] if t in read_dict else t.capitalize()) + "(Next(it));\n"
    return s

def build_block(prog:Block, lang:str):
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
                    pending_declarations[n] = ""
            else:
                t = build_type(c.type)[0] + " "
                for n in c.name:
                    pending_declarations[n] = t
        elif isinstance(c, Repeat):
            s += build_for(c.idx, c.start,  c.bound, indent(build_block(c.code, lang)))
        elif isinstance(c, InOutSequence):
            s += build_for('i', 0, c.type.dims[-1].value, indent(build_inout(c.out, "" if c.out else [c.type.base], [c.var.addIndex('i')], False)))
            s += build_inout(c.out, "", [], True)
        elif isinstance(c, InOutLine):
            s += build_inout(c.out, "" if c.out else c.types, c.items, True)
        elif isinstance(c, FormatLine):
            format = c.format[1:-1].replace('{}', '%s')
            s += build_inout(True, format, [c.var], False)
        elif isinstance(c, UserCode):
            s += "// %s\n" % locale[lang][2]
        elif isinstance(c, Instruction):
            s += "\n"
        else:
            raise Exception('Unrecognised instruction "%s"' % c)
    return s

def generate(name:str, prog:Block, lang:str, bounds:dict):
    return template % (locale[lang][0], name, locale[lang][1], indent(indent(indent(build_block(prog, lang)))))

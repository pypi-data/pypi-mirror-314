import sys
sys.path.append('..')
from ..tree import *

template = """' %s.

Imports System.IO
Module %s
    Public Tokens As String() = New String() { }
    Public CurrentToken As Integer = 0

    Public Function NextString() as String
        If CurrentToken + 1 >= Tokens.Length Then
            Dim input as String = Trim(Console.ReadLine)
            While Len(input) = 0
                input = Trim(Console.ReadLine)
            End While
            Tokens = input.Split(" ")
            CurrentToken = 0
        Else
            CurrentToken = CurrentToken + 1
        End If
        Return Tokens(CurrentToken)
    End Function

    Public Sub Main()
        Dim SR As StreamReader = Nothing, SW As StreamWriter = Nothing

        ' %s
        ' SR = New StreamReader("input.txt") : Console.SetIn(SR)
        ' SW = New StreamWriter("output.txt", append:=False) : Console.SetOut(SW)

%s
        If SR IsNot Nothing Then SR.Close()
        If SW IsNot Nothing Then SW.Close()
    End Sub
End Module
"""

locale = {
    'en' : ["NOTE: it is recommended to use this even if you don't understand the following code", "uncomment the two following lines if you want to read/write from files", "INSERT YOUR CODE HERE", "avoid unused variable error"],
    'it' : ["NOTA: si raccomanda di usare questo template anche se non lo si capisce completamente", "decommenta le due righe seguenti se vuoi leggere/scrivere da file", "INSERISCI IL TUO CODICE QUI", "evita errore variabili non usate"]
}

type_dict = {
    'int'    : 'Integer'
}

type_vals = {
    'int'     : '0',
    'long'    : '0',
    'double'  : '0.0',
    'char'    : '"-"c',
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

def build_type(t:VarType, name:str):
    vals = [x.value for x in t.dims]
    type = t.base
    init = type_vals[type]
    if type in type_dict:
        type = type_dict[type]
    return type.title(), init

def build_reference(r):
    if isinstance(r, str):
        return r
    assert isinstance(r, VarReference)
    return r.name if len(r.idx) == 0 else r.name + '(%s)' % ', '.join(r.idx)

def build_declaration(d:VarDeclaration):
    type, init = build_type(d.type, d.name[0])
    s = ""
    for n in d.name:
        if len(d.type.dims) > 0:
            s += 'Dim ' + n + '(' + ', '.join(x.value+'-1' for x in d.type.dims) + ') As ' + type + '\n'
        else:
            s += 'Dim ' + n + ' As ' + type + ' = ' + init + '\n'
    return s

def build_for(v:str, k:int, b:str, c:str):
    return ("For %s As Integer = %d To %s\n%sNext %s\n") % (v, k, b+'-1' if k == 0 else b, c, v)

def build_inout(out:bool, types:List[str], refs:List[VarReference], end:bool):
    if len(refs) == 0 and not (out and end):
        return ""
    if out:
        func = "Write"
        args = ' & " " & '.join(build_reference(r) for r in refs)
        if end is not None:
            if end:
                func += "Line"
            else:
                args += ' & " "'
        return 'Console.%s(%s)\n' % (func, args)
    s = ""
    for i in range(len(types)):
        t = types[i]
        r = refs[i]
        s += pending_declarations[r.name] % build_reference(r) + "NextString()\n"
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
                    pending_declarations[n] = "%s = "
            else:
                t = build_type(c.type, c.name[0])[0]
                for n in c.name:
                    pending_declarations[n] = "Dim %s As %s = " % ('%s', t)
        elif isinstance(c, Repeat):
            s += build_for(c.idx, c.start,  c.bound, indent(build_block(c.code, lang)))
        elif isinstance(c, InOutSequence):
            s += build_for('i', 0, c.type.dims[-1].value, indent(build_inout(c.out, [c.type.base], [c.var.addIndex('i')], False)))
            s += build_inout(c.out, [], [], True)
        elif isinstance(c, InOutLine):
            s += build_inout(c.out, c.types, c.items, True)
        elif isinstance(c, FormatLine):
            s += "Console.Write(%s)\n" % c.format.replace("{}", '" & %s & "' % c.var)
        elif isinstance(c, UserCode):
            s += "' %s\n" % locale[lang][2]
        elif isinstance(c, Instruction):
            s += "\n"
        else:
            raise Exception('Unrecognised instruction "%s"' % c)
    return s

def generate(name:str, prog:Block, lang:str, bounds:dict):
    return template % (locale[lang][0], name, locale[lang][1], indent(indent(build_block(prog, lang))))

from .parser.IOParser import IOParser
from .parser.IOParserVisitor import IOParserVisitor
from .tree import *

# Visitor analysing a parse tree and returning: list of errors, code structure, ?
class Analyzer(IOParserVisitor):
    # Initialize the analyzer.
    def __init__(self):
        self.section = ""
        self.repeatVar = None
        self.definedVars = {'i', 'j'}
        self.loweredVars = {'i', 'j'}
        self.keywords = {'ansistring', 'array', 'assert', 'begin', 'bufio', 'byte', 'char', 'cin', 'class', 'const', 'convert', 'cout', 'do', 'double', 'end', 'fin', 'float', 'float64', 'fmt', 'for', 'foreach', 'fout', 'from', 'if', 'import', 'in', 'input', 'int', 'int64', 'is', 'it', 'label', 'list', 'long', 'main', 'make', 'map', 'namespace', 'new', 'next', 'of', 'os', 'print', 'printf', 'private', 'prnt', 'public', 'range', 'read', 'return', 'scanf', 'scn', 'static', 'stdin', 'stdout', 'str', 'strconv', 'string', 'sys', 'system', 'to', 'using', 'var', 'vector', 'void', 'while', 'write', 'yield', 'zip'}


    # Adds a variable in the definition list.
    def defineVar(self, var:str):
        if var.lower() in self.keywords:
            self.definedVars.add(var)
            return ['Variable name "%s" forbidden' % var]
        if var.lower() in self.loweredVars:
            self.definedVars.add(var)
            return ['Redefinition of variable "%s"' % var]
        self.definedVars.add(var)
        self.loweredVars.add(var.lower())
        return []


    # Checks that a variable is in the definition list.
    def checkVar(self, var:str):
        if var in self.definedVars:
            return []
        return ['Reference to undefined variable "%s"' % var]


    # Visit a parse tree produced by IOParser#fileSpec.
    def visitFileSpec(self, ctx:IOParser.FileSpecContext):
        err = []
        instr = Block()
        if ctx.REPEAT():
            instr.append(InOutLine(False))
            idx, bound = ctx.IDENT()
            idx = idx.getText()
            bound = bound.getText()
            err += self.defineVar(idx)
            err += self.defineVar(bound)
            self.repeatVar = idx
        ei, i = self.visitInputFile(ctx.inputFile())
        eo, o = self.visitOutputFile(ctx.outputFile())
        instr.append(i)
        instr.append(o)
        if ctx.REPEAT():
            instr = Block(VarDeclaration(VarType('int'), bound), InOutLine(False, ('int', VarReference(bound))), Repeat(idx, 1, bound, instr))
        return err + ei + eo, instr


    # Visit a parse tree produced by IOParser#inputFile.
    def visitInputFile(self, ctx:IOParser.InputFileContext):
        self.section = "input"
        err = []
        block = Block()
        for line in ctx.inputLine():
            el, l = self.visitInputLine(line)
            err += el
            block.append(l)
        return err, block


    # Visit a parse tree produced by IOParser#outputFile.
    def visitOutputFile(self, ctx:IOParser.OutputFileContext):
        self.section = "output"
        err = []
        total_block = Block()
        block2 = Block()
        for line in ctx.outputLine():
            el, block = self.visitOutputLine(line)
            instr = block.code[-2]
            block.code = block.code[:-2]
            block2.append(instr)
            err += el
            total_block.append(block)

        total_block.append(Instruction())
        total_block.append(Instruction())
        total_block.append(UserCode())
        total_block.append(Instruction())
        total_block.append(Instruction())
        if ctx.STR():
            if self.repeatVar is None:
                err.append('Output header formatter is not allowed without a repeat clause: "%s"' % ctx.STR().getText())
            total_block.append(FormatLine(ctx.STR().getText(), self.repeatVar))
        total_block.append(block2)
        return err, total_block


    # Visit a parse tree produced by IOParser#inputLine.
    def visitInputLine(self, ctx:IOParser.InputLineContext):
        if ctx.values():
            return self.visitValues(ctx.values())
        elif ctx.vectors():
            return self.visitVectors(ctx.vectors())
        elif ctx.vector():
            return self.visitVector(ctx.vector())
        else:
            return self.visitMatrix(ctx.matrix())


    # Visit a parse tree produced by IOParser#outputLine.
    def visitOutputLine(self, ctx:IOParser.OutputLineContext):
        return self.visitInputLine(ctx)


    # Visit a parse tree produced by IOParser#values.
    def visitValues(self, ctx:IOParser.ValuesContext):
        err = []
        if self.section == "":
            raise Exception("Internal error: undefined section")
        block = Block()
        instr = InOutLine(self.section == "output")
        for c in ctx.homoValues():
            ev, v = self.visitHomoValues(c)
            err += ev
            block.append(v.get(0))
            instr.append(v.get(1))
        block.append(instr)
        block.append(Instruction())
        return err, block


    # Visit a parse tree produced by IOParser#homoValues.
    def visitHomoValues(self, ctx:IOParser.HomoValuesContext):
        err, t = self.visitVarType(ctx.varType())
        ids = []
        for i in ctx.IDENT():
            id = i.getText()
            err += self.defineVar(id)
            ids.append(id)
        type = VarType(t)
        if self.section == "":
            raise Exception("Internal error: undefined section")
        instr = InOutLine(self.section == "output", *[(t, VarReference(id)) for id in ids])
        return err, Block(VarDeclaration(type, *ids), instr)


    # Visit a parse tree produced by IOParser#vectors.
    def visitVectors(self, ctx:IOParser.VectorsContext):
        eb, b = self.visitValues(ctx.values())
        el, l = self.visitArithExpr(ctx.arithExpr())
        if self.section == "":
            raise Exception("Internal error: undefined section")
        for c in b.code[:-2]:
            c.addIndex(l)
        b.code[-2].addIndex('i')
        b.code[-2] = Repeat('i', 0, l.value, Block(b.code[-2]))
        return eb + el, b


    # Visit a parse tree produced by IOParser#vector.
    def visitVector(self, ctx:IOParser.VectorContext):
        id = ctx.IDENT().getText()
        err = self.defineVar(id)
        et, t = self.visitVarType(ctx.varType())
        el, l = self.visitArithExpr(ctx.arithExpr())
        type = VarType(t, l)
        ref = VarReference(id)
        if self.section == "":
            raise Exception("Internal error: undefined section")
        return et + el + err, Block(VarDeclaration(type, id), InOutSequence(self.section == "output", type, ref), Instruction())


    # Visit a parse tree produced by IOParser#matrix.
    def visitMatrix(self, ctx:IOParser.MatrixContext):
        id = ctx.IDENT().getText()
        err = self.defineVar(id)
        et, t = self.visitVarType(ctx.varType())
        en, n = self.visitArithExpr(ctx.arithExpr(0))
        em, m = self.visitArithExpr(ctx.arithExpr(1))
        type = VarType(t, n, m)
        ref = VarReference(id, 'j')
        rep = Repeat('j', 0, n.value, Block(InOutSequence(self.section == "output", type, ref)))
        return et + en + em + err, Block(VarDeclaration(type, id), rep, Instruction())


    # Visit a parse tree produced by IOParser#varType.
    def visitVarType(self, ctx:IOParser.VarTypeContext):
        return [], ctx.getText()


    # Visit a parse tree produced by IOParser#arithExpr.
    def visitArithExpr(self, ctx:IOParser.ArithExprContext):
        if not ctx.arithExpr():
            return self.visitAddend(ctx.addend())
        err = []
        op = ctx.PLUS() or ctx.MINUS()
        op = ' ' + op.getText() + ' '
        a, b = ctx.arithExpr(), ctx.addend()
        if op == " - ":
            if b.addend() is not None or b.term().NUM() is None:
                err.append('Subtraction by a non-constant expression is forbidden: "%s"' % ctx.getText())
        if a.arithExpr() is None and a.addend().addend() is None and not b.addend() and a.addend().term().NUM() and b.term().NUM():
            err.append('Operations between constants are forbidden: "%s"' % ctx.getText())
        ea, a = self.visitArithExpr(a)
        eb, b = self.visitAddend(b)
        return ea + eb + err, Length(a.value + op + b.value, a.bound + op + b.bound, a.consts | b.consts)


    # Visit a parse tree produced by IOParser#addend.
    def visitAddend(self, ctx:IOParser.AddendContext):
        if not ctx.addend():
            return self.visitTerm(ctx.term())
        err = []
        op = ctx.MULT() or ctx.DIV()
        op = ' ' + op.getText() + ' '
        a, b = ctx.addend(), ctx.term()
        if op == " / ":
            if b.NUM() is None:
                err.append('Division by a non-constant expression is forbidden: "%s"' % ctx.getText())
        if a.addend() is None and a.term().NUM() and b.NUM():
            err.append('Operations between constants are forbidden: "%s"' % ctx.getText())
        ea, a = self.visitAddend(a)
        eb, b = self.visitTerm(b)
        return ea + eb + err, Length(a.value + op + b.value, a.bound + op + b.bound, a.consts | b.consts)


    # Visit a parse tree produced by IOParser#term.
    def visitTerm(self, ctx:IOParser.TermContext):
        err = []
        if ctx.IDENT():
            id = ctx.IDENT().getText()
            err = self.checkVar(id)
            if id != id.upper() or len(id) != 1:
                err.append('Variables used to define array lengths should be single uppercase letters: "%s"' % id)
            return err, Length(id, 'MAX'+id, set(['MAX'+id]))
        elif ctx.NUM():
            n = ctx.NUM().getText()
            return err, Length(n, n, set())
        else:
            if ctx.arithExpr().addend() and ctx.arithExpr().addend().term():
                err.append('Parentheses around a primitive term are forbidden: "%s"' % ctx.getText())
            l = self.visitArithExpr(ctx.arithExpr())
            l.value = '(' + l.value + ')'
            l.bound = '(' + l.bound + ')'
            return err, l

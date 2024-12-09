# Generated from /Users/harniver/Git/olimpiadi/make-templates/grammar/IOParser.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .IOParser import IOParser
else:
    from IOParser import IOParser

# This class defines a complete generic visitor for a parse tree produced by IOParser.

class IOParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by IOParser#fileSpec.
    def visitFileSpec(self, ctx:IOParser.FileSpecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IOParser#inputFile.
    def visitInputFile(self, ctx:IOParser.InputFileContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IOParser#outputFile.
    def visitOutputFile(self, ctx:IOParser.OutputFileContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IOParser#inputLine.
    def visitInputLine(self, ctx:IOParser.InputLineContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IOParser#outputLine.
    def visitOutputLine(self, ctx:IOParser.OutputLineContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IOParser#values.
    def visitValues(self, ctx:IOParser.ValuesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IOParser#homoValues.
    def visitHomoValues(self, ctx:IOParser.HomoValuesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IOParser#vectors.
    def visitVectors(self, ctx:IOParser.VectorsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IOParser#vector.
    def visitVector(self, ctx:IOParser.VectorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IOParser#matrix.
    def visitMatrix(self, ctx:IOParser.MatrixContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IOParser#varType.
    def visitVarType(self, ctx:IOParser.VarTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IOParser#arithExpr.
    def visitArithExpr(self, ctx:IOParser.ArithExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IOParser#addend.
    def visitAddend(self, ctx:IOParser.AddendContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by IOParser#term.
    def visitTerm(self, ctx:IOParser.TermContext):
        return self.visitChildren(ctx)



del IOParser
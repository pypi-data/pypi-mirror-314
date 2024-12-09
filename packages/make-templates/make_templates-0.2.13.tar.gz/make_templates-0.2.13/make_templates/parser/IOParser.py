# Generated from /home/davide/Desktop/olinfo/make-templates/grammar/IOParser.g4 by ANTLR 4.13.1
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,29,195,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        1,0,5,0,30,8,0,10,0,12,0,33,9,0,1,0,1,0,1,0,1,0,1,0,1,0,3,0,41,8,
        0,1,0,5,0,44,8,0,10,0,12,0,47,9,0,1,0,1,0,4,0,51,8,0,11,0,12,0,52,
        1,0,1,0,5,0,57,8,0,10,0,12,0,60,9,0,1,0,1,0,1,1,1,1,1,1,4,1,67,8,
        1,11,1,12,1,68,1,1,1,1,4,1,73,8,1,11,1,12,1,74,1,1,5,1,78,8,1,10,
        1,12,1,81,9,1,1,2,1,2,1,2,4,2,86,8,2,11,2,12,2,87,1,2,1,2,4,2,92,
        8,2,11,2,12,2,93,3,2,96,8,2,1,2,1,2,4,2,100,8,2,11,2,12,2,101,1,
        2,5,2,105,8,2,10,2,12,2,108,9,2,1,3,1,3,1,3,1,3,3,3,114,8,3,1,4,
        1,4,1,4,1,4,3,4,120,8,4,1,5,1,5,1,5,4,5,125,8,5,11,5,12,5,126,1,
        6,1,6,1,6,1,6,5,6,133,8,6,10,6,12,6,136,9,6,1,7,1,7,1,7,1,7,1,7,
        1,7,1,7,1,7,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,9,1,9,1,9,1,9,1,9,1,9,
        1,9,1,9,1,9,1,9,1,10,1,10,1,11,1,11,1,11,1,11,1,11,1,11,5,11,171,
        8,11,10,11,12,11,174,9,11,1,12,1,12,1,12,1,12,1,12,1,12,5,12,182,
        8,12,10,12,12,12,185,9,12,1,13,1,13,1,13,1,13,1,13,1,13,3,13,193,
        8,13,1,13,0,2,22,24,14,0,2,4,6,8,10,12,14,16,18,20,22,24,26,0,3,
        1,0,1,5,1,0,6,7,1,0,8,9,205,0,31,1,0,0,0,2,63,1,0,0,0,4,82,1,0,0,
        0,6,113,1,0,0,0,8,119,1,0,0,0,10,124,1,0,0,0,12,128,1,0,0,0,14,137,
        1,0,0,0,16,145,1,0,0,0,18,152,1,0,0,0,20,162,1,0,0,0,22,164,1,0,
        0,0,24,175,1,0,0,0,26,192,1,0,0,0,28,30,5,19,0,0,29,28,1,0,0,0,30,
        33,1,0,0,0,31,29,1,0,0,0,31,32,1,0,0,0,32,40,1,0,0,0,33,31,1,0,0,
        0,34,35,5,20,0,0,35,36,5,29,0,0,36,37,5,21,0,0,37,38,5,29,0,0,38,
        39,5,17,0,0,39,41,5,19,0,0,40,34,1,0,0,0,40,41,1,0,0,0,41,45,1,0,
        0,0,42,44,5,19,0,0,43,42,1,0,0,0,44,47,1,0,0,0,45,43,1,0,0,0,45,
        46,1,0,0,0,46,48,1,0,0,0,47,45,1,0,0,0,48,50,3,2,1,0,49,51,5,19,
        0,0,50,49,1,0,0,0,51,52,1,0,0,0,52,50,1,0,0,0,52,53,1,0,0,0,53,54,
        1,0,0,0,54,58,3,4,2,0,55,57,5,19,0,0,56,55,1,0,0,0,57,60,1,0,0,0,
        58,56,1,0,0,0,58,59,1,0,0,0,59,61,1,0,0,0,60,58,1,0,0,0,61,62,5,
        0,0,1,62,1,1,0,0,0,63,64,5,22,0,0,64,66,5,17,0,0,65,67,5,19,0,0,
        66,65,1,0,0,0,67,68,1,0,0,0,68,66,1,0,0,0,68,69,1,0,0,0,69,70,1,
        0,0,0,70,79,3,6,3,0,71,73,5,19,0,0,72,71,1,0,0,0,73,74,1,0,0,0,74,
        72,1,0,0,0,74,75,1,0,0,0,75,76,1,0,0,0,76,78,3,6,3,0,77,72,1,0,0,
        0,78,81,1,0,0,0,79,77,1,0,0,0,79,80,1,0,0,0,80,3,1,0,0,0,81,79,1,
        0,0,0,82,83,5,23,0,0,83,85,5,17,0,0,84,86,5,19,0,0,85,84,1,0,0,0,
        86,87,1,0,0,0,87,85,1,0,0,0,87,88,1,0,0,0,88,95,1,0,0,0,89,91,5,
        27,0,0,90,92,5,19,0,0,91,90,1,0,0,0,92,93,1,0,0,0,93,91,1,0,0,0,
        93,94,1,0,0,0,94,96,1,0,0,0,95,89,1,0,0,0,95,96,1,0,0,0,96,97,1,
        0,0,0,97,106,3,8,4,0,98,100,5,19,0,0,99,98,1,0,0,0,100,101,1,0,0,
        0,101,99,1,0,0,0,101,102,1,0,0,0,102,103,1,0,0,0,103,105,3,8,4,0,
        104,99,1,0,0,0,105,108,1,0,0,0,106,104,1,0,0,0,106,107,1,0,0,0,107,
        5,1,0,0,0,108,106,1,0,0,0,109,114,3,10,5,0,110,114,3,14,7,0,111,
        114,3,16,8,0,112,114,3,18,9,0,113,109,1,0,0,0,113,110,1,0,0,0,113,
        111,1,0,0,0,113,112,1,0,0,0,114,7,1,0,0,0,115,120,3,10,5,0,116,120,
        3,14,7,0,117,120,3,16,8,0,118,120,3,18,9,0,119,115,1,0,0,0,119,116,
        1,0,0,0,119,117,1,0,0,0,119,118,1,0,0,0,120,9,1,0,0,0,121,122,3,
        12,6,0,122,123,5,18,0,0,123,125,1,0,0,0,124,121,1,0,0,0,125,126,
        1,0,0,0,126,124,1,0,0,0,126,127,1,0,0,0,127,11,1,0,0,0,128,129,3,
        20,10,0,129,134,5,29,0,0,130,131,5,16,0,0,131,133,5,29,0,0,132,130,
        1,0,0,0,133,136,1,0,0,0,134,132,1,0,0,0,134,135,1,0,0,0,135,13,1,
        0,0,0,136,134,1,0,0,0,137,138,5,14,0,0,138,139,3,10,5,0,139,140,
        5,15,0,0,140,141,5,12,0,0,141,142,3,22,11,0,142,143,5,13,0,0,143,
        144,5,18,0,0,144,15,1,0,0,0,145,146,3,20,10,0,146,147,5,29,0,0,147,
        148,5,12,0,0,148,149,3,22,11,0,149,150,5,13,0,0,150,151,5,18,0,0,
        151,17,1,0,0,0,152,153,3,20,10,0,153,154,5,29,0,0,154,155,5,12,0,
        0,155,156,3,22,11,0,156,157,5,13,0,0,157,158,5,12,0,0,158,159,3,
        22,11,0,159,160,5,13,0,0,160,161,5,18,0,0,161,19,1,0,0,0,162,163,
        7,0,0,0,163,21,1,0,0,0,164,165,6,11,-1,0,165,166,3,24,12,0,166,172,
        1,0,0,0,167,168,10,1,0,0,168,169,7,1,0,0,169,171,3,24,12,0,170,167,
        1,0,0,0,171,174,1,0,0,0,172,170,1,0,0,0,172,173,1,0,0,0,173,23,1,
        0,0,0,174,172,1,0,0,0,175,176,6,12,-1,0,176,177,3,26,13,0,177,183,
        1,0,0,0,178,179,10,1,0,0,179,180,7,2,0,0,180,182,3,26,13,0,181,178,
        1,0,0,0,182,185,1,0,0,0,183,181,1,0,0,0,183,184,1,0,0,0,184,25,1,
        0,0,0,185,183,1,0,0,0,186,193,5,29,0,0,187,193,5,28,0,0,188,189,
        5,10,0,0,189,190,3,22,11,0,190,191,5,11,0,0,191,193,1,0,0,0,192,
        186,1,0,0,0,192,187,1,0,0,0,192,188,1,0,0,0,193,27,1,0,0,0,20,31,
        40,45,52,58,68,74,79,87,93,95,101,106,113,119,126,134,172,183,192
    ]

class IOParser ( Parser ):

    grammarFileName = "IOParser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'int'", "'long'", "'double'", "'char'", 
                     "'string'", "'+'", "'-'", "'*'", "'/'", "'('", "')'", 
                     "'['", "']'", "'{'", "'}'", "','", "':'", "';'", "'\\n'", 
                     "'repeat'", "'upto'", "'input'", "'output'" ]

    symbolicNames = [ "<INVALID>", "INT", "LONG", "DOUBLE", "CHAR", "STRING", 
                      "PLUS", "MINUS", "MULT", "DIV", "LPAREN", "RPAREN", 
                      "LBRACK", "RBRACK", "LBRACE", "RBRACE", "COMMA", "COLON", 
                      "SEMICOL", "NL", "REPEAT", "UPTO", "INPUT", "OUTPUT", 
                      "WS", "INLINE_COMMENT", "BLOCK_COMMENT", "STR", "NUM", 
                      "IDENT" ]

    RULE_fileSpec = 0
    RULE_inputFile = 1
    RULE_outputFile = 2
    RULE_inputLine = 3
    RULE_outputLine = 4
    RULE_values = 5
    RULE_homoValues = 6
    RULE_vectors = 7
    RULE_vector = 8
    RULE_matrix = 9
    RULE_varType = 10
    RULE_arithExpr = 11
    RULE_addend = 12
    RULE_term = 13

    ruleNames =  [ "fileSpec", "inputFile", "outputFile", "inputLine", "outputLine", 
                   "values", "homoValues", "vectors", "vector", "matrix", 
                   "varType", "arithExpr", "addend", "term" ]

    EOF = Token.EOF
    INT=1
    LONG=2
    DOUBLE=3
    CHAR=4
    STRING=5
    PLUS=6
    MINUS=7
    MULT=8
    DIV=9
    LPAREN=10
    RPAREN=11
    LBRACK=12
    RBRACK=13
    LBRACE=14
    RBRACE=15
    COMMA=16
    COLON=17
    SEMICOL=18
    NL=19
    REPEAT=20
    UPTO=21
    INPUT=22
    OUTPUT=23
    WS=24
    INLINE_COMMENT=25
    BLOCK_COMMENT=26
    STR=27
    NUM=28
    IDENT=29

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class FileSpecContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def inputFile(self):
            return self.getTypedRuleContext(IOParser.InputFileContext,0)


        def outputFile(self):
            return self.getTypedRuleContext(IOParser.OutputFileContext,0)


        def EOF(self):
            return self.getToken(IOParser.EOF, 0)

        def NL(self, i:int=None):
            if i is None:
                return self.getTokens(IOParser.NL)
            else:
                return self.getToken(IOParser.NL, i)

        def REPEAT(self):
            return self.getToken(IOParser.REPEAT, 0)

        def IDENT(self, i:int=None):
            if i is None:
                return self.getTokens(IOParser.IDENT)
            else:
                return self.getToken(IOParser.IDENT, i)

        def UPTO(self):
            return self.getToken(IOParser.UPTO, 0)

        def COLON(self):
            return self.getToken(IOParser.COLON, 0)

        def getRuleIndex(self):
            return IOParser.RULE_fileSpec

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFileSpec" ):
                return visitor.visitFileSpec(self)
            else:
                return visitor.visitChildren(self)




    def fileSpec(self):

        localctx = IOParser.FileSpecContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_fileSpec)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 31
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,0,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 28
                    self.match(IOParser.NL) 
                self.state = 33
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,0,self._ctx)

            self.state = 40
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==20:
                self.state = 34
                self.match(IOParser.REPEAT)
                self.state = 35
                self.match(IOParser.IDENT)
                self.state = 36
                self.match(IOParser.UPTO)
                self.state = 37
                self.match(IOParser.IDENT)
                self.state = 38
                self.match(IOParser.COLON)
                self.state = 39
                self.match(IOParser.NL)


            self.state = 45
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==19:
                self.state = 42
                self.match(IOParser.NL)
                self.state = 47
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 48
            self.inputFile()
            self.state = 50 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 49
                self.match(IOParser.NL)
                self.state = 52 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==19):
                    break

            self.state = 54
            self.outputFile()
            self.state = 58
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==19:
                self.state = 55
                self.match(IOParser.NL)
                self.state = 60
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 61
            self.match(IOParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class InputFileContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INPUT(self):
            return self.getToken(IOParser.INPUT, 0)

        def COLON(self):
            return self.getToken(IOParser.COLON, 0)

        def inputLine(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(IOParser.InputLineContext)
            else:
                return self.getTypedRuleContext(IOParser.InputLineContext,i)


        def NL(self, i:int=None):
            if i is None:
                return self.getTokens(IOParser.NL)
            else:
                return self.getToken(IOParser.NL, i)

        def getRuleIndex(self):
            return IOParser.RULE_inputFile

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInputFile" ):
                return visitor.visitInputFile(self)
            else:
                return visitor.visitChildren(self)




    def inputFile(self):

        localctx = IOParser.InputFileContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_inputFile)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 63
            self.match(IOParser.INPUT)
            self.state = 64
            self.match(IOParser.COLON)
            self.state = 66 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 65
                self.match(IOParser.NL)
                self.state = 68 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==19):
                    break

            self.state = 70
            self.inputLine()
            self.state = 79
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,7,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 72 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    while True:
                        self.state = 71
                        self.match(IOParser.NL)
                        self.state = 74 
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if not (_la==19):
                            break

                    self.state = 76
                    self.inputLine() 
                self.state = 81
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,7,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class OutputFileContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def OUTPUT(self):
            return self.getToken(IOParser.OUTPUT, 0)

        def COLON(self):
            return self.getToken(IOParser.COLON, 0)

        def outputLine(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(IOParser.OutputLineContext)
            else:
                return self.getTypedRuleContext(IOParser.OutputLineContext,i)


        def NL(self, i:int=None):
            if i is None:
                return self.getTokens(IOParser.NL)
            else:
                return self.getToken(IOParser.NL, i)

        def STR(self):
            return self.getToken(IOParser.STR, 0)

        def getRuleIndex(self):
            return IOParser.RULE_outputFile

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOutputFile" ):
                return visitor.visitOutputFile(self)
            else:
                return visitor.visitChildren(self)




    def outputFile(self):

        localctx = IOParser.OutputFileContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_outputFile)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 82
            self.match(IOParser.OUTPUT)
            self.state = 83
            self.match(IOParser.COLON)
            self.state = 85 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 84
                self.match(IOParser.NL)
                self.state = 87 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==19):
                    break

            self.state = 95
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==27:
                self.state = 89
                self.match(IOParser.STR)
                self.state = 91 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 90
                    self.match(IOParser.NL)
                    self.state = 93 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==19):
                        break



            self.state = 97
            self.outputLine()
            self.state = 106
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,12,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 99 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    while True:
                        self.state = 98
                        self.match(IOParser.NL)
                        self.state = 101 
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if not (_la==19):
                            break

                    self.state = 103
                    self.outputLine() 
                self.state = 108
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,12,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class InputLineContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def values(self):
            return self.getTypedRuleContext(IOParser.ValuesContext,0)


        def vectors(self):
            return self.getTypedRuleContext(IOParser.VectorsContext,0)


        def vector(self):
            return self.getTypedRuleContext(IOParser.VectorContext,0)


        def matrix(self):
            return self.getTypedRuleContext(IOParser.MatrixContext,0)


        def getRuleIndex(self):
            return IOParser.RULE_inputLine

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInputLine" ):
                return visitor.visitInputLine(self)
            else:
                return visitor.visitChildren(self)




    def inputLine(self):

        localctx = IOParser.InputLineContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_inputLine)
        try:
            self.state = 113
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,13,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 109
                self.values()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 110
                self.vectors()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 111
                self.vector()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 112
                self.matrix()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class OutputLineContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def values(self):
            return self.getTypedRuleContext(IOParser.ValuesContext,0)


        def vectors(self):
            return self.getTypedRuleContext(IOParser.VectorsContext,0)


        def vector(self):
            return self.getTypedRuleContext(IOParser.VectorContext,0)


        def matrix(self):
            return self.getTypedRuleContext(IOParser.MatrixContext,0)


        def getRuleIndex(self):
            return IOParser.RULE_outputLine

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOutputLine" ):
                return visitor.visitOutputLine(self)
            else:
                return visitor.visitChildren(self)




    def outputLine(self):

        localctx = IOParser.OutputLineContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_outputLine)
        try:
            self.state = 119
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,14,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 115
                self.values()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 116
                self.vectors()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 117
                self.vector()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 118
                self.matrix()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ValuesContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def homoValues(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(IOParser.HomoValuesContext)
            else:
                return self.getTypedRuleContext(IOParser.HomoValuesContext,i)


        def SEMICOL(self, i:int=None):
            if i is None:
                return self.getTokens(IOParser.SEMICOL)
            else:
                return self.getToken(IOParser.SEMICOL, i)

        def getRuleIndex(self):
            return IOParser.RULE_values

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitValues" ):
                return visitor.visitValues(self)
            else:
                return visitor.visitChildren(self)




    def values(self):

        localctx = IOParser.ValuesContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_values)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 124 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 121
                self.homoValues()
                self.state = 122
                self.match(IOParser.SEMICOL)
                self.state = 126 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 62) != 0)):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class HomoValuesContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def varType(self):
            return self.getTypedRuleContext(IOParser.VarTypeContext,0)


        def IDENT(self, i:int=None):
            if i is None:
                return self.getTokens(IOParser.IDENT)
            else:
                return self.getToken(IOParser.IDENT, i)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(IOParser.COMMA)
            else:
                return self.getToken(IOParser.COMMA, i)

        def getRuleIndex(self):
            return IOParser.RULE_homoValues

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitHomoValues" ):
                return visitor.visitHomoValues(self)
            else:
                return visitor.visitChildren(self)




    def homoValues(self):

        localctx = IOParser.HomoValuesContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_homoValues)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 128
            self.varType()
            self.state = 129
            self.match(IOParser.IDENT)
            self.state = 134
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==16:
                self.state = 130
                self.match(IOParser.COMMA)
                self.state = 131
                self.match(IOParser.IDENT)
                self.state = 136
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class VectorsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LBRACE(self):
            return self.getToken(IOParser.LBRACE, 0)

        def values(self):
            return self.getTypedRuleContext(IOParser.ValuesContext,0)


        def RBRACE(self):
            return self.getToken(IOParser.RBRACE, 0)

        def LBRACK(self):
            return self.getToken(IOParser.LBRACK, 0)

        def arithExpr(self):
            return self.getTypedRuleContext(IOParser.ArithExprContext,0)


        def RBRACK(self):
            return self.getToken(IOParser.RBRACK, 0)

        def SEMICOL(self):
            return self.getToken(IOParser.SEMICOL, 0)

        def getRuleIndex(self):
            return IOParser.RULE_vectors

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVectors" ):
                return visitor.visitVectors(self)
            else:
                return visitor.visitChildren(self)




    def vectors(self):

        localctx = IOParser.VectorsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_vectors)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 137
            self.match(IOParser.LBRACE)
            self.state = 138
            self.values()
            self.state = 139
            self.match(IOParser.RBRACE)
            self.state = 140
            self.match(IOParser.LBRACK)
            self.state = 141
            self.arithExpr(0)
            self.state = 142
            self.match(IOParser.RBRACK)
            self.state = 143
            self.match(IOParser.SEMICOL)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class VectorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def varType(self):
            return self.getTypedRuleContext(IOParser.VarTypeContext,0)


        def IDENT(self):
            return self.getToken(IOParser.IDENT, 0)

        def LBRACK(self):
            return self.getToken(IOParser.LBRACK, 0)

        def arithExpr(self):
            return self.getTypedRuleContext(IOParser.ArithExprContext,0)


        def RBRACK(self):
            return self.getToken(IOParser.RBRACK, 0)

        def SEMICOL(self):
            return self.getToken(IOParser.SEMICOL, 0)

        def getRuleIndex(self):
            return IOParser.RULE_vector

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVector" ):
                return visitor.visitVector(self)
            else:
                return visitor.visitChildren(self)




    def vector(self):

        localctx = IOParser.VectorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_vector)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 145
            self.varType()
            self.state = 146
            self.match(IOParser.IDENT)
            self.state = 147
            self.match(IOParser.LBRACK)
            self.state = 148
            self.arithExpr(0)
            self.state = 149
            self.match(IOParser.RBRACK)
            self.state = 150
            self.match(IOParser.SEMICOL)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MatrixContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def varType(self):
            return self.getTypedRuleContext(IOParser.VarTypeContext,0)


        def IDENT(self):
            return self.getToken(IOParser.IDENT, 0)

        def LBRACK(self, i:int=None):
            if i is None:
                return self.getTokens(IOParser.LBRACK)
            else:
                return self.getToken(IOParser.LBRACK, i)

        def arithExpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(IOParser.ArithExprContext)
            else:
                return self.getTypedRuleContext(IOParser.ArithExprContext,i)


        def RBRACK(self, i:int=None):
            if i is None:
                return self.getTokens(IOParser.RBRACK)
            else:
                return self.getToken(IOParser.RBRACK, i)

        def SEMICOL(self):
            return self.getToken(IOParser.SEMICOL, 0)

        def getRuleIndex(self):
            return IOParser.RULE_matrix

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMatrix" ):
                return visitor.visitMatrix(self)
            else:
                return visitor.visitChildren(self)




    def matrix(self):

        localctx = IOParser.MatrixContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_matrix)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 152
            self.varType()
            self.state = 153
            self.match(IOParser.IDENT)
            self.state = 154
            self.match(IOParser.LBRACK)
            self.state = 155
            self.arithExpr(0)
            self.state = 156
            self.match(IOParser.RBRACK)
            self.state = 157
            self.match(IOParser.LBRACK)
            self.state = 158
            self.arithExpr(0)
            self.state = 159
            self.match(IOParser.RBRACK)
            self.state = 160
            self.match(IOParser.SEMICOL)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class VarTypeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INT(self):
            return self.getToken(IOParser.INT, 0)

        def LONG(self):
            return self.getToken(IOParser.LONG, 0)

        def DOUBLE(self):
            return self.getToken(IOParser.DOUBLE, 0)

        def CHAR(self):
            return self.getToken(IOParser.CHAR, 0)

        def STRING(self):
            return self.getToken(IOParser.STRING, 0)

        def getRuleIndex(self):
            return IOParser.RULE_varType

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVarType" ):
                return visitor.visitVarType(self)
            else:
                return visitor.visitChildren(self)




    def varType(self):

        localctx = IOParser.VarTypeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_varType)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 162
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 62) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArithExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def addend(self):
            return self.getTypedRuleContext(IOParser.AddendContext,0)


        def arithExpr(self):
            return self.getTypedRuleContext(IOParser.ArithExprContext,0)


        def PLUS(self):
            return self.getToken(IOParser.PLUS, 0)

        def MINUS(self):
            return self.getToken(IOParser.MINUS, 0)

        def getRuleIndex(self):
            return IOParser.RULE_arithExpr

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArithExpr" ):
                return visitor.visitArithExpr(self)
            else:
                return visitor.visitChildren(self)



    def arithExpr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = IOParser.ArithExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 22
        self.enterRecursionRule(localctx, 22, self.RULE_arithExpr, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 165
            self.addend(0)
            self._ctx.stop = self._input.LT(-1)
            self.state = 172
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,17,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = IOParser.ArithExprContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_arithExpr)
                    self.state = 167
                    if not self.precpred(self._ctx, 1):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                    self.state = 168
                    _la = self._input.LA(1)
                    if not(_la==6 or _la==7):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 169
                    self.addend(0) 
                self.state = 174
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,17,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class AddendContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def term(self):
            return self.getTypedRuleContext(IOParser.TermContext,0)


        def addend(self):
            return self.getTypedRuleContext(IOParser.AddendContext,0)


        def MULT(self):
            return self.getToken(IOParser.MULT, 0)

        def DIV(self):
            return self.getToken(IOParser.DIV, 0)

        def getRuleIndex(self):
            return IOParser.RULE_addend

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAddend" ):
                return visitor.visitAddend(self)
            else:
                return visitor.visitChildren(self)



    def addend(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = IOParser.AddendContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 24
        self.enterRecursionRule(localctx, 24, self.RULE_addend, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 176
            self.term()
            self._ctx.stop = self._input.LT(-1)
            self.state = 183
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,18,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = IOParser.AddendContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_addend)
                    self.state = 178
                    if not self.precpred(self._ctx, 1):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                    self.state = 179
                    _la = self._input.LA(1)
                    if not(_la==8 or _la==9):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 180
                    self.term() 
                self.state = 185
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,18,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class TermContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENT(self):
            return self.getToken(IOParser.IDENT, 0)

        def NUM(self):
            return self.getToken(IOParser.NUM, 0)

        def LPAREN(self):
            return self.getToken(IOParser.LPAREN, 0)

        def arithExpr(self):
            return self.getTypedRuleContext(IOParser.ArithExprContext,0)


        def RPAREN(self):
            return self.getToken(IOParser.RPAREN, 0)

        def getRuleIndex(self):
            return IOParser.RULE_term

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTerm" ):
                return visitor.visitTerm(self)
            else:
                return visitor.visitChildren(self)




    def term(self):

        localctx = IOParser.TermContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_term)
        try:
            self.state = 192
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [29]:
                self.enterOuterAlt(localctx, 1)
                self.state = 186
                self.match(IOParser.IDENT)
                pass
            elif token in [28]:
                self.enterOuterAlt(localctx, 2)
                self.state = 187
                self.match(IOParser.NUM)
                pass
            elif token in [10]:
                self.enterOuterAlt(localctx, 3)
                self.state = 188
                self.match(IOParser.LPAREN)
                self.state = 189
                self.arithExpr(0)
                self.state = 190
                self.match(IOParser.RPAREN)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[11] = self.arithExpr_sempred
        self._predicates[12] = self.addend_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def arithExpr_sempred(self, localctx:ArithExprContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 1)
         

    def addend_sempred(self, localctx:AddendContext, predIndex:int):
            if predIndex == 1:
                return self.precpred(self._ctx, 1)
         





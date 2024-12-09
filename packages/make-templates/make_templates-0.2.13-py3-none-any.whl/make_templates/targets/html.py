import sys
sys.path.append('..')
from ..tree import *

template = """<!-- %s. -->

<!DOCTYPE html>
<html lang="it" data-theme="dark" class="loading">

<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=400, initial-scale=1">
  <link rel="stylesheet" href="https://olinfo.it/territoriali/template/main.css">
  <link rel="icon" href="https://olinfo.it/favicon.ico">
  <title>%s</title>

  <!--  1. Modifica la funzione solve                          -->
  <!--  2. Apri la pagina in un browser                        -->
  <!--  3. Incolla l'input nel form oppure caricalo da un file -->
  <!--  4. Genera l'output e scaricalo in un file              -->
  <!--  5. Carica questo file e l'output sulla piattaforma     -->

  <script id="solution">

    function solve(%s) {
%s
        // %s

        return %s;
    }

  </script>

  <script id="template">

    function* main(input) {
%s    }

  </script>
</head>

<body>
  <div class="container mt-3 mb-4">
    <div class="row">
      <div class="col mt-2">
        <div class="container">
          <div class="row mb-1 justify-content-between">
            <div class="col-auto">
              <p class="h2">
                <i class="fa fa-file-code fs-3 pe-2"></i>Codice
              </p>
            </div>
            <div class="col-auto order-md-last text-md-end pe-0">
              <button class="btn shadow-none pe-0" id="btn-theme">
                <i class="fa fa-sun fs-4 text-warning d-dark-none"></i>
                <i class="fa fa-moon fs-4 text-light d-light-none"></i>
              </button>
            </div>
            <div class="col-md-auto text-md-end">
              <p class="lead mb-0 lh-lg">Modifica questo file e ricarica la pagina!</p>
            </div>
          </div>
          <div class="row">
            <pre class="border rounded pt-2 pb-2 mb-0"><code id="txt-code"></code></pre>
          </div>
        </div>
      </div>
    </div>
    <div class="row mt-2">
      <div class="col-lg-6 mt-2">
        <div class="container">
          <div class="row justify-content-between mb-1">
            <div class="col-auto">
              <label class="h2" for="txt-input">
                <i class="fa fa-file-upload fs-3 pe-2"></i>Input
              </label>
            </div>
            <div class="col-auto p-0" role="group">
              <form class="container btn-group p-0">
                <label class="btn btn-outline-primary shadow-none">
                  <input class="d-none" type="reset" id="btn-reset">
                  <i class="fa fa-trash pe-2"></i>Cancella
                </label>
                <label class="btn btn-outline-primary shadow-none">
                  <input class="d-none" type="file" id="btn-open">
                  <i class="fa fa-upload pe-2"></i>Scegli file
                </label>
              </form>
            </div>
          </div>
          <div class="row">
            <textarea class="form-control border" rows="9" id="txt-input"
              placeholder="Incolla oppure trascina l'input qui"></textarea>
          </div>
        </div>
      </div>
      <div class="col-lg-6 mt-2">
        <div class="container">
          <div class="row justify-content-between mb-1">
            <div class="col-auto">
              <label class="h2" for="txt-output">
                <i class="fa fa-file-download fs-3 pe-2"></i>Output
              </label>
            </div>
            <div class="col-auto p-0" role="group">
              <div class="container btn-group p-0">
                <button class="btn btn-outline-primary shadow-none" title="Copiato!"
                  data-bs-trigger="manual" id="btn-copy">
                  <i class="fa fa-copy pe-1"></i>Copia
                </button>
                <button class="btn btn-outline-primary shadow-none" id="btn-download">
                  <i class="fa fa-download pe-1"></i>Scarica
                </button>
              </div>
            </div>
          </div>
          <div class="row">
            <textarea class="form-control border" rows="9" id="txt-output"
              placeholder="Premi “Esegui” per ottenere l'output" readonly></textarea>
          </div>
        </div>
      </div>
    </div>
    <div class="row justify-content-center mt-2">
      <div class="col-auto mt-2">
        <button class="btn btn-primary shadow-none" id="btn-exec">
          <i class="fa fa-running pe-1"></i>Esegui
        </button>
        <button class="btn btn-primary shadow-none" id="btn-kill">
          <i class="fa fa-skull pe-1"></i>Termina
        </button>
      </div>
    </div>
  </div>
  <script src="https://olinfo.it/territoriali/template/main.js"></script>
</body>
</html>
"""

locale = {
    'en' : ["NOTE: it is recommended to use this even if you don't understand the following code", "INSERT YOUR CODE HERE"],
    'it' : ["NOTA: si raccomanda di usare questo template anche se non lo si capisce completamente", "INSERISCI IL TUO CODICE QUI"]
}

type_vals = {
    'int'    : '0',
    'long'   : '0',
    'double' : '0.0',
    'char'   : "'-'",
    'string' : "''"
}

type_read = {
    'int'    : 'Int',
    'long'   : 'Int',
    'double' : 'Float',
    'char'   : 'String',
    'string' : 'String'
}

pending_declarations = {}

input_vars = []
output_vars = []

def get_output_vars():
    return output_vars[0] if len(output_vars) == 1 else "[%s]" % (', '.join(output_vars))

def build_type(t:VarType):
    vals = [x.value for x in t.dims]
    if len(vals) == 0:
        init = " = " + type_vals[t.base]
    elif len(vals) == 1:
        init = " = Array(%s)" % vals[0]
    else:
        assert(len(vals) == 2)
        init = " = Array.from(Array(%s), () => Array(%s))" % tuple(vals)
    return init

def build_reference(r):
    if isinstance(r, str):
        return r
    assert isinstance(r, VarReference)
    return r.name + ''.join('[%s]' % i for i in r.idx)

def build_declaration(d:VarDeclaration):
    init = build_type(d.type)
    return 'var ' + ', '.join(n + init for n in d.name) + ';\n'

def build_for(v:str, k:int, b:str, c:str):
    return ("for (var %s = %d; %s %s %s; ++%s)" + (" {\n%s}\n" if c.count('\n') > 1 else "\n%s")) % (v, k, v, "<" if k == 0 else "<=", b, v, c)

def build_inout(out:bool, types:List[str], refs:List[VarReference], end:bool):
    if len(refs) == 0 and not (out and end):
        return ""
    if out:
        s = " ".join(("${%s}" % build_reference(r)) for r in refs)
        if end is not None:
            s += ('\\r\\n' if end else ' ')
        return "yield `%s`;\n" % s
    s = ""
    for i in range(len(types)):
        t = types[i]
        r = refs[i]
        s += pending_declarations[r.name] + build_reference(r) + " = input.next" + type_read[t] + "();\n"
    return s

def build_block(prog:Block, lang:str):
    global input_vars, output_vars
    s = ""
    t = ""
    u = ""
    testref = ""
    outsec = False
    for i in range(len(prog.code)):
        c = prog.code[i]
        if isinstance(c, VarDeclaration):
            j = i+1
            while isinstance(prog.code[j], VarDeclaration):
                j = j+1
            is_input = isinstance(prog.code[j], InOutLine) or isinstance(prog.code[j], InOutSequence) or isinstance(prog.code[j], Repeat)
            if is_input:
                input_vars += c.name
            else:
                output_vars += c.name
            if len(c.type.dims) > 0 or not isinstance(prog.code[j], InOutLine):
                if is_input:
                    s += build_declaration(c)
                else:
                    t += build_declaration(c)
                for n in c.name:
                    pending_declarations[n] = ""
            else:
                for n in c.name:
                    pending_declarations[n] = "var "
        elif isinstance(c, Repeat):
            ss, tt = build_block(c.code, lang)
            temp = build_for(c.idx, c.start,  c.bound, indent(ss))
            if outsec:
                u += temp
            else:
                s += temp
            t += tt
        elif isinstance(c, InOutSequence):
            temp = build_for('i', 0, c.type.dims[-1].value, indent(build_inout(c.out, [c.type.base], [c.var.addIndex('i')], False)))
            temp += build_inout(c.out, [], [], True)
            if outsec and c.out:
                u += temp
            else:
                s += temp
        elif isinstance(c, InOutLine):
            temp = build_inout(c.out, c.types, c.items, True)
            if outsec and c.out:
                u += temp
            else:
                s += temp
        elif isinstance(c, FormatLine):
            testref = "Case #${%s} " % c.var
            u += "yield `%s`;\n" % c.format[1:-1].replace('{}', '${%s}' % c.var)
        elif isinstance(c, UserCode):
            outsec = True
            u += "var " + get_output_vars() + " = solve(%s);\n" % (', '.join(input_vars))
        elif isinstance(c, Instruction):
            if len(s) < 2 or s[-2] != '\n':
                s += '\n'
        else:
            raise Exception('Unrecognised instruction "%s"' % c)
    if len(u):
        s += "try {\n"
        s += indent(u)
        s += "} catch (e) {\n"
        s += "    yield `%sfailed with error: ${e}\\r\\n`;\n" % testref
        s += "}\n"
    return s, t

def generate(name:str, prog:Block, lang:str, bounds:dict):
    code, outcode = build_block(prog, lang)
    return template % (locale[lang][0], name, ', '.join(input_vars), indent(indent(outcode)), locale[lang][1], get_output_vars(), indent(indent(code)))

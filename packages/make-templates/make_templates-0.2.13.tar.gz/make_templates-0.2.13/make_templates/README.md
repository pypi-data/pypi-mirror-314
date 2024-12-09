# make-templates 0.2.013

This is a simple python-based tool generating solution templates (containing code for reading input and writing output), for tasks in either the yaml format for CMS or in the Terry format.

### Targets

The tool allows to generate from the input/output description:

- `md`: description of the input/output format as Markdown code (especially designed for Terry)
- `tex`: description of the input/output format as Latex code (especially designed for CMS)
- solution templates in languages: `c`, `cpp`, `cs`, `go`, `html` (form based on Javascript), `java`, `pas`, `py` (Python3), `vb`

Template code can be useful for writing solutions and validators, but that adaptation is left to end users.

### Usage

The tool can be used as follows, from the root directory of a task:

```
make-templates [-h] [-l LANG] [-d DESCRIPTION] [--limits LIMITS] [-t] [-c] [-n] [targets ...]
```

**Positional arguments:**

- `targets`: Language targets that should be considered (if none specified, the default is c/cpp/cs/java/pas/py/tex for CMS and c/cpp/cs/go/html/java/md/pas/py/vb for Terry)

**Options:**

- `-h`, `--help`: Show the help message and exit.
- `-l LANG`, `--lang LANG`: Language to be used for generating the files (either *it* or *en*, defaults to *it* for Terry and *en* for CMS).
- `-d DESCRIPTION`, `--description DESCRIPTION`: Path of the file containing the I/O description in SLIDe (defaults to `inout.slide`).
- `--limits LIMITS`: Path of the file containing task limits (defaults to `gen/limiti.py` for CMS and `managers/limits.py` for Terry).
- `-t`, `--terry`: Forces the tool to interpret the task as being in the Terry format.
- `-c`, `--cms`: Forces the tool to interpret the task as being in the yaml format for CMS.
- `-n`, `--no-replace`: Prevents the tool from replacing already-generated files (including task statements).

### SLIDe: Simple Language for Input Description

SLIDe is a simple language for describing most common input and output files for competitive programming tasks. It is designed to be convenient for most tasks, and not general enough to cover all tasks. In particular, it is not suited for interactive or grader-based tasks. The language allows to write an `inout.slide` file like the following simple example:

```
input:

int N;
double V[N];

output:

int W[N];
```

The output description has the same syntax as for the input description.

A more complex (and valid) example is:

```
/*
 * Optional notation if T cases indexed by
 * test are present in a single input/output
 * (numbering is 1-based)
 */
repeat test upto T:

// the description of a single test follows

input:

char problem_type; // a single value in a line
int N, M; long K; // three values in another line 
double W[N]; // N values in a single line
/*
 * Notation for M lines, each with 2 integers and a string
 */
{int efrom, eto; string elabel;}[M];

// you can leave empty rows with no effect

int matrix[N][M]; // N lines with M integers each

output:

"Case #{}: " // something to prepend to each test
{int L; string S; long key, value; char letter; double x;}[N];
```

### Further details

The grammar is based on [ANTLR4](https://github.com/antlr/antlr4), compiled into a Python3 parser, validator and visitor. A VS code settings file is available in the repository, that should work after installing the ANTLR extension. The precise grammar can be read in files `grammar/IOLexer.g4` and `grammar/IOParser.g4` and is mostly self-explanatory. The validator checks the following constraints:

- variables names $i$ and $j$ are not used (those names are reserved for loop variables);
- when a variable is declared, there is no previous declaration with the same name (**ignoring case**);
- when a varilable is referenced (for a length expression), the variable is a **single uppercase letter** with a previous declaration;
- arithmetic operations between numeric constants are forbidden;
- subtraction and division by a non-constant term is forbidden;
- redundant parentheses around a primitive term are forbidden;
- the output header formatter is only allowed if a `repeat` clause is present.

### Development

While adding support for a new target language, you should:

- write the language generator in `make_templates/targets/<lang code>.py`
- import it in `make_templates/targets/__init__.py`
- add a test for the language in `tests/test.sh`, function `check_terry`
- add the long name for the target in dictionary `tnames` in `make_templates/main.py:72`
- update this README accordingly

Each time a new commit is pushed, a publish action towards [test-pypi](https://test.pypi.org) is triggered. **The action will fail unless the build number in `setup.py` is increased.**

Each time a new tag is pushed, a publish action towards [pypi](https://pypi.org) is triggered. **Remember to increase the minor (or major) version number to match the new tag pushed,** and reset the build number to zero.

Before pushing any new commit, make sure that the automated tests pass and that the version number is increased.
In order to ensure that build version numbers are increased at every pushed commit, we recommend to add the following pre-commit hook in `.git/hooks/pre-commit`:

```
build=`head -n 1 README.md | sed 's|^.*\.||'`
next=`printf "%03d" $[build+1]`
sed -i "" "s|$build$|$next|" README.md
git add README.md
```

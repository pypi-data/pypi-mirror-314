import argparse
import yaml
from os import path, symlink
from copy import deepcopy
from re import fullmatch, sub
from typing import List
from importlib import util
from importlib.resources import files

from antlr4 import InputStream, CommonTokenStream
from antlr4.error.ErrorListener import ErrorListener

from .parser.IOLexer import IOLexer
from .parser.IOParser import IOParser
from .analyzer import Analyzer
from . import targets


def find_version():
    with files('make_templates').joinpath('README.md').open() as f:
        return f.readline()[17:].strip()


# Error listener to make sure that parsing errors are not ignored.
class FailOnError(ErrorListener):
    def syntaxError(self, recognizer, offending, line, column, msg, e):
        assert False

languages = [x for x in dir(targets) if x[0] != '_']
cms_langs = 'c/cpp/cs/java/pas/py/tex'.split('/')
terry_langs = [x for x in languages if x != 'tex']

def replace_section(lines : List[str], target : str, body : str):
    pattern = "## [a-zA-Z/ ]+\n" if target == "md" else r"\\[a-zA-Z]+\n"
    bodylines = [line+'\n' for line in body.split('\n')]
    sections = [line for line in bodylines if fullmatch(pattern, line)]
    start = 0
    while start < len(lines):
        if lines[start] == sections[0]:
            break
        start += 1
    end = start+1
    for section in sections[1:]:
        while end < len(lines):
            if lines[end] == section:
                break
            elif fullmatch(pattern, lines[end]):
                print(f"[ERROR] Unexpected section '{lines[end].strip()}' in statement for target {target}")
                exit(1)
            end += 1
    if end == len(lines):
        print(f"[ERROR] Statement sections not found for target {target}")
        exit(1)
    end += 1
    while end < len(lines):
        if fullmatch(pattern, lines[end]):
            break
        end += 1
    return lines[:start] + bodylines + lines[end:]

def replace_start(lines : List[str], targets : List[str], lang : str, name : str):
    j = 0
    while lines[j][:1] != '#':
        j += 1
    while lines[j-1] == "\n":
        j -= 1
    i = j - 1
    while lines[i-1][:5] == "> - _":
        i -= 1
    v = []
    base = "Scarica la traccia" if lang == "it" else "Download the template"
    tnames = {
        "c"    : "C",
        "cpp"  : "C++",
        "cs"   : "C#",
        "go"   : "Go",
        "html" : "JavaScript",
        "java" : "Java",
        "pas"  : "Pascal",
        "py"   : "Python",
        "vb"   : "VisualBasic"
    }
    for target in targets:
        if target in tnames:
            file = f"{name}.{target}"
            tname = tnames[target]
            v.append(f"> - _{base} in {tname}: [{file}]({file})_\n")
    return lines[:i] + v + lines[j:]

def main(args):
    if args.version:
        print("make-templates " + find_version())
        exit(0)
    # load task yaml
    if not path.isfile(args.yaml):
        print("[ERROR] File %s not found" % args.yaml)
        exit(1)
    task_yaml = yaml.safe_load(''.join(open(args.yaml, 'r').readlines()))

    # load input/output description
    if not path.isfile(args.description):
        print(f"[ERROR] Description file {args.description} not found")
        exit(1)
    error_listener = FailOnError()
    input_stream = InputStream(''.join(open(args.description, 'r').readlines()))
    try:
        lexer = IOLexer(input_stream)
        lexer.addErrorListener(error_listener)
        token_stream = CommonTokenStream(lexer)
        parser = IOParser(token_stream)
        parser.addErrorListener(error_listener)
        analyzer = Analyzer()
        err, res = analyzer.visitFileSpec(parser.fileSpec())
    except Exception as e:
        print("[ERROR] Parsing failed, aborting")
        exit(1)
    for e in err:
        print("[ERROR]", e)
    if len(err) > 0:
        exit(1)

    # infer task format
    if args.terry and args.cms:
        print("[ERROR] Cannot specify both --terry and --cms")
        exit(1)
    if args.terry:
        format = "terry"
    elif args.cms:
        format = "cms"
    elif path.isdir('statement') and path.isdir('solutions') and 'description' in task_yaml:
        format = "terry"
    elif path.isdir('statement') and path.isdir('att') and path.isdir('sol') and 'title' in task_yaml:
        format = "cms"
    else:
        print("[ERROR] Cannot recognise task format")
        exit(1)

    # set generation language
    if args.lang is None:
        args.lang = "it" if format == "terry" else "en"
    if args.lang not in ['en', 'it']:
        print(f"[ERROR] Language '{args.lang}' not supported")
        exit(1)

    # set generation paths
    if format == "terry":
        att_folder = "statement"
        sol_folder = "solutions"
        txt_file = "statement/statement"
    if format == "cms":
        att_folder = "att"
        sol_folder = "sol"
        txt_file = "statement/" + ("english" if args.lang == "en" else "italian")

    # load limits file
    if args.limits is None:
        args.limits = "gen/constraints.py" if format == "cms" else "managers/limits.py"
    if not path.isfile(args.limits):
        print(f"[ERROR] File {args.limits} not found")
        exit(1)
    spec = util.spec_from_file_location('limits', args.limits)
    limits = util.module_from_spec(spec)
    spec.loader.exec_module(limits)

    # process targets
    if len(args.targets) == 0:
        args.targets = terry_langs if format == "terry" else cms_langs
    for t in args.targets:
        if t not in dir(targets):
            print(f"[ERROR] Target '{t}' not supported")
            exit(1)
        if 'name' in task_yaml:
            name = task_yaml['name']
        else:
            name = path.basename(path.dirname(path.abspath(args.yaml)))
        body = getattr(targets, t).generate(name, deepcopy(res), args.lang, limits.__dict__)
        body = sub('\n +\n', '\n\n', body)
        body = sub('\n +\n', '\n\n', body)
        if t in ['md', 'tex']:
            file = txt_file + '.' + t
            if not path.isfile(file):
                print(f"[ERROR] File {file} not found")
                exit(1)
            elif args.no_replace:
                print(f"[WARNING] Skipping target {t}: {file} exists")
                continue
            lines = replace_section(open(file, 'r').readlines(), t, body)
            if t == "md":
                lines = replace_start(lines, args.targets, args.lang, name)
            with open(file, 'w') as f:
                f.writelines(lines)
        else:
            file = path.join(att_folder, name + '.' + t)
            link = path.join(sol_folder, 'template_' + t + '.' + t)
            if args.no_replace and path.isfile(file):
                print(f"[WARNING] Skipping target {t}: {file} exists")
                continue
            with open(file, 'w') as f:
                f.writelines(body)
            if not path.isfile(link):
                symlink("../" + file, link)


def script():
    parser = argparse.ArgumentParser(
        description="make-templates " + find_version(),
        epilog="This script should be run in the root directory of a task.",
    )
    parser.add_argument(
        "-v", "--version",
        action="store_true",
        help="prints the version number and exits",
    )
    parser.add_argument(
        "targets",
        nargs="*",
        help=f"language targets that should be considered (if none specified, the default is {'/'.join(cms_langs)} for CMS and {'/'.join(terry_langs)} for Terry)"
    )
    parser.add_argument(
        "-l", "--lang",
        help="language to be used for generating the files (either 'it' or 'en', defaults to 'it' for Terry and 'en' for CMS)",
    )
    parser.add_argument(
        "-d", "--description",
        default="inout.slide",
        help="path of the file containing the I/O description in SLIDe (defaults to 'inout.slide')",
    )
    parser.add_argument(
        "-y", "--yaml",
        default="task.yaml.orig",
        help="path of the file containing the task description in YAML (defaults to 'task.yaml.orig')",
    )
    parser.add_argument(
        "--limits",
        help="path of the file containing task limits (defaults to 'gen/constraints.py' for CMS and 'managers/limits.py' for Terry)",
    )
    parser.add_argument(
        "-t", "--terry",
        action="store_true",
        help="forces the tool to interpret the task as being in the Terry format",
    )
    parser.add_argument(
        "-c", "--cms",
        action="store_true",
        help="forces the tool to interpret the task as being in the yaml format for CMS",
    )
    parser.add_argument(
        "-n", "--no-replace",
        action="store_true",
        help="prevents the tool from replacing already-generated files (including task statements)",
    )
    main(parser.parse_args())


if __name__ == "__main__":
    script()

import os
import re
import inspect


def _get_parser_list(directory_name):
    files = [f.replace(".py", "") for f in os.listdir(directory_name)
             if not f.startswith("__")]
    return files


def _import_parsers(parser_files):
    m = re.compile('.+parser$', re.I)
    _modules = __import__("weatherterm.parsers", globals(), locals(), parser_files, 0)
    _parsers = [(k, v) for k, v in inspect.getmembers(_modules)
                if inspect.ismodule(v) and m.match(k)]
    _classes = dict()
    for k, v in _parsers:
        _classes.update({k: v for k, v in inspect.getmembers(v) if inspect.isclass(v) and m.match(k)})
    return _classes


def load(directory_name):
    parser_files = _get_parser_list(directory_name)
    return _import_parsers(parser_files)

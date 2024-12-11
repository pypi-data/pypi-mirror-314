import os
try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backport to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources

from ..assets import css
from ..assets import js


class StaticFilesManager(object):
    def __init__(self):
        pass

    @staticmethod
    def js(file):
        code = ''
        try:
            code = pkg_resources.read_text(js, f'{file}.js')
        except Exception as e:
            print(e)
        return code

    @staticmethod
    def css():
        styles = ''
        try:
            styles = pkg_resources.read_text(css, 'style.css')
        except Exception as e:
            print(e)
        return styles
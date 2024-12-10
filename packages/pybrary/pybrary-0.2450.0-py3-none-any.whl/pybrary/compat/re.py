from pybrary.compat import version


if version >= '3.13':
    from re import PatternError
else:
    from re import error as PatternError


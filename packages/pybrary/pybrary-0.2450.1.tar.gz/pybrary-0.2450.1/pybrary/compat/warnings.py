from pybrary.compat import version


if version >= '3.13':
    from warnings import deprecated
else:
    from pybrary.compat.backport_warnings import deprecated

# SPDX-License-Identifier: GPL-3.0-or-later
# These exceptions are caught by cmdline.py,
# which selects an exit status accordingly.


class GenericError(Exception):
    """errors running LaTeX, finding essential files, etc."""


class SyntaxError(Exception):
    """signal invalid Rubber command-line"""

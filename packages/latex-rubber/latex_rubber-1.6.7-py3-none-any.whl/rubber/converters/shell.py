# SPDX-License-Identifier: GPL-3.0-or-later
# (c) Emmanuel Beffara, 2005
"""
Generic shell conversion rule.

The action of this rule is defined by variables specified in the rule file:
- "command" is the command line, it is split the same way as directives,
   other variables are substituted,
- "source" is the input file name,
- "target" is the output file name.
"""

from rubber.util import parse_line, prog_available
from rubber.depend import Shell


def check(source, target, context):
    line = parse_line(context['command'], context)
    return prog_available(line[0])


def convert(source, target, context, env):
    result = Shell(parse_line(context['command'], context))
    result.add_product(target)
    result.add_source(source)
    return result

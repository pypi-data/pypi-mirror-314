# SPDX-License-Identifier: GPL-3.0-or-later
"""
This module contains code for file conversion, including implicit conversion
rule management.
"""

import re, os.path
import importlib
from configparser import ConfigParser, ParsingError, NoOptionError
import logging

msg = logging.getLogger(__name__)
from rubber.util import _
import rubber.converters

re_variable = re.compile('[a-zA-Z]+')


def expand_cases(string, vars):
    """
    Expand variables and cases in a template string. Variables must occur as
    $VAR (with only letters in the name) or ${VAR}, their values are taken
    from the dictionary-like object 'vars'. The "$" character can be written
    litterally by saying "$$". Cases are written in braces, separated with
    commas, as in {foo,bar,quux}. Commas at top-level also count as choice
    separators, as if there was a pair of braces around the whole string.
    Returns a pair (cases,pos) where 'cases' is the list of expansions of the
    string and 'pos' is the position of the first unbalanced "}" or the end of
    the string.
    """
    pos = 0  # current position
    start = 0  # starting point of the current chunk
    cases = []  # possible expansions from previous cases
    current = ['']  # possible values for the current case, up to 'start'

    while pos < len(string):

        # Cases

        if string[pos] == ',':
            suffix = string[start:pos]
            cases.extend([s + suffix for s in current])
            current = ['']
            start = pos = pos + 1

        elif string[pos] == '{':
            mid = string[start:pos]
            next, shift = expand_cases(string[pos + 1:], vars)
            current = [left + mid + right for left in current for right in next]
            start = pos = pos + shift + 2

        elif string[pos] == '}':
            suffix = string[start:pos]
            return cases + [s + suffix for s in current], pos

        # Variable expansion

        elif string[pos] == '$' and pos < len(string):
            if string[pos + 1] == '{':
                end = string.find('}', pos + 2)
                if end < 0:
                    end = len(string)
                name = string[pos + 2:end]
                suffix = string[start:pos]
                if name in vars:
                    suffix += vars[name]
                current = [s + suffix for s in current]
                start = pos = end + 1
            elif string[pos + 1] == '$':
                suffix = string[start:pos + 1]
                current = [s + suffix for s in current]
                start = pos = pos + 2
            else:
                m = re_variable.match(string, pos + 1)
                if m:
                    name = m.group()
                    suffix = string[start:pos]
                    if name in vars:
                        suffix += vars[name]
                    current = [s + suffix for s in current]
                    start = pos = m.end()
                else:
                    pos += 1

        else:
            pos += 1

    suffix = string[start:]
    return cases + [s + suffix for s in current], pos


class Converter(object):
    """
    This class represents a set of translation rules that may be used to
    produce input files. Objects contain a table of rewriting rules to deduce
    potential source names from the target's name, and each rule has a given
    cost that indicates how expensive the translation is.

    Each rule contains a module name. The module is searched for in the
    package rubber.converters and it is supposed to contain two functions:

    - check(source, target, context):
        Returns True if conversion from 'source' to 'target' is possible (i.e.
        the source file is suitable, all required tools are available, etc.).
        The 'context' object is a dictionary-like object that contains values
        from the rule and possibly additional user settings. If the function
        is absent, conversion is always assumed to be possible.

    - convert(source, target, context, env):
        Produce a dependency node to produce 'target' from
        'source', using settings from the environment 'env'.
    """

    def __init__(self, env):
        """
        Initialize the converter, associated with a given dependency set, with
        an empty set of rules.
        """
        self.env = env
        self.modules = {}
        self.rules = []

    def read_ini(self, filename):
        """
        Read a set of rules from a file. The file has the form of an INI file,
        each section describes a rule.
        """
        cp = ConfigParser()
        try:
            cp.read(filename)
        except ParsingError:
            msg.error(rubber.util._format({'file': filename}, _("parse error, ignoring it")))
            return
        for name in cp.sections():
            dict = {'name': name}
            for key in cp.options(name):
                dict[key] = cp.get(name, key)
            try:
                dict['cost'] = cp.getint(name, 'cost')
            except NoOptionError:
                msg.warning(rubber.util._format({'file': filename}, _("ignoring rule `%s' (no cost found)") % name))
                continue
            except ValueError:
                msg.warning(rubber.util._format({'file': filename}, _("ignoring rule `%s' (invalid cost)") % name))
                continue
            if 'target' not in dict:
                msg.warning(rubber.util._format({'file': filename}, _("ignoring rule `%s' (no target found)") % name))
                continue
            if 'rule' not in dict:
                msg.warning(rubber.util._format({'file': filename}, _("ignoring rule `%s' (no module found)") % name))
            if not self.load_module(dict['rule']):
                msg.warning(rubber.util._format({'file': filename}, _("ignoring rule `%s' (module `%s' not found)") % (name, dict['rule'])))
            dict["re_target"] = re.compile(dict['target'] + '$')
            self.rules.append(dict)

    def load_module(self, name):
        """
        Check if the module of the given name exists and load it. Returns True
        if the module was loaded and False otherwise.
        """
        if name in self.modules:
            return self.modules[name] is not None

        spec = importlib.machinery.PathFinder().find_spec(name, rubber.converters.__path__)
        if spec is None:
            self.modules[name] = None
            return False

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.modules[name] = module
        return True

    def may_produce(self, name):
        """
        Return true if the given filename may be that of a file generated by
        this converter, i.e. if it matches one of the target regular
        expressions.
        """
        for rule in self.rules:
            if rule["re_target"].match(name):
                return True
        return False

    def best_rule(self, target, check, context):
        """
        Search for an applicable rule for the given target with the least
        cost. The returned value is a dictionary that describes the best rule
        found, or None if no rule is applicable. The optional argument 'check'
        is a function that takes the rule parameters as arguments (as a
        dictionary that contains at least 'source' and 'target') and can
        return false if the rule is refused. The optional argument 'context'
        is expected to be a Variables instance attached to a Node.
        """
        candidates = []

        for rule in self.rules:
            match = rule["re_target"].match(target)
            if not match:
                continue
            templates, _ = expand_cases(rule['source'], {})
            for template in templates:
                source = match.expand(template)
                if source == target:
                    continue
                if not os.path.exists(source):
                    continue
                candidates.append((rule['cost'], source, target, rule))

        candidates.sort()
        for cost, source, target, rule in candidates:
            instance = context.copy()
            for k, v in rule.items():
                instance[k] = v
            # Replace in this instance generic patterns set from rule with actual paths.
            instance['source'] = source
            instance['target'] = target
            if check is not None and not check(instance):
                continue
            module = self.modules[rule['rule']]
            if hasattr(module, 'check'):
                if not module.check(source=source, target=target, context=instance):
                    continue
            return instance

        return None

    def apply(self, instance):
        """
        Apply a rule with the variables given in the dictionary passed as
        argument (as returned from the 'best_rule' method), and return a
        dependency node for the result.
        """
        module = self.modules[instance['rule']]
        return module.convert(source=instance['source'],
                              target=instance['target'],
                              context=instance,
                              env=self.env)

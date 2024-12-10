# SPDX-License-Identifier: GPL-3.0-or-later
# (c) Emmanuel Beffara, 2004--2006
# vim: noet:ts=4
"""
Multibib support for Rubber

This package allows several bibliographies in one document. Each occurence of
the \\newcites macro creates a new bibliography with its associated commands,
using a new aux file. This modules behaves like the default BibTeX module for
each of those files.

The directives are the same as those of the BibTeX module. They all accept an
optional argument first, enclosed in parentheses as in "multibib.path
(foo,bar) here/", to specify which bibliography they apply to. Without this
argument, they apply to all bibliographies.
"""

import re
from rubber.util import _
import logging

msg = logging.getLogger(__name__)
import rubber.biblio
import rubber.module_interface

re_optarg = re.compile(r'\((?P<list>[^()]*)\) *')


class Module(rubber.module_interface.Module):

    def __init__(self, document, opt):
        self.doc = document
        self.bibs = {}
        self.defaults = []
        self.commands = {}
        document.hook_macro('newcites', 'a', self.hook_newcites)

    def command(self, cmd, args):
        names = None

        # Check if there is the optional argument.

        if len(args) > 0:
            match = re_optarg.match(args[0])
            if match:
                names = match.group('list').split(',')
                args = args[1:]

        # If not, this command will also be executed for newly created indices
        # later on.

        if names is None:
            self.defaults.append([cmd, args])
            names = self.bibs.keys()

        # Then run the command for each index it concerns.

        for name in names:
            if name in self.bibs:
                super().command(cmd, args, _dep=self.bibs[name])
            elif name in self.commands:
                self.commands[name].append([cmd, args])
            else:
                self.commands[name] = [[cmd, args]]

    def hook_newcites(self, loc, name):
        self.doc.add_product(name + ".aux")
        bib = self.bibs[name] = rubber.biblio.BibTeXDep(self.doc, name)
        self.doc.hook_macro('bibliography' + name, 'a', bib.hook_bibliography)
        self.doc.hook_macro('bibliographystyle' + name, 'a', bib.hook_bibliographystyle)
        for cmd in self.defaults:
            super().command(*cmd, _dep=bib)
        if name in self.commands:
            for cmd in self.commands[name]:
                super().command(*cmd, _dep=bib)
        msg.debug(_("bibliography %s registered") % name)

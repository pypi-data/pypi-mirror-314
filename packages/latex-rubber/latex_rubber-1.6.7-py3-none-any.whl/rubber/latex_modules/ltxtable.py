# SPDX-License-Identifier: GPL-3.0-or-later
# (c) Sebastian Reichel, 2012
"""
Dependency analysis for package 'ltxtable' in Rubber.
"""

import rubber.module_interface


class Module(rubber.module_interface.Module):

    def __init__(self, document, opt):
        self.doc = document
        document.hook_macro('LTXtable', 'aa', self.hook_ltxtable)

    def hook_ltxtable(self, loc, width, file):
        # If the file name looks like it contains a control sequence or a macro
        # argument, forget about this \LTXtable.
        if file.find('\\') < 0 and file.find('#') < 0:
            self.doc.add_source(file)

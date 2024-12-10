# SPDX-License-Identifier: GPL-3.0-or-later
# (c) Emmanuel Beffara, 2002--2006

import rubber.index
import rubber.module_interface


class Module(rubber.module_interface.Module):

    def __init__(self, document, opt):
        self.dep = rubber.index.Index(document, 'idx', 'ind', 'ilg')

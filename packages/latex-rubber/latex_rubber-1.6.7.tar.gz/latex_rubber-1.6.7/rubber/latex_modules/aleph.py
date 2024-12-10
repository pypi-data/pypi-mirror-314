# SPDX-License-Identifier: GPL-3.0-or-later
import rubber.module_interface


class Module(rubber.module_interface.Module):

    def __init__(self, document, opt):

        document.program = 'lamed'
        document.engine = 'Aleph'

# SPDX-License-Identifier: GPL-3.0-or-later
import rubber.depend
import rubber.module_interface


class Module(rubber.module_interface.Module):

    def __init__(self, document, opt):
        job = document.basename()

        document.add_product(job + '.ist')

        dep = rubber.depend.Shell(('makeglossaries', job))
        dep.add_source(job + '.aux')

        if opt is None or 'nomain' not in opt:
            glo = job + '.glo'
            # FIXME: does probably fail with --inplace and friends.
            document.add_source(glo)

            dep.add_product(glo)
            dep.add_product(job + '.gls')
            dep.add_product(job + '.glg')

        if opt is not None and 'acronym' in opt:
            acn = job + '.acn'
            document.add_source(acn)

            dep.add_product(acn)
            dep.add_product(job + '.acr')
            dep.add_product(job + '.alg')

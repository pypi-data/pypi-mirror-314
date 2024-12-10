# SPDX-License-Identifier: GPL-3.0-or-later
# vim: noet:ts=4
# Sebastian Kapfer <sebastian.kapfer@fau.de> 2015.
# based on code by Sebastian Reichel and others.
"""
BibLaTeX support for Rubber
"""

import logging

msg = logging.getLogger(__name__)
from rubber.util import _
import rubber.util
import rubber.biblio
import re
import rubber.module_interface


class Module(rubber.module_interface.Module):

    def __init__(self, document, opt):
        doc = document

        options = rubber.util.parse_keyval(opt)
        backend = options.setdefault("backend", "biber")

        if backend not in ("biber", "bibtex", "bibtex8", "bibtexu"):
            # abort rather than guess
            raise rubber.GenericError(_("Garbled biblatex backend: backend=%s (aborting)") % backend)

        self.dep = BibLaTeXDep(doc, backend)
        doc.hook_macro("bibliography", "a", self.dep.add_bibliography)

        # overwrite the hook which would load the bibtex module
        doc.hook_macro("bibliographystyle", "a", self.dep.bibliographystyle)


# for parsing the Biber log file
re_updatefile = re.compile(".*INFO - Found BibTeX data source '(?P<filename>.*)'$")
re_error = re.compile(
    ".*Utils.pm:[0-9]+> (?P<kind>(WARN|ERROR)) .* line (?P<line>[0-9]+), (?P<text>.*)")
biber_to_rubber = {"ERROR": "error", "WARN": "warning"}


class BibLaTeXDep(rubber.biblio.BibToolDep):

    def __init__(self, doc, tool):
        super().__init__()
        self.doc = doc
        self.tool = tool
        self.blg = doc.basename(with_suffix=".blg")

        for suf in [".bbl", ".blg", ".run.xml"]:
            self.add_product(doc.basename(with_suffix=suf))

        if tool == "biber":
            for macro in ("addbibresource", "addglobalbib", "addsectionbib"):
                doc.hook_macro(macro, "oa", self.add_bib_resource)
            self.source = doc.basename(with_suffix=".bcf")
            doc.add_product(self.source)
        else:
            self.source = doc.basename(with_suffix=".aux")
            doc.add_product(doc.basename(with_suffix="-blx.bib"))

        self.add_source(self.source)
        doc.add_source(doc.basename(with_suffix=".bbl"))

    def build_command(self):
        return [self.tool, self.source]

    def add_bib_resource(self, doc, opt, name):
        msg.debug(_("bibliography resource discovered: %s") % name)
        options = rubber.util.parse_keyval(opt)

        # If the file name looks like it contains a control sequence
        # or a macro argument, forget about this resource.
        if name.find('\\') > 0 or name.find('#') > 0:
            return

        # skip Biber remote resources
        if "location" in options and options["location"] == "remote":
            return

        filename = self.find_bib(name)
        if filename is None:
            msg.error(_("cannot find bibliography resource %s") % name)
        else:
            self.add_source(filename)

    def add_bibliography(self, doc, names):
        for bib in names.split(","):
            self.add_bib_resource(doc, None, bib.strip())

    def bibliographystyle(self, loc, bibs):
        msg.warning(_("\\usepackage{biblatex} incompatible with \\bibliographystyle"))

    def get_errors(self):
        """
        Read the log file, identify error messages and report them.
        """
        if self.tool != "biber":
            # we re-use the BibTeX support in superclass
            for error in super(BibLaTeXDep, self).get_errors():
                yield error
            return

        current_bib = None

        try:
            log = open(self.blg, encoding='utf_8', errors='replace')
        except:
            msg.warning(_("cannot open Biber logfile: %s") % self.blg)
            return

        with log:
            for line in log:
                m = re_updatefile.match(line)
                if m:
                    current_bib = m.group("filename")
                m = re_error.match(line)
                if m:
                    d = {"pkg": "biber"}
                    d["kind"] = biber_to_rubber[m.group("kind")]
                    if current_bib:
                        d["file"] = current_bib
                    d["line"] = int(m.group("line"))
                    d["text"] = m.group("text")
                    yield d

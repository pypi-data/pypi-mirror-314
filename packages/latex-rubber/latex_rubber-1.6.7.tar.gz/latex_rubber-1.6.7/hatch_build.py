# SPDX-License-Identifier: GPL-3.0-or-later
# vim: et:ts=4
#
# This is the Hatchling/Hatch custom build hook
# that builds Rubber documentation.  Is invoked by `python3 -m build`
# automatically, but can also be executed directly.
#
# Copyright 2002-2010 Emmanuel Beffara
# Copyright 2015-2018 Sebastian Kapfer
# Copyright 2015-2019 Nicolas Boulenguez
# Copyright 2020      Florian Schmaus
# Copyright 2024      Sebastian Pipping

import logging
import os
import re
import shlex
import subprocess
from contextlib import contextmanager
from os.path import join, lexists

from hatchling.builders.hooks.plugin.interface import BuildHookInterface

_logger = logging.getLogger(__name__)


class _RubberDocumentationBuilder:
    """
    Builds Rubber documentaton by (1) substituting placeholders
    and (2) calling out to GNU Texinfo for rendering.
    """

    # A file f is generated from f.in by replacing @author@, @version@ by
    # sensible values (as ./configure does in the autoconf world).
    _FILES_WITH_SUBSTITUTIONS = (
        join("man", "man1", "rubber.1"),
        join("man", "man1", "rubber-info.1"),
        join("man", "fr", "man1", "rubber.1"),
        join("man", "fr", "man1", "rubber-info.1"),
        join("doc", "rubber", "rubber.texi"),
    )

    _MANUAL_BASENAME = join("doc", "rubber", "rubber.")

    _DOC_RECIPES = (
        ("html", ("makeinfo", "--html", "--no-split")),
        ("info", ("makeinfo", "--info")),
        ("pdf", ("texi2dvi", "--pdf", "--quiet", "--tidy")),
        ("txt", ("makeinfo", "--plaintext")),
    )

    def __init__(self, metadata):
        self.__metadata = metadata

    def _remove_file(self, filename):
        if lexists(filename):
            _logger.info(f"Removing {filename!r}...")
            os.remove(filename)

    def _make_file(self, infile, outfile, func, args):
        """
        Remake of ``distutils.cmd.Command.make_file``
        """
        try:
            in_mod_time = os.stat(infile).st_mtime
        except FileNotFoundError:
            in_mod_time = 0  # i.e. Unix epoch 1970-01-01

        try:
            out_mod_time = os.stat(outfile).st_mtime
        except FileNotFoundError:
            # NOTE: This is intended to fake an out-of-date output file
            #       which will trigger a build below.
            #       If both input and ouput files are missing, an error
            #       is to be expected below in ``func(..)``.
            out_mod_time = in_mod_time - 1

        if out_mod_time >= in_mod_time:
            # Either (a) output present and input missing
            #     or (b) output present and up to date
            return

        _logger.info(f"Generating {outfile!r} from {infile!r}...")
        func(*args)

    def _spawn(self, *args):
        command_display = " ".join(shlex.quote(a) for a in args)
        _logger.info(f"Running...... # {command_display}")
        subprocess.check_call(args)

    def _generate_file_with_substitutions(self, subs):
        pattern = "|".join(subs.keys())
        pattern = "@(" + pattern + ")@"
        pattern = re.compile(pattern)

        def repl(match_object):
            return subs[match_object.group(1)]

        def func(in_path, out_path):
            # Rubber sources are encoded in utf_8.
            with open(in_path, encoding="utf-8") as in_file:
                with open(out_path, "w", encoding="utf-8") as out_file:
                    for in_line in in_file:
                        out_line = pattern.sub(repl, in_line)
                        out_file.write(out_line)

        for out_path in self._FILES_WITH_SUBSTITUTIONS:
            in_path = out_path + ".in"
            self._make_file(in_path, out_path, func, (in_path, out_path))

    def _generate_documentation(self):
        infile = self._MANUAL_BASENAME + "texi"
        for fmt, recipe in self._DOC_RECIPES:
            outfile = self._MANUAL_BASENAME + fmt
            cmd = recipe + ("--output=" + outfile, infile)
            self._make_file(infile, outfile, self._spawn, cmd)

    def build(self):
        project_metadata = self.__metadata.config["project"]
        project_version = self.__metadata.version

        subs = {
            "author": project_metadata["authors"][0]["name"],
            "author_email": project_metadata["authors"][0]["email"],
            "maintainer": project_metadata["maintainers"][0]["name"],
            "maintainer_email": project_metadata["maintainers"][0]["email"],
            "url": project_metadata["urls"]["Homepage"],
            "version": project_version,
        }

        self._generate_file_with_substitutions(subs)

        self._generate_documentation()

    def iterate_filenames(self):
        for filename in self._FILES_WITH_SUBSTITUTIONS:
            yield filename

        for file_extension, _ in self._DOC_RECIPES:
            filename = self._MANUAL_BASENAME + file_extension
            yield filename

    def clean(self):
        for filename in self.iterate_filenames():
            self._remove_file(filename)


@contextmanager
def _logging_ensured(logger, target_level):
    original_level = None
    if logger.level < target_level:
        original_level = logger.level
        logger.setLevel(target_level)

    added_handler = None
    if not logger.hasHandlers():
        added_handler = logging.StreamHandler()
        logger.addHandler(added_handler)

    try:
        yield
    finally:
        if original_level is not None:
            logger.setLevel(original_level)
        if added_handler is not None:
            logger.removeHandler(added_handler)


class CustomBuildHook(BuildHookInterface):
    """
    Hatchling integration to build additional files, and
    make them get included with ``sdist`` and ``wheel`` archives.
    """

    __generated_during_sdist = False

    def initialize(self, version, build_data):
        with _logging_ensured(_logger, logging.INFO):
            _logger.info(f"Hooking into target {self.target_name!r}...")
            doc_builder = _RubberDocumentationBuilder(self.metadata)

            if self.target_name == "sdist":
                doc_builder.clean()
                doc_builder.build()
                self.__generated_during_sdist = True
            elif self.target_name == "wheel":
                if not self.__generated_during_sdist:
                    doc_builder.build()

        return super().initialize(version, build_data)


def _run_clean_command(config):
    from hatchling.metadata.core import ProjectMetadata
    from hatchling.plugin.manager import PluginManager

    logging.basicConfig(level=logging.INFO)

    metadata = ProjectMetadata(root=".", plugin_manager=PluginManager())

    _logger.info(f"Cleaning generated files for {metadata.name} version {metadata.version}...")

    doc_builder = _RubberDocumentationBuilder(metadata)
    doc_builder.clean()

    _logger.info("Done.")


def _run_generate_command(_config):
    from hatchling.metadata.core import ProjectMetadata
    from hatchling.plugin.manager import PluginManager

    logging.basicConfig(level=logging.INFO)

    metadata = ProjectMetadata(root=".", plugin_manager=PluginManager())

    _logger.info(f"Generating files for {metadata.name} version {metadata.version}...")

    doc_builder = _RubberDocumentationBuilder(metadata)
    doc_builder.clean()
    doc_builder.build()

    _logger.info("Done.")


def _run_tar_command(config):
    from hatchling.metadata.core import ProjectMetadata
    from hatchling.plugin.manager import PluginManager

    metadata = ProjectMetadata(root=".", plugin_manager=PluginManager())

    argv = [
        "git",
        "archive",
        config.revision,
        "-9",
        f"--prefix=rubber-{metadata.version}/",
        f"--output=rubber-{metadata.version}.{config.extension}",
    ]

    command_display = " ".join(shlex.quote(a) for a in argv)
    print(f"# {command_display}")

    subprocess.check_call(argv)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=("Run custom build commands for Rubber."
                                                  " Direct invocation is purely optional"
                                                  ", `python3 -m build` has you covered!"))
    subparsers = parser.add_subparsers(required=True,
                                       title="subcommands",
                                       help="call with --help for details")

    clean_command = subparsers.add_parser("clean",
                                          description="Clean generated files shipped with Rubber")
    clean_command.set_defaults(func=_run_clean_command)

    generate_command = subparsers.add_parser("generate",
                                             description="Generate files needed to ship Rubber")
    generate_command.set_defaults(func=_run_generate_command)

    tar_command = subparsers.add_parser("tar", description='Wrapper for "git archive"')
    tar_command.add_argument(
        "--revision",
        metavar="REV",
        default="HEAD",
        help="Git tree-ish (default: %(default)s)",
    )
    tar_command.add_argument(
        "--extension",
        metavar="EXT",
        default="tar.gz",
        help='archive extension (default: "%(default)s")',
    )
    tar_command.set_defaults(func=_run_tar_command)

    config = parser.parse_args()
    config.func(config)

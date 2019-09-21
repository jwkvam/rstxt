#!/usr/bin/env python
"""Extract text from reStructuredText."""

import os
import sys
import select

import click
from docutils.parsers.rst import Parser, Directive, directives, roles
from docutils.utils import new_document
from docutils.frontend import OptionParser
from docutils.nodes import Text


__version__ = '0.2.0-dev'


class IgnoredDirective(Directive):
    """Stub for unknown directives."""

    has_content = True

    def run(self):
        """Do nothing."""
        return []


def ignore_role(name, rawtext, text, lineno, inliner, options=None, content=None):
    """Stub for unknown roles."""
    # pylint: disable=unused-argument
    return ([], [])


def has_stdin():
    """Test if there is data in stdin."""
    # return os.isatty(sys.stdin.fileno()) and select.select([sys.stdin], [], [], 0.0)[0]
    return select.select([sys.stdin], [], [], 0.0)[0]


@click.command()
@click.argument('files', nargs=-1)
def main(files):
    """Extract reStructuredText text."""
    if not files:
        if not has_stdin():
            sys.exit(os.EX_OK)
        files = [sys.stdin]

    # ignore Sphinx directives
    text_nodes = set(
        ['block_quote', 'paragraph', 'list_item', 'term', 'definition_list_item', 'title']
    )
    ignored = ['todo', 'toctree', 'autoclass', 'graphviz', 'automodule']
    iroles = ['py:class', 'ref']
    for ignore in ignored:
        directives.register_directive(ignore, IgnoredDirective)
    for role in iroles:
        roles.register_local_role(role, ignore_role)

    parser = Parser()
    settings = OptionParser(components=(Parser,)).get_default_values()
    for file in files:
        document = new_document(file, settings)
        try:
            content = file.read()  # pylint: disable=assignment-from-no-return
        except AttributeError:
            try:
                content = open(file, 'r').read()
            except FileNotFoundError:
                print(f'rstxt: {file}: no such file', file=sys.stderr)
                continue
        parser.parse(content, document)
        for node in parser.document.traverse(Text):
            if (
                node.tagname == '#text'
                and node.parent
                and node.parent.tagname in text_nodes
                and (
                    (node.parent.parent and node.parent.parent.tagname != 'system_message')
                    or not node.parent.parent
                )
            ):
                print(node.astext())
    sys.exit(os.EX_OK)


if __name__ == '__main__':
    # pylint: disable=no-value-for-parameter
    main()

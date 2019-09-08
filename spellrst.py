#!/usr/bin/env python
"""Spell check reStructuredText."""

import os
import sys

import click
from docutils.parsers.rst import Parser, Directive, directives, roles
from docutils.utils import new_document
from docutils.frontend import OptionParser
from docutils.nodes import Text
import spacy
import toml


__version__ = '0.1.0'


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


class Misspell:
    """Detect misspelled words."""

    def __init__(self, config):
        """Setup whitelist."""
        try:
            options = toml.load(config)
            self.sensitive = options.get('sensitive', [])
            self.insensitive = options.get('insensitive', [])
        except FileNotFoundError:
            pass

    def is_misspelled(self, token):
        """Detect if token is misspelled."""
        if (
            token.like_url
            or token.like_num
            or token.like_email
            or token.text in self.sensitive
            or token.lower_ in self.insensitive
        ):
            return False
        return token.is_oov


DEFAULT_CONFIG = 'spellrst.toml'


@click.command()
@click.argument('files', nargs=-1)
@click.option(
    '-d',
    '--dictionary',
    help='spaCy language model (spacy.io/models), e.g. en_core_web_md',
    default='en_core_web_md',
)
@click.option('-c', '--config', help='Configuration file (whitelist)', default=DEFAULT_CONFIG)
def main(files, dictionary, config):
    """Spell check reStructuredText."""
    if not files:
        sys.exit(os.EX_USAGE)
    if config != DEFAULT_CONFIG and os.path.isfile(config):
        print(f"Configuration file '{config}' not found.", file=sys.stderr)
        sys.exit(os.EX_NOINPUT)
    # ignore Sphinx directives
    misspell = Misspell(config)
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
    nlp = spacy.load(dictionary)
    any_misspellings = False
    for file in files:
        document = new_document(file, settings)
        try:
        parser.parse(open(file, 'r').read(), document)
        except FileNotFoundError:
            print(f"File not found '{file}'", file=sys.stderr)
            any_misspellings = True
            continue
        misspellings = set()
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
                misspellings |= set(
                    token.text for token in nlp(node.astext()) if misspell.is_misspelled(token)
                )

        if misspellings:
            any_misspellings = True
            print(f'✘ {file}')
            print(*misspellings, sep='\n')
        else:
            print(f'✔ {file}')
    sys.exit(os.EX_DATAERR if any_misspellings else os.EX_OK)


if __name__ == '__main__':
    # pylint: disable=no-value-for-parameter
    main()

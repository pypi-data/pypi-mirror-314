from ast import parse
from typing import Optional
from pathlib import Path

import click
from pypxml import PageXML, PageType
from pypxml.ops import regularize

from .util import parse_path, parse_paths, parse_suffix, expand_path, expand_paths


def parse_rules(ctx, param, value):
    def split_types(rule: str) -> tuple[PageType, str]:
        pass

    if not value:
        return None
    rules = {}
    for v in value:
        from_rules, to_rule = v.split(':')
        for from_rule in from_rules.split(','):
            r = from_rule.split('_')
            if len(r) == 1:
                r.append(None)


@click.command('regularize', help="""
    Regularize regions and region types. 

    This module regularizes a set of PageXML files by changing/merging PageXML regions 
    and their types by a set of rules. 
    
    XMLs: List of PageXML files to be processed. Supports multiple file paths, wildcards, 
    or directories (when used with the -g option).
    """)
@click.help_option('--help')
@click.argument('xmls',
                type=click.Path(exists=True, file_okay=True, dir_okay=True),
                callback=parse_paths,
                required=True,
                nargs=-1)
@click.option('-o', '--output',
              help='Directory where output files will be saved. If not set, overwrite original files.',
              type=click.Path(exists=False, file_okay=False, dir_okay=True),
              required=False,
              callback=parse_path)
@click.option('-g', '--glob', 'glob',
              help='Specify a glob pattern to match PageXML files within directories passed to XMLs.',
              type=click.STRING,
              default='*.xml',
              show_default=True)
@click.option('-r', '--rule',
              help='Specify a merge rule in the format `source1,source2:target`, where `source1` and `source2` are '
                   'merged into `target`. The left side can contain multiple sources, separated by commas, '
                   'but the target can only contain one target.'
                   'Each source and target should be specified in the form `RegionType_subtype` '
                   '(e.g. TextRegion_paragraph) or `RegionType` if the Region does not contain a `type` attribute.',
              multiple=True,
              callback=parse_rules)
def regularize_cli(xmls: list[Path], output: Optional[Path] = None, glob: str = '*.xml', rule: Optional[dict[str, str]] = None):
    pass
# Skeleton of a CLI

import click

import latex_fragment


@click.command('latex_fragment')
@click.argument('count', type=int, metavar='N')
def cli(count):
    """Echo a value `N` number of times"""
    for i in range(count):
        click.echo(latex_fragment.has_legs)

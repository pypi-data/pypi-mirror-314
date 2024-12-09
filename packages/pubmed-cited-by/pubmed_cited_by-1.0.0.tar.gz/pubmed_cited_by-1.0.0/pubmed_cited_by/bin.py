from pathlib import Path

import click
import loguru

from pubmed_cited_by import version_info, utils
from pubmed_cited_by.core import PubmedCitedBy


CONTEXT_SETTINGS = dict(help_option_names=['-?', '-h', '--help'])


__epilog__ = click.style('''
\n\b
expamles:
    {prog} --help
\b
    {prog}  1 2 3
    {prog}  pmid.list
\b
    {prog}  1 2 3 -o output.xlsx
    {prog}  1 2 3 -o output.csv
    {prog}  1 2 3 -o output.tsv
    {prog}  1 2 3 -o output.json
    {prog}  1 2 3 -o output.jl
                         
contact: {author} <{author_email}>
'''.format(**version_info), fg='yellow')

@click.command(
    name=version_info['prog'],
    help=click.style(version_info['desc'], italic=True, fg='cyan', bold=True),
    context_settings=CONTEXT_SETTINGS,
    no_args_is_help=True,
    epilog=__epilog__,
)
@click.version_option(version=version_info['version'], prog_name=version_info['prog'])
@click.argument('pmids', nargs=-1)
@click.option('-o', '--output', help='the output file')
def cli(pmids, output):

    pcb = PubmedCitedBy()

    data = pcb.get_cited_by(pmids)
    if not output:
        for line in data:
            print(line)
    else:
        output = Path(output)
        if output.suffix == '.xlsx':
            utils.save_excel(data, output)
        elif output.suffix == '.csv':
            utils.save_csv(data, output)
        elif output.suffix == '.tsv':
            utils.save_csv(data, output, sep='\t')
        elif output.suffix == '.json':
            utils.save_json(data, output)
        elif output.suffix == '.jl':
            utils.save_jsonlines(data, output)

        loguru.logger.info(f'save file to: {output}')


def main():
    cli()


if __name__ == '__main__':
    main()

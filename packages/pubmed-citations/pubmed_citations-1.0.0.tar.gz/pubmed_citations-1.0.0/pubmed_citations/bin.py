from pathlib import Path

import click
import loguru

from pubmed_citations import version_info
from pubmed_citations.core import PubmedCitations, CiteFormat


CONTEXT_SETTINGS = dict(
    help_option_names=['-?', '-h', '--help'],
    max_content_width=120,
)


__epilog__ = click.style('''

\b
example:
    {prog} --help
    {prog} 1 2 3
    {prog} pmid.list
    {prog} 1 2 3 -f apa -o output.xlsx
    {prog} 1 2 3 -f apa -o output.docx
    {prog} 1 2 3 -f apa -o output.csv
    {prog} 1 2 3 -f apa -o output.json
    {prog} 1 2 3 -f apa -o output.jl
    {prog} 1 2 3 -f apa -o output.tsv

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
@click.option('-f', '--cite-fmt', help='the citation format', type=click.Choice(CiteFormat.__members__.keys()), default='MLA', show_default=True)
@click.option('-o', '--output', help='the output file')
def cli(pmids, output, cite_fmt):

    cit = PubmedCitations(*pmids, cite_fmt=cite_fmt)

    if not output:
        for item in cit.orig_data:
            print('\t'.join(item))
    else:
        output = Path(output)
        if output.suffix == '.xlsx':
            cit.to_excel(output)
        elif output.suffix == '.json':
            cit.to_json(output)
        elif output.suffix == '.jl':
            cit.to_jsonlines(output)
        elif output.suffix == '.docx':
            cit.to_docx(output)
        elif output.suffix == '.csv':
            cit.to_csv(output)
        elif output.suffix == '.tsv':
            cit.to_csv(output, sep='\t')
        else:
            loguru.logger.error(f'unsupported file format: {output.suffix}')
            exit(1)

        loguru.logger.info(f'save file: {output}')
    

def main():
    cli()


if __name__ == '__main__':
    main()
